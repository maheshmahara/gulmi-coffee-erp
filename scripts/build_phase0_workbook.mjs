import fs from "node:fs/promises";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const outputDir = "outputs/gulmi-coffee-erp-phase-0";
const outputPath = `${outputDir}/gulmi-coffee-erp-phase-0-workbook.xlsx`;

const workbook = Workbook.create();

function addSheet(name, headers, rows = []) {
  const sheet = workbook.worksheets.add(name);
  sheet.getRangeByIndexes(0, 0, 1, headers.length).values = [headers];
  if (rows.length > 0) {
    sheet.getRangeByIndexes(1, 0, rows.length, headers.length).values = rows;
  }
  return sheet;
}

addSheet(
  "README",
  ["Section", "Details"],
  [
    ["Purpose", "Phase-0 workbook for Gulmi Coffee ERP. One sheet maps to one future ERP table."],
    ["MVP Chain", "Farmer -> Lot -> Procurement -> QIR-B -> Bag -> Storage -> Internal QR"],
    ["Rule", "One row equals one master record or document. Posted rows should not be edited."],
    ["Correction Method", "Use adjustment, exception, inventory ledger, and audit rows instead of silent edits."],
    ["Sensitive Fields", "rate_npr, total_npr, payments, costs, and margin are Admin/Manager-only."],
    ["Color Convention", "Grey system-generated, Yellow user-entry, Green calculated, Red sensitive, Blue status/control."],
    ["Next Use", "Use this workbook to pilot one real procurement-to-bag workflow before software development."],
  ],
);

addSheet(
  "Farmers",
  [
    "farmer_id",
    "farmer_code",
    "farmer_name",
    "father_or_family_name",
    "phone",
    "village",
    "municipality",
    "district",
    "ward_no",
    "gps_location",
    "photo_url",
    "bank_or_wallet",
    "farmer_type",
    "active_status",
    "notes",
    "created_at",
    "created_by",
  ],
  [
    [
      "AUTO",
      "FARM-2026-000001",
      "Ram Bahadur",
      "Bahadur Family",
      "98XXXXXXXX",
      "Tamghas",
      "Resunga",
      "Gulmi",
      "4",
      "",
      "",
      "eSewa/Bank",
      "farmer",
      "active",
      "Sample farmer for pilot workflow",
      "2026-06-11 09:00",
      "Admin",
    ],
  ],
);

addSheet(
  "Users",
  ["user_id", "user_code", "full_name", "phone", "role", "active_status", "created_at", "created_by"],
  [
    ["AUTO", "USER-2026-000001", "Admin User", "98XXXXXXXX", "Admin", "active", "2026-06-11 09:00", "Admin"],
    ["AUTO", "USER-2026-000002", "Quality User", "98XXXXXXXX", "Quality", "active", "2026-06-11 09:00", "Admin"],
    ["AUTO", "USER-2026-000003", "Storage User", "98XXXXXXXX", "Storage", "active", "2026-06-11 09:00", "Admin"],
  ],
);

addSheet(
  "Storage_Locations",
  [
    "location_id",
    "location_code",
    "location_name",
    "location_type",
    "parent_location_code",
    "active_status",
    "notes",
    "created_at",
    "created_by",
  ],
  [
    ["AUTO", "WH-001", "Main Warehouse", "warehouse", "", "active", "Main storage building", "2026-06-11 09:00", "Admin"],
    ["AUTO", "RACK-PAR-001", "Parchment Rack 1", "rack", "WH-001", "active", "For parchment bags", "2026-06-11 09:00", "Admin"],
    ["AUTO", "RACK-GRN-001", "Green Bean Rack 1", "rack", "WH-001", "active", "For green beans", "2026-06-11 09:00", "Admin"],
    ["AUTO", "HOLD-001", "Defect/Recheck Area", "hold_area", "WH-001", "active", "Risk or rejected bags", "2026-06-11 09:00", "Admin"],
    ["AUTO", "DRY-001", "Solar Drying Area", "drying_area", "", "active", "Drying area", "2026-06-11 09:00", "Admin"],
    ["AUTO", "PROD-HULL-001", "Hulling Area", "production_area", "", "active", "Hulling input area", "2026-06-11 09:00", "Admin"],
  ],
);

addSheet(
  "Lots",
  ["lot_id", "lot_code", "farmer_code", "item_type", "harvest_year", "lot_status", "created_at", "created_by", "notes"],
  [["AUTO", "LOT-2026-000001", "FARM-2026-000001", "parchment", 2026, "quality_pending", "2026-06-11 09:30", "Admin", "Sample parchment lot"]],
);

