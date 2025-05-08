def _print_results(self):
        """Print the results of the password test"""
        print("\n\n" + "="*50)
        if COLORAMA_AVAILABLE:
            print(f"{Fore.YELLOW} RESULTS {Style.RESET_ALL}".center(50, "*"))
        else:
            print(" RESULTS ".center(50, "*"))
        print("="*50)
        
        duration = (self.end_time - self.start_time).total_seconds()
        
        if self.successful:
            if COLORAMA_AVAILABLE:
                print(f"\n[{Fore.GREEN}+{Style.RESET_ALL}]#!/usr/bin/env python3
"""
Educational Password Testing Tool

Copyright (c) 2025 worksbyahamed
All rights reserved.

This tool demonstrates password testing concepts for educational purposes only.
USE ONLY ON SYSTEMS YOU OWN OR HAVE EXPLICIT PERMISSION TO TEST.

Features:
- Basic dictionary-based password testing
- Rate limiting to prevent service disruption
- Logging for educational analysis
- Restricted to localhost testing by default
"""

import argparse
import time
import logging
import hashlib
import getpass
import os
import sys
import requests
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

try:
    from colorama import init, Fore, Style
    from tqdm import tqdm
    COLORAMA_AVAILABLE = True
    init()  # Initialize colorama
except ImportError:
    COLORAMA_AVAILABLE = False

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("password_test_log.txt"),
        logging.StreamHandler()
    ]
)

