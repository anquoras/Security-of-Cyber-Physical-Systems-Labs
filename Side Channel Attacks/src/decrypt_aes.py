# decrypt_aes.py
#
# Decrypts the Appendix-A ciphertext using the AES-128 key recovered from the
# ChipWhisperer `ecslabs-aes` target via a CPA (Correlation Power Analysis) attack.
#
# The target encrypts with AES-128 in ECB mode (the ChipWhisperer SimpleSerial
# default), so decryption is a straight ECB decrypt with the recovered key.
#
# Environment: standalone Python 3. Requires `pycryptodome` (provides Crypto.Cipher).
#   pip install pycryptodome
#   python3 decrypt_aes.py

from Crypto.Cipher import AES
import binascii

# Ciphertext from Appendix A, concatenated into one hex string (PDF line breaks removed).
ciphertext_hex = (
    "F68E619820F41B0705759AC116193829"
    "098872E175F0859012F6F88DF2246CB7"
    "CE68526A85380F9AF5D6A2965A7CFD3A"
    "7691B998F672581BDE316F8AA243B3B2"
    "173F3C4A05E3B51932D194FC02C93AC9"
    "2A4FEB6C3B666B4EAF1E275520F886D7"
    "A63B47E128C478D838EA699690777FE1"
    "1ABB9280F9510A9D45125CE29741E04C"
    "7C643D72487E3889710178266AF0DD5C"
    "81C0FFC6750F968269F151B23039BD20"
    "57D672D8F4D9B5D3C592285E3E7B80E1"
)

# 16-byte AES key recovered from the Analyzer's CPA attack.
extracted_key_hex = "01189998819991197253FFFFFFFFFFFF"


def decrypt_message(key_hex, cipher_hex):
    try:
        key = binascii.unhexlify(key_hex)
        ciphertext = binascii.unhexlify(cipher_hex)

        # SimpleSerial AES on the target uses ECB mode.
        cipher = AES.new(key, AES.MODE_ECB)

        decrypted_bytes = cipher.decrypt(ciphertext)

        # errors='ignore' drops any trailing padding bytes that aren't valid UTF-8.
        return decrypted_bytes.decode('utf-8', errors='ignore')

    except ValueError as e:
        return "Decryption failed. Please check your key format: {}".format(e)


if __name__ == "__main__":
    print("\n--- DECRYPTING MESSAGE ---")
    print(decrypt_message(extracted_key_hex, ciphertext_hex))
