import { useState, useEffect } from 'react';
import { VocabularyItem, getVocabulary } from '@/pages/api/common-words';
import { Book, ChevronLeft, ChevronRight } from "lucide-react";
import { SpeakButton } from "@/components/ui/speak-button";
import { Button } from "@/components/ui/button";
import { useTextToSpeech } from "@/hooks/use-text-to-speech";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const CEFR_LEVELS = ['All Levels', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2'] as const;
const THEMES = ['All Themes', 'General', 'Food', 'Travel', 'Numbers'] as const;
const ITEMS_PER_PAGE = 15;

const CommonWords = () => {
  const [vocabulary, setVocabulary] = useState<VocabularyItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<string>('All Levels');
  const [selectedTheme, setSelectedTheme] = useState<string>('All Themes');
  const [currentPage, setCurrentPage] = useState(1);
  const { speak } = useTextToSpeech();

  useEffect(() => {
    const fetchVocabulary = async () => {
      try {
        console.log('Component: Starting vocabulary fetch');
        const data = await getVocabulary();
        console.log('Component: Successfully received vocabulary data');
        setVocabulary(data);
        setLoading(false);
      } catch (err) {
        console.error('Component: Error details:', {
          error: err,
          message: err instanceof Error ? err.message : 'Unknown error',
          type: err instanceof Error ? err.name : typeof err
        });
        setError(err instanceof Error ? 
          `${err.name}: ${err.message}` : 
          'Failed to load vocabulary'
        );
        setLoading(false);
      }
    };

    fetchVocabulary();
  }, []);

  const filteredVocabulary = vocabulary.filter(item => 
    (selectedLevel === 'All Levels' || item.cefr_level === selectedLevel) && 
    (selectedTheme === 'All Themes' || item.theme === selectedTheme)
  );

  // Reset to first page when filters change
  useEffect(() => {
    setCurrentPage(1);
  }, [selectedLevel, selectedTheme]);

  const totalPages = Math.ceil(filteredVocabulary.length / ITEMS_PER_PAGE);
  const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
  const paginatedVocabulary = filteredVocabulary.slice(startIndex, startIndex + ITEMS_PER_PAGE);

  const toggleLevel = (level: string) => {
    setSelectedLevel(level);
  };

  const toggleTheme = (theme: string) => {
    setSelectedTheme(theme);
  };

  if (loading) return (
    <div className="p-8 animate-pulse">
      <div className="h-8 w-48 bg-gray-200 rounded mb-4"></div>
      <div className="space-y-3">
        {[...Array(5)].map((_, i) => (
          <div key={i} className="h-16 bg-gray-100 rounded"></div>
        ))}
      </div>
    </div>
  );

  if (error) return (
    <div className="p-8 text-red-600">
      <h2 className="text-xl font-bold">Error Loading Vocabulary</h2>
      <p>{error}</p>
      <p className="mt-2 text-sm">
        Unable to connect to the vocabulary server. Please try refreshing the page.
      </p>
    </div>
  );

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Book className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold">German Vocabulary by Level</h1>
        </div>
        <div className="flex items-center space-x-4">
          <Select
            value={selectedLevel}
            onValueChange={setSelectedLevel}
          >
            <SelectTrigger className="w-[180px]">
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

          <Select
            value={selectedTheme}
            onValueChange={setSelectedTheme}
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select Theme" />
            </SelectTrigger>
            <SelectContent>
              {THEMES.map(theme => (
                <SelectItem key={theme} value={theme}>
                  {theme}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="flex items-center justify-between">
        <p className="text-muted-foreground">
          Master essential German vocabulary organized by CEFR proficiency levels and themes.
        </p>
        <p className="text-sm text-muted-foreground">
          Showing {Math.min(startIndex + 1, filteredVocabulary.length)}-{Math.min(startIndex + ITEMS_PER_PAGE, filteredVocabulary.length)} of {filteredVocabulary.length} words
        </p>
      </div>
      
      {/* Table header */}
      <div className="grid grid-cols-[auto,1fr,1fr,auto,auto] gap-4 px-4 py-2 bg-gray-100 rounded-t-lg font-semibold">
        <div></div>
        <div>German</div>
        <div>English</div>
        <div>Theme</div>
        <div>Level</div>
      </div>
      
      {/* Vocabulary list */}
      <div className="space-y-2">
        {paginatedVocabulary.map((item) => (
          <div 
            key={item.id} 
            className="grid grid-cols-[auto,1fr,1fr,auto,auto] gap-4 p-4 border rounded-lg hover:bg-gray-50 transition-colors"
          >
            <SpeakButton 
              text={item.german_word} 
              onClick={() => speak(item.german_word)}
            />
            <div className="font-semibold">{item.german_word}</div>
            <div className="text-muted-foreground">{item.english_translation}</div>
            <div className="text-sm text-gray-600 px-2 py-1 bg-gray-100 rounded">
              {item.theme}
            </div>
            <div className={`text-sm font-medium px-2 py-1 rounded ${
              item.cefr_level === 'A1' ? 'bg-green-100 text-green-700' :
              item.cefr_level === 'A2' ? 'bg-blue-100 text-blue-700' :
              item.cefr_level === 'B1' ? 'bg-yellow-100 text-yellow-700' :
              item.cefr_level === 'B2' ? 'bg-orange-100 text-orange-700' :
              item.cefr_level === 'C1' ? 'bg-red-100 text-red-700' :
              'bg-purple-100 text-purple-700'
            }`}>
              {item.cefr_level}
            </div>
          </div>
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between border-t pt-4 mt-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
            disabled={currentPage === 1}
            className="space-x-2"
          >
            <ChevronLeft className="h-4 w-4" />
            <span>Previous</span>
          </Button>

          <span className="mx-4">
            Page {currentPage} of {totalPages}
          </span>

          <Button
            variant="outline"
            size="sm"
            onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
            disabled={currentPage === totalPages}
            className="space-x-2"
          >
            <span>Next</span>
            <ChevronRight className="h-4 w-4" />
          </Button>
        </div>
      )}
    </div>
  );
};

export default CommonWords;
