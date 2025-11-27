// src/service/antecedenteService.ts

import axios from 'axios';
import {
  type Antecedente,
  type AntecedenteCreate,
  type AntecedenteUpdate,
} from '../types/Antecedente';

const API_URL = 'http://localhost:8000/antecedentes';

export class AntecedenteService {
  static async getAll(): Promise<Antecedente[]> {
    const res = await axios.get(API_URL + '/');
    return res.data;
  }

  static async getById(id: number): Promise<Antecedente> {
    const res = await axios.get(API_URL + `/${id}`);
    return res.data;
  }

  static async create(data: AntecedenteCreate): Promise<Antecedente> {
    const res = await axios.post(API_URL + '/', data);
    return res.data;
  }

  static async update(
    id: number,
    data: AntecedenteUpdate
  ): Promise<Antecedente> {
    const res = await axios.put(API_URL + `/${id}`, data);
    return res.data;
  }

  static async delete(id: number): Promise<void> {
    await axios.delete(API_URL + `/${id}`);
  }
}
