import { Brain, Book, Trophy, Gamepad, Rocket, Pencil, Languages, ScrollText, LayoutGrid, Timer } from "lucide-react";
import { AppCard } from "@/components/app-card";
import { StatsDashboard } from "@/components/stats-dashboard";
import { Button } from "@/components/ui/button";
import { toast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";

const Index = () => {
  const navigate = useNavigate();

  const handleAppLaunch = (path: string) => {
    toast({
      title: "Navigating",
      description: "Loading your learning experience...",
    });
    navigate(path);
  };

  return (
    <div className="min-h-screen p-8 space-y-8">
      {/* Header with Profile Button */}
      <div className="flex justify-between items-center">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">WortWunder Launchpad</h1>
          <p className="text-muted-foreground">
            Your central hub for German language learning
          </p>
        </div>
        <Button 
          variant="outline" 
          onClick={() => handleAppLaunch("/profile-settings")}
        >
          Profile Settings
        </Button>
      </div>

      {/* Stats Dashboard */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold tracking-tight">Your Progress</h2>
        <StatsDashboard />
      </div>

      {/* Vocabulary Resources */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold tracking-tight">Vocabulary Resources</h2>
        <div className="grid gap-4 md:grid-cols-2">
          <AppCard
            title="2000 Most Common German Words"
            description="Access the essential German vocabulary list"
            icon={<Book className="h-6 w-6" />}
            onClick={() => handleAppLaunch("/vocabulary/common-words")}
            xpReward="Study Material"
            difficulty="Easy"
            buttonText="Learn"
          />
          <AppCard
            title="Vocabulary Explorer"
            description="Browse and manage your vocabulary inventory"
            icon={<ScrollText className="h-6 w-6" />}
            onClick={() => handleAppLaunch("/vocabulary/explorer")}
            xpReward="Varies"
            difficulty="Easy"
            buttonText="Learn"
          />
        </div>
      </div>

      {/* Learning Games */}
      <div className="space-y-4">
        <h2 className="text-2xl font-semibold tracking-tight">Learning Games</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <AppCard
            title="Spelling Bee"
            description="Practice spelling German words correctly"
            icon={<Pencil className="h-6 w-6" />}
            onClick={() => handleAppLaunch("/games/spelling-bee")}
            difficulty="Medium"
            xpReward="20-60 XP"
          />
          <AppCard
            title="Multiple Choice Quiz"
            description="Test your vocabulary knowledge"
            icon={<Brain className="h-6 w-6" />}
            onClick={() => handleAppLaunch("/games/multiple-choice-quiz")}
            difficulty="Medium"
            xpReward="10-50 XP"
          />
          <AppCard
            title="Flashcards"
            description="Learn words using interactive flashcards"
            icon={<LayoutGrid className="h-6 w-6" />}
            onClick={() => handleAppLaunch("/games/flashcards")}
            difficulty="Easy"
            xpReward="10-50 XP"
          />
        </div>
      </div>

      {/* Quick Actions */}
      <div className="animated-bg rounded-lg p-6 text-center space-y-4">
        <Rocket className="h-12 w-12 mx-auto text-primary" />
        <h3 className="text-xl font-semibold">Ready to start learning?</h3>
        <p className="text-muted-foreground max-w-md mx-auto">
          Choose a game above to begin your learning journey or explore the vocabulary resources.
        </p>
      </div>
    </div>
  );
};

export default Index;
