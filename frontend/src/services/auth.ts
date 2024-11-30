import api from './api';
import { AuthResponse } from '../types';

export const login = async (username: string, password: string): Promise<AuthResponse> => {
  const response = await api.post<AuthResponse>('/auth/login', { username, password });
  return response.data;
};

export const register = async (username: string, password: string): Promise<void> => {
  await api.post('/auth/register', { username, password });
}; 