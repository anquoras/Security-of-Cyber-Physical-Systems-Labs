# Power Side-Channel Attacks: From Reading Traces to Breaking AES

A hardware-security project: using a ChipWhisperer-Lite and a power
oscilloscope to read secrets straight out of a microcontroller's *power consumption*,
with no software bug required. It builds from first principles (what does a `for` loop
look like in a power trace?) up to recovering a full AES-128 key with Correlation
Power Analysis (CPA).

> ### Scope and ethics
> This work was carried out as an authorised university laboratory (University of
> Southampton, COMP3217, *Security of Cyber-Physical Systems*) on a ChipWhisperer-Lite
> training board running lab-provided firmware, with hardware passed through to a
> dedicated VM. The passwords, secrets and AES key recovered here are synthetic
> challenge values baked into the lab firmware, not real credentials. The author's
> ECS usernames are redacted. This is documented for education and defensive
> understanding of hardware leakage.

---

## Overview

Every instruction a CPU runs draws a slightly different amount of power. That tiny,
data-dependent variation is a *side channel*: measure it precisely enough and you can
tell what the chip is doing, and eventually what secrets it is working on. This
project works through three stages of exactly that.

| # | Investigation | Headline result | Deep-dive |
|---|---------------|------------------|-----------|
| 1 | **Reading power traces** | Mapped a power trace back to its C source and measured one loop iteration = **~32 samples** | [docs/01-reading-power-traces.md](docs/01-reading-power-traces.md) |
| 2 | **Password timing attack** | Recovered an 11-character password **one character at a time** from timing leakage, unlocking a hidden secret | [docs/02-password-timing-attack.md](docs/02-password-timing-attack.md) |
| 3 | **CPA against AES-128** | Recovered the **full 128-bit AES key** from 100 traces and decrypted the challenge message | [docs/03-cpa-aes-key-recovery.md](docs/03-cpa-aes-key-recovery.md) |

## Key results and highlights

- Trace → code mapping: identified the `atoi()` setup, the `x = x * 77` counting
  loop, and the UART output phase purely from the shape of the power trace, and measured
  a single loop iteration at ~32 samples.
- Timing side channel: each correct password character triggers one extra
  comparison loop; a total-energy metric over the whole trace made the correct
  character the highest-energy guess at every position (stable against jitter).
- CPA on AES: using an S-box Hamming-weight leakage model, recovered all 16 key
  bytes by correlating predicted vs. measured power across 256 hypotheses per byte.
- End-to-end break: fed the recovered key into an ECB decrypt to reveal the
  plaintext challenge message.

## Skills and tools

ChipWhisperer-Lite (Capture + Analyzer) · XMEGA (CW303) target · SimpleSerial protocol ·
Simple Power Analysis (SPA) / timing attacks · Correlation Power Analysis (CPA) vs. DPA ·
AES S-box / Hamming-weight leakage models · power-trace capture & interpretation ·
`numpy` · `pycryptodome` · VM / USB pass-through workflow.

## What I learned

- Timing is leakage too. Before touching cryptography, the password attack showed
  that *how long* code runs is itself a secret-dependent signal, visible as width in a
  power trace.
- Measure the whole signal, not a single point. Switching from "read sample 275" to
  "total energy of the trace" turned a jitter-sensitive guess into a reliable one, a
  general lesson in choosing stable side-channel metrics.
- CPA beats brute force by modelling the leakage. You never guess 2¹²⁸ keys; you
  guess 256 values per byte and let statistics find the one whose predicted power
  matches reality.
- Constant-time comparisons and masking matter. Both attacks exploit *data-dependent*
  time and power. The defences (constant-time comparisons, masking, hiding/jitter) follow
  directly from seeing the leak.

---

### Repository layout

```
.
├── README.md
├── docs/
│   ├── 01-reading-power-traces.md     # platform + interpreting traces
│   ├── 02-password-timing-attack.md   # SPA/timing brute-force
│   └── 03-cpa-aes-key-recovery.md     # CPA vs AES + decryption
├── src/
│   ├── bruteforce.py                  # password attack (ChipWhisperer v4 / Python 2)
│   └── decrypt_aes.py                 # ECB decrypt with recovered key (Python 3)
└── assets/                            # captured traces & result screenshots
```

> **Note on the scripts:** `bruteforce.py` runs *inside* the ChipWhisperer Capture GUI
> on the legacy v4 VM and is therefore Python 2 (it uses the GUI-injected `self.*`
> objects). `decrypt_aes.py` is standalone Python 3 and needs `pycryptodome`.
