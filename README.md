# Security of Cyber-Physical Systems - Project Portfolio

A set of four hands-on hardware- and radio-security projects, each taking a real-world
device or protocol apart to understand *why* it is (in)secure. The work spans contactless
smartcards, power side-channels, IoT radio control, and mobile telephony - the physical
layer where cryptography meets the real world, and where it so often breaks.

Every project follows the same spine: **build or capture → break → explain the lesson**,
with findings written up as a results-first `README` plus focused deep-dives.

> ### ⚠️ Scope & ethics
> All four projects were carried out as **authorised university laboratories**
> (University of Southampton, COMP3217 - *Security of Cyber-Physical Systems*) against
> **lab-issued hardware, synthetic data, and private test networks**. No real individual,
> device, network or payment system was ever targeted. Personal identifiers are redacted,
> and the radio work in particular (IoT RF and GSM) was confined to equipment I control or
> authorised test frequencies - **intercepting or transmitting on real networks is a
> criminal offence**. Everything here is documented for **education and defensive
> understanding** only.

---

## The four projects

| # | Project | What it breaks | Headline result |
|---|---------|----------------|-----------------|
| 1 | **[Contactless Card Security](Contactless%20card%20security/README.md)** | NFC / MIFARE Classic, ID cards, EMV | Cracked all 16 sectors of a MIFARE Classic token in ~58 s; reconstructed an ID card from an LDAP dump |
| 2 | **[Power Side-Channel Attacks](Side%20Channel%20Attacks/README.md)** | A microcontroller's power consumption | Recovered a password by timing leakage and a full **AES-128 key** via CPA from 100 traces |
| 3 | **[IoT RF Security](IOT%20Devices%20Security/README.md)** | A 433 MHz radio-controlled relay | Working replay attack; identified the EV1527 chip and a **2²⁰ keyspace** (~9.47 h brute force) |
| 4 | **[GSM Security](Security%20of%20GSM%20Communication/README.md)** | 2G / GSM over the air | Intercepted a plaintext **SMS 2FA code** and decoded a **voice-call password** on an A5/0 cell |

---

## Project summaries

### 1 - Contactless Card Security
Building and breaking everyday contactless technology across three investigations:
reconstructing a university ID card from an unauthenticated LDAP dump (including
reverse-engineering its Codabar barcode), breaking a **MIFARE Classic 1K** token
end-to-end (key cracking with `mfoc`, reading secured sectors, carving a hidden GIF,
cloning a UID onto a magic card), and reviewing the EMV/CAP "chip-and-PIN" reader attack
from *Optimised to Fail*.
**Tools:** `libnfc`, `mfoc`, `nfc-mfclassic`, hex editing, OSINT, Codabar.
→ **[Open project](Contactless%20card%20security/README.md)**

### 2 - Power Side-Channel Attacks
Using a **ChipWhisperer-Lite** to read secrets from a chip's power consumption: learning
to map a power trace back to its C source, recovering an 11-character password from timing
leakage (each correct character adds a measurable loop iteration), and recovering a full
**AES-128 key** with **Correlation Power Analysis (CPA)** before decrypting the challenge
message.
**Tools:** ChipWhisperer (Capture + Analyzer), CPA/DPA, S-box leakage models, `numpy`,
`pycryptodome`.
→ **[Open project](Side%20Channel%20Attacks/README.md)**

### 3 - IoT RF Security
Attacking a 433.92 MHz radio-controlled relay (EV1527 "garage-door-opener" tech) with a
**PlutoSDR**: predicting its RF behaviour from the datasheet, locating the carrier in gqrx,
performing a **replay attack** with Universal Radio Hacker, and decoding the protocol to
compute its keyspace and brute-force time - ending in a security verdict on static-code
devices.
**Tools:** SDR (PlutoSDR), gqrx, Universal Radio Hacker, OOK/ASK, EV1527, replay vs.
rolling codes.
→ **[Open project](IOT%20Devices%20Security/README.md)**

### 4 - GSM Security
Passively intercepting a **private test GSM cell** with an SDR and `gr-gsm`: decoding the
broadcast parameters from live GSMTAP packets in Wireshark, following the control channels
to read a plaintext **SMS two-factor code**, proving the cell runs **A5/0 (no
encryption)**, and decoding a Full-Rate traffic channel to recover a **spoken password**.
**Tools:** SDR (LimeSDR/PlutoSDR), `gr-gsm`, Wireshark/GSMTAP, A5 cipher family, GSM
identities & channels.
→ **[Open project](Security%20of%20GSM%20Communication/README.md)**

---

## Themes across the portfolio

- **Identifiers are not secrets.** A card UID, a GSM IMSI/TMSI, an EV1527 address - each
  gets treated as proof of identity, and each is readable or forgeable by a passive
  attacker.
- **Optional or weak cryptography is no cryptography.** MIFARE's broken Crypto-1, GSM's
  A5/0 fallback, and static RF codes all fail the moment an attacker shows up - the
  defence is *mandatory, modern* crypto with freshness (rolling codes, session keys,
  mutual authentication).
- **The physical layer leaks.** Power, timing and radio emissions all carry secret-
  dependent signal; sound algorithms still fall to their implementations (CPA on AES) and
  to plaintext transmission (GSM SMS/voice).
- **Cheap, open tools lower the barrier.** `mfoc`, a ChipWhisperer, a £30 SDR with
  `gr-gsm` or URH - the hardware and software to run every attack here are inexpensive and
  freely available, which is exactly why these designs can no longer be trusted for
  anything sensitive.

## Skills demonstrated

Hardware & RF security · SDR (PlutoSDR / LimeSDR) · NFC/RFID (MIFARE Classic) · power
side-channel analysis (SPA, CPA) · protocol reverse-engineering · Wireshark / GSMTAP ·
cryptographic weaknesses (Crypto-1, A5, static codes) · OSINT · Python tooling · Linux/VM
workflows · and throughout a focus on tying each finding to a concrete **defensive
takeaway**.
