#!/usr/bin/env python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pyrage",
#     "pyyaml",
# ]
# ///
import argparse
from pyrage import encrypt, decrypt, x25519
import yaml
import base64

def encrypt_secret(file_path, recipient):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)
    public_key = x25519.Recipient.from_str(recipient)

    encrypted = encrypt(str.encode(data["spec"]["secret"]), [public_key])
    encoded_secret = base64.b64encode(encrypted).decode()

    data["spec"]["secret"] = f"ENC[{encoded_secret}]"

    yaml_output = yaml.dump(data, sort_keys=False)
    print(yaml_output)

def decrypt_secret(file_path, key):
    with open(file_path, "r") as f:
        data = yaml.safe_load(f)

    if "ENC[" in data["spec"]["secret"]:
        secret = data["spec"]["secret"][4:-1]
    else:
        print("Secret is already decrypted")
        return 1

    encrypted_secret = base64.b64decode(secret)
    decrypted = decrypt(encrypted_secret, [x25519.Identity.from_str(key)])
    decoded_secret = decrypted.decode()

    data["spec"]["secret"] = decoded_secret

    yaml_output = yaml.dump(data, sort_keys=False)
    print(yaml_output)

def main():
    parser = argparse.ArgumentParser(description="Encrypt and decrypt Kubernetes AgeSecret manifests.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a secret and output it as a Kubernetes manifest.")
    encrypt_parser.add_argument("--file", required=True, help="File containing the secret to encrypt.")
    encrypt_parser.add_argument("-r", required=True, help="Recipient public key.")

    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a secret from a Kubernetes manifest.")
    decrypt_parser.add_argument("--file", required=True, help="Kubernetes manifest file.")
    decrypt_parser.add_argument("-k", required=True, help="File containing the private key.")

    args = parser.parse_args()

    if args.command == "encrypt":
        encrypt_secret(args.file, args.r)
    elif args.command == "decrypt":
        decrypt_secret(args.file, args.k)

if __name__ == "__main__":
    main()
