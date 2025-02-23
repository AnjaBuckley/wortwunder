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
    console.log('Attempting to fetch from URL:', url);
    
    const response = await fetch(url);
    console.log('Response status:', response.status);
    console.log('Response headers:', response.headers);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error('Response not OK:', {
        status: response.status,
        statusText: response.statusText,
        errorText
      });
      throw new Error(`Failed to fetch vocabulary: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    console.log('Successfully fetched data:', {
      itemCount: data.length,
      sampleItem: data[0]
    });
    return data;
  } catch (error) {
    console.error('Error in getVocabulary:', {
      error,
      API_BASE_URL,
      level
    });
    return [];
  }
};