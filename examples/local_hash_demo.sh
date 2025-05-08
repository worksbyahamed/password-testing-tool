#!/bin/bash

# Educational Password Testing Tool - Local Hash Demo
# Copyright (c) 2025 worksbyahamed

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}====================================${NC}"
echo -e "${YELLOW}  Local Hash Testing Demonstration  ${NC}"
echo -e "${YELLOW}====================================${NC}"
echo

# Check if the password testing tool exists
if [ ! -f "../password_tester.py" ]; then
    echo "Error: password_tester.py not found!"
    echo "Make sure you're running this script from the examples directory."
    exit 1
fi

# Make sure we have the wordlist
if [ ! -f "../wordlists/common_passwords.txt" ]; then
    echo "Error: wordlist not found!"
    echo "Make sure the wordlists directory is properly set up."
    exit 1
fi

# Check if the hash file exists
if [ ! -f "../hashes/md5_example.txt" ]; then
    echo "Error: hash file not found!"
    echo "Make sure the hashes directory is properly set up."
    exit 1
fi

# Run the tool with the MD5 example hash
echo -e "${GREEN}Testing MD5 hash example...${NC}"
echo "This demo will use the md5_example.txt hash and common_passwords.txt wordlist."
echo
echo "Command:"
echo "python3 ../password_tester.py --mode local --wordlist ../wordlists/common_passwords.txt --hash-file ../hashes/md5_example.txt"
echo
echo "Press Enter to continue..."
read

python3 ../password_tester.py --mode local --wordlist ../wordlists/common_passwords.txt --hash-file ../hashes/md5_example.txt

echo
echo -e "${GREEN}Demo completed.${NC}"
echo
echo "To try with a different hash, modify the command above."
echo "For example, to test the SHA-256 example:"
echo "python3 ../password_tester.py --mode local --wordlist ../wordlists/common_passwords.txt --hash-file ../hashes/sha256_example.txt"
echo
echo "Copyright (c) 2025 worksbyahamed"
