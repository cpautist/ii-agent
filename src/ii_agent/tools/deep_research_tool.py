"""Tool for performing deep research on a complex topic."""

from typing import Any, Optional
import asyncio
import logging
import uuid

from ii_agent.llm.message_history import MessageHistory
from ii_agent.tools.base import LLMTool, ToolImplOutput
from ii_agent.core.event import EventType, RealtimeEvent
from ii_agent.tools.message_tool import MessageTool
from ii_researcher.reasoning.agent import ReasoningAgent
from ii_researcher.reasoning.builders.report import ReportType

logger = logging.getLogger("tool_calls")


def on_token(token: str):
    """Callback for processing streamed tokens."""
    print(token, end="", flush=True)


def get_event_loop():
    try:
        # Try to get the existing event loop
        loop = asyncio.get_event_loop()
    except RuntimeError:
        # If no event loop exists, create a new one
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop


class DeepResearchTool(LLMTool):
    name = "deep_research"
    """The model should call this tool when it needs to perform a deep research on a complex topic. This tool is good for providing a comprehensive survey and deep analysis of a topic or niche answers that are hard to find with single search. You can also use this tool to gain large amount of context information."""

    description = "You should call this tool when you need to perform a deep research on a complex topic. This tool is good for providing a comprehensive survey and deep analysis of a topic or niche answers that are hard to find with single search. You can also use this tool to gain large amount of context information."
    input_schema = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to perform deep research on.",
            },
        },
        "required": ["query"],
    }

    def __init__(self, message_queue: asyncio.Queue | None = None):
        super().__init__()
        self.answer: str = ""
        self.message_queue = message_queue

    def _send_progress(self, text: str) -> None:
        """Send a progress update via the message queue."""
        if self.message_queue is None:
            return
        call_id = str(uuid.uuid4())
        self.message_queue.put_nowait(
            RealtimeEvent(
                type=EventType.TOOL_CALL,
                content={
                    "tool_call_id": call_id,
                    "tool_name": MessageTool.name,
                    "tool_input": {"text": text},
                },
            )
        )
        self.message_queue.put_nowait(
            RealtimeEvent(
                type=EventType.TOOL_RESULT,
                content={
                    "tool_call_id": call_id,
                    "tool_name": MessageTool.name,
                    "result": text,
                },
            )
        )

    async def _progress_loop(self, query: str) -> None:
        """Periodically notify the user that research is ongoing."""
        try:
            while True:
                await asyncio.sleep(15)
                self._send_progress(f"Still researching {query}...")
        except asyncio.CancelledError:
            pass

    @property
    def should_stop(self):
        return self.answer != ""

    def reset(self):
        self.answer = ""

    async def run_impl(
        self,
        tool_input: dict[str, Any],
        message_history: Optional[MessageHistory] = None,
    ) -> ToolImplOutput:
        logger.info("DeepResearchTool START query=%s", tool_input["query"])
        print(f"Performing deep research on {tool_input['query']}")
        self._send_progress(f"Starting deep research for {tool_input['query']}")
        progress_task = asyncio.create_task(self._progress_loop(tool_input["query"]))

        agent = ReasoningAgent(
            question=tool_input["query"], report_type=ReportType.BASIC
        )
        try:
            result = await agent.run(on_token=on_token, is_stream=True)
        finally:
            progress_task.cancel()

        assert result, "Model returned empty answer"
        self.answer = result
        logger.info("DeepResearchTool END chars=%d", len(result))
        return ToolImplOutput(result, "Task completed")

    def get_tool_start_message(self, tool_input: dict[str, Any]) -> str:
        return f"Performing deep research on {tool_input['query']}"
