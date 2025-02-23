import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface AppCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  onClick: () => void;
  xpReward?: string;
  difficulty?: 'Easy' | 'Medium' | 'Hard';
  className?: string;
  buttonText?: string;
}

export function AppCard({ 
  title, 
  description, 
  icon, 
  onClick, 
  xpReward = "10-50 XP",
  difficulty = "Easy",
  className,
  buttonText = "Launch Game"
}: AppCardProps) {
  return (
    <Card 
      className={cn(
        "transition-all hover:shadow-lg cursor-pointer flex flex-col h-[250px]", 
        className
      )} 
      onClick={onClick}
    >
      <CardHeader>
        <div className="flex items-center space-x-4">
          <div className="p-2 bg-primary/10 rounded-full shrink-0">{icon}</div>
          <div>
            <CardTitle className="text-xl">{title}</CardTitle>
            <CardDescription className="line-clamp-2">{description}</CardDescription>
          </div>
        </div>
      </CardHeader>
      <CardContent className="flex flex-col flex-1 justify-end space-y-4">
        <div className="flex justify-between text-sm text-muted-foreground">
          <span>Reward: {xpReward}</span>
          <span>Difficulty: {difficulty}</span>
        </div>
        <Button className="w-full" onClick={onClick}>
          {buttonText}
        </Button>
      </CardContent>
    </Card>
  );
}
