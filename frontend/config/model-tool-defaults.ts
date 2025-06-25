export const MODEL_TOOL_DEFAULTS: Record<string, Partial<import("@/typings/agent").ToolSettings>> = {
  "anthropic/claude-sonnet-4": {
    deep_research: false,
    pdf: true,
    media_generation: true,
    audio_generation: true,
    browser: true,
  },
  "anthropic/claude-opus-4": {
    deep_research: false,
    pdf: true,
    media_generation: true,
    audio_generation: true,
    browser: true,
  },
  "openrouter/google/gemini-2.5-flash-001": {
    deep_research: true,
  },
  "openrouter/google/gemini-2.5-pro": {
    deep_research: true,
  },
  "openrouter/openai/gpt-4.1-mini": {
    deep_research: true,
  },
  "openrouter/openai/gpt-4.1-nano": {
    deep_research: true,
  },
};
