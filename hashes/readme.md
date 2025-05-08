# Hash Examples for Educational Testing

This directory contains example hash files for educational testing with the password testing tool.

## File Format

Hash files can be in two formats:

1. **Simple format** - Just the hash value:
   ```
   5f4dcc3b5aa765d61d8327deb882cf99
   ```

2. **Extended format** - Algorithm and hash separated by a colon:
   ```
   md5:5f4dcc3b5aa765d61d8327deb882cf99
   ```

## Example Files

### sha256_example.txt
Contains an SHA-256 hash of a common password.

### md5_example.txt
Contains an MD5 hash of a common password.

## Creating Your Own Hash Files

You can create your own hash files for educational testing:

### On Linux/Mac:
```bash
# Create MD5 hash
echo -n "password" | md5sum | awk '{print $1}' > my_md5.txt

# Create SHA-256 hash
echo -n "password" | sha256sum | awk '{print $1}' > my_sha256.txt

# Create algorithm-specified hash
echo "sha256:$(echo -n "password" | sha256sum | awk '{print $1}')" > my_specified_hash.txt
```

### On Windows (PowerShell):
```powershell
# Create MD5 hash
"md5:$((Get-FileHash -Algorithm MD5 -InputStream ([IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes("password")))).Hash.ToLower())" | Out-File -FilePath my_md5.txt

# Create SHA-256 hash
"sha256:$((Get-FileHash -Algorithm SHA256 -InputStream ([IO.MemoryStream]::new([Text.Encoding]::UTF8.GetBytes("password")))).Hash.ToLower())" | Out-File -FilePath my_sha256.txt
```

## Educational Purpose

These examples are provided for educational purposes to demonstrate different hashing algorithms and how password cracking tools match plaintext passwords against stored hashes.

---

Copyright (c) 2025 worksbyahamed  
All rights reserved.
