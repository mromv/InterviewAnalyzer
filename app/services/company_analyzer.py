from app.schemas import *
from app.utils import PromptFactory

from .agent import BaseAgent
from .llm_client import llm_clients

class CompanyAnalyzer(BaseAgent):
    def __init__(self):
        self.llm = llm_clients.company_analyzer

    async def _process_interview(self, request: InterviewResult) -> InterviewCompanyAnalysis:
        hypotheses = []

        for hypothesis in request.interview_hypotheses:
            prompt = PromptFactory.build_prompt(
                "company_analyzer", request=request, hypo_request=hypothesis
            )
            struct_analysis = await self._generate(prompt=prompt, hypothesis=hypothesis)
            hypotheses.append(struct_analysis)

        return InterviewCompanyAnalysis(
            company=request.company,
            industry=request.industry,
            interview_hypotheses=hypotheses
        )

    async def process(self, request: InterviewsContainer) -> InterviewsContainer:
        analyzed_interviews = []
        for interview in request.interviews:
            result = await self._process_interview(interview)
            analyzed_interviews.append(result)

        return InterviewsContainer(interviews=analyzed_interviews)
