import { Activity, ClipboardCheck, Gauge, PackageSearch, QrCode, ShieldCheck, Warehouse } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import type { ReactNode } from "react";
import { HealthBadge } from "./components/HealthBadge";
import {
  createFarmer,
  createLot,
  createProcurement,
  getFarmers,
  getLots,
  getMe,
  getProcurements,
  getStorageLocations,
  postProcurement,
  type CurrentUser,
  type Farmer,
  type Lot,
  type Procurement,
  type Role,
  type StorageLocation
} from "./lib/api";
import { LoginPanel } from "./pages/LoginPanel";

const navByRole: Record<Role, string[]> = {
  admin: ["Dashboard", "QR Scan", "Farmers", "Lots", "Procurements", "QIR-B", "Bags", "Storage", "Environment", "Exceptions", "Inventory", "Audit", "Settings"],
  manager: ["Dashboard", "QR Scan", "Farmers", "Lots", "Procurements", "QIR-B", "Bags", "Storage", "Environment", "Exceptions", "Inventory", "Audit"],
  quality: ["Dashboard", "QR Scan", "Farmers", "Lots", "Procurements", "QIR-B", "Exceptions"],
  storage: ["Dashboard", "QR Scan", "Farmers", "Lots", "Procurements", "Bags", "Storage", "Environment", "Exceptions", "Inventory"],
  production: ["Dashboard", "QR Scan", "Bags", "Inventory"],
  sales: ["Dashboard", "QR Scan", "Inventory"],
  viewer: ["Dashboard", "QR Scan", "Farmers", "Lots", "Procurements", "Bags", "Inventory"]
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
            <h1>ERP Sprint 2</h1>
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
            <h3>Farmer to Lot to Procurement to QIR-B to Bag to Storage to Internal QR</h3>
            <p>
              Sprint 2 adds farmer, lot, and procurement receipts with posting locks and role-safe cost visibility.
            </p>
          </div>
        </section>

        <section className="grid">
          <StatusCard icon={<ShieldCheck />} title="Sensitive fields" body="Backend filtering is mandatory for rate, total, cost, payment, margin, and profit." />
          <StatusCard icon={<ClipboardCheck />} title="Posted documents" body="Draft records may change. Posted records are locked and corrected with adjustment or exception records." />
          <StatusCard icon={<PackageSearch />} title="Inventory truth" body="Stock is derived from inventory ledger rows only. Direct quantity edits are not allowed." />
          <StatusCard icon={<QrCode />} title="Role-aware QR" body="Logged-in staff see internal traceability. Public visitors see only safe information." />
        </section>

        {activeNav === "Dashboard" ? (
          <DashboardPreview role={role} />
        ) : activeNav === "Farmers" ? (
          <FarmersPanel canEdit={role === "admin" || role === "manager"} />
        ) : activeNav === "Lots" ? (
          <LotsPanel canEdit={role === "admin" || role === "manager"} />
        ) : activeNav === "Procurements" ? (
          <ProcurementsPanel canEdit={role === "admin" || role === "manager"} canViewCost={role === "admin" || role === "manager"} />
        ) : activeNav === "Storage" ? (
          <StorageLocationsPanel />
        ) : (
          <PlaceholderScreen name={activeNav} />
        )}
        <LoginPanel user={user} onLogin={(nextUser) => { setUser(nextUser); setRole(nextUser.role); }} onLogout={() => setUser(null)} />
      </section>
    </main>
  );
}

