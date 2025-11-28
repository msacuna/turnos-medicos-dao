import axios from 'axios';
import type {
  Especialidad,
  EspecialidadCreate,
  EspecialidadUpdate,
} from '../types/Especialidad';

const API_URL = 'http://localhost:8000/especialidades';

export class EspecialidadService {
  static async getAll(): Promise<Especialidad[]> {
    const res = await axios.get(API_URL);
    return res.data;
  }

  static async getById(id: number): Promise<Especialidad> {
    const res = await axios.get(`${API_URL}/${id}`);
    return res.data;
  }

  static async create(data: EspecialidadCreate): Promise<Especialidad> {
    const res = await axios.post(API_URL, data);
    return res.data;
  }

  static async update(
    id: number,
    data: EspecialidadUpdate
  ): Promise<Especialidad> {
    const res = await axios.put(`${API_URL}/${id}`, data);
    return res.data;
  }

  static async delete(id: number): Promise<void> {
    await axios.delete(`${API_URL}/${id}`);
  }
}
