import { useEffect, useState } from "react";
import { getHealth, type HealthResponse } from "../lib/api";

export function HealthBadge() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getHealth()
      .then((response) => {
        setHealth(response);
        setError("");
      })
      .catch(() => {
        setError("Backend offline");
      });
  }, []);

  if (error) {
    return <span className="health-badge offline">{error}</span>;
  }

  return <span className="health-badge">{health ? `API ${health.data.status}` : "Checking API"}</span>;
}
