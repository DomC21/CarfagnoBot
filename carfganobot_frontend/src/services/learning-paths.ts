import { api } from './api';

export interface LearningPathTopic {
  id: string;
  title: string;
}

export interface LearningPath {
  user_id: number;
  proficiency_level: string;
  learning_path: LearningPathTopic[];
}

export interface LearningProgress {
  user_id: number;
  completed_topics: string[];
  completed_count: number;
  total_topics: number;
  progress_percentage: number;
  quiz_scores: Record<string, number>;
  average_quiz_score: number;
}

/**
 * Get a personalized learning path for the authenticated user
 */
export const getPersonalizedLearningPath = async (): Promise<LearningPath> => {
  const response = await api.get('/api/learning-paths/recommended');
  return response.data;
};

/**
 * Get the user's learning progress
 */
export const getLearningProgress = async (): Promise<LearningProgress> => {
  const response = await api.get('/api/learning-paths/progress');
  return response.data;
};

/**
 * Mark a topic as completed for the authenticated user
 */
export const markTopicCompleted = async (topicId: string): Promise<{ status: string; message: string }> => {
  const response = await api.post(`/api/learning-paths/mark-completed/${topicId}`);
  return response.data;
};