class PasswordTester:
    def __init__(self, args):
        self.args = args
        self.successful = False
        self.found_password = None
        self.attempts = 0
        self.start_time = None
        self.end_time = None
        
        # Verification
        if not self._verify_ethical_use():
            sys.exit(1)
            
        logging.info("Initialized password testing tool in educational mode")
    
    def _verify_ethical_use(self):
        """Verify the user understands the ethical implications"""
        print("\n" + "="*80)
        print(" EDUCATIONAL PURPOSE ONLY ".center(80, "*"))
        print("="*80)
        print("\nThis tool is for EDUCATIONAL PURPOSES ONLY.")
        print("Using this tool against systems without permission is illegal and unethical.")
        print("\nBy continuing, you confirm that:")
        print("1. You are using this ONLY on systems you own or have explicit permission to test")
        print("2. You understand this is for learning about security, not for unauthorized access")
        print("3. You take full responsibility for how this tool is used\n")
        
        consent = input("Do you understand and agree to these terms? (yes/no): ").lower()
        if consent != "yes":
            logging.warning("User did not confirm ethical use agreement")
            print("Exiting program.")
            return False
        
        # Log the consent for educational records
        logging.info("User confirmed educational purpose and ethical use agreement")
        return True
    
    def test_local_password(self):
        """Test against a local password hash"""
        if not self.args.hash_file:
            correct_password = getpass.getpass("Enter the password to test against: ")
            hash_algo = 'sha256'
            correct_hash = hashlib.sha256(correct_password.encode()).hexdigest()
        else:
            try:
                with open(self.args.hash_file, 'r') as f:
                    hash_data = f.read().strip().split(':')
                    if len(hash_data) == 1:
                        correct_hash = hash_data[0]
                        hash_algo = 'sha256'  # Default
                    else:
                        hash_algo = hash_data[0]
                        correct_hash = hash_data[1]
            except Exception as e:
                logging.error(f"Error reading hash file: {e}")
                return
        
        logging.info(f"Starting local password test using {hash_algo} algorithm")
        self._run_dictionary_attack(correct_hash, hash_algo)
    
    def test_web_form(self):
        """Test against a local web application form - LOCALHOST ONLY"""
        if not self.args.url:
            logging.error("URL is required for web form testing")
            return
            
        # Safety check - only allow localhost testing
        if not (self.args.url.startswith('http://localhost') or 
                self.args.url.startswith('http://127.0.0.1')):
            logging.error("For educational purposes, only localhost testing is permitted")
            print("Error: For safety reasons, this tool only allows testing on localhost.")
            return
            
        logging.info(f"Starting web form test against {self.args.url}")
        
        if not self.args.username:
            username = input("Enter username to test: ")
        else:
            username = self.args.username
            
        self._run_web_dictionary_attack(username)
    
    def _calculate_hash(self, password, algorithm):
        """Calculate hash based on specified algorithm"""
        if algorithm.lower() == 'md5':
            return hashlib.md5(password.encode()).hexdigest()
        elif algorithm.lower() == 'sha1':
            return hashlib.sha1(password.encode()).hexdigest()
        else:  # Default to SHA-256
            return hashlib.sha256(password.encode()).hexdigest()
            
    def _run_dictionary_attack(self, correct_hash, hash_algo):
        """Run a dictionary attack against a password hash"""
        if not self.args.wordlist:
            logging.error("Wordlist is required")
            return
            
        try:
            with open(self.args.wordlist, 'r', errors='ignore') as f:
                passwords = [line.strip() for line in f]
        except Exception as e:
            logging.error(f"Error reading wordlist: {e}")
            return
            
        logging.info(f"Loaded {len(passwords)} passwords from wordlist")
        self.start_time = datetime.now()
        
        # Progress display thread
        stop_thread = False
        
        def show_progress():
            last_attempts = 0
            while not stop_thread:
                if last_attempts != self.attempts:
                    passwords_per_sec = self.attempts / max(1, (datetime.now() - self.start_time).total_seconds())
                    sys.stdout.write(f"\rTested {self.attempts}/{len(passwords)} passwords " +
                                    f"({passwords_per_sec:.2f} passwords/sec)")
                    sys.stdout.flush()
                    last_attempts = self.attempts
                time.sleep(0.1)
                
        progress_thread = Thread(target=show_progress)
        progress_thread.daemon = True
        progress_thread.start()
        
        try:
            for password in passwords:
                if self.successful:
                    break
                    
                # Calculate hash of current password
                password_hash = self._calculate_hash(password, hash_algo)
                
                # Compare against correct hash
                if password_hash == correct_hash:
                    self.successful = True
                    self.found_password = password
                    break
                
                self.attempts += 1
                
                # Add a small delay to prevent resource exhaustion
                time.sleep(0.001)
        finally:
            stop_thread = True
            progress_thread.join()
            self.end_time = datetime.now()
            self._print_results()
    
    def _run_web_dictionary_attack(self, username):
        """Run a dictionary attack against a web form"""
        if not self.args.wordlist:
            logging.error("Wordlist is required")
            return
            
        try:
            with open(self.args.wordlist, 'r', errors='ignore') as f:
                passwords = [line.strip() for line in f]
        except Exception as e:
            logging.error(f"Error reading wordlist: {e}")
            return
            
        logging.info(f"Loaded {len(passwords)} passwords from wordlist")
        self.start_time = datetime.now()
        
        # Progress display thread
        stop_thread = False
        
        def show_progress():
            last_attempts = 0
            while not stop_thread:
                if last_attempts != self.attempts:
                    passwords_per_sec = self.attempts / max(1, (datetime.now() - self.start_time).total_seconds())
                    sys.stdout.write(f"\rTested {self.attempts}/{len(passwords)} passwords " +
                                    f"({passwords_per_sec:.2f} passwords/sec)")
                    sys.stdout.flush()
                    last_attempts = self.attempts
                time.sleep(0.1)
                
        progress_thread = Thread(target=show_progress)
        progress_thread.daemon = True
        progress_thread.start()
        
        # Request session for cookies
        session = requests.Session()
        
        try:
            for password in passwords:
                if self.successful:
                    break
                    
                # Prepare login data
                login_data = {
                    self.args.user_field: username,
                    self.args.pass_field: password
                }
                
                try:
                    # Send the request
                    response = session.post(
                        self.args.url,
                        data=login_data,
                        allow_redirects=True,
                        timeout=5
                    )
                    
                    # Check for successful login
                    if self.args.success_text and self.args.success_text in response.text:
                        self.successful = True
                        self.found_password = password
                        break
                    elif self.args.failure_text and self.args.failure_text not in response.text:
                        self.successful = True
                        self.found_password = password
                        break
                        
                except Exception as e:
                    logging.warning(f"Request error: {e}")
                    
                self.attempts += 1
                
                # Rate limiting to prevent DOS
                time.sleep(self.args.delay)
                
        finally:
            stop_thread = True
            progress_thread.join()
            self.end_time = datetime.now()
            self._print_results()
    
    def _print_results(self):
        """Print the results of the password test"""
        print("\n\n" + "="*50)
        print(" RESULTS ".center(50, "*"))
        print("="*50)
        
        duration = (self.end_time - self.start_time).total_seconds()
        
        if self.successful:
            print(f"\n[+] Password found: {self.found_password}")
        else:
            print("\n[-] Password not found in wordlist")
            
        print(f"\n[*] Attempts: {self.attempts}")
        print(f"[*] Duration: {duration:.2f} seconds")
        print(f"[*] Speed: {self.attempts / max(1, duration):.2f} passwords/second")
        
        logging.info(f"Test completed - Success: {self.successful}, " +
                     f"Attempts: {self.attempts}, Duration: {duration:.2f}s")
                     
        print("\n" + "="*50)
        print(" EDUCATIONAL FINDINGS ".center(50, "*"))
        print("="*50)
        print("\nSecurity lessons from this exercise:")
        print("1. Simple passwords can be quickly discovered")
        print("2. Password complexity dramatically increases testing time")
        print("3. Rate limiting is an effective defense mechanism")
        print("4. Account lockout policies prevent this type of attack")
        print("5. Multi-factor authentication provides additional security")
        
        if self.successful:
            password_entropy = self._calculate_entropy(self.found_password)
            print(f"\nThe discovered password has approximately {password_entropy:.1f} bits of entropy.")
            print("A strong password should have at least 60 bits of entropy.")
            
    def _calculate_entropy(self, password):
        """Calculate approximate password entropy"""
        # This is a simplified entropy calculation
        char_set_size = 0
        if any(c.islower() for c in password):
            char_set_size += 26
        if any(c.isupper() for c in password):
            char_set_size += 26
        if any(c.isdigit() for c in password):
            char_set_size += 10
        if any(not c.isalnum() for c in password):
            char_set_size += 33  # Common special characters
            
        # Calculate entropy bits
        if char_set_size == 0:  # Empty password
            return 0
            
        import math
        entropy_bits = math.log2(char_set_size) * len(password)
        return entropy_bits

