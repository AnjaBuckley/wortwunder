import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";

interface LanguageToggleProps {
  showGermanFirst: boolean;
  onToggle: (value: boolean) => void;
}

export function LanguageToggle({ showGermanFirst, onToggle }: LanguageToggleProps) {
  return (
    <div className="flex items-center space-x-2">
      <Label htmlFor="language-toggle" className="text-sm text-muted-foreground">Show German First</Label>
      <Switch
        id="language-toggle"
        checked={showGermanFirst}
        onCheckedChange={onToggle}
      />
    </div>
  );
}
