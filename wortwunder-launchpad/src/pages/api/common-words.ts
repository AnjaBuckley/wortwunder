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
  example_sentence?: string;
  example_sentence_translation?: string;
  is_favorite?: boolean;
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
      throw new Error(`Failed to fetch vocabulary: ${response.statusText}`);
    }

    const data = await response.json();
    console.log('Successfully fetched vocabulary data');
    return data;
  } catch (error) {
    console.error('Error fetching vocabulary:', error);
    throw error;
  }
};

export const addToFavorites = async (vocabularyId: number): Promise<void> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/favorites/${vocabularyId}`, {
      method: 'POST',
    });
    
    if (!response.ok) {
      throw new Error('Failed to add to favorites');
    }
  } catch (error) {
    console.error('Error adding to favorites:', error);
    throw error;
  }
};

export const removeFromFavorites = async (vocabularyId: number): Promise<void> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/favorites/${vocabularyId}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error('Failed to remove from favorites');
    }
  } catch (error) {
    console.error('Error removing from favorites:', error);
    throw error;
  }
};

export const getFavorites = async (): Promise<VocabularyItem[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/favorites`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch favorites');
    }

    return await response.json();
  } catch (error) {
    console.error('Error fetching favorites:', error);
    throw error;
  }
};