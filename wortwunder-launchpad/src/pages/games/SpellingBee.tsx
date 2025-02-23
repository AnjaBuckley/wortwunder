import { useEffect, useState } from 'react';
import { Pencil, RefreshCw, Volume2 } from "lucide-react";
import { VocabularyItem, getVocabulary } from '@/pages/api/common-words';
import { LevelSelector, CEFRLevel } from '@/components/games/level-selector';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

const SpellingBee = () => {
  const [words, setWords] = useState<VocabularyItem[]>([]);
  const [currentWord, setCurrentWord] = useState<VocabularyItem | null>(null);
  const [userInput, setUserInput] = useState('');
  const [score, setScore] = useState(0);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<CEFRLevel>('All Levels');
  const [showAnswer, setShowAnswer] = useState(false);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  // Load vocabulary
  useEffect(() => {
    const loadVocabulary = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const data = await getVocabulary(selectedLevel);
        
        if (!data || data.length === 0) {
          setError('No vocabulary items found for this level');
          return;
        }

        setWords(data);
        pickNewWord(data);
      } catch (err) {
        setError('Failed to load vocabulary');
      } finally {
        setLoading(false);
      }
    };

    loadVocabulary();
  }, [selectedLevel]);

  const pickNewWord = (wordList: VocabularyItem[]) => {
    if (!wordList.length) return;
    
    const wordIndex = Math.floor(Math.random() * wordList.length);
    const word = wordList[wordIndex];
    
    setCurrentWord(word);
    setUserInput('');
    setShowAnswer(false);
    setIsCorrect(null);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentWord) return;

    setTotal(prev => prev + 1);
    const correct = userInput.toLowerCase().trim() === currentWord.german_word.toLowerCase();
    setIsCorrect(correct);
    setShowAnswer(true);
    
    if (correct) {
      setScore(prev => prev + 1);
    }
  };

  const handleNextWord = () => {
    pickNewWord(words);
  };

  const speakWord = () => {
    if (!currentWord) return;
    
    const utterance = new SpeechSynthesisUtterance(currentWord.german_word);
    utterance.lang = 'de-DE';
    window.speechSynthesis.speak(utterance);
  };

  if (loading) {
    return (
      <div className="p-8 animate-pulse">
        <div className="h-8 w-48 bg-gray-200 rounded mb-4"></div>
        <div className="h-32 bg-gray-100 rounded"></div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-4">
          <Pencil className="h-6 w-6" />
          <div>
            <h2 className="text-2xl font-bold">Spelling Bee</h2>
            <p className="text-gray-600 mt-1">
              Practice spelling German words. You'll see an English word - try to write its German translation.
              Need help? Click the speaker button to hear the German word pronounced.
            </p>
          </div>
        </div>
        <LevelSelector selectedLevel={selectedLevel} onLevelChange={setSelectedLevel} />
      </div>

      {error ? (
        <div className="text-red-500 p-4 rounded bg-red-50">{error}</div>
      ) : currentWord ? (
        <div>
          <div className="mb-8">
            <p className="text-lg mb-2">Write the German word for:</p>
            <p className="text-2xl font-bold">{currentWord.english_translation}</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="flex gap-2">
              <Input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Type the German word..."
                className="text-lg flex-1"
                autoFocus
                disabled={showAnswer}
              />
              <Button
                type="button"
                variant="outline"
                size="icon"
                onClick={speakWord}
                className="flex-shrink-0"
                title="Listen to the German word"
              >
                <Volume2 className="h-4 w-4" />
              </Button>
            </div>
            
            {showAnswer ? (
              <div>
                <div className={`p-4 rounded mb-4 ${isCorrect ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                  {isCorrect ? 'Correct!' : 'Incorrect!'} The answer is: {currentWord.german_word}
                </div>
                <Button
                  onClick={handleNextWord}
                  className="w-full"
                >
                  Next Word
                </Button>
              </div>
            ) : (
              <Button
                type="submit"
                className="w-full"
              >
                Check Answer
              </Button>
            )}
          </form>

          <div className="mt-8 flex items-center justify-between">
            <div className="text-lg">
              Score: {score} / {total}
            </div>
            <button
              onClick={() => {
                setScore(0);
                setTotal(0);
                pickNewWord(words);
              }}
              className="flex items-center gap-2 px-4 py-2 border rounded hover:bg-purple-50 hover:border-purple-500 hover:text-purple-700 transition-colors"
            >
              <RefreshCw className="h-4 w-4" />
              Reset
            </button>
          </div>
        </div>
      ) : (
        <div className="text-center p-8">
          <p className="text-lg text-gray-600">No words available. Try selecting a different level.</p>
        </div>
      )}
    </div>
  );
};

export default SpellingBee;
