import { useEffect, useState } from 'react';
import { Brain, RefreshCw } from "lucide-react";
import { VocabularyItem, getVocabulary } from '@/pages/api/common-words';
import { LevelSelector, CEFRLevel } from '@/components/games/level-selector';

interface AnswerState {
  option: string;
  isCorrect: boolean;
}

const MultipleChoiceQuiz = () => {
  const [words, setWords] = useState<VocabularyItem[]>([]);
  const [currentWord, setCurrentWord] = useState<VocabularyItem | null>(null);
  const [options, setOptions] = useState<string[]>([]);
  const [score, setScore] = useState(0);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<CEFRLevel>('All Levels');
  const [answerState, setAnswerState] = useState<AnswerState | null>(null);
  const [isProcessingAnswer, setIsProcessingAnswer] = useState(false);

  // Load vocabulary
  useEffect(() => {
    const loadVocabulary = async () => {
      try {
        console.log('Loading vocabulary for level:', selectedLevel);
        setLoading(true);
        setError(null);
        
        const data = await getVocabulary(selectedLevel);
        console.log('Loaded vocabulary:', data);
        
        if (!data || data.length < 4) {
          console.error('Not enough vocabulary items');
          setError('Not enough vocabulary items for this level');
          return;
        }

        setWords(data);
        pickNewWord(data);
      } catch (err) {
        console.error('Failed to load vocabulary:', err);
        setError('Failed to load vocabulary');
      } finally {
        setLoading(false);
      }
    };

    loadVocabulary();
  }, [selectedLevel]);

  const pickNewWord = (wordList: VocabularyItem[]) => {
    if (!wordList.length) return;

    // Pick a random word
    const wordIndex = Math.floor(Math.random() * wordList.length);
    const word = wordList[wordIndex];
    console.log('Picked word:', word);

    // Get 3 random wrong answers
    const wrongAnswers = wordList
      .filter(w => w.id !== word.id)
      .sort(() => Math.random() - 0.5)
      .slice(0, 3)
      .map(w => w.english_translation);

    // Add correct answer and shuffle
    const allOptions = [...wrongAnswers, word.english_translation]
      .sort(() => Math.random() - 0.5);

    console.log('Generated options:', allOptions);
    
    setCurrentWord(word);
    setOptions(allOptions);
    setAnswerState(null);
    setIsProcessingAnswer(false);
  };

  const handleAnswer = async (answer: string) => {
    if (!currentWord || isProcessingAnswer) return;
    
    setIsProcessingAnswer(true);
    const isCorrect = answer === currentWord.english_translation;
    setAnswerState({ option: answer, isCorrect });

    setTotal(prev => prev + 1);
    if (isCorrect) {
      setScore(prev => prev + 1);
    }
    
    // Wait a moment to show the answer feedback
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    pickNewWord(words);
  };

  const resetQuiz = () => {
    setScore(0);
    setTotal(0);
    pickNewWord(words);
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
          <Brain className="h-6 w-6" />
          <div>
            <h2 className="text-2xl font-bold">Multiple Choice Quiz</h2>
            <p className="text-gray-600 mt-1">
              Test your German vocabulary knowledge with this multiple choice quiz. You'll be shown a German word
              and need to select its correct English translation from four options. This game helps you practice
              word recognition and strengthen your vocabulary recall.
            </p>
          </div>
        </div>
        <LevelSelector selectedLevel={selectedLevel} onLevelChange={setSelectedLevel} />
      </div>

      {error ? (
        <div className="text-red-500 p-4 rounded bg-red-50">{error}</div>
      ) : currentWord && options.length > 0 ? (
        <div>
          <div className="mb-8">
            <p className="text-lg mb-2">Translate to English:</p>
            <p className="text-2xl font-bold">{currentWord.german_word}</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            {options.map((option, index) => {
              const isSelected = answerState?.option === option;
              const showFeedback = isSelected && answerState !== null;
              const isCorrect = showFeedback && answerState.isCorrect;
              
              return (
                <button
                  key={index}
                  onClick={() => handleAnswer(option)}
                  disabled={isProcessingAnswer}
                  className={`
                    p-4 text-lg border rounded transition-colors
                    ${showFeedback 
                      ? isCorrect
                        ? 'bg-green-100 border-green-500 text-green-700'
                        : 'bg-red-100 border-red-500 text-red-700'
                      : 'hover:bg-purple-50 hover:border-purple-500 hover:text-purple-700'
                    }
                  `}
                >
                  {option}
                </button>
              );
            })}
          </div>

          <div className="mt-8 flex items-center justify-between">
            <div className="text-lg">
              Score: {score} / {total}
            </div>
            <button
              onClick={resetQuiz}
              className="flex items-center gap-2 px-4 py-2 border rounded hover:bg-purple-50 hover:border-purple-500 hover:text-purple-700 transition-colors"
            >
              <RefreshCw className="h-4 w-4" />
              Reset
            </button>
          </div>
        </div>
      ) : (
        <div className="text-center p-8">
          <p className="text-lg text-gray-600">No questions available. Try selecting a different level.</p>
        </div>
      )}
    </div>
  );
};

export default MultipleChoiceQuiz;