function StatusCard({ icon, title, body }: { icon: ReactNode; title: string; body: string }) {
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

function FarmersPanel({ canEdit }: { canEdit: boolean }) {
  const [farmers, setFarmers] = useState<Farmer[]>([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ farmer_name: "", phone: "", village: "", district: "Gulmi", farmer_type: "farmer" });

  const refresh = () => getFarmers().then((response) => setFarmers(response.data));

  useEffect(() => {
    refresh().catch((err) => setError(err instanceof Error ? err.message : "Could not load farmers"));
  }, []);

  const submit = async () => {
    setError("");
    try {
      await createFarmer(form);
      setForm({ farmer_name: "", phone: "", village: "", district: "Gulmi", farmer_type: "farmer" });
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create farmer");
    }
  };

  return (
    <section className="panel">
      <div className="panel-heading">
        <ClipboardCheck />
        <div>
          <h3>Farmers and collectors</h3>
          <p>Admin/Manager can create suppliers. Other roles can read only.</p>
        </div>
      </div>
      {error ? <p className="form-error">{error}</p> : null}
      {canEdit ? (
        <div className="inline-form">
          <input placeholder="Farmer name" value={form.farmer_name} onChange={(event) => setForm({ ...form, farmer_name: event.target.value })} />
          <input placeholder="Phone" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} />
          <input placeholder="Village" value={form.village} onChange={(event) => setForm({ ...form, village: event.target.value })} />
          <select value={form.farmer_type} onChange={(event) => setForm({ ...form, farmer_type: event.target.value })}>
            <option value="farmer">Farmer</option>
            <option value="collector">Collector</option>
            <option value="cooperative">Cooperative</option>
            <option value="supplier">Supplier</option>
          </select>
          <button onClick={submit}>Create farmer</button>
        </div>
      ) : null}
      <DataTable>
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Phone</th>
            <th>Village</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {farmers.map((farmer) => (
            <tr key={farmer.id}>
              <td>{farmer.code}</td>
              <td>{farmer.farmer_name}</td>
              <td>{farmer.phone}</td>
              <td>{farmer.village}</td>
              <td>{farmer.farmer_type}</td>
            </tr>
          ))}
        </tbody>
      </DataTable>
    </section>
  );
}

function LotsPanel({ canEdit }: { canEdit: boolean }) {
  const [farmers, setFarmers] = useState<Farmer[]>([]);
  const [lots, setLots] = useState<Lot[]>([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ farmer_id: "", item_type: "parchment", harvest_year: new Date().getFullYear(), notes: "" });

  const refresh = async () => {
    const [farmerResponse, lotResponse] = await Promise.all([getFarmers(), getLots()]);
    setFarmers(farmerResponse.data);
    setLots(lotResponse.data);
    setForm((current) => ({ ...current, farmer_id: current.farmer_id || farmerResponse.data[0]?.id || "" }));
  };

  useEffect(() => {
    refresh().catch((err) => setError(err instanceof Error ? err.message : "Could not load lots"));
  }, []);

  const submit = async () => {
    setError("");
    try {
      await createLot(form);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create lot");
    }
  };

  return (
    <section className="panel">
      <div className="panel-heading">
        <PackageSearch />
        <div>
          <h3>Lots</h3>
          <p>Create a lot for one farmer/collector and coffee item type.</p>
        </div>
      </div>
      {error ? <p className="form-error">{error}</p> : null}
      {canEdit ? (
        <div className="inline-form">
          <select value={form.farmer_id} onChange={(event) => setForm({ ...form, farmer_id: event.target.value })}>
            <option value="">Select farmer</option>
            {farmers.map((farmer) => (
              <option key={farmer.id} value={farmer.id}>{farmer.code} - {farmer.farmer_name}</option>
            ))}
          </select>
          <select value={form.item_type} onChange={(event) => setForm({ ...form, item_type: event.target.value })}>
            <option value="fresh_cherry">Fresh cherry</option>
            <option value="dry_cherry">Dry cherry</option>
            <option value="parchment">Parchment</option>
            <option value="green_bean">Green bean</option>
          </select>
          <input type="number" value={form.harvest_year} onChange={(event) => setForm({ ...form, harvest_year: Number(event.target.value) })} />
          <button onClick={submit} disabled={!form.farmer_id}>Create lot</button>
        </div>
      ) : null}
      <DataTable>
        <thead>
          <tr>
            <th>Code</th>
            <th>Farmer</th>
            <th>Item</th>
            <th>Harvest</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {lots.map((lot) => (
            <tr key={lot.id}>
              <td>{lot.code}</td>
              <td>{lot.farmer.farmer_name}</td>
              <td>{lot.item_type}</td>
              <td>{lot.harvest_year}</td>
              <td><span className={lot.status === "quality_pending" ? "status-pill warning" : "status-pill"}>{lot.status}</span></td>
            </tr>
          ))}
        </tbody>
      </DataTable>
    </section>
  );
}

