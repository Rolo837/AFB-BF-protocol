#!/usr/bin/env node
// Generates ts/src/models.ts from spec/schemas/**/*.json (draft 2020-12).
//
// json-schema-to-typescript (and its ref-parser) don't reliably bundle this
// repo's cross-file $ref graph (self-referencing $defs inside a $ref'd whole
// file trip up the automatic hoisting). Instead we do our own minimal, fully
// deterministic bundling: every file's own $defs (and its root shape) get a
// namespaced key in one flat $defs object, every $ref gets rewritten to point
// at that flat key, and a SINGLE compile() call (unreachableDefinitions:
// true) emits one named interface/type per key — so a $def reused by several
// schemas (e.g. condition.v1.json's priceExpr, shared by deal.v2/tradeplan.v2
// /alarm.v1) is declared once and referenced by name everywhere else.
//
// Keys that are part of NAMED_SCHEMAS (the public export surface) use the
// export name itself as the $defs key, so the single compile() call names
// them exactly right with no extra step.
//
// Run via `afb-bf-protocol-generate` (python calls this as a subprocess) or
// directly: `node ts/tools/generate-models.mjs`.
import { createHash } from "node:crypto";
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join, normalize, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { compile } from "json-schema-to-typescript";

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(__dirname, "..", "..");
const schemasDir = join(repoRoot, "spec", "schemas");
const payloadsDir = join(schemasDir, "payloads");
const outFile = join(repoRoot, "ts", "src", "models.ts");
// Ephemeral hand-off to the Python side (datamodel-codegen), so Python
// TypedDicts and TS interfaces share the exact same $defs bundling/naming.
// Not committed — see .gitignore.
const bundledSchemaFile = join(repoRoot, "spec", ".generated", "bundled-schema.json");

function pascalCase(stem) {
  return stem
    .split(/[._-]/)
    .filter(Boolean)
    .map((part) => part[0].toUpperCase() + part.slice(1))
    .join("");
}

// relative-to-spec/schemas path -> desired export name for the file's ROOT.
function namedRootSchemas() {
  const entries = {
    "envelope.json": "Envelope",
    "deal.v1.json": "DealV1",
    "deal.v2.json": "DealV2",
    "deal_state.v2.json": "DealStateV2",
    "tradeplan.v1.json": "TradePlanV1",
    "tradeplan.v2.json": "TradePlanV2",
    "alarm.v1.json": "AlarmV1",
    "gp.v1.json": "GpV1",
    "notification.deal.v1.json": "NotificationDealV1",
    "notification.alarm.v1.json": "NotificationAlarmV1",
    "notification.link.v1.json": "NotificationLinkV1",
    "afbws/deal.event.v1.json": "DealEventPush",
    "afbws/deal.pnl.v1.json": "DealPnlPush",
    "afbws/deal.record.v1.json": "DealRecordPush",
    "afbws/bf_registry_entry.v1.json": "BfRegistryEntry",
    "afbws/connector.record.v1.json": "ConnectorRecord",
    "afbws/connector.list.v1.json": "ConnectorListData",
    "afbws/bfs.registry.v1.json": "BfsRegistryPush",
    "afbws/account.snapshot.v1.json": "AccountSnapshotPush",
    "afbws/account.orders.v1.json": "AccountOrdersPush",
    "afbws/account.catalog.v1.json": "AccountCatalogPush",
    "afbws/account.instrument.v1.json": "AccountInstrumentPush",
    "afbws/account.events.v1.json": "AccountEventsPush",
    "afbws/alarm.channel.v1.json": "AlarmChannelV1Message",
    "afbws/tradeplan.channel.v1.json": "TradeplanChannelV1Message",
    "afbws/link.user.v1.json": "LinkUserV1",
    "afbws/link.admin.v1.json": "LinkAdminV1",
    "afbws/link.status.v1.json": "LinkStatusV1",
    "afbws/link.channel.v1.json": "LinkChannelV1Message",
    "afbws/gp.channel.v1.json": "GpChannelV1Message",
  };
  for (const file of readdirSync(payloadsDir).sort()) {
    if (!file.endsWith(".json")) continue;
    const stem = file.replace(/\.json$/, "");
    entries[`payloads/${file}`] = `${pascalCase(stem)}Payload`;
  }
  return entries;
}

