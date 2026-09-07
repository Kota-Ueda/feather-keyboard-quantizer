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

`usbpcap.pcapng` is staging evidence. It may be committed only if the privacy
gate below confirms that it contains traffic for the newly inserted DEFT
receiver and no other USB input device. A root-hub-wide capture containing other
devices must never be committed to this public repository. After an eligible
capture is committed, Task 003 will
extract the schema-defined descriptor binaries, decoded descriptors,
`device-metadata.json`, `input-reports.ndjson`, `stimulus-checklist.md`, and KQM
constraint worksheet without changing the observed packet bytes.

Before committing, inspect all five files for a unique device serial number or
traffic belonging to another USB device. If either is present, stop and report
the issue rather than publishing the capture; do not replace bytes inside the
PCAP. Receiver label text that is not a unique serial should remain intact.

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
   [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.fffffff'Z'") | Out-File -Append -Encoding utf8 "$Work\host-info.txt"
   ```

5. Transcribe the receiver's physical label (including model/revision text but
   excluding a unique serial number) into `receiver-label.txt`. Write
   `not observable` if the receiver has no readable label. Do not infer missing
   text from the trackball label or a web search.

## Capture USB enumeration and input traffic

1. Unplug the DEFT receiver. Start Wireshark and open the capture options for the
   USBPcap interface associated with the destination USB root hub (for example,
   `USBPcap1`). If USBPcap offers its **capture newly connected devices** /
   **new-device-only** option, enable it and start capturing before insertion.
   This is the preferred mode because it excludes devices that were already on
   the root hub.
2. If that option is not available, do not assume an unfiltered root-hub capture
   is publishable. Use a port/root hub on which all other USB input devices can
   be safely disconnected, capture locally, and apply the privacy gate below.
   Keep any raw root-hub-wide PCAP outside the repository. If the receiver's
   packets cannot be distinguished from and isolated against every other USB
   input device on that root hub, stop: **do not copy or commit the PCAP**.
3. Record whether new-device-only mode was used, and which devices remained on
   the captured root hub, in `capture-notes.md`.
4. Record the capture start time in `capture-notes.md` using this command, which
   works in Windows PowerShell 5.1 as well as PowerShell 7:

   ```powershell
   [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ss.fffffff'Z'")
   ```

5. Insert the receiver directly into that root hub. Wait at least five seconds
   without touching the DEFT. Confirm in Wireshark that new USB traffic appears.
   If it does not, stop without performing stimuli and repeat on the USBPcap
   interface corresponding to that port. This insertion is required so the PCAP
   includes device, configuration, string, HID, and report-descriptor requests.
6. Leave the DEFT untouched for at least **10 seconds**. Record the UTC start and
   end and call this interval `idle-01`.
7. Perform the checklist below. Before and after every trial, obtain a UTC time
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
- USBPcap new-device-only mode enabled: yes/no
- Other devices present on captured root hub:
- PCAP privacy gate result: pass/fail
- Receiver USB port/root hub:
- Remapping software closed:
- Pairing state observed:

| Stimulus ID | Physical action | Trial | Start UTC | End UTC | Result/notes |
|---|---|---:|---|---|---|
| idle-01 | untouched for >=10 seconds | 1 | | | |
```

## Validate and apply the privacy gate before handoff

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
and every timestamped stimulus.

Before copying anything into the repository, inspect Wireshark's USB device and
endpoint columns over the **entire** capture, including the enumeration period.
Confirm all of the following in `capture-notes.md`:

1. new-device-only capture was enabled; or every other device on the root hub
   was identified and no packet from another USB input device is present;
2. every interrupt transfer in the PCAP belongs to the inserted DEFT receiver;
3. no keyboard, other mouse, camera, headset, storage device, security token, or
   other unrelated device traffic is present;
4. no unique serial number is present in the PCAP or text files.

If any condition cannot be confirmed, set the privacy gate to `fail`, retain the
raw PCAP only in the local working directory, and **do not commit it or a filtered
guess**. Repeat using new-device-only mode or an isolated root hub. Only after
the privacy gate passes may the five requested files be copied into this evidence
directory and committed on `loop/003-deft-hid-capture`. Task 003 can then resume
to extract and validate the complete evidence set.
