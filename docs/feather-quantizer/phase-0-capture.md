# Phase 0 USB/HID capture procedure

## Purpose and limits

This procedure defines the evidence a human must collect before implementing the
Feather HID proxy. It is non-destructive: do not alter device firmware, send
undocumented feature/output reports, or flash the Feather while following it.
Task 002 records no hardware results and **does not prove compatibility** with
ELECOM DEFT or ELECOM HUGE PLUS. Compatibility requires a later capture on each
physical device and connection mode, followed by analysis against the constraints
below.

## Target matrix

| Device | Identity to record from the label | Connection mode | Task 002 result |
|---|---|---|---|
| Current initial device: ELECOM DEFT | Exact product number still to be recorded by a human | wired, if supported | not captured |
| Current initial device: ELECOM DEFT | Exact product number still to be recorded by a human | supplied 2.4 GHz receiver, if supported | not captured |
| Primary future target: ELECOM HUGE PLUS | Exact product number/revision from the unit | wired, if supported | not captured |
| Primary future target: ELECOM HUGE PLUS | Exact product number/revision from the unit | supplied 2.4 GHz receiver, if supported | not captured |

Create one independent evidence directory for every applicable row. Never mix a
wired capture with a receiver capture. Mark an inapplicable mode `not_applicable`
in the capture index only after inspecting the product and its documentation; do
not infer it from another model.

## Safety and preparation

1. Identify the device and receiver from their physical labels. Photograph or
   transcribe the exact model/product number, hardware revision, and receiver
   identity without guessing missing text.
2. Use an isolated test host, close software that remaps mouse input, and note OS,
   kernel/build, capture-tool name/version, and UTC clock source. Capture tools
   must only read descriptors and interrupt-IN traffic.
3. Connect exactly one test mode. For receiver mode, record the receiver's USB
   identity separately from the paired peripheral's label and pairing state.
4. Record the commands/configuration used and SHA-256 hashes of every evidence
   file. Preserve descriptor and report bytes exactly as observed; decoded text
   is an annotation, never a replacement for raw bytes.
5. Do not flash hardware during Task 002. A later Feather capture task may use a
   reviewed capture program, but flashing requires that task's explicit approval.

The project wiring requirement is PIO USB host D+ on GP16 and D- on GP17
(`docs/feather-quantizer/spec.md`, "Hardware topology"). GP18 is identified there
only as USB-A VBUS enable. Before any later powered-host test, a human must record
an authoritative Adafruit schematic/board-guide URL and revision, the enable
signal's active level, power-up default, required stabilization delay, and any
current/backfeed warnings in `device-metadata.json`. Confirm those facts against
the exact board revision (and, where the source requires it, with a non-destructive
meter/logic measurement). If polarity or timing is absent or ambiguous, stop the
later hardware task; do not energize VBUS or derive a value from KQM code.

## Capture procedure (repeat for each applicable matrix row)

### 1. Create and identify the capture

1. Create the deterministic directory described in
   `research/hid-captures/README.md`; start all files as a new capture, never by
   appending to another mode's corpus.
2. Fill `device-metadata.json` with capture UUID, UTC start time, physical-label
   identity, connection mode, host/tool versions, and operator notes.
3. Record USB VID, PID, `bcdDevice`, manufacturer/product/serial strings (including
   unavailable string indexes), speed, and whether the visible USB device is the
   peripheral, a composite receiver, or a hub.

### 2. Capture enumeration data

1. Save the complete device descriptor and every configuration descriptor in
   raw form or a lossless byte dump. Decode every configuration, interface,
   alternate setting, class/subclass/protocol, endpoint address/direction/type,
   maximum packet size, and polling interval into metadata.
2. Enumerate every HID interface by its USB interface number. Do not capture only
   the boot-mouse interface of a composite device.
3. Read and save each HID interface's **complete** HID report descriptor twice:
   exact bytes in `hid-interface-<n>-report-descriptor.bin` and a decoded,
   annotated rendering in the matching `.txt`. Verify the binary byte count
   against the HID descriptor's declared report-descriptor length and record its
   SHA-256.
4. In the decoded rendering, inventory all top-level collections, usage pages,
   usages, report IDs, report sizes/counts, logical bounds, and Input/Output/
   Feature fields. Explicitly flag vendor-defined pages/usages. Do not send a
   vendor command to discover its meaning.

### 3. Capture an idle baseline

1. Start a monotonic and UTC-timestamped interrupt-IN capture for every HID
   interface simultaneously. Each `input-reports.ndjson` record identifies the
   interface and endpoint and contains the exact transfer bytes and exact transfer
   length; a decoded report ID is interpretation, not removed from `data_hex`.
2. With the device untouched, capture at least 10 seconds, including repeated
   idle reports if the device emits them. Record the duration even if no transfer
   occurs.