// relative-to-spec/schemas path -> { defName: exportName } for named $defs
// members (as opposed to named file roots).
const NAMED_DEF_SCHEMAS = {
  "condition.v1.json": { conditionNode: "ConditionNode" },
  "afbws/bfs.registry.v1.json": { entry: "BfsRegistryEntry" },
  "afbws/account.events.v1.json": { record: "AccountEventRecord" },
  "afbws/connector.record.v1.json": {
    backstop: "ConnectorBackstop",
    executionPolicy: "ConnectorExecutionPolicy",
  },
  "afbws/alarm.channel.v1.json": {
    getRequest: "AlarmGetRequest",
    getResponse: "AlarmGetResponse",
    listRequest: "AlarmListRequest",
    listResponse: "AlarmListResponse",
    setRequest: "AlarmSetRequest",
    setResponse: "AlarmSetResponse",
    deleteRequest: "AlarmDeleteRequest",
    deleteResponse: "AlarmDeleteResponse",
    errorResponse: "AlarmErrorResponse",
    triggerEvent: "AlarmTriggerEvent",
    triggeredPush: "AlarmTriggeredPush",
    ackEvent: "AlarmAckEvent",
    ackRequest: "AlarmAckRequest",
    ackResultItem: "AlarmAckResultItem",
    ackResponse: "AlarmAckResponse",
  },
  "afbws/tradeplan.channel.v1.json": {
    entityV1: "TradeplanEntityV1",
    entity: "TradeplanEntity",
    amendResultItem: "TradeplanAmendResultItem",
    getRequest: "TradeplanGetRequest",
    getResponse: "TradeplanGetResponse",
    listRequest: "TradeplanListRequest",
    listResponse: "TradeplanListResponse",
    setRequest: "TradeplanSetRequest",
    setResponse: "TradeplanSetResponse",
    deleteRequest: "TradeplanDeleteRequest",
    deleteResponse: "TradeplanDeleteResponse",
    errorResponse: "TradeplanErrorResponse",
    syncPush: "TradeplanSyncPush",
  },
  "afbws/link.user.v1.json": {
    sharedFields: "LinkSharedFields",
    setInputShared: "LinkSetInputShared",
    setInput: "LinkUserSetInput",
  },
  "afbws/link.admin.v1.json": {
    setInput: "LinkAdminSetInput",
  },
  "afbws/link.status.v1.json": {
    session: "LinkSession",
  },
  "afbws/link.channel.v1.json": {
    entity: "LinkEntity",
    setInput: "LinkSetInput",
    getRequest: "LinkGetRequest",
    getResponse: "LinkGetResponse",
    listRequest: "LinkListRequest",
    listResponse: "LinkListResponse",
    setRequest: "LinkSetRequest",
    setResponse: "LinkSetResponse",
    deleteRequest: "LinkDeleteRequest",
    deleteResponse: "LinkDeleteResponse",
    pairRequest: "LinkPairRequest",
    pairResponse: "LinkPairResponse",
    restartRequest: "LinkRestartRequest",
    restartResponse: "LinkRestartResponse",
    errorResponse: "LinkErrorResponse",
    syncPush: "LinkSyncPush",
    statusSyncPush: "LinkStatusSyncPush",
    statusPush: "LinkStatusPush",
  },
  "afbws/gp.channel.v1.json": {
    getRequest: "GpGetRequest",
    getResponse: "GpGetResponse",
    listRequest: "GpListRequest",
    listResponse: "GpListResponse",
    setRequest: "GpSetRequest",
    setResponse: "GpSetResponse",
    deleteRequest: "GpDeleteRequest",
    deleteResponse: "GpDeleteResponse",
    errorResponse: "GpErrorResponse",
    errorDetails: "GpErrorDetails",
  },
};

