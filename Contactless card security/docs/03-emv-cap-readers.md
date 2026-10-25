# 03 — EMV / CAP: Analysing a Software Card Reader

> **Scope:** Literature review + static code assessment only. **No live payment card,
> account, or PIN was ever used.** This section is a security analysis, not an attack.

## Context

The final investigation moves from access tokens to **payment cards**. The reference is
Drimer, Murdoch & Anderson's *["Optimised to Fail: Card Readers for Online
Banking"](https://murdoch.is/papers/fc09optimised.pdf)* (FC 2009), which dissects the
**CAP** (Chip Authentication Program) readers UK banks issued for online-banking login.
Alongside it, I examined an archived software implementation of a CAP reader
([`emv-cardreader-sec`](https://code.google.com/archive/p/emv-cardreader-sec/)).

CAP works by having a handheld reader challenge the chip card; the card computes a MAC
(using keys that never leave the chip) and the reader displays a one-time code. The
paper's core argument: moving trust assumptions around this design quietly breaks it.

## C1 — Can it be built?

**Likely yes, with effort.** It is a software implementation of the CAP protocol over
PC/SC, so it should compile — but the project is **archived (Google Code era, ~2009)**.
Building it today would mean sourcing period-correct dependencies (specific PC/SC
smartcard libraries, an older toolchain/Mono runtime) and resolving environment
incompatibilities. Feasible, not turnkey.

## C2 — Will it work, and how would you test it safely?

**Probably, because of EMV's extreme backwards-compatibility:**
- CAP rides on **standard EMV chip-and-PIN commands**, which payment networks keep
  stable for decades.
- The software does **no cryptography itself** — it is only a messenger. The card holds
  the keys and computes the MAC.
- It talks **PC/SC**, still the default smartcard API on modern OSes.

**Testing it safely:**
- Run inside an **isolated VM** with PC/SC-Lite.
- Use a **cheap PC/SC reader** and **EMV test / expired cards** — never a live card,
  account, or real PIN.
- Validate incrementally: basic APDU exchange → protocol conformance → CAP modes →
  edge cases → security checks.
- Treat it as research only: no transaction attempts; debug AID mismatches against the
  EMV specs.

## C3 — Is it wise to implement?

**No.** The paper's central finding is that the value of a CAP reader is being a
**trusted, offline, single-purpose device**. Re-implementing it in software on a
general-purpose PC **destroys that property**:

- **Trust boundary collapse** — the PC is exposed to keyloggers and malware, so card
  interactions and PINs can be captured (enabling cloning or relay attacks). This is
  exactly the hardware purpose the paper says such a device exists to protect
  (§4.2).
- **Distribution risk** — shipping such software invites tampered builds and
  supply-chain attacks (§4.4).
- **It amplifies EMV's existing weaknesses** — e.g. the middleperson/relay issues
  discussed in §4.3 — rather than containing them.
- **Ethical/legal** — the paper already criticises banks for shifting liability to
  customers; a software reader weakens customer protection further and could facilitate
  fraud if misused.

## C4 — Could it work with all modern cards? Would you want to?

**Not without major rework — and no, I wouldn't.** The code is tied to **2009-era UK
EMV/CAP** (specific AIDs and bit-filters for particular banks). Modern cards have moved
on:

- Updated EMV specs (4.3+), **contactless**, and **dynamic data authentication (DDA/CDA)**.
- Stricter risk management — anti-replay, tighter ATC handling.
- Regional divergence — different cryptograms across US/EU, **PSD2 SCA** in Europe.
- Tokenisation and mobile wallets (Apple Pay / Google Pay), biometrics, deprecated
  legacy modes.

Adapting it would mean reverse-engineering current cards, rewriting CDOLs/bit-filters,
and adding new AID handling — all requiring deep EMV expertise and legal test cards.
Given the security and ethical downsides in C3, the effort isn't justified.

## Security takeaway

CAP is a case study in **why security boundaries belong in dedicated hardware.** A
protocol can be perfectly sound and still fail catastrophically when its trusted
component is relocated onto an untrusted platform. The right lesson for builders is to
*preserve* the hardware trust anchor (secure element, trusted display/input), not to
emulate it away for convenience.