addSheet(
  "Procurements",
  [
    "procurement_id",
    "procurement_code",
    "lot_code",
    "farmer_code",
    "item_type",
    "gross_kg",
    "tare_kg",
    "net_kg",
    "rate_npr",
    "total_npr",
    "received_date",
    "received_by",
    "status",
    "posted_at",
    "notes",
  ],
  [
    [
      "AUTO",
      "PROC-2026-000001",
      "LOT-2026-000001",
      "FARM-2026-000001",
      "parchment",
      705,
      5,
      "=F2-G2",
      1300,
      "=H2*I2",
      "2026-06-11 09:45",
      "Manager",
      "posted",
      "2026-06-11 09:45",
      "Sample receipt",
    ],
  ],
);

addSheet(
  "QIRB_Readings",
  ["reading_id", "qirb_code", "sequence_no", "moisture", "density", "bean_temp", "reading_time", "entered_by"],
  [
    ["AUTO", "QIRB-2026-000001", 1, 11.2, 670, 24.5, "2026-06-11 10:00", "Quality"],
    ["AUTO", "QIRB-2026-000001", 2, 11.4, 665, 24.6, "2026-06-11 10:01", "Quality"],
    ["AUTO", "QIRB-2026-000001", 3, 11.3, 668, 24.7, "2026-06-11 10:02", "Quality"],
    ["AUTO", "QIRB-2026-000001", 4, 11.5, 662, 24.6, "2026-06-11 10:03", "Quality"],
    ["AUTO", "QIRB-2026-000001", 5, 11.2, 671, 24.5, "2026-06-11 10:04", "Quality"],
  ],
);

addSheet(
  "QIRB_Summary",
  [
    "qirb_id",
    "qirb_code",
    "subject_type",
    "subject_code",
    "bean_stage",
    "reading_count",
    "avg_moisture",
    "moisture_sd",
    "avg_density",
    "density_sd",
    "avg_bean_temp",
    "bean_temp_sd",
    "estimated_green_yield_pct",
    "decision",
    "status",
    "checked_by",
    "checked_at",
    "posted_at",
    "notes",
  ],
  [
    [
      "AUTO",
      "QIRB-2026-000001",
      "lot",
      "LOT-2026-000001",
      "parchment",
      '=COUNTIF(QIRB_Readings!B:B,B2)',
      '=AVERAGEIF(QIRB_Readings!B:B,B2,QIRB_Readings!D:D)',
      '=STDEV.S(FILTER(QIRB_Readings!D:D,QIRB_Readings!B:B=B2))',
      '=AVERAGEIF(QIRB_Readings!B:B,B2,QIRB_Readings!E:E)',
      '=STDEV.S(FILTER(QIRB_Readings!E:E,QIRB_Readings!B:B=B2))',
      '=AVERAGEIF(QIRB_Readings!B:B,B2,QIRB_Readings!F:F)',
      '=STDEV.S(FILTER(QIRB_Readings!F:F,QIRB_Readings!B:B=B2))',
      "=70+(I2/50)-0.5*(G2-11)",
      '=IF(F2<5,"retake",IF(H2>0.7,"retake",IF(J2>50,"retake",IF(I2<300,"retake",IF(AND(E2="parchment",G2>12.5),"hold",IF(AND(E2="parchment",G2>=11.6,G2<=12.5),"monitor","approved"))))))',
      "posted",
      "Quality",
      "2026-06-11 10:10",
      "2026-06-11 10:10",
      "Sample QIR-B summary",
    ],
  ],
);

addSheet(
  "Bags",
  [
    "bag_id",
    "bag_code",
    "lot_code",
    "qirb_code",
    "item_type",
    "weight_kg",
    "bag_type",
    "current_location_code",
    "sealed_at",
    "status",
    "qr_url",
    "created_at",
    "created_by",
    "notes",
  ],
  [
    ["AUTO", "BAG-2026-000001", "LOT-2026-000001", "QIRB-2026-000001", "parchment", 60, "jute", "RACK-PAR-001", "2026-06-11 11:00", "in_storage", "https://app.gulmicoffee.com/r/BAG-2026-000001", "2026-06-11 11:00", "Storage", "Sample first bag"],
    ["AUTO", "BAG-2026-000002", "LOT-2026-000001", "QIRB-2026-000001", "parchment", 60, "jute", "RACK-PAR-001", "2026-06-11 11:00", "in_storage", "https://app.gulmicoffee.com/r/BAG-2026-000002", "2026-06-11 11:00", "Storage", "Sample second bag"],
  ],
);