3. Determine observed report IDs and exact transfer lengths per `(interface,
   endpoint, report ID)`. Treat a leading byte as an ID only when the report
   descriptor establishes that interpretation.

### 4. Execute the stimulus checklist

Return every control to neutral between trials, run at least three trials of each
stimulus, and place start/end markers or annotation records around each trial.
Update `stimulus-checklist.md` with timestamps and relevant NDJSON sequence ranges.

1. Press and release every physical button individually, including all extra and
   mode/function buttons that emit USB input. Name buttons by physical label and
   location until their HID meaning is demonstrated.
2. Move X positive, X negative, Y positive, and Y negative separately. Record the
   operator's physical direction as well as the eventual decoded sign.
3. Operate the vertical wheel in both directions.
4. Operate horizontal tilt/pan in both directions when the hardware provides it;
   otherwise mark `not_present` with label/manual evidence. Determine from the
   descriptor and bytes whether it is Consumer AC Pan (`0x000C0238`), another
   standard usage, or a vendor-defined field.
5. Capture useful simultaneous inputs: each button while moving X/Y, each button
   while scrolling, at least two buttons together, diagonal X+Y, and combined
   movement plus wheel/pan where physically possible. Record impossible
   combinations rather than synthesizing them.
6. Exercise any consumer/system controls exposed on the product. Annotate every
   vendor-defined report or field that changes, but retain unknown semantics as
   `unknown`.
7. Stop capture, record UTC end time and tool exit status, and compute the maximum
   **observed full input-transfer length** across all interfaces. Keep observed
   maximum separate from the descriptor/theoretical maximum.

### 5. Validate evidence before disconnecting

- Every enumerated HID interface has matching raw and decoded descriptors.
- Every applicable checklist item has trials, timestamps, and sequence ranges;
  omissions have an explicit reason.
- Report bytes are even-length lowercase hexadecimal in NDJSON and `length`
  equals the decoded byte count. Raw files and metadata hashes agree.
- Press and release, positive and negative axes, both vertical wheel directions,
  both pan directions when present, and simultaneous examples are distinguishable
  in the raw corpus without relying only on prose.
- The observed and descriptor-derived report-ID/length tables are both complete;
  disagreement remains recorded as an unresolved finding.

## KQM compatibility worksheet

Complete this worksheet only from captured evidence. The constraints are source
facts summarized in `research/task-001-upstream-analysis.md` sections 3.3, 3.4,
and 4; the cited source files remain read-only.

| Current KQM constraint | Repository source | Required comparison |
|---|---|---|
| One shared 64-byte report buffer | `keyboards/sekigon/keyboard_quantizer/mini/matrix.c`, `hid_report_buffer`; Task 001 sections 3.3/4 | Compare every full observed and descriptor-derived input length to 64; also note interleaving across interfaces because the buffer is shared. |
| `CFG_TUH_DEVICE_MAX=4` | `keyboards/sekigon/keyboard_quantizer/mini/tusb_config.h`; Task 001 sections 3.2/4 | Count the receiver/hub topology's simultaneously addressed USB devices. |
| `CFG_TUH_HID=8` | `keyboards/sekigon/keyboard_quantizer/mini/tusb_config.h`; Task 001 sections 3.2/4 | Count all simultaneously mounted HID interfaces. |
| Parser pools: 8 devices / 16 collections / 32 members / 32 usages | `keyboards/sekigon/keyboard_quantizer/parser/report_descriptor_parser.h`, `HID_DEVICE_COUNT`, `HID_ID_COLLECTION_COUNT`, `HID_REPORT_MEMBER_COUNT`, `HID_USAGE_COUNT`; Task 001 sections 3.3/4 | For each descriptor and the combined topology, tabulate required devices, report-ID collections, parsed members, and peak temporary usages; do not call borderline counts compatible without a parser fixture. |
| Vial mouse path reduces actionable buttons to 8 bits | `keyboards/sekigon/keyboard_quantizer/mini/keymaps/vial/quantizer_mouse.c`, `uint8_t button_current`; Task 001 sections 3.4/4 | Count independently actionable mouse buttons and identify any button above bit 7. |
| Horizontal pan recognizes Consumer AC Pan, while devices may use another/vendor usage | `keyboards/sekigon/keyboard_quantizer/parser/report_parser.c`, `mouse_report_parser()`; Task 001 sections 3.4/6 | Record the exact usage page/usage and raw transitions for both physical directions; flag non-AC-Pan encoding for later parser design. |

Record each result as `within_constraint`, `exceeds_constraint`, or
`requires_parser_fixture`, with byte/count evidence and no overall compatibility
claim. A successful capture is evidence collection, not proof that enumeration,
parsing, passthrough, timing, or Vial behavior works on a Feather.
