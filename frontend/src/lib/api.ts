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

export async function getHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_BASE}/health`);
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.status}`);
  }
  return response.json();
}
