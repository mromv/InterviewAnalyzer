from app.schemas import *
from app.utils import PromptFactory, get_industries, get_hypotheses

from .industry_analyzer import IndustryAnalyzer
from .llm_client import llm_clients

class FinalAnalyzer(IndustryAnalyzer):
    def __init__(self):
        self.llm = llm_clients.final_analyzer
    
    async def process(
        self,
        request: InterviewsContainer
    ) -> InterviewBase:
        hypotheses = get_hypotheses()

        analyzed_hypotheses = []
        for _, val in hypotheses.items():
            hypothesis_name = val[0]
            
            temp_interviews = self._filter_interviews(request, hypothesis_name=hypothesis_name)

            if temp_interviews.interviews:
                hypothesis = temp_interviews.interviews[0].interview_hypotheses[0]
                prompt = PromptFactory.build_prompt(
                    "final_analyzer",
                    request=temp_interviews,
                    hypo_request=hypothesis
                )
                struct_analysis = await self._generate(prompt=prompt, hypothesis=hypothesis)
    
                analyzed_hypotheses.append(struct_analysis)

        return InterviewBase(interview_hypotheses=analyzed_hypotheses)
