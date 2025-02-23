import { Book, Brain, Rocket, ScrollText, Menu, LayoutGrid, Pencil } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Sidebar,
  SidebarContent,
  SidebarTrigger,
  SidebarHeader,
  SidebarFooter,
} from "@/components/ui/sidebar";

export function AppSidebar() {
  const games = [
    {
      name: 'Flashcards',
      href: '/games/flashcards',
      icon: LayoutGrid,
      description: 'Practice vocabulary with interactive flashcards'
    },
    {
      name: 'Spelling Bee',
      href: '/games/spelling-bee',
      icon: Pencil,
      description: 'Test your spelling skills'
    },
    {
      name: 'Multiple Choice Quiz',
      href: '/games/multiple-choice-quiz',
      icon: Brain,
      description: 'Test your vocabulary knowledge with multiple choice questions'
    }
  ];

  return (
    <Sidebar>
      <SidebarHeader className="border-b px-4 py-2">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">WortWunder</h2>
          <SidebarTrigger>
            <Menu className="h-4 w-4" />
          </SidebarTrigger>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <div className="space-y-4 py-4">
          <div className="px-4 py-2">
            <h2 className="mb-2 px-2 text-lg font-semibold">Vocabulary</h2>
            <div className="space-y-1">
              <Button variant="ghost" className="w-full justify-start" asChild>
                <Link to="/vocabulary/common-words">
                  <Book className="mr-2 h-4 w-4" />
                  Common Words
                </Link>
              </Button>
              <Button variant="ghost" className="w-full justify-start" asChild>
                <Link to="/vocabulary/explorer">
                  <ScrollText className="mr-2 h-4 w-4" />
                  Vocabulary Explorer
                </Link>
              </Button>
            </div>
          </div>
          <div className="px-4 py-2">
            <h2 className="mb-2 px-2 text-lg font-semibold">Games</h2>
            <div className="space-y-1">
              {games.map((game) => (
                <Button variant="ghost" className="w-full justify-start" asChild key={game.href}>
                  <Link to={game.href}>
                    <game.icon className="mr-2 h-4 w-4" />
                    {game.name}
                  </Link>
                </Button>
              ))}
            </div>
          </div>
        </div>
      </SidebarContent>
      <SidebarFooter className="border-t p-4">
        <Button variant="ghost" className="w-full justify-start" asChild>
          <Link to="/">
            <Rocket className="mr-2 h-4 w-4" />
            Back to Launchpad
          </Link>
        </Button>
      </SidebarFooter>
    </Sidebar>
  );
}
