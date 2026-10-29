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

// Schema files whose ROOT is deliberately not emitted as a type: AFB-internal
// shapes (never an AsyncAPI wire message) whose allOf/if root the compiler can
// only render as an empty `{[k]: unknown}`. Their `$defs` are still bundled.
const SKIPPED_ROOTS = new Set(["instrument.v1.json"]);

// relative-to-spec/schemas path -> desired export name for the file's ROOT.
function namedRootSchemas() {
  const entries = {
    "envelope.json": "Envelope",
    "deal.v2.json": "DealV2",
    "deal_state.v2.json": "DealStateV2",
    "tradeplan.v2.json": "TradePlanV2",
    "alarm.v1.json": "AlarmV1",
    "alarm.v2.json": "AlarmV2",
    "gp.v1.json": "GpV1",
    "gp.v2.json": "GpV2",
    "notification.deal.v1.json": "NotificationDealV1",
    "notification.alarm.v1.json": "NotificationAlarmV1",
    "notification.link.v1.json": "NotificationLinkV1",
    "afbws/deal.public.v1.json": "DealPublicV1",
    "afbws/deal.channel.v2.json": "DealChannelV2Message",
    "afbws/bf_registry_entry.v1.json": "BfRegistryEntry",
    "afbws/connector.record.v1.json": "ConnectorRecord",
    "afbws/connector.list.v1.json": "ConnectorListData",
    "afbws/bfs.registry.v1.json": "BfsRegistryPush",
    "afbws/account.channel.v2.json": "AccountChannelV2Message",
    "afbws/alarm.channel.v2.json": "AlarmChannelV2Message",
    "afbws/tradeplan.channel.v2.json": "TradeplanChannelV2Message",
    "afbws/link.user.v1.json": "LinkUserV1",
    "afbws/link.admin.v1.json": "LinkAdminV1",
    "afbws/link.channel.v2.json": "LinkChannelV2Message",
    "afbws/gp.channel.v2.json": "GpChannelV2Message",
    "afbws/market.channel.v1.json": "MarketChannelV1Message",
    "config.v1.json": "ConfigSettingsV1",
    "afbws/config.channel.v1.json": "ConfigChannelV1Message",
    "afbws/screener.channel.v1.json": "ScreenerChannelV1Message",
    "afbws/auth.v1.json": "AuthV1Message",
    "afbws/access.channel.v1.json": "AccessChannelV1Message",
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
  "gp.v2.json": {
    indicator: "GpV2Indicator",
    indicatorSettings: "GpV2IndicatorSettings",
    primitiveSettingsLine: "GpV2PrimitiveSettingsLine",
    primitiveSettingsNote: "GpV2PrimitiveSettingsNote",
    primitiveSettingsTwoPoint: "GpV2PrimitiveSettingsTwoPoint",
    point: "GpV2Point",
    primitiveKindStyle: "GpV2PrimitiveKindStyle",
    primitiveStyles: "GpV2PrimitiveStyles",
  },
  "common.v1.json": {
    decimalString: "DecimalString",
    dealStatus: "DealStatus",
    executionPhase: "DealExecutionPhase",
    legId: "LegId",
    tradeplanId: "TradeplanId",
    instrument: "DealInstrument",
    target: "DealTarget",
    sizing: "DealSizing",
    executionPolicy: "DealExecutionPolicy",
    source: "DealSource",
  },
  // afbws/common.v1.json — only the access block is exported under a public
  // name; requestId/errorCode/instrumentKey keep their namespaced keys.
  "afbws/common.v1.json": {
    accessTier: "AccessTier",
    accessMode: "AccessMode",
    accessLimits: "AccessLimits",
    access: "Access",
  },
  "afbws/bfs.registry.v1.json": { entry: "BfsRegistryEntry" },
  "afbws/account.channel.v2.json": {
    bfId: "AccountV2BfId",
    accountId: "AccountV2AccountId",
    accountSnapshot: "AccountV2Snapshot",
    order: "AccountV2Order",
    eventRecord: "AccountV2EventRecord",
    list: "AccountV2List",
    orders: "AccountV2Orders",
    events: "AccountV2Events",
    error: "AccountV2Error",
  },
  "afbws/connector.record.v1.json": {
    backstop: "ConnectorBackstop",
    executionPolicy: "ConnectorExecutionPolicy",
  },
  "afbws/alarm.channel.v2.json": {
    list: "AlarmV2List",
    set: "AlarmV2Set",
    delete: "AlarmV2Delete",
    rejection: "AlarmV2Rejection",
    error: "AlarmV2Error",
    triggerEvent: "AlarmV2TriggerEvent",
    triggered: "AlarmV2Triggered",
    ackEvent: "AlarmV2AckEvent",
    ackResultItem: "AlarmV2AckResultItem",
    ack: "AlarmV2Ack",
  },
  "afbws/tradeplan.channel.v2.json": {
    condition: "TradeplanV2Condition",
    legInput: "TradeplanV2LegInput",
    legItem: "TradeplanV2LegItem",
    planInput: "TradeplanV2PlanInput",
    planItem: "TradeplanV2PlanItem",
    amendResultItem: "TradeplanV2AmendResultItem",
    rejection: "TradeplanV2Rejection",
    list: "TradeplanV2List",
    set: "TradeplanV2Set",
    delete: "TradeplanV2Delete",
    archive: "TradeplanV2Archive",
    sync: "TradeplanV2Sync",
    error: "TradeplanV2Error",
  },
  "afbws/link.user.v1.json": {
    sharedFields: "LinkSharedFields",
    setInputShared: "LinkSetInputShared",
    setInput: "LinkUserSetInput",
  },
  "afbws/link.admin.v1.json": {
    setInput: "LinkAdminSetInput",
  },
  "afbws/link.channel.v2.json": {
    entity: "LinkV2Entity",
    setInput: "LinkV2SetInput",
    session: "LinkV2Session",
    statusItem: "LinkV2StatusItem",
    rejection: "LinkV2Rejection",
    pairItem: "LinkV2PairItem",
    list: "LinkV2List",
    set: "LinkV2Set",
    delete: "LinkV2Delete",
    pair: "LinkV2Pair",
    restart: "LinkV2Restart",
    status: "LinkV2Status",
    error: "LinkV2Error",
  },
  "afbws/gp.channel.v2.json": {
    list: "GpV2List",
    set: "GpV2Set",
    delete: "GpV2Delete",
    rejection: "GpV2Rejection",
    indicatorList: "GpV2IndicatorList",
    indicatorSet: "GpV2IndicatorSet",
    indicatorDelete: "GpV2IndicatorDelete",
    indicatorRejection: "GpV2IndicatorRejection",
    style: "GpV2Style",
    error: "GpV2Error",
    errorDetails: "GpV2ErrorDetails",
  },
  "config.v1.json": {
    profile: "ConfigProfile",
    layout: "ConfigLayout",
    interface: "ConfigInterface",
    dataset: "ConfigDataset",
    dashboard: "ConfigDashboard",
    trade: "ConfigTrade",
    defaults: "ConfigDefaults",
  },
  "afbws/config.channel.v1.json": {
    settings: "ConfigSettings",
    defaults: "ConfigDefaultsMessage",
    help: "ConfigHelp",
    roles: "ConfigRoles",
    roleTier: "ConfigRoleTier",
    token: "ConfigToken",
    error: "ConfigError",
  },
  "afbws/screener.channel.v1.json": {
    list: "ScreenerV1List",
    get: "ScreenerV1Get",
    participants: "ScreenerV1Participants",
    participantsList: "ScreenerV1ParticipantsList",
    participantsDerivatives: "ScreenerV1ParticipantsDerivatives",
    participantsCollection: "ScreenerV1ParticipantsCollection",
    error: "ScreenerV1Error",
  },
  "afbws/auth.v1.json": {
    auth: "AuthV1",
    error: "AuthV1Error",
  },
  "afbws/access.channel.v1.json": {
    window: "AccessV1Window",
    policy: "AccessV1Policy",
    tierRow: "AccessV1TierRow",
    policyRow: "AccessV1PolicyRow",
    tierLabel: "AccessV1TierLabel",
    capabilityLabel: "AccessV1CapabilityLabel",
    provider: "AccessV1Provider",
    groupRole: "AccessV1GroupRole",
    userRow: "AccessV1UserRow",
    showcase: "AccessV1Showcase",
    subscription: "AccessV1Subscription",
    providerGroup: "AccessV1ProviderGroup",
    statsWeek: "AccessV1StatsWeek",
    usersList: "AccessV1UsersList",
    userSet: "AccessV1UserSet",
    userTierSet: "AccessV1UserTierSet",
    policyGet: "AccessV1PolicyGet",
    policySet: "AccessV1PolicySet",
    tiersGet: "AccessV1TiersGet",
    tiersSet: "AccessV1TiersSet",
    groupsGet: "AccessV1GroupsGet",
    groupsSet: "AccessV1GroupsSet",
    stats: "AccessV1Stats",
    denied: "AccessV1Denied",
    error: "AccessV1Error",
  },
  "afbws/market.channel.v1.json": {
    table: "MarketTable",
    period: "MarketPeriod",
    seriesTableEntry: "MarketSeriesTable",
    snapshotTableEntry: "MarketSnapshotTable",
    series: "MarketSeries",
    snapshot: "MarketSnapshot",
    subscriptionQuotesSpec: "MarketSubscriptionQuotesSpec",
    subscribe: "MarketSubscribe",
    subscriptionRejection: "MarketSubscriptionRejection",
    subscription: "MarketSubscription",
    get: "MarketGet",
    error: "MarketErrorResponse",
  },
  "afbws/deal.public.v1.json": {
    source: "DealPublicSource",
    v2: "DealPublicDealV2",
    exitList: "DealPublicExitList",
  },
  "afbws/deal.channel.v2.json": {
    dealId: "DealV2Id",
    bfId: "DealV2BfId",
    amendField: "DealV2AmendField",
    dealResultStatus: "DealV2ResultStatus",
    dealSizingDisplay: "DealV2SizingDisplay",
    dealOpenPosition: "DealV2OpenPosition",
    dealRealizedPnl: "DealV2RealizedPnl",
    dealSummary: "DealV2Summary",
    dealDetail: "DealV2Detail",
    dealItem: "DealV2Item",
    dealLegEdit: "DealV2LegEdit",
    dealNewLeg: "DealV2NewLeg",
    dealRoleEdit: "DealV2RoleEdit",
    dealEdit: "DealV2Edit",
    dealResult: "DealV2Result",
    publishItem: "DealV2PublishItem",
    rebindItem: "DealV2RebindItem",
    amendItem: "DealV2AmendItem",
    amendResult: "DealV2AmendResult",
    outcomeItem: "DealV2OutcomeItem",
    pnlItem: "DealV2PnlItem",
    orderRole: "DealV2OrderRole",
    orderSide: "DealV2OrderSide",
    orderEventStatus: "DealV2OrderEventStatus",
    createdData: "DealV2CreatedData",
    amendedData: "DealV2AmendedData",
    acceptedData: "DealV2AcceptedData",
    rejectedData: "DealV2RejectedData",
    statusChangedData: "DealV2StatusChangedData",
    deletedData: "DealV2DeletedData",
    reportFill: "DealV2ReportFill",
    reportData: "DealV2ReportData",
    ordersSyncedData: "DealV2OrdersSyncedData",
    positionsSyncedData: "DealV2PositionsSyncedData",
    orderCreatedData: "DealV2OrderCreatedData",
    orderData: "DealV2OrderData",
    positionData: "DealV2PositionData",
    conditionTriggeredData: "DealV2ConditionTriggeredData",
    eventDealCreated: "DealV2EventDealCreated",
    eventDealAmended: "DealV2EventDealAmended",
    eventDealAccepted: "DealV2EventDealAccepted",
    eventDealRejected: "DealV2EventDealRejected",
    eventDealStatusChanged: "DealV2EventDealStatusChanged",
    eventDealDeleted: "DealV2EventDealDeleted",
    eventDealReport: "DealV2EventDealReport",
    eventDealOrdersSynced: "DealV2EventDealOrdersSynced",
    eventDealPositionsSynced: "DealV2EventDealPositionsSynced",
    eventOrderCreated: "DealV2EventOrderCreated",
    eventOrderFilled: "DealV2EventOrderFilled",
    eventOrderPartiallyFilled: "DealV2EventOrderPartiallyFilled",
    eventOrderCancelled: "DealV2EventOrderCancelled",
    eventOrderRejected: "DealV2EventOrderRejected",
    eventPositionOpened: "DealV2EventPositionOpened",
    eventPositionChanged: "DealV2EventPositionChanged",
    eventPositionClosed: "DealV2EventPositionClosed",
    eventConditionTriggered: "DealV2EventConditionTriggered",
    eventItem: "DealV2EventItem",
    event: "DealV2Event",
    operationItem: "DealV2OperationItem",
    triggerReportData: "DealV2TriggerReportData",
    triggerStatusChanged: "DealV2TriggerStatusChanged",
    triggerRejected: "DealV2TriggerRejected",
    triggerReport: "DealV2TriggerReport",
    triggerEvent: "DealV2TriggerEvent",
    ackEvent: "DealV2AckEvent",
    ackResultItem: "DealV2AckResultItem",
    list: "DealV2List",
    publish: "DealV2Publish",
    rebind: "DealV2Rebind",
    operation: "DealV2Operation",
    amend: "DealV2Amend",
    ack: "DealV2Ack",
    error: "DealV2Error",
    record: "DealV2Record",
    outcome: "DealV2Outcome",
    pnl: "DealV2Pnl",
    triggered: "DealV2Triggered",
  },
};

function loadSchemas() {
  const files = new Map(); // relPath -> parsed JSON
  const walk = (dir) => {
    for (const entry of readdirSync(dir, { withFileTypes: true })) {
      const full = join(dir, entry.name);
      // Meta-schemas (spec/schemas/**/meta/) — a meta-schema validates OTHER
      // schema documents (e.g. iss/meta/iss.market.v1.json validates
      // iss/markets/*.json's own shape), it is never itself a data instance,
      // and datamodel-codegen/json-schema-to-typescript hoist its
      // hyphenated x-*-prefixed properties into a forward-referenced class
      // that the functional TypedDict form of Python's generated module
      // cannot resolve (NameError at import time) — see iss_registry.py.
      if (entry.isDirectory()) {
        if (entry.name === "meta") continue;
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
        // Only the `title` KEYWORD (a string) is dropped: inside a
        // `properties` map a key named `title` is a property whose value is a
        // schema object (e.g. `{"title": {"type": "string"}}`) and must stay,
        // otherwise the generated interface silently loses its `title` field.
        if (k === "title" && typeof v === "string") continue;
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
    if (!SKIPPED_ROOTS.has(relPath) && (!isRedirectOnly || rootExportName[relPath])) {
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
        if (entry.name === "meta") continue;
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
