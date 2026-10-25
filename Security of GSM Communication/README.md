# GSM Security — Sniffing SMS and Voice Calls Over the Air

A hands-on telecoms-security project: using a **Software-Defined Radio** and the
open-source **`gr-gsm`** toolchain to passively intercept a live **2G / GSM** cell —
decoding its broadcast parameters, reading an **SMS two-factor code in plaintext**, and
recovering a **password spoken in a voice call**. GSM is a 1980s standard that still
underpins mobile networks worldwide, and this project shows why its original design is
no longer safe for anything sensitive.

> ### ⚠️ Scope & ethics — read this first
> This work was carried out **in an authorised university laboratory** (University of
> Southampton, COMP3217 — *Security of Cyber-Physical Systems*) against a **private test
> GSM cell** (Mobile Country Code **999**, reserved for test networks) on the single
> frequency the lab authorised (1878.8 MHz).
>
> **Intercepting, decoding or disclosing traffic on real mobile networks is a criminal
> offence in the UK under the Wireless Telegraphy Act 2006 (and equivalent laws
> elsewhere), punishable by imprisonment.** Nothing here was performed on a public
> network, and nothing here should be. The author's ECS usernames are redacted. This is
> documented for **education and defensive understanding** only.

---

## Overview

GSM encrypts traffic with the A5 cipher family — but encryption is optional, negotiated
by the network, and several A5 variants are broken. When a cell runs **A5/0 (no
encryption)**, everything it sends is readable by anyone nearby with a cheap radio. This
project walks that entire path, from understanding the protocol to pulling secrets out of
the air.

| # | Investigation | Headline result | Deep-dive |
|---|---------------|------------------|-----------|
| 1 | **GSM fundamentals** | Mapped the protocol's identities, ciphers and channels — and where each is weak | [docs/01-gsm-fundamentals.md](docs/01-gsm-fundamentals.md) |
| 2 | **Finding & sniffing the cell** | Located the signal and decoded its broadcast parameters (ARFCN 880, MCC/MNC 999/70) from live GSMTAP packets | [docs/02-finding-and-sniffing.md](docs/02-finding-and-sniffing.md) |
| 3 | **Intercepting SMS & voice** | Read a plaintext **SMS 2FA code** and decoded a **voice-call password** — proving the cell ran **A5/0** | [docs/03-intercepting-sms-and-voice.md](docs/03-intercepting-sms-and-voice.md) |

## Key results & highlights

- 📶 **Passive cell fingerprinting** — decoded System Information 1/3 to read the cell's
  ARFCN, country/operator codes, access thresholds, TX-power cap, retransmit limit and
  radio-link timeout, all without transmitting a thing.
- 💬 **Plaintext SMS interception** — followed Paging → Immediate Assignment → SMS-DELIVER
  on the **SDCCH/4** control channel to read a **two-factor authentication code** meant
  for another device.
- 🕵️ **Subscriber-tracking insight** — observed the target's **TMSI cycling between two
  values**, the privacy mechanism GSM uses (imperfectly) to avoid exposing the IMSI.
- 🔓 **No-encryption proof** — showed the absence of a *Ciphering Mode Command* means the
  cell uses **A5/0**, so all traffic is in the clear.
- 🎙️ **Voice-call recovery** — followed the Assignment Command to the **TCH/F** traffic
  channel, decoded Full-Rate speech to audio, and recovered a spoken **password**.

## Skills & tools

Software-Defined Radio (LimeSDR Mini / PlutoSDR) · `gr-gsm` (`grgsm_livemon`,
`grgsm_capture`, `grgsm_decode`) · Wireshark + GSMTAP dissection · gqrx · GSM air
interface (BCCH / CCCH / SDCCH / TCH) · A5/0–A5/3 cipher family · GSM identities
(IMSI / IMEI / TMSI / Ki / Kc) · ARFCN & antenna calculation.

## What I learned

- **Encryption you can turn off isn't encryption.** GSM's security collapses the moment a
  cell negotiates A5/0 — the handsets comply silently, and the user never knows.
- **Plaintext SMS is a terrible second factor.** An SMS 2FA code is readable by anyone in
  radio range of an unencrypted cell — a concrete argument for app-based or hardware MFA.
- **Metadata leaks too.** Even without reading content, the paging/TMSI structure reveals
  device presence and activity; TMSI reassignment is a partial, imperfect defence.
- **Open tools make this accessible.** A cheap SDR and free software reconstruct SMS and
  voice from raw RF — the barrier to intercepting legacy GSM is now very low, which is the
  whole reason sensitive traffic must not ride on it.

---

### Repository layout

```
.
├── README.md
├── docs/
│   ├── 01-gsm-fundamentals.md             # identities, ciphers, channels
│   ├── 02-finding-and-sniffing.md         # spectrum + broadcast parameters
│   └── 03-intercepting-sms-and-voice.md   # SMS 2FA + voice-call decode
└── assets/                                # Wireshark captures + decoded voice.au
```
