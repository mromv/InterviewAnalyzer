import asyncio

import app.logger
from app.services import Orchestrator

async def run():
    orchestrator = Orchestrator()
    results = await orchestrator.process()
    return results

if __name__ == "__main__":
    asyncio.run(run())
