#!/usr/bin/env python3
"""
Educational Password Testing Tool

Copyright (c) 2025 worksbyahamed
All rights reserved.

This tool demonstrates password testing concepts for educational purposes only.
USE ONLY ON SYSTEMS YOU OWN OR HAVE EXPLICIT PERMISSION TO TEST.

Features:
- Local password hash testing
- Web form testing (localhost only)
- Password entropy calculation
- Rate limiting and logging
- Explicit ethical consent and restricted testing domains
"""

import argparse
import time
import logging
import hashlib
import getpass
import os
import sys
import requests
from threading import Thread, Event
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Colorama for colored console output
try:
    import colorama
    from colorama import Fore, Style
    colorama.init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:
    COLORAMA_AVAILABLE = False

LOG_FILE = "password_tester.log"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def print_banner():
    banner = "Educational Password Testing Tool"
    if COLORAMA_AVAILABLE:
        print(Fore.CYAN + Style.BRIGHT + banner.center(60, "=") + Style.RESET_ALL)
    else:
        print(banner.center(60, "="))

def confirm_ethics():
    print("\n" + ("!" * 60))
    print("This tool is for EDUCATIONAL USE ONLY.")
    print("You must have EXPLICIT PERMISSION to test any system.")
    print("Unauthorized use is illegal and unethical.")
    print(("!" * 60) + "\n")
    consent = input("Do you have permission to test this system? (yes/no): ").strip().lower()
    if consent != "yes":
        print("Permission not granted. Exiting.")
        sys.exit(1)

def calculate_entropy(password):
    import math
    unique_chars = len(set(password))
    if unique_chars == 0:
        return 0
    entropy = len(password) * math.log2(unique_chars)
    return round(entropy, 2)

def load_wordlist(wordlist_path):
    if not os.path.exists(wordlist_path):
        logging.error(f"Wordlist file not found: {wordlist_path}")
        sys.exit(1)
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]

def hash_password(password, algorithm="sha256"):
    try:
        h = hashlib.new(algorithm)
        h.update(password.encode("utf-8"))
        return h.hexdigest()
    except Exception as e:
        logging.error(f"Hashing error: {e}")
        return None

def parse_hash_file(hash_file_path):
    if not os.path.exists(hash_file_path):
        logging.error(f"Hash file not found: {hash_file_path}")
        sys.exit(1)
    with open(hash_file_path, "r") as f:
        content = f.read().strip()
    if ":" in content:
        algorithm, hash_value = content.split(":", 1)
        algorithm = algorithm.lower()
    else:
        algorithm = "sha256"
        hash_value = content
    return algorithm, hash_value

def is_probably_hash(s):
    # SHA-256 is 64 hex chars, SHA-1 is 40, MD5 is 32
    return len(s) in (32, 40, 64) and all(c in "0123456789abcdefABCDEF" for c in s)

def get_valid_hash_or_password():
    while True:
        hash_input = input("Enter the hash to test against (or plain text password): ").strip()
        if ":" in hash_input:
            algorithm, value = hash_input.split(":", 1)
            algorithm = algorithm.lower()
            if is_probably_hash(value):
                return algorithm, value
            else:
                print(Fore.RED + "[!] The value after ':' does not look like a valid hash." + Style.RESET_ALL if COLORAMA_AVAILABLE else "[!] The value after ':' does not look like a valid hash.")
                continue
        elif is_probably_hash(hash_input):
            # Assume SHA-256 if not specified
            return "sha256", hash_input
        else:
            # Assume plain text password, hash it
            if COLORAMA_AVAILABLE:
                print(Fore.YELLOW + "[!] Input does not look like a hash. Treating as plain text password and hashing with SHA-256." + Style.RESET_ALL)
            else:
                print("[!] Input does not look like a hash. Treating as plain text password and hashing with SHA-256.")
            hashed = hash_password(hash_input, "sha256")
            print(f"[i] SHA-256 hash of your password is: {hashed}")
            return "sha256", hashed

def local_hash_test(wordlist, algorithm, target_hash, delay=0.5):
    start_time = time.time()
    found = False
    attempts = 0
    for password in wordlist:
        attempts += 1
        hashed = hash_password(password, algorithm)
        if hashed == target_hash:
            elapsed = time.time() - start_time
            print_result(password, attempts, elapsed, True)
            found = True
            break
        time.sleep(delay)
    if not found:
        elapsed = time.time() - start_time
        print_result(None, attempts, elapsed, False)