function loadSchemas() {
  const files = new Map(); // relPath -> parsed JSON
  const walk = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      // Parked drafts (spec/schemas/draft/) stay out of models.ts.
      if (entry.isDirectory()) {
        if (entry.name === "draft") continue;
        walk(full);
      } else if (entry.name.endsWith(".json")) {
        const rel = relative(schemasDir, full).split("\\").join("/");
        files.set(rel, JSON.parse(readFileSync(full, "utf8")));
      }
    }
  };
  walk(schemasDir);
  return files;
}

function resolveRefPath(fromRelPath, ref) {
  // ref is either "name.json", "name.json#/$defs/x", "../x.json#/...", or "#/$defs/x" (same-file, handled by caller).
  const hashIdx = ref.indexOf("#");
  const filePart = hashIdx === -1 ? ref : ref.slice(0, hashIdx);
  const fragment = hashIdx === -1 ? "" : ref.slice(hashIdx + 1);
  const fromDir = dirname(fromRelPath);
  const resolved = normalize(join(fromDir, filePart)).split("\\").join("/");
  const defName = fragment.startsWith("/$defs/") ? fragment.slice("/$defs/".length) : null;
  return { file: resolved, defName };
}

function main() {
  const schemas = loadSchemas();
  const rootExportName = namedRootSchemas();

  // Some files re-export another file's $def verbatim as a pure redirect
  // (e.g. deal.v2.json's own `priceExpr` $def is just `{"$ref":
  // "condition.v1.json#/$defs/priceExpr"}`, kept for readability of deal.v2
  // itself). Collapse those aliases so every use site — regardless of which
  // file's name it was reached through — points at the ONE canonical def;
  // otherwise the compiler ends up with two structurally-identical $defs and
  // picks a name for each unpredictably.
  const aliasTarget = new Map(); // "file\0defName" -> "file\0defName"
  for (const [relPath, doc] of schemas.entries()) {
    for (const [defName, defValue] of Object.entries(doc.$defs ?? {})) {
      const keys = Object.keys(defValue).filter((k) => k !== "description" && k !== "title");
      if (keys.length === 1 && keys[0] === "$ref" && typeof defValue.$ref === "string") {
        const ref = defValue.$ref;
        const target = ref.startsWith("#/$defs/")
          ? { file: relPath, defName: ref.slice("#/$defs/".length) }
          : resolveRefPath(relPath, ref);
        aliasTarget.set(`${relPath}\0${defName}`, `${target.file}\0${target.defName}`);
      }
    }
  }

  function resolveAlias(relPath, defName) {
    let current = `${relPath}\0${defName}`;
    const seen = new Set([current]);
    while (aliasTarget.has(current)) {
      current = aliasTarget.get(current);
      if (seen.has(current)) break; // cycle guard, shouldn't happen
      seen.add(current);
    }
    const [file, name] = current.split("\0");
    return { file, defName: name };
  }

  function keyFor(relPath, defName) {
    if (defName === null) {
      const exported = rootExportName[relPath];
      if (exported) return exported;
      return `${pascalCase(relPath.replace(/\.json$/, "").replace(/\//g, "_"))}_Root`;
    }
    const resolved = resolveAlias(relPath, defName);
    const exported = NAMED_DEF_SCHEMAS[resolved.file]?.[resolved.defName];
    if (exported) return exported;
    return `${pascalCase(resolved.file.replace(/\.json$/, "").replace(/\//g, "_"))}_${pascalCase(resolved.defName)}`;
  }

  function rewrite(node, fromRelPath) {
    if (Array.isArray(node)) return node.map((item) => rewrite(item, fromRelPath));
    if (node && typeof node === "object") {
      const out = {};
      for (const [k, v] of Object.entries(node)) {
        // `title` drives json-schema-to-typescript's naming heuristic and
        // would override our deterministic $defs-key naming (and collides
        // across files — several oneOf branches share titles like "price
        // touch"). `description` is kept — it becomes a useful JSDoc comment.
        if (k === "title") continue;
        if (k === "$ref" && typeof v === "string") {
          if (v.startsWith("#/$defs/")) {
            out.$ref = `#/$defs/${keyFor(fromRelPath, v.slice("#/$defs/".length))}`;
          } else {
            const { file, defName } = resolveRefPath(fromRelPath, v);
            out.$ref = `#/$defs/${keyFor(file, defName)}`;
          }
        } else {
          out[k] = rewrite(v, fromRelPath);
        }
      }
      return out;
    }
    return node;
  }

  const bundledDefs = {};
  for (const [relPath, doc] of schemas.entries()) {
    const { $schema, $id, $defs, ...rootRest } = doc;
    // Files whose root is just `{"type":"object","$ref":"#/$defs/x"}` (a
    // redirect, e.g. condition.v1.json) have no independent shape worth a
    // ROOT entry, and a $ref-with-siblings root confuses the compiler's
    // naming. Skip it unless the file is an explicit named export (none are,
    // today) — nothing in this repo references such a file whole anyway.
    const isRedirectOnly = typeof rootRest.$ref === "string";
    if (!isRedirectOnly || rootExportName[relPath]) {
      bundledDefs[keyFor(relPath, null)] = rewrite(rootRest, relPath);
    }
    for (const [defName, defValue] of Object.entries($defs ?? {})) {
      if (aliasTarget.has(`${relPath}\0${defName}`)) continue; // pure redirect, collapsed onto its target
      bundledDefs[keyFor(relPath, defName)] = rewrite(defValue, relPath);
    }
  }

  const bundledRoot = {
    $schema: "https://json-schema.org/draft/2020-12/schema",
    $defs: bundledDefs,
  };

  return { bundledRoot, fileCount: schemas.size, defCount: Object.keys(bundledDefs).length };
}

