import asyncio
import logging
import pytest
import tempfile
from pathlib import Path

pytest_plugins = ("pytest_asyncio",)

from ii_agent.agents.function_call import FunctionCallAgent, TOOL_CALL_TIMEOUT_MESSAGE
from ii_agent.llm.base import LLMClient, ToolCall, TextResult
from ii_agent.llm.message_history import MessageHistory
from ii_agent.tools.base import LLMTool, ToolImplOutput
from ii_agent.utils.workspace_manager import WorkspaceManager


class DummyContextManager:
    def apply_truncation_if_needed(self, messages):
        return messages

    def count_tokens(self, messages):
        return 0


class SlowTool(LLMTool):
    name = "slow_tool"
    description = "slow"
    input_schema = {"type": "object", "properties": {}, "required": []}

    async def run_impl(self, tool_input, message_history=None):
        await asyncio.sleep(2)
        return ToolImplOutput(tool_output="done", tool_result_message="done")


class DummyLLM(LLMClient):
    def __init__(self):
        self.model_name = "dummy"
        self.called = False

    def generate(self, *args, **kwargs):
        if not self.called:
            self.called = True
            return [ToolCall(tool_call_id="1", tool_name="slow_tool", tool_input={})], None
        return [TextResult(text="done")], None


@pytest.mark.asyncio
async def test_tool_timeout():
    tmp_dir = tempfile.TemporaryDirectory()
    agent = FunctionCallAgent(
        system_prompt="",
        client=DummyLLM(),
        tools=[SlowTool()],
        init_history=MessageHistory(context_manager=DummyContextManager()),
        workspace_manager=WorkspaceManager(Path(tmp_dir.name)),
        message_queue=asyncio.Queue(),
        logger_for_agent_logs=logging.getLogger("test"),
        max_turns=1,
        tool_timeout=0.1,
    )

    result = await agent.run_agent_async("do it")
    assert TOOL_CALL_TIMEOUT_MESSAGE in result
    tmp_dir.cleanup()
