"use client";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";

export const MODEL_OPTIONS = [
  "openai/o4-mini",
  "openai/gpt-4o-2024-11-20",
  "openai/gpt-4.1",
  "qwen/qwen3-30b-a3b:free",
  "deepseek/deepseek-chat-v3-0324:free",
];

export default function ModelSelector({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger className="w-60" />
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