function sourceHash() {
  const hash = createHash("sha256");
  const files = [];
  const walk = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      if (entry.isDirectory()) {
        if (entry.name === "draft") continue;
        walk(full);
      } else if (entry.name.endsWith(".json")) files.push(full);
    }
  };
  walk(schemasDir);
  files.sort();
  for (const file of files) hash.update(readFileSync(file));
  return hash.digest("hex");
}

const ROOT_TYPE_NAME = "_GeneratedRoot";

async function run() {
  const { bundledRoot, fileCount, defCount } = main();

  mkdirSync(dirname(bundledSchemaFile), { recursive: true });
  writeFileSync(bundledSchemaFile, JSON.stringify(bundledRoot, null, 2));

  const ts = await compile(bundledRoot, ROOT_TYPE_NAME, {
    bannerComment: "",
    additionalProperties: false,
    unreachableDefinitions: true,
    style: { semi: true, singleQuote: true },
  });

  // Drop the synthetic root type/interface block — it has no meaning of its own.
  const cleaned = ts.replace(
    new RegExp(`export (?:interface|type) ${ROOT_TYPE_NAME}[\\s\\S]*?\\n\\}\\n|export type ${ROOT_TYPE_NAME} = [^\\n]*\\n`, "g"),
    "",
  );

  const banner = [
    "/**",
    " * DO NOT EDIT BY HAND — generated from spec/schemas/ (all *.json files) by",
    " * ts/tools/generate-models.mjs (invoked via `afb-bf-protocol-generate`).",
    ` * source-hash: ${sourceHash()}`,
    " */",
    "",
    "",
  ].join("\n");

  writeFileSync(outFile, banner + cleaned.trimStart());
  console.log(`wrote ${outFile} (${fileCount} schema files, ${defCount} named types)`);
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
