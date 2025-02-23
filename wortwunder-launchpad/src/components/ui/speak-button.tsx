import { Volume2 } from "lucide-react";
import { Button } from "@/components/ui/button";

interface SpeakButtonProps {
  text: string;
  onClick: () => void;
  className?: string;
}

export function SpeakButton({ text, onClick, className }: SpeakButtonProps) {
  return (
    <Button
      variant="ghost"
      size="icon"
      className={className}
      onClick={onClick}
      title={`Listen to "${text}"`}
    >
      <Volume2 className="h-4 w-4" />
    </Button>
  );
}