function ProcurementsPanel({ canEdit, canViewCost }: { canEdit: boolean; canViewCost: boolean }) {
  const [lots, setLots] = useState<Lot[]>([]);
  const [procurements, setProcurements] = useState<Procurement[]>([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ lot_id: "", gross_kg: "", tare_kg: "0", rate_npr: "", notes: "" });

  const refresh = async () => {
    const [lotResponse, procurementResponse] = await Promise.all([getLots(), getProcurements()]);
    setLots(lotResponse.data);
    setProcurements(procurementResponse.data);
    setForm((current) => ({ ...current, lot_id: current.lot_id || lotResponse.data[0]?.id || "" }));
  };

  useEffect(() => {
    refresh().catch((err) => setError(err instanceof Error ? err.message : "Could not load procurements"));
  }, []);

  const submit = async () => {
    setError("");
    try {
      await createProcurement(form);
      setForm((current) => ({ ...current, gross_kg: "", tare_kg: "0", rate_npr: "", notes: "" }));
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not create procurement");
    }
  };

  const post = async (id: string) => {
    setError("");
    try {
      await postProcurement(id);
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not post procurement");
    }
  };

  return (
    <section className="panel">
      <div className="panel-heading">
        <Warehouse />
        <div>
          <h3>Procurement receipts</h3>
          <p>Net kg and total NPR are calculated by the backend. Posted receipts are locked.</p>
        </div>
      </div>
      {error ? <p className="form-error">{error}</p> : null}
      {canEdit ? (
        <div className="inline-form">
          <select value={form.lot_id} onChange={(event) => setForm({ ...form, lot_id: event.target.value })}>
            <option value="">Select lot</option>
            {lots.map((lot) => (
              <option key={lot.id} value={lot.id}>{lot.code} - {lot.farmer.farmer_name}</option>
            ))}
          </select>
          <input placeholder="Gross kg" value={form.gross_kg} onChange={(event) => setForm({ ...form, gross_kg: event.target.value })} />
          <input placeholder="Tare kg" value={form.tare_kg} onChange={(event) => setForm({ ...form, tare_kg: event.target.value })} />
          {canViewCost ? <input placeholder="Rate NPR" value={form.rate_npr} onChange={(event) => setForm({ ...form, rate_npr: event.target.value })} /> : null}
          <button onClick={submit} disabled={!form.lot_id || !form.gross_kg}>Create receipt</button>
        </div>
      ) : null}
      <DataTable>
        <thead>
          <tr>
            <th>Code</th>
            <th>Lot</th>
            <th>Farmer</th>
            <th>Net kg</th>
            {canViewCost ? <th>Rate</th> : null}
            {canViewCost ? <th>Total</th> : null}
            <th>Status</th>
            {canEdit ? <th>Action</th> : null}
          </tr>
        </thead>
        <tbody>
          {procurements.map((procurement) => (
            <tr key={procurement.id}>
              <td>{procurement.code}</td>
              <td>{procurement.lot_code}</td>
              <td>{procurement.farmer_name}</td>
              <td>{procurement.net_kg}</td>
              {canViewCost ? <td>{procurement.rate_npr ?? "-"}</td> : null}
              {canViewCost ? <td>{procurement.total_npr ?? "-"}</td> : null}
              <td><span className={procurement.status === "posted" ? "status-pill success" : "status-pill"}>{procurement.status}</span></td>
              {canEdit ? <td>{procurement.status === "draft" ? <button className="table-action" onClick={() => post(procurement.id)}>Post</button> : "Locked"}</td> : null}
            </tr>
          ))}
        </tbody>
      </DataTable>
    </section>
  );
}

function DataTable({ children }: { children: ReactNode }) {
  return (
    <div className="table-wrap">
      <table>{children}</table>
    </div>
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
