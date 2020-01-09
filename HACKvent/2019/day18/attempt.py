from Crypto.Cipher import Salsa20
import binascii

cipher = binascii.unhexlify("096CD446EBC8E04D2FDE299BE44F322863F7A37C18763554EEE4C99C3FAD15")
secret = binascii.unhexlify("0320634661B63CAFAA76C27EEA00B59BFB2F7097214FD04CB257AC2904EFEE46")
nonce = binascii.unhexlify("11458fe7a8d032b1")
salsa = Salsa20.new(key=secret, nonce=nonce)
plain= salsa.decrypt(cipher)
print(plain)
