# Contactless Card Security: Building, Breaking and Analysing NFC / EMV Systems

A security investigation into three everyday contactless-card technologies: how
identity cards can be rebuilt from leaked directory data, how the widely deployed
MIFARE Classic access token is broken from end to end, and how the EMV/CAP
"chip-and-PIN" reader ecosystem fails in practice.

> ### Scope and ethics
> This work was carried out as an authorised university laboratory (University of
> Southampton, COMP3217, *Security of Cyber-Physical Systems*) against a
> lab-issued NFC token and synthetic test data provided by the module.
> All personal data has been fictionalised or redacted: the "target" identity is a
> deliberately fabricated test record supplied by the lab, and the author's own
> credentials are masked throughout. Nothing here targets a real individual, a real
> access-control system, or a live payment card. The techniques are documented for
> education and defensive understanding only.

---

## Overview

Contactless cards are everywhere: building access, transit, ID, payments. Yet many
still rely on cryptography and trust assumptions that were broken years ago. This
project works through three self-contained investigations, each taking a system apart
and asking *"what does an attacker actually gain, and why is this broken?"*

| # | Investigation | Headline result | Deep-dive |
|---|---------------|------------------|-----------|
| 1 | **ID-card reconstruction** | Rebuilt a true-to-life university ID card from an unauthenticated LDAP dump, including reverse-engineering the barcode format | [docs/01-id-card-forgery.md](docs/01-id-card-forgery.md) |
| 2 | **MIFARE Classic 1K** | Cracked all 16 sectors in ~58 s, recovered hidden data (flags and an embedded GIF), analysed access-control bits, and cloned the UID | [docs/02-mifare-classic.md](docs/02-mifare-classic.md) |
| 3 | **EMV / CAP readers** | Reviewed the *Optimised to Fail* attack and assessed a real software CAP-reader implementation | [docs/03-emv-cap-readers.md](docs/03-emv-cap-readers.md) |

## Key results and highlights

- Full key recovery on a MIFARE Classic EV1 1K token using the `mfoc` nested
  attack: every sector key recovered in under a minute on commodity USB hardware.
- Data carving: identified a hidden file across sectors 6-9 from its
  `GIF87a` magic bytes and recovered it.
- Access-control forensics: decoded the C1/C2/C3 access bits to explain why
  one sector was permanently locked and another made Key-B-only.
- Identity reconstruction: reverse-engineered the ID card's Codabar
  barcode (an `A…C` wrapper around the staff number) and verified it byte for byte
  against the original.
- UID cloning: rewrote the manufacturer block on a "magic" card, including
  recomputing the BCC checksum by hand.

## Skills and tools

`libnfc` · `nfc-list` · `mfoc` (MIFARE Classic Offline Cracker) · `nfc-mfclassic` ·
hex editing · Crypto-1 / nested-authentication attacks · MIFARE access-bit analysis ·
OSINT · `base64` · Codabar barcode encoding · Kali Linux / VM workflow · EMV and CAP
protocol analysis.

## What I learned

- "Can't read the key" does not mean secure. MIFARE Classic never exposes Key A
  directly, yet the Crypto-1 cipher leaks enough during authentication that offline
  cracking is trivial. It is a clear example of a *protocol* weakness defeating a
  *storage* protection.
- Trust has to live in hardware, not software. The EMV/CAP analysis shows why moving
  a security boundary onto a general-purpose PC (malware, keyloggers) dismantles the
  whole point of a trusted offline device.
- Identity leaks are an aggregation problem. No single field in the directory dump
  was secret, but combined with a public card template they were enough to forge a
  convincing physical credential.
- Access-control bits are easy to get wrong. Small differences in three bits per
  block flip a sector between writable, Key-B-only, and permanently frozen.

---

### Repository layout

```
.
├── README.md
├── docs/
│   ├── 01-id-card-forgery.md
│   ├── 02-mifare-classic.md
│   └── 03-emv-cap-readers.md
└── assets/
    ├── id-card-redacted.png       # reconstructed card (redact before publishing, see note)
    ├── mifare-write-sector1.png
    └── mifare-uid-rewrite.png
```

> **Image redaction note:** the PNGs under `assets/` are the original lab screenshots.
> Before making this repository public, blur the photo, staff number and barcode on
> `id-card-redacted.png`, and mask any visible usernames in the two MIFARE
> screenshots. These are raster images, so the redaction must be done in an image editor.
