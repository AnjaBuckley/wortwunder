import { useCallback } from 'react';

export function useTextToSpeech() {
  const speak = useCallback((text: string) => {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'de-DE';
    window.speechSynthesis.speak(utterance);
  }, []);

  return { speak };
}
