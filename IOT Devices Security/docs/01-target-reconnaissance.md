# 01. Target Reconnaissance: Reading the Device Before Touching the Radio

> **Scope:** Authorised lab. The target is a lab-issued GV-RK04S-12 relay board
> that I powered and controlled myself.

Good RF work starts on paper. Before assembling an SDR, you can predict almost
everything about how a cheap wireless device behaves: its frequency, its modulation,
even the antenna you'd need, just from its datasheet and some first-principles physics.
This chapter does exactly that for the target relay.

## Context: the device

The target is a GV-RK04S-12, a 4-channel wireless remote-control relay switch
(branded Geekcreit / Pengjing), bought from a mainstream components supplier. It's the
archetypal cheap 433 MHz IoT actuator: a remote with four buttons, and a relay board
that closes one of four high-current switches when it hears the matching code.

| Property | Value (from datasheet) |
|----------|------------------------|
| Manufacturer | Geekcreit / Pengjing |
| Supply | DC **12 V** (across the 12V+ / 12V− terminals) |
| Relay rating | **20 A** per relay |
| Operating frequency | **315 / 433.92 MHz** |

## Objective

From the datasheet alone, predict the device's RF characteristics and design a matching
antenna, then state what the SDR work should later confirm.

## Approach and findings

### Designing a quarter-wave antenna

A simple, effective antenna is a quarter-wavelength monopole. With
`λ = c / f` and a quarter-wave element `L = c / (4f)`:

| Frequency | Wavelength λ | Quarter-wave L | Practical cut |
|-----------|-------------|----------------|---------------|
| 433.92 MHz (global) | 69.1 cm | **17.3 cm** | 17.2-17.5 cm |
| 315.00 MHz (N. America) | 95.2 cm | **23.8 cm** | 23.7-24.0 cm |

**Construction:** cut a stiff copper wire to 17.3 cm, insert one end into the board's
"receiving antenna" hole, stand it straight, and secure it. A straight quarter-wave
element is the simplest antenna that resonates efficiently at the target frequency.

### Modulation: it's going to be OOK

The device almost certainly uses OOK (On-Off Keying), a degenerate form of ASK
where the carrier is simply switched on for a `1` and off for a `0`. The
reasoning is economic: OOK needs the cheapest possible transmitter (one oscillator you
turn on and off), which is exactly right for a low-cost COTS relay. FSK or anything more
complex would add cost for no benefit on a simple 24-bit learning protocol.

### Encoding: probably not Manchester

Manchester encoding represents each bit as a mid-bit *transition* (0 → one edge
direction, 1 → the other). Its virtues (automatic clock recovery, no DC bias, better
noise immunity) would genuinely suit short, low-power 433 MHz bursts with drift-prone
oscillators.

But this device probably won't use it. Strict Manchester decoding needs slightly more
capable hardware, and ultra-low-cost boards minimise every cent: they lean on simpler
pulse-width-style OOK timing instead. So Manchester is useful in principle but unlikely
here, a prediction the signal analysis later bears out (the frames turn out to be
pulse-width-timed EV1527, not Manchester).

### Will co-located devices interfere?

Not under normal use. Each receiver is "learned" to a specific remote via a 20-bit
address (EV1527), and only reacts to its exact stored code; different receivers simply
ignore each other's transmissions. Collisions are rare because button presses are short
(~100-200 ms) and unsynchronised, and a corrupted packet is just discarded (no false
trigger). The manual's claim of "no interference with each other" is really a statement
about *addressing*, not about the shared RF channel.

## Security takeaway

Two reconnaissance facts already foreshadow the device's weakness: it uses the
simplest possible modulation (trivial to capture and regenerate) and a fixed learned
address (no freshness between transmissions). Everything in the next two chapters
(replay, decode, brute force) follows from those two design choices made in the name of
cost.
