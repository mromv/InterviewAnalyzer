import pandas as pd

from typing import List, Dict

from app.schemas import *
from .get_info import get_hypotheses, read_interviews
from .util import save_model_to_json

# расшифрока наименований гипотез
HYPOTHESES = get_hypotheses()


def parse_interview_to_dict(file_path: str, company_name: str, industry_name: str) -> Dict:
    df = pd.read_excel(file_path, usecols=range(6))
    df = df[df.iloc[:, 1].notna() & df.iloc[:, 4].notna()]
    df = df.fillna('')
    df['Гипотеза'] = df['Гипотеза'].str.split(', ')
    df = df.explode('Гипотеза')

    hyps = {}
    common_questions = []
    for _, row in df.iterrows():
        hypothesis = row['Гипотеза'] or 'Общий вопрос'

        if HYPOTHESES.get(hypothesis):
            hypothesis_name, description = HYPOTHESES.get(hypothesis)
            values = hyps.setdefault(hypothesis_name, (description, []))
            array = values[1]
        else:
            array = common_questions
            
        array.append((
            row.iloc[1].strip(),
            row.iloc[2].strip(),
            row.iloc[4].strip(),
            row.iloc[5].strip()
        ))
    return {
        "company_name": company_name,
        "industry_name": industry_name,
        "hypotheses": hyps,
        "common_questions": common_questions
    }


def parse_interviews_to_dicts(meta_file_path: str) -> List:
    interviews = []
    with open(meta_file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                filepath, company, industry = line.split(",")
                interviews.append(
                    parse_interview_to_dict(filepath, company, industry)
                )
    return interviews


def parse_interviews_from_dicts(interviews_list: List[Dict]) -> InterviewsContainer:
    interview_results = []
    
    for interview_dict in interviews_list:
        hypotheses_list = []
        for hyp_name, (description, questions) in interview_dict["hypotheses"].items():
            hyp_questions = [
                QuestionAnswer(
                    question=q[0],
                    goal=q[1],
                    answer=q[2],
                    excerpt=q[3]
                ) for q in questions
            ]
            
            hypotheses_list.append(
                HypothesisQuestions(
                    hypothesis=Hypothesis(
                        hypothesis_name=hyp_name,
                        description=description
                    ),
                    questions=hyp_questions
                )
            )
        
        common_questions = [
            QuestionAnswer(
                question=q[0],
                goal=q[1],
                answer=q[2],
                excerpt=q[3]
            ) for q in interview_dict["common_questions"]
        ]
        
        interview_result = InterviewResult(
            company=interview_dict["company_name"],
            industry=interview_dict["industry_name"],
            interview_hypotheses=hypotheses_list,
            common_questions=common_questions
        )
        
        interview_results.append(interview_result)
    
    return InterviewsContainer(interviews=interview_results)


def parse_interviews(meta_file_path: str = "data/input_meta.txt") -> InterviewsContainer:
    interviews = [
        parse_interview_to_dict(filepath, company, industry)
        for filepath, company, industry in read_interviews(meta_file_path)
    ]
    struct_interviews = parse_interviews_from_dicts(interviews)
    save_model_to_json(struct_interviews, "outputs/source_interviews.json", exclude_questions=False)
    return struct_interviews
