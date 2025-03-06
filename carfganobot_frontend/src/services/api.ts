import axios from 'axios';
import { ChatResponse } from '../types/chat';

// API base URL - will be replaced with deployed URL in production
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatApi = {
  // Get list of topics
  getTopics: async () => {
    const response = await api.get('/api/chat/topics');
    return response.data;
  },

  // Get content for a specific topic
  getTopic: async (topicId: string): Promise<ChatResponse> => {
    const response = await api.post('/api/chat/topic', { topic_id: topicId });
    return response.data;
  },

  // Send a chat message
  sendMessage: async (message: string, conversationHistory: any[]): Promise<ChatResponse> => {
    const response = await api.post('/api/chat/message', {
      message,
      conversation_history: conversationHistory,
    });
    return response.data;
  },
};
