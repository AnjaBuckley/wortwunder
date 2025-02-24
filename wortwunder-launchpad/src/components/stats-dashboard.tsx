import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Brain, Heart, Book, Trophy, Zap, Star, Target } from "lucide-react";
import { Progress } from "@/components/ui/progress";
import { getFavorites } from "@/pages/api/common-words";
import { getStudySessionsCount } from "@/pages/api/study-sessions";

interface Stats {
  favoriteWords: number;
  totalWords: number;
  streak: number;
  studySessions: number;
  progress: number;
}

export function StatsDashboard() {
  const [stats, setStats] = useState<Stats>({
    favoriteWords: 0,
    totalWords: 2000, // Total words in our database
    streak: 0,
    studySessions: 0,
    progress: 0
  });

  const loadStats = async () => {
    try {
      // Get favorite words count
      const favorites = await getFavorites();
      
      // Get study sessions count
      const sessionsCount = await getStudySessionsCount();
      
      // Calculate progress percentage
      const progress = (favorites.length / stats.totalWords) * 100;
      
      setStats(prev => ({
        ...prev,
        favoriteWords: favorites.length,
        studySessions: sessionsCount,
        progress: progress
      }));
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  // Initial load
  useEffect(() => {
    loadStats();
  }, []);

  // Refresh stats every 30 seconds
  useEffect(() => {
    const interval = setInterval(loadStats, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="space-y-6">
      {/* Progress Overview */}
      <Card className="border-2">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <div>
            <CardTitle className="text-lg font-bold">German Learning Progress</CardTitle>
            <p className="text-sm text-muted-foreground">Track your vocabulary journey</p>
          </div>
          <Target className="h-6 w-6 text-primary" />
        </CardHeader>
        <CardContent className="space-y-3">
          <Progress value={stats.progress} className="h-2" />
          <div className="flex justify-between text-sm text-muted-foreground">
            <span>{stats.favoriteWords} words</span>
            <span>{stats.totalWords} words</span>
          </div>
        </CardContent>
      </Card>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        <Card className="border-2 relative overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Favorite Words</CardTitle>
            <Heart className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.favoriteWords}</div>
            <p className="text-xs text-muted-foreground">Words you've marked as favorites</p>
          </CardContent>
          <div className="absolute inset-0 bg-gradient-to-r from-red-500/5 to-transparent" />
        </Card>
        
        <Card className="border-2 relative overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Study Sessions</CardTitle>
            <Brain className="h-4 w-4 text-violet-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.studySessions}</div>
            <p className="text-xs text-muted-foreground">Total learning sessions completed</p>
          </CardContent>
          <div className="absolute inset-0 bg-gradient-to-r from-violet-500/5 to-transparent" />
        </Card>

        <Card className="border-2 relative overflow-hidden">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Learning Streak</CardTitle>
            <Zap className="h-4 w-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.streak} days</div>
            <p className="text-xs text-muted-foreground">Keep the momentum going!</p>
          </CardContent>
          <div className="absolute inset-0 bg-gradient-to-r from-primary/5 to-transparent" />
        </Card>
      </div>
    </div>
  );
}
