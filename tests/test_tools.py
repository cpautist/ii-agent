import asyncio
from unittest.mock import MagicMock

import pytest

from ii_agent.core.config.model_tool_map import MODEL_TOOL_DEFAULTS
from ii_agent.tools import get_system_tools
from ii_agent.utils import WorkspaceManager


@pytest.mark.parametrize("model_name", list(MODEL_TOOL_DEFAULTS.keys()))
def test_deep_research_tool_present(tmp_path, model_name):
    client = MagicMock()
    client.model_name = model_name

    workspace_manager = WorkspaceManager(tmp_path)
    tools = get_system_tools(
        client=client,
        workspace_manager=workspace_manager,
        message_queue=asyncio.Queue(),
        container_id=None,
        ask_user_permission=False,
        tool_args={"deep_research": True},
    )
    tool_names = [tool.name for tool in tools]
    assert "deep_research" in tool_names
