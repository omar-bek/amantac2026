import apiClient from './client'

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  phone?: string
  full_name: string
  role: 'parent' | 'teacher' | 'admin' | 'staff' | 'driver'
  password: string
}

export interface User {
  id: number
  email: string
  phone?: string
  full_name: string
  role: string
  is_active: boolean
  created_at: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export const authAPI = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/auth/login', credentials)
    return response.data
  },

  register: async (data: RegisterData): Promise<User> => {
    const response = await apiClient.post<User>('/auth/register', data)
    return response.data
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/me')
    return response.data
  },
}





