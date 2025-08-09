from abc import ABC, abstractmethod
from typing import Dict, Any

from app.schemas import *


class BaseAgent(ABC):
    def __init__(self):
        self.llm = ...

    @abstractmethod
    async def process(self, *args, **kwargs) -> Any:
        ...
    
    def _structure_analysis(self, analysis: str, hypothesis: HypothesisQuestions) -> HypothesisAnalysis:
        proofs = analysis.get("proofs", [])
        disproofs = analysis.get("disproofs", [])

        proofs = [
            Proof(
                question=i.get("question"), 
                proof=i.get("proof")
            ) for i in proofs
        ]

        disproofs = [
            Disproof(
                question=i.get("question"), 
                disproof=i.get("disproof")
            ) for i in disproofs
        ]

        decision = HypothesisDecision(
            decision=analysis.get("decision", ""),
            description=analysis.get("description", "")
        )

        return HypothesisAnalysis(
            hypothesis=hypothesis.hypothesis,
            questions=hypothesis.questions,
            decision=decision,
            proofs=proofs,
            disproofs=disproofs
        )

    async def _generate(self, prompt: str, max_retries: int = 3, **kwargs) -> Dict:
        for attempt in range(max_retries):
            try:
                analysis = await self.llm.generate(prompt=prompt)
                struct_analysis = self._structure_analysis(analysis, **kwargs)
                return struct_analysis
            except Exception as e:
                if attempt == max_retries - 1:
                    raise ValueError(f"Failed to generate valid output after {max_retries} attempts") from e
                continue
        
        raise ValueError("Unexpected error in _generate method")
