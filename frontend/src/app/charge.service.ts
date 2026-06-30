import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ClinicCharge {
  id: number;
  medical_centre_name: string;
  patient_visit_type: string;
  charge_type: string;
  amount: number;
}

export interface PaginatedResult {
  rows: ClinicCharge[];
  total: number;
}

@Injectable({ providedIn: 'root' })
export class ChargeService {

  private base = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  getCharges(startRow: number, endRow: number, chargeType?: string, centreName?: string): Observable<PaginatedResult> {

    let params = new HttpParams().set('startRow', startRow).set('endRow', endRow);

    if (chargeType) {
      params = params.set('charge_type', chargeType);
    }

    if (centreName) {
      params = params.set('medical_centre_name', centreName);
    }

    return this.http.get<PaginatedResult>(`${this.base}/charges`, { params });
  }

  createCharge(charge: Omit<ClinicCharge, 'id'>): Observable<ClinicCharge> {
    return this.http.post<ClinicCharge>(`${this.base}/charges`, charge);
  }

  updateCharge(id: number, fields: Partial<ClinicCharge>): Observable<ClinicCharge> {
    return this.http.patch<ClinicCharge>(`${this.base}/charges/${id}`, fields);
  }

  fetchFilterChargesType() {
      return this.http.get<string[]>(`${this.base}/charge-types`);
  }

  fetchVisitTypes() {
    return this.http.get<string[]>(`${this.base}/patient-visit-types`);
  }

}
