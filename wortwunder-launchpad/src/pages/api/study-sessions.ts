import { API_BASE_URL } from "@/config";

export const getStudySessionsCount = async (): Promise<number> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/study-sessions/count`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch study sessions count');
    }

    const data = await response.json();
    return data.count;
  } catch (error) {
    console.error('Error fetching study sessions count:', error);
    return 0;
  }
};

export const addStudySession = async (activityType: string): Promise<number> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/study-sessions`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ activity_type: activityType }),
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Failed to add study session');
    }

    const data = await response.json();
    return data.count;
  } catch (error) {
    console.error('Error adding study session:', error);
    throw error;
  }
};
