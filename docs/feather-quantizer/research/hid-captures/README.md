# HID capture evidence layout and schema

This directory will hold reviewed Phase 0 hardware evidence. Task 002 defines the
schema only; it contains no DEFT or HUGE PLUS capture and makes no compatibility
claim.

## Deterministic paths

Use lowercase ASCII slugs. Device slug is the manufacturer/model printed on the
unit once known (for example, `elecom-deft-<exact-product-number>`); do not use a
guessed DEFT number. Connection mode is exactly `wired` or `2_4ghz-receiver`.

```text
<device>/<connection-mode>/device-metadata.json
<device>/<connection-mode>/hid-interface-<n>-report-descriptor.bin
<device>/<connection-mode>/hid-interface-<n>-report-descriptor.txt
<device>/<connection-mode>/input-reports.ndjson
<device>/<connection-mode>/stimulus-checklist.md
```

`<n>` is the decimal USB `bInterfaceNumber` with no zero padding. One directory
represents one device, mode, and completed capture session. If a repeat capture
must be retained, put both immutable sessions below a dated revision directory
agreed in review rather than overwriting evidence, and reference the selected
session from metadata.

## `device-metadata.json`

UTF-8 JSON, two-space indentation, stable key order as shown. `null` means the
field was queried but unavailable; `unknown` in a notes/status field means it
was not established. Numeric descriptor values use JSON integers; raw descriptor
bytes live in `.bin` and hashes bind interpretations to those bytes.

Required top-level content:

```json
{
  "schema_version": 1,
  "capture_id": "uuid",
  "capture_started_utc": "YYYY-MM-DDTHH:MM:SS.sssZ",
  "capture_ended_utc": "YYYY-MM-DDTHH:MM:SS.sssZ",
  "device_slug": "elecom-...-exact-product-number",
  "connection_mode": "wired",
  "physical_identity": {
    "marketing_name": "ELECOM DEFT",
    "product_number": null,
    "hardware_revision": null,
    "receiver_label": null
  },
  "host": {"os": "...", "os_version": "...", "architecture": "..."},
  "tools": [{"name": "...", "version": "...", "command": "..."}],
  "usb": {
    "vid": "hhhh",
    "pid": "hhhh",
    "bcd_device": "hhhh",
    "manufacturer_string": null,
    "product_string": null,
    "serial_string": null,
    "speed": "low|full|high",
    "topology": "direct-device|receiver|hub|composite",
    "configurations": [],
    "interfaces": []
  },
  "report_inventory": [],
  "maximum_observed_input_report_length": 0,
  "maximum_descriptor_derived_input_report_length": 0,
  "feather_vbus_source": {
    "board_revision": null,
    "authoritative_url_or_document": null,
    "source_revision_or_accessed_utc": null,
    "gp18_active_level": null,
    "power_up_default": null,
    "stabilization_time_ms": null,
    "warnings": [],
    "verification_status": "not_verified"
  },
  "artifacts": [{"path": "...", "sha256": "64 lowercase hex digits", "byte_length": 0}],
  "unresolved_findings": [],
  "operator_notes": ""
}
```

Each configuration entry records value, attributes, maximum power, and complete
raw-artifact reference. Each interface entry records configuration value,
interface number, alternate setting, class/subclass/protocol, string, HID
descriptor/report-descriptor declared lengths, and all endpoints (address,
direction, transfer type, maximum packet size, and interval). Each
`report_inventory` entry records interface, endpoint, descriptor-established
report ID (`null` when reports have no ID), descriptor-derived byte length,
sorted observed transfer lengths, and observed sample count. Preserve conflicts
in `unresolved_findings`; never normalize raw evidence to fit the inventory.

The GP18 object records an authoritative source for a **later** Feather hardware
task. Null values are required until verified; this schema does not authorize
powering the port or flashing the Feather.

## Raw report descriptor and decoded descriptor

- `.bin` is the byte-for-byte report descriptor returned for that interface. It
  is authoritative observed evidence and must never contain a text/hex wrapper.
- `.txt` begins with interface number, byte length, binary SHA-256, capture tool,
  and command, followed by a lossless hex rendering and decoded items. Clearly
  label all decoded usages, calculated bit offsets/lengths, and commentary as
  **interpretation**. Unknown/vendor semantics remain unknown.

## `input-reports.ndjson`

UTF-8 newline-delimited JSON, one object per observed transfer or explicit
annotation marker. Sequence numbers increase from zero. A transfer record is:

```json
{"schema_version":1,"sequence":0,"record_type":"input_transfer","monotonic_ns":0,"timestamp_utc":"YYYY-MM-DDTHH:MM:SS.ssssssZ","interface_number":0,"endpoint_address":"81","transfer_length":4,"data_hex":"00000000","interpretation":{"report_id":null,"stimulus_id":"idle-01","notes":""}}
```

`data_hex` and `transfer_length` are the observed facts: lowercase, separator-free
hex and the full transfer length, including a report-ID byte when present. The
entire `interpretation` object is annotation and may be corrected without
changing those facts. A marker uses `record_type: "annotation"`, omits endpoint,
length, and bytes, and supplies `stimulus_id` plus notes. Never put synthesized,
reconstructed, or decoded bytes in `data_hex`.

## `stimulus-checklist.md`

Record capture ID and a table with: stable stimulus ID; physical control/action;
direction; applicable/not-present/not-applicable status and evidence; trial
number; UTC start/end; NDJSON sequence range; interface/report ID; neutral return
confirmed; and observations explicitly labelled as interpretation.

The checklist must cover idle, every individual button press and release, X+/X-,
Y+/Y-, vertical wheel both directions, horizontal tilt/pan both directions when
present, consumer/system controls, simultaneous button combinations, button plus
movement/wheel, diagonal movement, and changed vendor-defined reports/usages.
Also tabulate exact observed lengths by interface/report ID and the maximum
observed full input-transfer length.

## Review rules

1. Validate JSON/NDJSON syntax and byte-length consistency programmatically.
2. Verify artifact hashes and descriptor declared-versus-captured lengths.
3. Review raw evidence independently from all interpretation fields.
4. Keep wired and receiver modes separate and identify receiver versus peripheral.
5. Do not add a compatibility verdict to capture evidence. Compatibility is a
   later, hardware-backed engineering conclusion.