addSheet(
  "Storage_Movements",
  [
    "movement_id",
    "movement_code",
    "bag_code",
    "from_location_code",
    "to_location_code",
    "movement_type",
    "moved_at",
    "moved_by",
    "reason",
    "notes",
  ],
  [
    ["AUTO", "MOVE-2026-000001", "BAG-2026-000001", "RECEIVING", "RACK-PAR-001", "receive_to_storage", "2026-06-11 11:05", "Storage", "Initial storage after bagging", "Good condition"],
    ["AUTO", "MOVE-2026-000002", "BAG-2026-000002", "RECEIVING", "RACK-PAR-001", "receive_to_storage", "2026-06-11 11:05", "Storage", "Initial storage after bagging", "Good condition"],
  ],
);

addSheet(
  "Environment_Logs",
  [
    "environment_log_id",
    "location_code",
    "temperature_c",
    "humidity_pct",
    "ac_status",
    "exhaust_status",
    "risk_flag",
    "logged_at",
    "logged_by",
    "remarks",
  ],
  [["AUTO", "RACK-PAR-001", 24.5, 58, "off", "on", "ideal", "2026-06-11 12:00", "Storage", "Normal condition"]],
);

addSheet(
  "Exception_Log",
  [
    "exception_id",
    "exception_code",
    "subject_type",
    "subject_code",
    "exception_type",
    "severity",
    "reason",
    "action_taken",
    "raised_by",
    "approved_by",
    "status",
    "created_at",
    "resolved_at",
    "notes",
  ],
  [["AUTO", "EXC-2026-000001", "qirb", "QIRB-2026-000001", "manual_override", "low", "Sample exception row only", "No action needed", "Admin", "Manager", "resolved", "2026-06-11 12:30", "2026-06-11 12:45", "Delete sample row when operating"]],
);

addSheet(
  "Inventory_Ledger",
  [
    "ledger_id",
    "ledger_code",
    "item_type",
    "item_code",
    "location_code",
    "qty_delta",
    "uom",
    "movement_reason",
    "ref_doc_type",
    "ref_doc_code",
    "created_at",
    "created_by",
    "notes",
  ],
  [
    ["AUTO", "LEDGER-2026-000001", "bag", "BAG-2026-000001", "RACK-PAR-001", 60, "kg", "bag_created", "bag", "BAG-2026-000001", "2026-06-11 11:05", "Storage", "Bag created after approved QIR-B"],
    ["AUTO", "LEDGER-2026-000002", "bag", "BAG-2026-000002", "RACK-PAR-001", 60, "kg", "bag_created", "bag", "BAG-2026-000002", "2026-06-11 11:05", "Storage", "Bag created after approved QIR-B"],
  ],
);

addSheet(
  "Audit_Log",
  [
    "audit_id",
    "audit_code",
    "table_name",
    "record_code",
    "action",
    "old_value_json",
    "new_value_json",
    "actor",
    "action_time",
    "ip_address",
    "device_id",
    "notes",
  ],
  [
    ["AUTO", "AUDIT-2026-000001", "Farmers", "FARM-2026-000001", "create", "{}", '{"farmer_name":"Ram Bahadur","village":"Tamghas"}', "Admin", "2026-06-11 09:00", "192.168.1.10", "LAPTOP-ADMIN", "Sample farmer created"],
    ["AUTO", "AUDIT-2026-000002", "Bags", "BAG-2026-000001", "print_qr", "{}", '{"qr_url":"https://app.gulmicoffee.com/r/BAG-2026-000001"}', "Storage", "2026-06-11 11:10", "192.168.1.20", "PHONE-STORE-01", "Sample QR printed"],
  ],
);

addSheet(
  "Validation_Lists",
  ["List Name", "Allowed Values"],
  [
    ["farmer_type", "farmer, collector, cooperative, supplier"],
    ["user_role", "Admin, Manager, Quality, Storage, Production, Sales, Viewer"],
    ["item_type", "fresh_cherry, dry_cherry, parchment, green_bean, roasted_bean"],
    ["lot_status", "draft, received, quality_pending, approved, hold, bagged, closed"],
    ["procurement_status", "draft, posted, cancelled, adjusted"],
    ["qirb_decision", "approved, monitor, hold, retake"],
    ["bag_status", "in_storage, on_hold, moved, consumed, lost, closed"],
    ["movement_type", "receive_to_storage, transfer, move_to_drying, return_from_drying, move_to_hulling, hold, release, adjustment"],
    ["environment_risk", "dry_risk, ideal, monitor, risk, critical"],
    ["exception_severity", "low, medium, high, critical"],
    ["audit_action", "create, update_draft, post, cancel, adjust, approve, reject, login, logout, export, print_qr, scan_qr, override, delete_draft"],
  ],
);

await fs.mkdir(outputDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);

console.log(outputPath);
