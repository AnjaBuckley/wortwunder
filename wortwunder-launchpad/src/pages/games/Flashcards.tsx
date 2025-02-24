import { useEffect, useState } from 'react';
import { LayoutGrid, RefreshCw, ThumbsUp, ThumbsDown, RotateCw } from "lucide-react";
import { VocabularyItem, getVocabulary } from '@/pages/api/common-words';
import { LevelSelector, CEFRLevel } from '@/components/games/level-selector';
import { SpeakButton } from '@/components/ui/speak-button';
import { useTextToSpeech } from '@/hooks/use-text-to-speech';
import { LanguageToggle } from '@/components/ui/language-toggle';
import { addStudySession } from '@/pages/api/study-sessions';

interface FlashcardItem extends VocabularyItem {
  correctCount: number;
  lastSeen?: Date;
}

const Flashcards = () => {
  const [vocabulary, setVocabulary] = useState<FlashcardItem[]>([]);
  const [currentCard, setCurrentCard] = useState<FlashcardItem | null>(null);
  const [isFlipped, setIsFlipped] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [remainingCards, setRemainingCards] = useState<FlashcardItem[]>([]);
  const [selectedLevel, setSelectedLevel] = useState<CEFRLevel>('All Levels');
  const [showGermanFirst, setShowGermanFirst] = useState(false);
  const { speak, speaking } = useTextToSpeech();

  useEffect(() => {
    const fetchVocabulary = async () => {
      try {
        setLoading(true);
        const data = await getVocabulary(selectedLevel);
        if (data.length === 0) {
          setError('No vocabulary items found');
          return;
        }
        const flashcardData = data.map(word => ({
          ...word,
          correctCount: 0,
          lastSeen: undefined,
        }));
        setVocabulary(flashcardData);
        setRemainingCards(flashcardData);
        setCurrentCard(null);
        setError(null);
      } catch (err) {
        setError('Failed to load vocabulary');
      } finally {
        setLoading(false);
      }
    };

    fetchVocabulary();
  }, [selectedLevel]);

  useEffect(() => {
    if (remainingCards.length > 0 && !currentCard) {
      const randomIndex = Math.floor(Math.random() * remainingCards.length);
      setCurrentCard(remainingCards[randomIndex]);
    }
  }, [remainingCards, currentCard]);

  const handleResponse = (wasCorrect: boolean) => {
    if (!currentCard) return;

    const updatedCards = remainingCards.filter(card => card.id !== currentCard.id);
    const updatedCard = { ...currentCard };

    if (wasCorrect) {
      updatedCard.correctCount++;
      if (updatedCard.correctCount >= 2) {
        setRemainingCards(updatedCards);
      } else {
        updatedCards.push(updatedCard);
        setRemainingCards(updatedCards);
      }
    } else {
      updatedCard.correctCount = 0;
      updatedCards.push(updatedCard);
      setRemainingCards(updatedCards);
    }

    // Check if this was the last card and all words are mastered
    if (updatedCards.length === 0) {
      console.log('Game completed! Adding study session...');
      addStudySession('flashcards')
        .then(() => console.log('Successfully added study session'))
        .catch(error => {
          console.error('Error adding study session:', error);
          // Log more details about the error
          if (error instanceof Error) {
            console.error('Error message:', error.message);
            console.error('Error stack:', error.stack);
          }
        });
    }

    setCurrentCard(null);
    setIsFlipped(false);
  };

  const resetGame = () => {
    const flashcardData = vocabulary.map(word => ({
      ...word,
      correctCount: 0,
      lastSeen: undefined,
    }));
    setRemainingCards(flashcardData);
    setCurrentCard(null);
    setIsFlipped(false);
  };

  return (
    <div className="p-8 space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <LayoutGrid className="h-6 w-6 text-primary" />
          <h1 className="text-3xl font-bold">Flashcards</h1>
        </div>
        <div className="flex items-center space-x-4">
          <LevelSelector selectedLevel={selectedLevel} onLevelChange={setSelectedLevel} />
          <LanguageToggle showGermanFirst={showGermanFirst} onToggle={setShowGermanFirst} />
          <button
            onClick={resetGame}
            className="flex items-center space-x-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90"
          >
            <RefreshCw className="h-4 w-4" />
            <span>Reset</span>
          </button>
        </div>
      </div>

      <p className="text-muted-foreground">
        Learn words using interactive flashcards.
      </p>

      <div className="bg-blue-50 text-blue-800 rounded-lg p-6">
        <h3 className="font-semibold mb-2">How it works:</h3>
        <ul className="list-disc list-inside space-y-1">
          <li>Click a card to flip it and see the translation</li>
          <li>Each word needs to be answered correctly twice to be mastered</li>
          <li>If you get a word wrong, your progress for that word resets</li>
          <li>Words will keep appearing until you master them</li>
        </ul>
      </div>

      {loading ? (
        <div className="flex justify-center items-center min-h-[300px]">
          <RotateCw className="h-8 w-8 animate-spin" />
        </div>
      ) : error ? (
        <div className="text-red-500">{error}</div>
      ) : currentCard ? (
        <div className="flex flex-col items-center space-y-8">
          <div 
            className="relative w-full max-w-lg aspect-[3/2] cursor-pointer"
            onClick={() => setIsFlipped(!isFlipped)}
          >
            <div className="w-full h-full p-8 rounded-xl bg-card text-card-foreground shadow-lg">
              <div className="flex flex-col items-center justify-center h-full">
                <p className="text-sm text-muted-foreground mb-4">
                  {isFlipped 
                    ? (showGermanFirst ? "English Translation:" : "German Translation:") 
                    : `What's the ${showGermanFirst ? "English" : "German"} word for:`}
                </p>
                <div className="flex items-center justify-center space-x-2">
                  <p className="text-4xl font-bold">
                    {isFlipped 
                      ? (showGermanFirst ? currentCard.english_translation : currentCard.german_word) 
                      : (showGermanFirst ? currentCard.german_word : currentCard.english_translation)}
                  </p>
                  {/* Only show speaker when German word is visible */}
                  {((isFlipped && !showGermanFirst) || (!isFlipped && showGermanFirst)) && (
                    <SpeakButton 
                      text={currentCard.german_word} 
                      speaking={speaking} 
                      onSpeak={speak} 
                    />
                  )}
                </div>
                {/* Show example sentence when card is flipped */}
                {isFlipped && currentCard.example_sentence && (
                  <div className="mt-6 text-center">
                    <p className="text-sm text-muted-foreground mb-1">Example:</p>
                    <p className="text-lg mb-1">{currentCard.example_sentence}</p>
                    <p className="text-md text-muted-foreground">{currentCard.example_sentence_translation}</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4 w-full max-w-lg">
            <button
              onClick={() => handleResponse(false)}
              className="p-4 flex items-center justify-center space-x-2 bg-red-100 text-red-800 rounded-lg hover:bg-red-200"
            >
              <ThumbsDown className="h-5 w-5" />
              <span>Didn't Know</span>
            </button>
            <button
              onClick={() => handleResponse(true)}
              className="p-4 flex items-center justify-center space-x-2 bg-green-100 text-green-800 rounded-lg hover:bg-green-200"
            >
              <ThumbsUp className="h-5 w-5" />
              <span>Knew It</span>
            </button>
          </div>
        </div>
      ) : (
        <div className="p-8 text-center bg-green-100 text-green-800 rounded-lg">
          <h2 className="text-2xl font-bold mb-2">Congratulations! 🎉</h2>
          <p>You've mastered all the words in this set!</p>
          <button
            onClick={resetGame}
            className="mt-4 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Practice Again
          </button>
        </div>
      )}
    </div>
  );
};

export default Flashcards;
