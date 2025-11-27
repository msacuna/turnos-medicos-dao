import axios from 'axios';
import {
  type Alergia,
  type AlergiaCreate,
  type AlergiaUpdate,
} from '../types/Alergia';

const API_URL = 'http://localhost:8000/alergias';

export class AlergiaService {
  static async getAll(): Promise<Alergia[]> {
    const res = await axios.get(API_URL + '/');
    return res.data;
  }

  static async getById(id: number): Promise<Alergia> {
    const res = await axios.get(API_URL + `/${id}`);
    return res.data;
  }

  static async create(data: AlergiaCreate): Promise<Alergia> {
    const res = await axios.post(API_URL + '/', data);
    return res.data;
  }

  static async update(id: number, data: AlergiaUpdate): Promise<Alergia> {
    const res = await axios.put(API_URL + `/${id}`, data);
    return res.data;
  }

  static async delete(id: number): Promise<void> {
    await axios.delete(API_URL + `/${id}`);
  }
}
