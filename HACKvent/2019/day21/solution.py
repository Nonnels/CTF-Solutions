from Crypto.PublicKey import ECC
from Crypto.Cipher import AES
import hashlib
import base64
import binascii

# ----- globals ----- #
salt = b'TwoHundredFiftySix'
iterations = 256*256*256
x=0xc58966d17da18c7f019c881e187c608fcb5010ef36fba4a199e7b382a088072f
y=0xd91b949eaf992c464d3e0d09c45b173b121d53097a9d47c25220c0b4beb943c
cipher = b'Hy97Xwv97vpwGn21finVvZj5pK/BvBjscf6vffm1po0='

print("Generating Dictionary from Rockyou Dump")
dictionary = []
with open('/usr/share/wordlists/rockyou.txt','rb') as f:
    for line in f:
        if len(line.strip()) ==16:
            dictionary.append(line.strip()) 
   
print("Looking for Santas password...")
for guess in dictionary:
    # generate santa password
    passwd = hashlib.sha256(guess).hexdigest()
    try:
        #construct santa private key
        privatekey = ECC.construct(curve='NIST P-256',
                                   point_x=x,
                                   point_y=y,
                                   d=int(passwd, 16))                
        print(f"NIST P-256 Constructed: (d) found!")
        print(f"Santas password: {guess} found!")
        
        # Perform key derivation.
        print(f"Generating PBKDF2_HMAC using {guess}")
        hmac = hashlib.pbkdf2_hmac('sha256', guess, salt, iterations)    
                
        #AES decrypt
        print(f"Decrypting AES with PBKDF2_HMAC derived key")
        dec = AES.new(hmac, AES.MODE_ECB)
        plain = dec.decrypt(base64.b64decode(cipher))
        print(f"Solved!: {plain}")
        break
    except:
        pass
