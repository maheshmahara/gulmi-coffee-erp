import { Activity, ClipboardCheck, Gauge, PackageSearch, QrCode, ShieldCheck, Warehouse } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { HealthBadge } from "./components/HealthBadge";
import { getMe, getStorageLocations, type CurrentUser, type Role, type StorageLocation } from "./lib/api";
import { LoginPanel } from "./pages/LoginPanel";

const navByRole: Record<Role, string[]> = {
  admin: ["Dashboard", "QR Scan", "Farmers", "Lots", "Procurements", "QIR-B", "Bags", "Storage", "Environment", "Exceptions", "Inventory", "Audit", "Settings"],
  manager: ["Dashboard", "QR Scan", "Farmers", "Lots", "Procurements", "QIR-B", "Bags", "Storage", "Environment", "Exceptions", "Inventory", "Audit"],
  quality: ["Dashboard", "QR Scan", "Farmers", "Lots", "QIR-B", "Exceptions"],
  storage: ["Dashboard", "QR Scan", "Bags", "Storage", "Environment", "Exceptions", "Inventory"],
  production: ["Dashboard", "QR Scan", "Bags", "Inventory"],
  sales: ["Dashboard", "QR Scan", "Inventory"],
  viewer: ["Dashboard", "QR Scan", "Farmers", "Lots", "Bags", "Inventory"]
};

const roleLabels: Record<Role, string> = {
  admin: "Admin",
  manager: "Manager",
  quality: "Quality",
  storage: "Storage",
  production: "Production",
  sales: "Sales",
  viewer: "Viewer"
};

export function App() {
  const [role, setRole] = useState<Role>("admin");
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [activeNav, setActiveNav] = useState("Dashboard");
  const nav = useMemo(() => navByRole[role], [role]);

  useEffect(() => {
    getMe()
      .then((response) => {
        setUser(response.data.user);
        setRole(response.data.user.role);
      })
      .catch(() => undefined);
  }, []);

  useEffect(() => {
    if (!nav.includes(activeNav)) {
      setActiveNav(nav[0]);
    }
  }, [activeNav, nav]);

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">GC</div>
          <div>
            <p className="eyebrow">Gulmi Coffee</p>
            <h1>ERP Sprint 0</h1>
          </div>
        </div>

        <label className="role-switcher">
          <span>Preview role</span>
          <select value={role} onChange={(event) => setRole(event.target.value as Role)}>
            {Object.entries(roleLabels).map(([value, label]) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </label>

        <nav className="nav-list" aria-label="Phase 1 navigation">
          {nav.map((item) => (
            <button key={item} className={item === activeNav ? "active" : ""} onClick={() => setActiveNav(item)}>
              {item}
            </button>
          ))}
        </nav>
      </aside>

      <section className="content">
        <header className="topbar">
          <div>
            <p className="eyebrow">Phase 1 MVP</p>
            <h2>{activeNav}</h2>
          </div>
          <HealthBadge />
        </header>

        {user ? (
          <div className="session-strip">
            Logged in as <strong>{user.full_name}</strong> ({roleLabels[user.role]}) · {user.code ?? user.username}
          </div>
        ) : null}

        <section className="hero-panel">
          <div>
            <p className="eyebrow">Traceability backbone</p>
            <h3>Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR</h3>
            <p>
              Sprint 0 establishes the shell: backend health, project layout, role-aware navigation, and developer-ready Docker setup.
            </p>
          </div>
        </section>

        <section className="grid">
          <StatusCard icon={<ShieldCheck />} title="Sensitive fields" body="Backend filtering is mandatory for rate, total, cost, payment, margin, and profit." />
          <StatusCard icon={<ClipboardCheck />} title="Posted documents" body="Draft records may change. Posted records are locked and corrected with adjustment or exception records." />
          <StatusCard icon={<PackageSearch />} title="Inventory truth" body="Stock is derived from inventory ledger rows only. Direct quantity edits are not allowed." />
          <StatusCard icon={<QrCode />} title="Role-aware QR" body="Logged-in staff see internal traceability. Public visitors see only safe information." />
        </section>

        {activeNav === "Dashboard" ? <DashboardPreview role={role} /> : activeNav === "Storage" ? <StorageLocationsPanel /> : <PlaceholderScreen name={activeNav} />}
        <LoginPanel user={user} onLogin={(nextUser) => { setUser(nextUser); setRole(nextUser.role); }} onLogout={() => setUser(null)} />
      </section>
    </main>
  );
}

function StatusCard({ icon, title, body }: { icon: React.ReactNode; title: string; body: string }) {
  return (
    <article className="status-card">
      <div className="icon">{icon}</div>
      <h4>{title}</h4>
      <p>{body}</p>
    </article>
  );
}

function StorageLocationsPanel() {
  const [locations, setLocations] = useState<StorageLocation[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getStorageLocations()
      .then((response) => {
        setLocations(response.data);
        setError("");
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Could not load storage locations"));
  }, []);

  return (
    <section className="panel">
      <div className="panel-heading">
        <Warehouse />
        <div>
          <h3>Storage locations</h3>
          <p>Seed default locations with <code>python manage.py seed_phase1</code>.</p>
        </div>
      </div>
      {error ? <p className="form-error">{error}</p> : null}
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Code</th>
              <th>Name</th>
              <th>Type</th>
              <th>Parent</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {locations.map((location) => (
              <tr key={location.id}>
                <td>{location.code}</td>
                <td>{location.location_name}</td>
                <td>{location.location_type}</td>
                <td>{location.parent_location_code ?? "-"}</td>
                <td>{location.active ? "active" : "inactive"}</td>
              </tr>
            ))}
            {locations.length === 0 && !error ? (
              <tr>
                <td colSpan={5}>No locations yet. Run the seed command after migrations.</td>
              </tr>
            ) : null}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function DashboardPreview({ role }: { role: Role }) {
  const cards = [
    ["Total bags", "0", "Phase 1 data model pending Sprint 4"],
    ["QIR-B pending", "0", "Quality workflow begins Sprint 3"],
    ["Open exceptions", "0", "Exception workflow begins Sprint 5"],
    ["Latest environment risk", "No data", "Environment logs begin Sprint 5"]
  ];
  return (
    <section className="panel">
      <div className="panel-heading">
        <Gauge />
        <div>
          <h3>{roleLabels[role]} dashboard preview</h3>
          <p>These cards become live API-backed metrics in Sprint 6.</p>
        </div>
      </div>
      <div className="metric-grid">
        {cards.map(([label, value, note]) => (
          <div className="metric" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
            <small>{note}</small>
          </div>
        ))}
      </div>
    </section>
  );
}

function PlaceholderScreen({ name }: { name: string }) {
  return (
    <section className="panel">
      <div className="panel-heading">
        {name === "Storage" ? <Warehouse /> : <Activity />}
        <div>
          <h3>{name} workflow placeholder</h3>
          <p>This screen is registered in the role-aware navigation and will be implemented in its planned sprint.</p>
        </div>
      </div>
    </section>
  );
}
