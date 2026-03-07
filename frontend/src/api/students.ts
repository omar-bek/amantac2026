import apiClient from './client'

export interface Student {
  id: number
  student_id: string
  full_name: string
  date_of_birth?: string
  grade?: string
  class_name?: string
  parent_id: number
  bus_id?: number
  is_active: boolean
  created_at: string
}

export const studentsAPI = {
  getAll: async (): Promise<Student[]> => {
    const response = await apiClient.get<Student[]>('/students/')
    return response.data
  },

  getById: async (id: number): Promise<Student> => {
    const response = await apiClient.get<Student>(`/students/${id}`)
    return response.data
  },

  getByParent: async (parentId: number): Promise<Student[]> => {
    const response = await apiClient.get<Student[]>(`/students/parent/${parentId}`)
    return response.data
  },
}





