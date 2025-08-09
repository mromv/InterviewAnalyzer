"""
Общие модели данных
"""
from enum import Enum
from pydantic import Field
from typing import List, Dict, Optional

from .schema import AutoPromptModel


class Decision(str, Enum):
    ACCEPTED = ("accept", "Подтверждена")
    REJECTED = ("rejected", "Опровергнута")
    INCONSISTENCY = ("inconsistency", "Противоречиво")
    UNCLEAR = ("unclear", "Неопределенно")

    def __new__(cls, value, description):
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @classmethod
    def as_dict(cls) -> Dict:
        return {d.value: d.description for d in cls}

    @classmethod
    def as_prompt(cls) -> str:
        return "\n".join(
            f"- {d.value}: {d.description}"
            for d in cls
        )
    

class Hypothesis(AutoPromptModel):
    hypothesis_name: str
    description: str

class HypothesisDecision(AutoPromptModel):
    decision: Decision 
    description: str

class BaseQuestion(AutoPromptModel):
    question: str

class QuestionAnswer(BaseQuestion):
    goal: Optional[str] = None
    answer: str
    excerpt: str

class Proof(BaseQuestion):
    proof: str

class Disproof(BaseQuestion):
    disproof: str


class HypothesisQuestions(AutoPromptModel):
    hypothesis: Hypothesis
    questions: List[QuestionAnswer]

class HypothesisAnalysis(HypothesisQuestions):
    decision: HypothesisDecision
    proofs: List[Proof]
    disproofs: List[Disproof]
