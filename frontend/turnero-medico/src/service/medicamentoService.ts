// src/service/medicamentoService.ts

import axios from 'axios';
import {
  type Medicamento,
  type MedicamentoCreate,
  type MedicamentoUpdate,
} from '../types/Medicamento';

const API_URL = 'http://localhost:8000/medicamentos';

export class MedicamentoService {
  static async getAll(): Promise<Medicamento[]> {
    const res = await axios.get(API_URL + '/');
    return res.data;
  }

  static async getById(id: number): Promise<Medicamento> {
    const res = await axios.get(`${API_URL}/${id}`);
    return res.data;
  }

  static async create(data: MedicamentoCreate): Promise<Medicamento> {
    const payload: MedicamentoCreate = {
      nombre: data.nombre,
      descripcion: data.descripcion,
      ids_laboratorios: data.ids_laboratorios ?? [], // <-- CORRECTO
    };

    const res = await axios.post(API_URL + '/', payload);
    return res.data;
  }

  static async update(
    id: number,
    data: MedicamentoUpdate
  ): Promise<Medicamento> {
    const res = await axios.put(`${API_URL}/${id}`, data);
    return res.data;
  }

  static async delete(id: number): Promise<void> {
    await axios.delete(`${API_URL}/${id}`);
  }
}

export default MedicamentoService;