def main():
    parser = argparse.ArgumentParser(description="Educational Password Testing Tool")
    
    # Test mode
    parser.add_argument("--mode", choices=["local", "web"], default="local",
                        help="Testing mode: local hash or web form")
    
    # Local testing options
    parser.add_argument("--hash-file", help="File containing hash to test against")
    
    # Web testing options
    parser.add_argument("--url", help="URL of the login page (localhost only)")
    parser.add_argument("--username", help="Username to test")
    parser.add_argument("--user-field", default="username", 
                        help="HTML field name for username")
    parser.add_argument("--pass-field", default="password",
                        help="HTML field name for password")
    parser.add_argument("--success-text", help="Text found on successful login")
    parser.add_argument("--failure-text", help="Text found on failed login")
    parser.add_argument("--delay", type=float, default=0.5,
                        help="Delay between requests in seconds")
    
    # Common options
    parser.add_argument("--wordlist", help="Path to wordlist file")
    
    args = parser.parse_args()
    
    tester = PasswordTester(args)
    
    if args.mode == "local":
        tester.test_local_password()
    elif args.mode == "web":
        tester.test_web_form()

if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║  Educational Password Testing Tool                        ║
    ║  For cybersecurity educational purposes only              ║
    ║                                                           ║
    ║  Copyright (c) 2025 worksbyahamed                         ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    main()