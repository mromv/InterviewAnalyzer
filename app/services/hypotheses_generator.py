from typing import List

from app.schemas import *
from app.utils import PromptFactory

from .agent import BaseAgent
from .llm_client import llm_clients

class HypothesesGenerator(BaseAgent):
    def __init__(self):
        self.llm = llm_clients.hypotheses_generator
    
    def _structure_analysis(self, analysis: str) -> List[HypothesisAnalysis]:
        hypotheses = analysis.get("hypotheses")
        if not hypotheses:
            return 
        
        return [
            HypothesisAnalysis(
                hypothesis=Hypothesis(
                    hypothesis_name=hyp.get("hypothesis", {}).get("hypothesis_name", ""),
                    description=hyp.get("hypothesis", {}).get("description", "")
                ),
                questions = [],
                
                decision = HypothesisDecision(
                    decision=hyp.get("decision", ""),
                    description=hyp.get("description", "")
                ),

                proofs = [Proof(
                    question=p.get("question", ""),
                    proof=p.get("proof", ""),
                ) for p in hyp.get("proofs", [])],

                disproofs = [Disproof(
                    question=d.get("question", ""),
                    proof=d.get("disproof", ""),
                ) for d in hyp.get("disproofs", [])],
            ) for hyp in hypotheses
        ]

    async def _generate_hypotheses(self, request: InterviewCompanyAnalysis) -> InterviewCompanyAnalysis:
        prompt = PromptFactory.build_prompt(
            "hypotheses_generator", request=request
        )
        interview_hypotheses = await self._generate(prompt=prompt) or []

        return InterviewCompanyAnalysis(
            company=request.company,
            industry=request.industry,
            interview_hypotheses=interview_hypotheses
        )

    async def process(self, request: InterviewsContainer) -> InterviewsContainer:
        analyzed_interviews = []
        for interview in request.interviews:
            result = await self._generate_hypotheses(interview)
            analyzed_interviews.append(result)

        return InterviewsContainer(interviews=analyzed_interviews)
