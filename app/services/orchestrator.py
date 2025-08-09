from typing import List, Optional

from app.schemas import *
from app.utils import parse_interviews, save_model_to_json

from .company_analyzer import CompanyAnalyzer
from .industry_analyzer import IndustryAnalyzer
from .hypotheses_generator import HypothesesGenerator
from .final_analyzer import FinalAnalyzer

class Orchestrator:
    def __init__(self):
        self.mid_agents = {
            "company_analyzer": CompanyAnalyzer(),
            "industry_analyzer": IndustryAnalyzer()
        }
        self.hypotheses_generator = HypothesesGenerator()
        self.final_agent = FinalAnalyzer()
    
    async def process(self, request: Optional[InterviewsContainer] = None) -> List[InterviewsContainer]:
        results = []

        stage = request or parse_interviews()

        # middle agents
        for name, agent in self.mid_agents.items():
            stage = await agent.process(stage)
            results.append((name, stage))
        
        # final agent
        request = InterviewsContainer(interviews=[])
        for _, i in results:
            request.interviews += i.interviews
        
        result = await self.final_agent.process(request)
        results.append(("final_agent", result))

        # new hypotheses
        new_hypotheses = await self.hypotheses_generator.process(results[0])
        results.append(("hypotheses_generation", new_hypotheses))

        # save to json
        for n, result in results:
            save_model_to_json(result, f"outputs/{n}.json")
        
        return results
