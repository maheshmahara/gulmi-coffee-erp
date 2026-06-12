export type HealthResponse = {
  data: {
    status: string;
    database: string;
    version: string;
    service: string;
  };
  meta: Record<string, never>;
};

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {})
    },
    ...options
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload?.error?.message ?? `Request failed: ${response.status}`);
  }
  return payload;
}

export async function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export type Role = "admin" | "manager" | "quality" | "storage" | "production" | "sales" | "viewer";

export type CurrentUser = {
  id: string;
  code: string | null;
  username: string;
  full_name: string;
  phone: string;
  role: Role;
  active: boolean;
};

export type AuthResponse = {
  data: {
    user: CurrentUser;
  };
  meta: Record<string, never>;
};

export async function login(phoneOrUsername: string, password: string): Promise<AuthResponse> {
  return request<AuthResponse>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ phone: phoneOrUsername, username: phoneOrUsername, password })
  });
}

export async function logout(): Promise<void> {
  await request("/auth/logout", { method: "POST" });
}

export async function getMe(): Promise<AuthResponse> {
  return request<AuthResponse>("/me");
}

export type StorageLocation = {
  id: string;
  code: string;
  location_name: string;
  location_type: string;
  parent_location_code: string | null;
  active: boolean;
  notes: string;
};

export type StorageLocationListResponse = {
  data: StorageLocation[];
  meta: {
    total: number;
  };
};

export async function getStorageLocations(): Promise<StorageLocationListResponse> {
  return request<StorageLocationListResponse>("/storage-locations");
}

export type Farmer = {
  id: string;
  code: string;
  farmer_name: string;
  father_or_family_name: string;
  phone: string;
  village: string;
  municipality: string;
  district: string;
  ward_no: string;
  gps_location: string;
  photo_url: string;
  bank_or_wallet: string;
  farmer_type: string;
  active: boolean;
  notes: string;
};

export type Lot = {
  id: string;
  code: string;
  farmer: Farmer;
  item_type: string;
  harvest_year: number;
  status: string;
  notes: string;
};

export type Procurement = {
  id: string;
  code: string;
  lot_code: string;
  farmer_name: string;
  item_type: string;
  gross_kg: string;
  tare_kg: string;
  net_kg: string;
  rate_npr: string | null;
  total_npr: string | null;
  received_at: string;
  status: string;
  posted_at: string | null;
  notes: string;
};

export type ListResponse<T> = {
  data: T[];
  meta: {
    total: number;
  };
};

export async function getFarmers(): Promise<ListResponse<Farmer>> {
  return request<ListResponse<Farmer>>("/farmers");
}

export async function createFarmer(payload: Partial<Farmer>): Promise<{ data: Farmer; meta: Record<string, never> }> {
  return request<{ data: Farmer; meta: Record<string, never> }>("/farmers", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function getLots(): Promise<ListResponse<Lot>> {
  return request<ListResponse<Lot>>("/lots");
}

export async function createLot(payload: { farmer_id: string; item_type: string; harvest_year: number; notes?: string }): Promise<{ data: Lot; meta: Record<string, never> }> {
  return request<{ data: Lot; meta: Record<string, never> }>("/lots", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function getProcurements(): Promise<ListResponse<Procurement>> {
  return request<ListResponse<Procurement>>("/procurements");
}

export async function createProcurement(payload: { lot_id: string; gross_kg: string; tare_kg: string; rate_npr?: string; notes?: string }): Promise<{ data: Procurement; meta: Record<string, never> }> {
  return request<{ data: Procurement; meta: Record<string, never> }>("/procurements", {
    method: "POST",
    body: JSON.stringify(payload)
  });
}

export async function postProcurement(id: string): Promise<{ data: Procurement; meta: Record<string, never> }> {
  return request<{ data: Procurement; meta: Record<string, never> }>(`/procurements/${id}/post`, {
    method: "POST"
  });
}
