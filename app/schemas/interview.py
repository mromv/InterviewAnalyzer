"""
Модели данных на всех этапах
"""
from typing import List, TypeVar

from .schema import AutoPromptModel
from .hypothesis import (
    HypothesisAnalysis, HypothesisQuestions, QuestionAnswer, 
)

class InterviewBase(AutoPromptModel):
    interview_hypotheses: List[HypothesisAnalysis]

class InterviewIndustryAnalysis(InterviewBase):
    industry: str

class InterviewCompanyAnalysis(InterviewIndustryAnalysis):
    company: str

class InterviewResult(InterviewCompanyAnalysis):
    interview_hypotheses: List[HypothesisQuestions]
    common_questions: List[QuestionAnswer]

T = TypeVar('T', bound=InterviewBase)

class InterviewsContainer(AutoPromptModel):
    interviews: List[T]
