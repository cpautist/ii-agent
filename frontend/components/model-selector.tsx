import { Select, SelectTrigger, SelectContent, SelectItem, SelectValue } from "./ui/select";

export const MODEL_OPTIONS = [
  "openai/o4-mini-high",
  "qwen/qwen3-30b-a3b:free",
  "qwen/qwen3-235b-a22b:free",
  "tngtech/deepseek-r1t-chimera:free",
  "anthropic/claude-3.7-sonnet:thinking",
  "deepseek/deepseek-r1",
  "openai/gpt-4.1",
  "openai/o3",
  "openai/o4-mini",
  "openai/gpt-4.1-mini",
  "openai/gpt-4.1-nano",
  "x-ai/grok-3-mini-beta",
  "x-ai/grok-3-beta",
  "meta-llama/llama-4-maverick:free",
  "meta-llama/llama-4-maverick",
  "meta-llama/llama-4-scout:free",
  "deepseek/deepseek-v3-base:free",
  "google/gemini-2.5-pro-exp-03-25",
  "deepseek/deepseek-chat-v3-0324:free",
  "deepseek/deepseek-chat-v3-0324",
  "deepseek/deepseek-r1-zero:free",
  "anthropic/claude-3.7-sonnet:beta",
  "openai/o3-mini-high",
  "openai/o3-mini",
  "deepseek/deepseek-r1-distill-llama-70b:free",
  "deepseek/deepseek-r1:free",
  "deepseek/deepseek-chat:free",
  "google/gemini-2.0-flash-exp:free",
  "openai/gpt-4o-2024-11-20",
  "qwen/qwen-2.5-coder-32b-instruct:free",
  "anthropic/claude-3.5-haiku-20241022:beta",
  "meta-llama/Meta-Llama-3.1-70B-Instruct",
  "meta-llama/llama-3.1-8b-instruct",
  "mistralai/Mixtral-8x22B-Instruct-v0.1",
  "google/palm-2",
];

interface Props {
  value: string;
  onChange: (val: string) => void;
}

export default function ModelSelector({ value, onChange }: Props) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-full max-w-sm">
        <SelectValue placeholder="Select model" />
      </SelectTrigger>
      <SelectContent>
        {MODEL_OPTIONS.map((m) => (
          <SelectItem key={m} value={m}>
            {m}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
