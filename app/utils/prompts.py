"""
Шаблоны динамических промптов для LLM
"""
from abc import ABC, abstractmethod

from typing import Literal
from pathlib import Path

from app.schemas import *

PromptType = Literal["company_analyzer", "hypotheses_generator", "industry_analyzer", "final_analyzer"]


class BasePrompt(ABC):
    """Базовый класс для всех промптов"""
    _prompt_dir = Path("app/prompts")

    @classmethod
    def _load_template(cls, filename: str) -> str:
        """Подгружаем текстовый шаблон промпта"""
        path = cls._prompt_dir / filename
        with path.open("r", encoding="utf-8") as file:
            content = file.read()
        return content

    @classmethod
    @abstractmethod
    def build(cls, *args, **kwargs) -> str:
        """Генерация финального промпта"""
        ...


class CompanyAnalyzerPrompt(BasePrompt):
    @classmethod
    def build(cls, request: InterviewResult, hypo_request: HypothesisQuestions) -> str:
        template = cls._load_template("company_analyzer.txt")

        common_questions = "\n\n".join([i.as_prompt() for i in request.common_questions])
        answers = "\n\n".join([i.as_prompt() for i in hypo_request.questions])

        data = {
            "company": request.company,
            "industry": request.industry,
            "common_questions": common_questions,
            "hypothesis_name": hypo_request.hypothesis.hypothesis_name,
            "hypothesis_description": hypo_request.hypothesis.description,
            "answers": answers,
            "decisions": Decision.as_prompt(),
        }

        return template.format(**data)


class HypothesesGeneratorPrompt(BasePrompt):
    @classmethod
    def build(cls, request: InterviewCompanyAnalysis) -> str:
        template = cls._load_template("hypotheses_generator.txt")

        answers = "\n\n".join([i.as_prompt() for i in request.interview_hypotheses])

        data = {
            "company": request.company,
            "industry": request.industry,
            "answers": answers,
            "decisions": Decision.as_prompt(),
        }

        return template.format(**data)


class IndustryAnalyzerPrompt(BasePrompt):
    @classmethod
    def build(cls, request: InterviewsContainer, hypo_request: HypothesisQuestions) -> str:
        template = cls._load_template("industry_analyzer.txt")

        analysis = request.as_prompt(exclude_fields={"questions"})

        data = {
            "industry": request.interviews[0].industry,
            "hypothesis_name": hypo_request.hypothesis.hypothesis_name,
            "hypothesis_description": hypo_request.hypothesis.description,
            "analysis": analysis,
            "decisions": Decision.as_prompt(),
        }

        return template.format(**data)
    
    
class FinalAnalyzerPrompt(BasePrompt):
    @classmethod
    def build(cls, request: InterviewsContainer, hypo_request: HypothesisQuestions) -> str:
        template = cls._load_template("final_analyzer.txt")

        analysis = request.as_prompt(exclude_fields={"questions"})

        data = {
            "hypothesis_name": hypo_request.hypothesis.hypothesis_name,
            "hypothesis_description": hypo_request.hypothesis.description,
            "analysis": analysis,
            "decisions": Decision.as_prompt(),
        }

        return template.format(**data)


class PromptFactory:
    @staticmethod
    def build_prompt(prompt_type: PromptType, **kwargs) -> str:
        if prompt_type == "company_analyzer":
            return CompanyAnalyzerPrompt.build(**kwargs)
        
        if prompt_type == "hypotheses_generator":
            return HypothesesGeneratorPrompt.build(**kwargs)
        
        if prompt_type == "industry_analyzer":
            return IndustryAnalyzerPrompt.build(**kwargs)
        
        if prompt_type == "final_analyzer":
            return FinalAnalyzerPrompt.build(**kwargs)
        
        else:
            raise ValueError(f"Unknown prompt_type: {prompt_type}")
