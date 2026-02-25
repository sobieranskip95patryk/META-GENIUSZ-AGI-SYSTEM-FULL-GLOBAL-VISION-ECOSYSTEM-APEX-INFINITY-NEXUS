import asyncio

from intelligence_core.core.engine import UnifiedIntelligenceEngine


def test_engine_process_allows_and_executes():
    engine = UnifiedIntelligenceEngine(config={"policy": {"confidence_threshold": 0.0}})

    async def run():
        res = await engine.process({"a": 1, "b": 2})
        assert "prediction" in res
        assert "decision" in res
        assert "execution" in res
        assert res["decision"]["decision"] == "allow"

    asyncio.run(run())
