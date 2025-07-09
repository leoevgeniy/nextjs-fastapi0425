export interface Message {
    id: string;
    role: 'user' | 'assistant' | 'error';
    content: string;
    createdAt: string;
  }
  
  export interface ChatSession {
    id: string;
    name: string;
    lastActivity: string;
    messageCount: number;
  }