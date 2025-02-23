const API_BASE_URL = import.meta.env.VITE_API_URL;

// Log all environment variables (excluding any sensitive data)
console.log('Environment variables:', {
  VITE_API_URL: import.meta.env.VITE_API_URL,
  MODE: import.meta.env.MODE,
  DEV: import.meta.env.DEV,
  PROD: import.meta.env.PROD
});

if (!API_BASE_URL) {
  console.error('API_BASE_URL is not set. Please check your environment variables.');
}

import { CEFRLevel } from '@/components/games/level-selector';

export interface VocabularyItem {
  id: number;
  german_word: string;
  english_translation: string;
  theme: string;
  cefr_level: string;
  word_group_id?: number;
  word_group_name?: string;
}

interface FetchError extends Error {
  details?: {
    status: number;
    statusText: string;
    headers: Record<string, string>;
    body: string;
    url: string;
  };
}

export const getVocabulary = async (level: CEFRLevel = 'All Levels'): Promise<VocabularyItem[]> => {
  try {
    const url = `${API_BASE_URL}/api/vocabulary${level !== 'All Levels' ? `?level=${level}` : ''}`;
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error('Failed to fetch vocabulary');
    }
    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    return [];
  }
};