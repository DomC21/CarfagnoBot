import axios from 'axios';
import { ChatResponse, Message } from '../types/chat';

// API base URL - will be replaced with deployed URL in production
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Get auth token from local storage
const getToken = (): string | null => {
  return localStorage.getItem('auth_token');
};

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
  sendMessage: async (message: string, conversationHistory: { role: string; content: string }[]): Promise<ChatResponse> => {
    const response = await api.post('/api/chat/message', {
      message,
      conversation_history: conversationHistory,
    });
    return response.data;
  },
};

// Stream chat message function
export const streamChatMessage = async (
  message: string,
  conversationHistory: Message[],
  onChunk: (chunk: string) => void,
  onComplete: () => void
) => {
  try {
    console.log('Starting streaming request to API:', `${API_BASE_URL}/api/chat/stream`);
    console.log('Message:', message);
    console.log('Conversation history length:', conversationHistory.length);
    
    const response = await fetch(`${API_BASE_URL}/api/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(getToken() ? { Authorization: `Bearer ${getToken()}` } : {})
      },
      body: JSON.stringify({
        message,
        conversation_history: conversationHistory
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    console.log('Stream response received, status:', response.status);
    
    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Response body is not readable');
    }

    const decoder = new TextDecoder();
    let done = false;
    let buffer = '';
    const chunkSize = 5; // Process in small chunks for smoother streaming

    console.log('Starting to read stream chunks');
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;

      if (value) {
        const text = decoder.decode(value, { stream: !done });
        buffer += text;
        
        // Process buffer in small chunks for smoother streaming effect
        while (buffer.length > 0) {
          const chunk = buffer.slice(0, Math.min(chunkSize, buffer.length));
          buffer = buffer.slice(chunk.length);
          
          console.log('Processing chunk:', chunk);
          onChunk(chunk);
          
          // Small delay between chunks for visual effect
          if (buffer.length > 0) {
            await new Promise(resolve => setTimeout(resolve, 10));
          }
        }
      }
    }

    console.log('Stream completed');
    onComplete();
  } catch (error) {
    console.error('Error streaming chat message:', error);
    throw error;
  }
};
