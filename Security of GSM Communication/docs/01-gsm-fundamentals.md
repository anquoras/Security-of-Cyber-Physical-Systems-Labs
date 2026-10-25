# 01. GSM Fundamentals: Identities, Ciphers and Channels

> **Scope:** Background concepts for an authorised lab against a private test cell.
> No interception is performed in this chapter.

You can't meaningfully attack GSM without first understanding how it identifies devices,
how it (optionally) encrypts them, and how it organises its radio channels. This chapter
builds that foundation and flags the weak points that the later interception exploits.

## Reaching the signal: frequency, ARFCN and antenna

The lab cell transmits at 1878.8 MHz (GSM-1800 downlink band). Two quick
calculations locate it:

**Antenna.** `λ = c / f = 3×10⁸ / 1.8788×10⁹ ≈ 0.16 m`. A practical receive antenna is a
quarter-wave monopole ≈ 4 cm (or an ~8 cm half-wave dipole).

ARFCN (Absolute Radio Frequency Channel Number) is the integer that names each 200 kHz
GSM channel. For the GSM-1800 downlink:

```
ARFCN = (f − 1805.2) / 0.2 + 512
      = (1878.8 − 1805.2) / 0.2 + 512
      = 368 + 512 = 880
```

So the cell is ARFCN 880, a value the network also advertises in its broadcast data,
which [chapter 02](02-finding-and-sniffing.md) confirms.

**UK GSM bands:** GSM-900 (uplink 880-915 / downlink 925-960 MHz) and GSM-1800 (uplink
1710-1785 / downlink 1805-1880 MHz).

## The A5 cipher family and what's breakable

GSM air-interface encryption is the A5 family, *negotiated per connection*:

| Cipher | Type | Status |
|--------|------|--------|
| **A5/0** | None (plaintext) | Nothing to break; everything is in the clear |
| **A5/1** | Stream cipher | Crackable with pre-computed rainbow tables |
| **A5/2** | Deliberately weakened (export) | Crackable in near real-time |
| **A5/3** | Block cipher (KASUMI) | The modern upgrade; not broken the way A5/1 and A5/2 are |

Beyond A5/1 and A5/2 being weak, the bigger problem is that encryption is optional and
network-selected. A cell can simply run A5/0, and handsets comply without warning the
user. That is exactly what this lab's cell does.

## How a SIM authenticates (and the keys involved)

Authentication is a challenge-response built on a shared secret:

- IMSI: the subscriber's permanent identity.
- Ki: a 128-bit secret key, stored on the SIM and in the network's AuC, never
  transmitted.
- RAND: a random challenge from the network.
- Kc: the session key derived from RAND + Ki, used to key A5.

```
1. Phone → network:  IMSI (request access)
2. Network looks up Ki for that IMSI
3. Network picks RAND, computes expected SRES and Kc from (RAND, Ki)
4. Network → phone:  RAND
5. SIM computes SRES and Kc from (RAND, its Ki); phone → network: SRES
6. If SRES matches, access granted; Kc keys all further traffic
```

Note the asymmetry: the network authenticates the phone, but the phone does not
authenticate the network. That is the root cause of IMSI-catcher / fake-base-station
attacks.

## Three identities: IMEI vs IMSI vs TMSI

| | **IMEI** | **IMSI** | **TMSI** |
|---|----------|----------|----------|
| Identifies | the **device** | the **subscriber (SIM)** | a **temporary alias** for the subscriber |
| Lifetime | fixed to hardware | changes with the SIM | reassigned frequently |
| Example use | blacklisting a stolen phone | subscriber lookup | over-the-air addressing |

The TMSI exists for privacy: broadcasting the permanent IMSI over the air would let
anyone track a user, so the network issues a rotating temporary identity instead. In
[chapter 03](03-intercepting-sms-and-voice.md) we actually watch the target's TMSI rotate
between two values.

A "network-locked" (SIM-locked) device is one restricted to a specific operator's
SIMs (a given MCC/MNC), common on subsidised contract phones, and the reason MCC
(country) and MNC (operator) codes matter beyond mere routing.

## The channel map: BCCH, CCCH, TCH

GSM multiplexes several logical channels onto the air interface. Three matter here:

- BCCH (Broadcast Control Channel): one-way, network→all, constant power. Carries the
  cell's identity, MCC/MNC, frequency/neighbour info and access parameters. This is what
  [chapter 02](02-finding-and-sniffing.md) decodes.
- CCCH (Common Control Channels): paging (incoming call/SMS notifications), access
  management, channel assignment. The gateway to a specific device.
- TCH (Traffic Channels): the actual payload, encoded speech (Full/Half Rate), user
  data, and SMS content. The target of [chapter 03](03-intercepting-sms-and-voice.md).

## Security takeaway

Three structural weaknesses defined GSM from the start and drive everything that follows:
optional/weak encryption (A5/0 to A5/2), one-way authentication (the network proves
nothing about itself to the phone), and a broadcast control plane that reveals cell and
paging metadata to any listener. Modern 4G/5G fix most of these; GSM, still live as a
fallback, does not.