def print_result(password, attempts, elapsed, found):
    if COLORAMA_AVAILABLE:
        print(Fore.YELLOW + "\n" + " RESULTS ".center(50, "*") + Style.RESET_ALL)
    else:
        print("\n" + " RESULTS ".center(50, "*"))
    if found:
        print(Fore.GREEN + f"[+] Password FOUND: {password}" + Style.RESET_ALL if COLORAMA_AVAILABLE else f"[+] Password FOUND: {password}")
    else:
        print(Fore.RED + "[!] Password NOT found in wordlist." + Style.RESET_ALL if COLORAMA_AVAILABLE else "[!] Password NOT found in wordlist.")
    print(f"Attempts: {attempts}")
    print(f"Time elapsed: {elapsed:.2f} seconds\n")
    if found:
        entropy = calculate_entropy(password)
        print(f"Password entropy (approx.): {entropy} bits")
        if entropy < 30:
            print(Fore.RED + "Weak password! Easily guessable." + Style.RESET_ALL if COLORAMA_AVAILABLE else "Weak password! Easily guessable.")
        elif entropy < 50:
            print(Fore.YELLOW + "Moderate password. Could be improved." + Style.RESET_ALL if COLORAMA_AVAILABLE else "Moderate password. Could be improved.")
        else:
            print(Fore.GREEN + "Strong password!" + Style.RESET_ALL if COLORAMA_AVAILABLE else "Strong password!")
    print("*" * 50)

def web_form_test(url, username, user_field, pass_field, success_text, failure_text, wordlist, delay=0.5):
    if not url.startswith("http://localhost") and not url.startswith("https://localhost"):
        logging.error("Web testing is restricted to localhost for safety.")
        sys.exit(1)
    session = requests.Session()
    start_time = time.time()
    found = False
    attempts = 0
    for password in wordlist:
        attempts += 1
        data = {user_field: username, pass_field: password}
        try:
            resp = session.post(url, data=data, timeout=5)
            if success_text in resp.text and failure_text not in resp.text:
                elapsed = time.time() - start_time
                print_result(password, attempts, elapsed, True)
                found = True
                break
        except Exception as e:
            logging.warning(f"Request failed: {e}")
        time.sleep(delay)
    if not found:
        elapsed = time.time() - start_time
        print_result(None, attempts, elapsed, False)

def main():
    setup_logging()
    print_banner()
    confirm_ethics()

    parser = argparse.ArgumentParser(description="Educational Password Testing Tool")
    parser.add_argument("--mode", choices=["local", "web"], required=True, help="Testing mode: local or web")
    parser.add_argument("--wordlist", required=True, help="Path to password wordlist file")
    parser.add_argument("--hash-file", help="File containing target hash (local mode)")
    parser.add_argument("--url", help="Web login URL (localhost only)")
    parser.add_argument("--username", help="Username for web form")
    parser.add_argument("--user-field", help="HTML field name for username")
    parser.add_argument("--pass-field", help="HTML field name for password")
    parser.add_argument("--success-text", help="Text indicating successful login")
    parser.add_argument("--failure-text", help="Text indicating failed login")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between attempts (seconds)")
    args = parser.parse_args()

    wordlist = load_wordlist(args.wordlist)

    if args.mode == "local":
        if not args.hash_file:
            algorithm, target_hash = get_valid_hash_or_password()
        else:
            algorithm, target_hash = parse_hash_file(args.hash_file)
        print(f"\n[+] Loaded {len(wordlist)} passwords from wordlist.")
        print(f"[+] Using hash algorithm: {algorithm}")
        local_hash_test(wordlist, algorithm, target_hash, delay=args.delay)

    elif args.mode == "web":
        required = [args.url, args.username, args.user_field, args.pass_field, args.success_text, args.failure_text]
        if not all(required):
            print("Missing required web testing arguments.")
            parser.print_help()
            sys.exit(1)
        print(f"\n[+] Loaded {len(wordlist)} passwords from wordlist.")
        print(f"[+] Target URL: {args.url}")
        web_form_test(
            args.url,
            args.username,
            args.user_field,
            args.pass_field,
            args.success_text,
            args.failure_text,
            wordlist,
            delay=args.delay
        )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if COLORAMA_AVAILABLE:
            print(Fore.RED + "\n[!] Interrupted by user. Exiting gracefully." + Style.RESET_ALL)
        else:
            print("\n[!] Interrupted by user. Exiting gracefully.")
        sys.exit(0)
