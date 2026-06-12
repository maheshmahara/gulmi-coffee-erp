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
