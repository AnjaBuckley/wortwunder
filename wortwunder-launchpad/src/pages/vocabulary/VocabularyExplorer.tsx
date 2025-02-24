import { useState, useEffect } from "react";
import { ScrollText, Heart } from "lucide-react";
import { VocabularyItem, getFavorites, removeFromFavorites } from "@/pages/api/common-words";
import { Button } from "@/components/ui/button";
import { SpeakButton } from "@/components/ui/speak-button";
import { useTextToSpeech } from "@/hooks/use-text-to-speech";

const VocabularyExplorer = () => {
  const [favorites, setFavorites] = useState<VocabularyItem[]>([]);
  const { speak } = useTextToSpeech();

  useEffect(() => {
    loadFavorites();
  }, []);

  const loadFavorites = async () => {
    try {
      const data = await getFavorites();
      setFavorites(data);
    } catch (error) {
      console.error('Error loading favorites:', error);
    }
  };

  const handleRemoveFavorite = async (id: number) => {
    try {
      await removeFromFavorites(id);
      await loadFavorites(); // Refresh the list
    } catch (error) {
      console.error('Error removing favorite:', error);
    }
  };

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center space-x-4">
        <ScrollText className="h-6 w-6 text-primary" />
        <h1 className="text-3xl font-bold">Vocabulary Explorer</h1>
      </div>
      
      <div className="space-y-4">
        <div className="flex items-center space-x-2">
          <Heart className="h-5 w-5 text-red-500 fill-current" />
          <h2 className="text-xl font-semibold">Favorite Words</h2>
        </div>
        
        {favorites.length === 0 ? (
          <p className="text-muted-foreground">
            No favorite words yet. Visit the Common Words page to add some favorites!
          </p>
        ) : (
          <div className="space-y-2">
            {favorites.map((item) => (
              <div 
                key={item.id}
                className="grid grid-cols-[auto,1fr,1fr,auto] gap-4 p-4 border rounded-lg hover:bg-gray-50 transition-colors items-center"
              >
                <SpeakButton 
                  text={item.german_word}
                  onClick={() => speak(item.german_word)}
                />
                <div>
                  <div className="font-medium">{item.german_word}</div>
                  {item.example_sentence && (
                    <div className="text-sm text-gray-500 mt-1">{item.example_sentence}</div>
                  )}
                </div>
                <div>
                  <div>{item.english_translation}</div>
                  {item.example_sentence_translation && (
                    <div className="text-sm text-gray-500 mt-1">{item.example_sentence_translation}</div>
                  )}
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  className="text-red-500 hover:text-red-600"
                  onClick={() => handleRemoveFavorite(item.id)}
                  title="Remove from favorites"
                >
                  <Heart className="h-4 w-4 fill-current" />
                </Button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default VocabularyExplorer;
