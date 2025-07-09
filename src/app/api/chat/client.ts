import { MessageInfoResponse, SessionInfoResponse } from '@/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;


export async function createNewChatSession(): Promise<string> {
  const response = await fetch(`/api/chat/chat-stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: '', // Empty initial message
      session_id: null, // No session ID for new chat
    }),
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Failed to create new chat session');
  }
  console.log(response);
  // Extract session ID from the response
  const sessionId = response.headers.get('x-session-id') || '';
  return sessionId;
}

export async function getChatHistory(): Promise<SessionInfoResponse[]> {
  const response = await fetch(`/api/chat/history`, {
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Failed to fetch chat history');
  }

  return response.json();
}

export async function getSessionMessages(sessionId: string): Promise<MessageInfoResponse[]> {
  const response = await fetch(`/api/chat/history/${sessionId}`, {
    credentials: 'include',
  });

  if (!response.ok) {
    if (response.status === 404) {
      return null;
    }
    throw new Error('Failed to fetch session messages');
  }

  return response.json();
}

export async function renameSession(sessionId: string, newName: string): Promise<SessionInfoResponse> {
  const response = await fetch(`/api/chat/history/${sessionId}/rename`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ new_name: newName }),
    credentials: 'include',
  });

  if (!response.ok) {
    throw new Error('Failed to rename session');
  }

  return response.json();
}

export async function sendChatMessage(sessionId: string | null, message: string): Promise<ReadableStream> {
  const response = await fetch(`/api/chat/chat-stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      message: message,
      // Add this for guest tracking
      is_guest: !localStorage.getItem('authToken')
    }),
    credentials: 'include' // Important for session cookies
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw { 
      status: response.status,
      message: error.detail || 'Failed to send message' 
    };
  }

  return response.body!;
}