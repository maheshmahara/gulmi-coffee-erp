import { FormEvent, useState } from "react";

import { login, logout, type CurrentUser } from "../lib/api";


export function LoginPanel({ user, onLogin, onLogout }: { user: CurrentUser | null; onLogin: (user: CurrentUser) => void; onLogout: () => void }) {
  const [identifier, setIdentifier] = useState("admin");
  const [password, setPassword] = useState("ChangeMe123!");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await login(identifier, password);
      onLogin(response.data.user);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setLoading(false);
    }
  }

  async function handleLogout() {
    setLoading(true);
    setError("");
    try {
      await logout();
      onLogout();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Logout failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="panel login-panel">
      <div>
        <p className="eyebrow">Sprint 1</p>
        <h3>Login workflow</h3>
        <p>
          Seed users use password <code>ChangeMe123!</code>. Use this only for local/staging development.
        </p>
      </div>
      <form onSubmit={handleSubmit}>
        <label>
          Phone or username
          <input value={identifier} onChange={(event) => setIdentifier(event.target.value)} placeholder="admin" />
        </label>
        <label>
          Password/PIN
          <input value={password} onChange={(event) => setPassword(event.target.value)} type="password" />
        </label>
        {user ? <button type="button" onClick={handleLogout} disabled={loading}>Logout {user.full_name}</button> : <button type="submit" disabled={loading}>{loading ? "Working..." : "Login"}</button>}
        {error ? <p className="form-error">{error}</p> : null}
      </form>
    </section>
  );
}
