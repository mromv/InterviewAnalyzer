from typing import Optional

from app.schemas import *
from app.utils import PromptFactory, get_industries, get_hypotheses

from .agent import BaseAgent
from .llm_client import llm_clients

class IndustryAnalyzer(BaseAgent):
    def __init__(self):
        self.llm = llm_clients.industry_analyzer
    
    def _filter_interviews(
        self, 
        interviews: InterviewsContainer,
        industry: Optional[str] = None,
        hypothesis_name: Optional[str] = None,
    ) -> InterviewsContainer:
        filtered_interviews = []
        for interview in interviews.interviews:
            if industry is not None and interview.industry != industry:
                continue

            interview_copy = interview.model_copy()

            if hypothesis_name is not None:
                interview_copy.interview_hypotheses = [
                    h for h in interview.interview_hypotheses 
                    if h.hypothesis.hypothesis_name == hypothesis_name
                ]

            if not interview_copy.interview_hypotheses:
                continue

            filtered_interviews.append(interview_copy)

        return InterviewsContainer(interviews=filtered_interviews)
    
    async def process(self, request: InterviewsContainer) -> InterviewsContainer:
        industries, hypotheses = get_industries(), get_hypotheses()

        analyzed_industries = []
        for industry in industries:

            analyzed_hypotheses = []
            for _, val in hypotheses.items():
                hypothesis_name = val[0]

                temp_interviews = self._filter_interviews(request, industry, hypothesis_name)

                if temp_interviews.interviews:
                    hypothesis = temp_interviews.interviews[0].interview_hypotheses[0]
                    prompt = PromptFactory.build_prompt(
                        "industry_analyzer", 
                        request=temp_interviews,
                        hypo_request=hypothesis
                    )
                    struct_analysis = await self._generate(prompt=prompt, hypothesis=hypothesis)
                    analyzed_hypotheses.append(struct_analysis)

            analyzed_industries.append(
                InterviewIndustryAnalysis(industry=industry, interview_hypotheses=analyzed_hypotheses)
            )

        return InterviewsContainer(interviews=analyzed_industries)
