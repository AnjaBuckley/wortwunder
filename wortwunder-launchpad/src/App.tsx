import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/AppSidebar";
import Index from "./pages/Index";
import CommonWords from "./pages/vocabulary/CommonWords";
import VocabularyExplorer from "./pages/vocabulary/VocabularyExplorer";
import SpellingBee from "@/pages/games/SpellingBee";
import Flashcards from "@/pages/games/Flashcards";
import MultipleChoiceQuiz from "@/pages/games/MultipleChoiceQuiz";
import NotFound from "./pages/NotFound";
import ProfileSettings from "@/pages/ProfileSettings";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <BrowserRouter>
        <SidebarProvider>
          <div className="flex min-h-screen w-full">
            <AppSidebar />
            <main className="flex-1">
              <Routes>
                <Route path="/" element={<Index />} />
                <Route path="/vocabulary/common-words" element={<CommonWords />} />
                <Route path="/vocabulary/explorer" element={<VocabularyExplorer />} />
                <Route path="/games/spelling-bee" element={<SpellingBee />} />
                <Route path="/games/flashcards" element={<Flashcards />} />
                <Route path="/games/multiple-choice-quiz" element={<MultipleChoiceQuiz />} />
                <Route path="/profile-settings" element={<ProfileSettings />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </main>
          </div>
        </SidebarProvider>
      </BrowserRouter>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
