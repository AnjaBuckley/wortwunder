import { Filter } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

export type CEFRLevel = 'All Levels' | 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
export const CEFR_LEVELS: CEFRLevel[] = ['All Levels', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

interface LevelSelectorProps {
  selectedLevel: CEFRLevel;
  onLevelChange: (level: CEFRLevel) => void;
}

export function LevelSelector({ selectedLevel, onLevelChange }: LevelSelectorProps) {
  return (
    <Select value={selectedLevel} onValueChange={onLevelChange}>
      <SelectTrigger className="w-[180px]">
        <Filter className="h-4 w-4" />
        <SelectValue placeholder="Select Level" />
      </SelectTrigger>
      <SelectContent>
        {CEFR_LEVELS.map(level => (
          <SelectItem key={level} value={level}>
            {level}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}
