export interface User {
  id: number;
  username: string;
}

export interface Task {
  id: number;
  n: number;
  status: 'waiting' | 'running' | 'done' | 'cancelled' | 'error';
  result?: number;
  error?: string;
  progress: number;
  created_at: string;
  completed_at?: string;
}

export interface AuthResponse {
  token: string;
  user: User;
} 