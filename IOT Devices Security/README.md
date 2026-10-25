# IoT RF Security — Capturing, Replaying & Breaking a 433 MHz Device

A hands-on wireless-security project against a common **433.92 MHz radio-controlled
relay** (the same EV1527 technology inside cheap garage-door openers, remote switches
and doorbells). Using a **Software-Defined Radio (PlutoSDR)**, I locate the signal,
replay it to trigger the device, decode its protocol, and work out exactly how (in)secure
the whole system is.

> ### ⚠️ Scope & ethics
> This work was carried out as an **authorised university laboratory** (University of
> Southampton, COMP3217 — *Security of Cyber-Physical Systems*) against a
> **lab-issued relay board that I powered and controlled myself**, transmitting at very
> short range inside the lab. No third-party device, vehicle, or access-control system
> was ever targeted, and **transmitting on these bands to interfere with equipment you
> don't own is illegal**. The author's ECS usernames are redacted. This is documented
> for **education and defensive understanding** of wireless/IoT leakage.

---

## Overview

Countless "smart" and not-so-smart devices still secure themselves with nothing more
than a fixed code broadcast in the clear on 433 MHz. This project takes one such device
apart end to end — from reading its datasheet to replaying its command and calculating
how long a brute force would take.

| # | Investigation | Headline result | Deep-dive |
|---|---------------|------------------|-----------|
| 1 | **Target reconnaissance** | Predicted the device's RF behaviour (433.92 MHz, OOK, no Manchester) and designed a 17.3 cm quarter-wave antenna — from the datasheet alone | [docs/01-target-reconnaissance.md](docs/01-target-reconnaissance.md) |
| 2 | **Spectrum monitoring & replay** | Located the exact carrier and performed a **working replay attack** that triggered the relay | [docs/02-spectrum-and-replay.md](docs/02-spectrum-and-replay.md) |
| 3 | **Decoding & brute force** | Identified the **EV1527** encoder, decoded all four buttons, and computed a **2²⁰ keyspace → ~9.47 h** full brute force | [docs/03-decoding-and-bruteforce.md](docs/03-decoding-and-bruteforce.md) |

## Key results & highlights

- 📡 **First-principles recon** — derived the operating frequency, modulation (OOK),
  and antenna length before ever switching on the SDR.
- 🎯 **Carrier hunt** — found the transmit frequency at **433.92 MHz** in gqrx and
  measured the occupied bandwidth at **~2.35 MHz**.
- ▶️ **Replay attack** — captured, trimmed and re-transmitted the remote's signal with
  Universal Radio Hacker to operate the relay with no knowledge of the underlying code.
- 🧩 **Protocol reverse engineering** — identified the **EV1527** learning-code chip:
  a 24-bit frame = **20-bit fixed address + 4-bit button code**, retransmitted ~10–13×.
- ⏱️ **Keyspace analysis** — 2²⁰ = 1,048,576 possible IDs, exhaustible in **under 10
  hours**, and a reasoned verdict on why this device is unfit for security-critical use.

## Skills & tools

Software-Defined Radio (ADALM-PlutoSDR) · gqrx (spectrum monitoring) · Universal Radio
Hacker (capture/analyse/replay) · OOK / ASK modulation · EV1527 learning-code protocol ·
quarter-wave antenna design · replay attacks & rolling-code defences · RF brute-force
analysis · signal-to-noise / gain tuning.

## What I learned

- **Reconnaissance predicts the attack.** The datasheet alone told me the frequency,
  modulation and antenna length — the SDR work just confirmed first-principles reasoning.
- **Replay needs no understanding of the protocol.** A clean capture and retransmit was
  enough to operate the device without decoding a single bit — which is exactly why it's
  such a common real-world attack.
- **Static codes are the root cause.** Everything that makes this device weak — replay,
  brute force, interception — traces back to a *fixed* identifier with no counter or
  freshness. **Rolling codes** exist precisely to break the replay.
- **Small keyspaces don't need cleverness.** 2²⁰ sounds large until you multiply it by a
  33 ms transmission and get under 10 hours — brute force is a stopwatch problem, not a
  cryptographic one.

---

### Repository layout

```
.
├── README.md
├── docs/
│   ├── 01-target-reconnaissance.md    # datasheet, antenna, modulation reasoning
│   ├── 02-spectrum-and-replay.md      # find the signal + replay attack
│   └── 03-decoding-and-bruteforce.md  # EV1527 decode, keyspace, verdict
└── assets/                            # gqrx / URH captures & button bitstreams
```
