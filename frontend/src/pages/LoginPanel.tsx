export function LoginPanel() {
  return (
    <section className="panel login-panel">
      <div>
        <p className="eyebrow">Sprint 1 target</p>
        <h3>Login workflow foundation</h3>
        <p>
          Authentication UI is scaffolded here. Sprint 1 will wire it to `/api/v1/auth/login`, `/api/v1/auth/logout`, and `/api/v1/me`.
        </p>
      </div>
      <form>
        <label>
          Phone
          <input placeholder="98XXXXXXXX" disabled />
        </label>
        <label>
          Password/PIN
          <input placeholder="Sprint 1" disabled type="password" />
        </label>
        <button type="button" disabled>
          Login
        </button>
      </form>
    </section>
  );
}
