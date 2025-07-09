export interface MessageInfoResponse {
    id: string;
    session_id: string;
    role: string;
    content: string;
    created_at: string;
  }
  
  export interface SessionInfoResponse {
    session_id: string;
    user_id: string;
    name: string;
    created_at: string;
    last_activity?: string;
  }