
#!/usr/bin/env python3

import os
from cryptography.fernet import Fernet

SANDBOX = "sandbox"
BACKUP = "encrypted_backup"
KEY_FILE = "thekey.key"


def main():

    if not os.path.isdir(SANDBOX):
        print("[-] Sandbox folder not found")
        return

    os.makedirs(BACKUP, exist_ok=True)

    if os.path.exists(KEY_FILE):
        print("[-] Key already exists. Protect your existing key.")
        return

    key = Fernet.generate_key()

    with open(KEY_FILE, "xb") as f:
        f.write(key)

    cipher = Fernet(key)

    count = 0

    for root, dirs, filenames in os.walk(SANDBOX):

        for filename in filenames:

            if filename.endswith(".encrypted"):
                continue

            source = os.path.join(root, filename)
            relative = os.path.relpath(source, SANDBOX)

            backup = os.path.join(BACKUP, relative)
            encrypted_file = source + ".encrypted"

            try:
                with open(source, "rb") as f:
                    original = f.read()

                os.makedirs(
                    os.path.dirname(backup),
                    exist_ok=True
                )

                with open(backup, "xb") as f:
                    f.write(original)

                encrypted = cipher.encrypt(original)

                with open(encrypted_file, "xb") as f:
                    f.write(encrypted)

                with open(encrypted_file, "rb") as f:
                    recovered = cipher.decrypt(f.read())

                if recovered != original:
                    raise ValueError("Verification failed")

                print("[+] Backup:", backup)
                print("[+] Encrypted:", encrypted_file)

                count += 1

            except Exception as error:
                print("[-] Error:", source, error)

    print("\n[+] Processing completed")
    print("[+] Files processed:", count)

    remover = os.remove("test.txt")
    print("Test Deleted Sucess")

if __name__ == "__main__":
    main()

