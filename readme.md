# Educational Password Testing Tool

A cybersecurity educational tool for learning about password security, authentication testing, and security principles.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.6%2B-green)
![License](https://img.shields.io/badge/license-Custom-orange)

## Overview

This tool demonstrates various password security concepts for educational purposes in cybersecurity studies. It provides hands-on experience with password testing techniques while emphasizing ethical security practices.

**Important**: This tool is designed for educational purposes only and should be used only on systems you own or have explicit permission to test.

## Features

- **Multiple Testing Modes**:
  - Local password hash testing
  - Web form testing (restricted to localhost)
  
- **Security Education**:
  - Password entropy calculation
  - Performance metrics
  - Educational findings on password security

- **Ethical Controls**:
  - Explicit consent confirmation
  - Restricted testing domains
  - Rate limiting to prevent service disruption
  - Comprehensive logging

## Installation

```bash
# Clone the repository
git clone https://github.com/worksbyahamed/password-testing-tool.git
cd password-testing-tool

# Make the script executable
chmod +x password_tester.py

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Local Hash Testing

Test passwords against a specified hash:

```bash
./password_tester.py --mode local --wordlist wordlists/common_passwords.txt
```

With a specific hash file:

```bash
./password_tester.py --mode local --wordlist wordlists/common_passwords.txt --hash-file target_hash.txt
```

### Web Form Testing

Test against a local web application (localhost only for security):

```bash
./password_tester.py --mode web --url http://localhost:8000/login \
                    --username admin \
                    --user-field username \
                    --pass-field password \
                    --success-text "Welcome" \
                    --failure-text "Invalid" \
                    --wordlist wordlists/common_passwords.txt
```

## Options

| Option | Description |
|--------|-------------|
| `--mode` | Testing mode: `local` or `web` |
| `--wordlist` | Path to wordlist file |
| `--hash-file` | File containing hash to test against |
| `--url` | URL of the login page (localhost only) |
| `--username` | Username to test |
| `--user-field` | HTML field name for username |
| `--pass-field` | HTML field name for password |
| `--success-text` | Text found on successful login |
| `--failure-text` | Text found on failed login |
| `--delay` | Delay between requests in seconds (default: 0.5) |

## Educational Value

This tool helps cybersecurity students understand:

1. How password complexity affects security
2. The importance of rate limiting and account lockout
3. The value of multi-factor authentication
4. Basic principles of ethical security testing
5. Password entropy and strength assessment

## Creating Wordlists

For educational testing, you can create simple wordlists:

```bash
# Example of creating a small custom wordlist
echo -e "password\n123456\nqwerty\nadmin\nwelcome\nsecret" > wordlists/custom.txt
```

Several open-source wordlists are available for educational purposes.

## Contributing

Contributions that enhance the educational value of this tool are welcome. Please ensure all contributions maintain the ethical focus of the project.

## License

Copyright (c) 2025 worksbyahamed  
All rights reserved.

---

**Disclaimer**: This tool is for educational purposes only. Unauthorized testing of systems is illegal and unethical. Always obtain proper authorization before security testing.
