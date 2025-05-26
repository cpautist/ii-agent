"use client";

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";

export const MODEL_OPTIONS = [
  { label: "Gemini 2.5 Flash", value: "google/gemini-2.5-flash-preview-05-20" },
  { label: "OpenAI O4 Mini", value: "openai/o4-mini" },
  { label: "Claude 3.7 Sonnet", value: "anthropic/claude-3.7-sonnet" },
];

interface Props {
  model: string;
  setModel: (value: string) => void;
}

export default function ModelSelector({ model, setModel }: Props) {
  return (
    <Select value={model} onValueChange={setModel}>
      <SelectTrigger className="w-full mb-2">
        <SelectValue placeholder="Select model" />
      </SelectTrigger>
      <SelectContent>
        {MODEL_OPTIONS.map((m) => (
          <SelectItem key={m.value} value={m.value}>
            {m.label}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
