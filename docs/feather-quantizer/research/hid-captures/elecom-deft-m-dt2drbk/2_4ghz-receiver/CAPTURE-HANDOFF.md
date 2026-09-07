# Task 003 Windows capture handoff

Task 003 is blocked at the hardware checkpoint. The repository does not yet
contain USB descriptors or input transfers captured from the specified ELECOM
DEFT and receiver. Follow this read-only procedure on the Windows PC that has
the device. Do not use the Feather, install device firmware, pair a different
device, or send HID Output/Feature reports.

## Files to return

Place these files, without renaming them, in this directory:

```text
host-info.txt
receiver-label.txt
usbpcap.pcapng
capture-notes.md
capture-sha256.txt
```

`usbpcap.pcapng` is staging evidence. After it is committed, Task 003 will
extract the schema-defined descriptor binaries, decoded descriptors,
`device-metadata.json`, `input-reports.ndjson`, `stimulus-checklist.md`, and KQM
constraint worksheet without changing the observed packet bytes.

Before committing, inspect all five files for a unique device serial number. If
one is present, stop and report where it appears rather than publishing the
capture; do not replace bytes inside the PCAP. Receiver label text that is not a
unique serial should remain intact.

## Prerequisites

1. Use the Windows PC and the exact `M-DT2DRBK`, label revision `V02`, connected
   only through its supplied 2.4 GHz receiver.
2. Install the current stable Wireshark release with its USBPcap component. The
   installer must show **USBPcap** as installed. Do not install a USB filter
   driver from any other source.
3. Close ELECOM Mouse Assistant and other mouse remapping/macro tools. Disconnect
   other unnecessary USB input devices where doing so is safe. Keep the normal
   keyboard and another pointing device available to control Wireshark.
4. Open an ordinary, non-administrator PowerShell unless USBPcap explicitly
   requires elevation on this PC. Create an empty working directory and record
   the host/tool environment:

   ```powershell
   $Work = Join-Path $HOME 'deft-task-003-capture'
   New-Item -ItemType Directory -Force $Work | Out-Null
   Get-ComputerInfo | Select-Object WindowsProductName,WindowsVersion,OsBuildNumber,OsArchitecture | Format-List | Out-File -Encoding utf8 "$Work\host-info.txt"
   & "$env:ProgramFiles\Wireshark\tshark.exe" --version | Out-File -Append -Encoding utf8 "$Work\host-info.txt"
   Get-Date -AsUTC -Format 'yyyy-MM-ddTHH:mm:ss.fffffffZ' | Out-File -Append -Encoding utf8 "$Work\host-info.txt"
   ```

5. Transcribe the receiver's physical label (including model/revision text but
   excluding a unique serial number) into `receiver-label.txt`. Write
   `not observable` if the receiver has no readable label. Do not infer missing
   text from the trackball label or a web search.

## Capture USB enumeration and input traffic

1. Unplug the DEFT receiver. Start Wireshark and select the USBPcap interface
   for the USB root hub into which the receiver will be inserted (for example,
   `USBPcap1`). Do not apply a capture filter. Start capturing before insertion.
2. Record the capture start time in `capture-notes.md` using:

   ```powershell
   Get-Date -AsUTC -Format 'yyyy-MM-ddTHH:mm:ss.fffffffZ'
   ```

3. Insert the receiver directly into that root hub. Wait at least five seconds
   without touching the DEFT. Confirm in Wireshark that new USB traffic appears.
   If it does not, stop without performing stimuli and repeat on the USBPcap
   interface corresponding to that port. This insertion is required so the PCAP
   includes device, configuration, string, HID, and report-descriptor requests.
4. Leave the DEFT untouched for at least **10 seconds**. Record the UTC start and
   end and call this interval `idle-01`.
5. Perform the checklist below. Before and after every trial, obtain a UTC time
   with the PowerShell command above and record it in `capture-notes.md`. Return
   every control to neutral. Repeat every applicable action three times.

## Stimulus checklist

Use stable IDs such as `button-left-01`, `button-left-02`, and
`button-left-03`. Name every extra button by its printed label or physical
location, not by an assumed HID meaning.

- every physical button individually: press, hold about one second, release;
- X movement right and left, separately;
- Y movement away from and toward the operator, separately;
- vertical wheel forward and backward, separately;
- horizontal tilt/pan left and right, if physically present; otherwise record
  `not_present` and why;
- every consumer/system/mode control that produces normal user input;
- each button while moving X, then Y;
- each button while operating the vertical wheel;
- at least one two-button combination;
- diagonal movement in both diagonals;
- combined movement plus vertical wheel and, when present, horizontal pan.

For physically impossible combinations, write `not_applicable` and the concrete
reason. Do not synthesize a report. Note any visible receiver/device reaction,
but label it as operator interpretation. Do not send test Output or Feature
reports, even if Wireshark shows that Windows sent one automatically.

After the final stimulus, leave the DEFT untouched for five seconds, stop the
Wireshark capture, and save it as `usbpcap.pcapng`. Record the capture end UTC
time and Wireshark save result in `capture-notes.md`.

## `capture-notes.md` minimum content

```markdown
# Task 003 operator notes

- Device: ELECOM DEFT M-DT2DRBK
- Label revision: V02
- Connection: supplied 2.4 GHz receiver
- Receiver label: see receiver-label.txt
- Capture start UTC:
- Capture end UTC:
- USBPcap interface:
- Receiver USB port/root hub:
- Remapping software closed:
- Pairing state observed:

| Stimulus ID | Physical action | Trial | Start UTC | End UTC | Result/notes |
|---|---|---:|---|---|---|
| idle-01 | untouched for >=10 seconds | 1 | | | |
```

## Validate before handoff

Run these commands from PowerShell. They read the capture but do not communicate
with the DEFT:

```powershell
$Work = Join-Path $HOME 'deft-task-003-capture'
$Tshark = "$env:ProgramFiles\Wireshark\tshark.exe"
& $Tshark -r "$Work\usbpcap.pcapng" -q -z io,phs
if ($LASTEXITCODE -ne 0) { throw 'tshark could not read usbpcap.pcapng' }
& $Tshark -r "$Work\usbpcap.pcapng" -Y 'usb.transfer_type == 0x01' -c 1
if ($LASTEXITCODE -ne 0) { throw 'tshark interrupt-transfer check failed' }
Get-FileHash -Algorithm SHA256 "$Work\host-info.txt","$Work\receiver-label.txt","$Work\usbpcap.pcapng","$Work\capture-notes.md" |
  ForEach-Object { '{0}  {1}' -f $_.Hash.ToLowerInvariant(), (Split-Path $_.Path -Leaf) } |
  Set-Content -Encoding ascii "$Work\capture-sha256.txt"
Get-Content "$Work\capture-sha256.txt"
```

The second `tshark` command must display at least one interrupt transfer. Also
confirm that `usbpcap.pcapng` covers receiver insertion, the full idle interval,
and every timestamped stimulus. Copy the five requested files into this evidence
directory and commit them on `loop/003-deft-hid-capture`. Task 003 can then resume
to extract and validate the complete evidence set.
