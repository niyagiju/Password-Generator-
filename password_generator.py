#!/usr/bin/env python3
"""password_generator.py - simple, configurable password generator

Usage examples:
  # Basic: generate one 12-char password
  python3 password_generator.py --length 12

  # Generate 5 passwords with symbols and digits
  python3 password_generator.py -l 16 -n 5 --no-lower --no-upper

  # Save to file
  python3 password_generator.py -l 20 -n 10 -o passwords.txt
"""

import secrets
import string
import argparse
from typing import List

def generate_password(length: int = 12,
                      use_upper: bool = True,
                      use_lower: bool = True,
                      use_digits: bool = True,
                      use_symbols: bool = True) -> str:
    if length < 1:
        raise ValueError("Password length must be >= 1")

    alphabet = ""
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        # use a safe subset of punctuation to avoid shell issues
        alphabet += "!@#$%&*?-_+="

    if not alphabet:
        raise ValueError("At least one character set must be enabled")

    # Ensure the password contains at least one character from each selected set
    required = []
    if use_lower:
        required.append(secrets.choice(string.ascii_lowercase))
    if use_upper:
        required.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        required.append(secrets.choice(string.digits))
    if use_symbols:
        required.append(secrets.choice("!@#$%&*?-_+="))

    # If length is smaller than required characters, fill by truncating required
    if length < len(required):
        # Shuffle and return trimmed required characters
        return ''.join(secrets.choice(required) for _ in range(length))

    # Fill the rest securely
    remaining_length = length - len(required)
    password_chars = [secrets.choice(alphabet) for _ in range(remaining_length)]
    password_chars += required

    # Shuffle securely
    secrets.SystemRandom().shuffle(password_chars)
    return ''.join(password_chars)

def generate_many(count: int, **kwargs) -> List[str]:
    return [generate_password(**kwargs) for _ in range(count)]

def parse_args():
    p = argparse.ArgumentParser(description="Secure Password Generator")
    p.add_argument("-l", "--length", type=int, default=12, help="Length of each password (default: 12)")
    p.add_argument("-n", "--number", type=int, default=1, help="How many passwords to generate (default: 1)")
    p.add_argument("--no-upper", action="store_true", help="Disable uppercase letters")
    p.add_argument("--no-lower", action="store_true", help="Disable lowercase letters")
    p.add_argument("--no-digits", action="store_true", help="Disable digits")
    p.add_argument("--no-symbols", action="store_true", help="Disable symbols")
    p.add_argument("-o", "--output", type=str, help="Write passwords to a file (one per line)")
    return p.parse_args()

def main():
    args = parse_args()
    opts = {
        "length": args.length,
        "use_upper": not args.no_upper,
        "use_lower": not args.no_lower,
        "use_digits": not args.no_digits,
        "use_symbols": not args.no_symbols,
    }
    try:
        passwords = generate_many(args.number, **opts)
    except ValueError as e:
        print(f"Error: {e}")
        return

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            for pw in passwords:
                f.write(pw + "\\n")
        print(f"Wrote {len(passwords)} password(s) to {args.output}")
    else:
        for i, pw in enumerate(passwords, 1):
            print(f"{i}: {pw}")

if __name__ == "__main__":
    main()