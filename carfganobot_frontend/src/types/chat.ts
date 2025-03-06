export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface Topic {
  id: string;
  title: string;
}

export interface ChatResponse {
  message: string;
  disclaimer: string;
  suggested_topics?: Topic[];
}
