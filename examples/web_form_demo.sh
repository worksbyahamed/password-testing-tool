#!/bin/bash

# Educational Password Testing Tool - Web Form Demo
# Copyright (c) 2025 worksbyahamed

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}====================================${NC}"
echo -e "${YELLOW}   Web Form Testing Demonstration   ${NC}"
echo -e "${YELLOW}====================================${NC}"
echo

# Check if the password testing tool exists
if [ ! -f "../password_tester.py" ]; then
    echo "Error: password_tester.py not found!"
    echo "Make sure you're running this script from the examples directory."
    exit 1
fi

# Make sure we have the wordlist
if [ ! -f "../wordlists/default_creds.txt" ]; then
    echo "Error: wordlist not found!"
    echo "Make sure the wordlists directory is properly set up."
    exit 1
fi

# Check if a local web server is running
echo -e "${BLUE}Checking for local web server...${NC}"
if curl -s http://localhost:8000 > /dev/null; then
    echo "Local web server detected at http://localhost:8000"
else
    echo -e "${RED}No web server detected at http://localhost:8000${NC}"
    echo
    echo "This demo requires a local web server running on port 8000 with a login form."
    echo "You can start a simple Python web server for testing:"
    echo
    echo "1. Create a simple HTML login form in a file named index.html:"
    echo
    echo -e "${BLUE}cat > index.html << 'EOF'${NC}
<!DOCTYPE html>
<html>
<head>
    <title>Login Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .login-form { max-width: 300px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; }
        input { width: 100%; padding: 8px; margin: 8px 0; box-sizing: border-box; }
        button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-form">
        <h2>Login</h2>
        <form id="login-form" method="post">
            <div>
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required>
            </div>
            <div>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
            </div>
            <div>
                <button type="submit">Login</button>
            </div>
            <div id="message"></div>
        </form>
    </div>
    
    <script>
        document.getElementById('login-form').onsubmit = function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const messageEl = document.getElementById('message');
            
            // For demo purposes, check if username/password match any of these credentials
            const validCreds = [
                {user: 'admin', pass: 'admin'},
                {user: 'user', pass: 'password'}
            ];
            
            const isValid = validCreds.some(cred => 
                cred.user === username && cred.pass === password);
                
            if (isValid) {
                messageEl.innerHTML = '<p style="color: green;">Login successful!</p>';
            } else {
                messageEl.innerHTML = '<p style="color: red;">Invalid username or password.</p>';
            }
        };
    </script>
</body>
</html>
${NC}EOF"
    echo
    echo "2. Start a Python web server:"
    echo "   python3 -m http.server"
    echo
    echo "3. Then run this demo script again in another terminal."
    exit 1
fi

echo
echo -e "${GREEN}Running web form test...${NC}"
echo "This demo will test a login form running on localhost:8000"
echo "using the default_creds.txt wordlist."
echo
echo "Command:"
echo "python3 ../password_tester.py --mode web --url http://localhost:8000 \\"
echo "                     --username admin \\"
echo "                     --user-field username \\"
echo "                     --pass-field password \\"
echo "                     --success-text \"Login successful\" \\"
echo "                     --failure-text \"Invalid username\" \\"
echo "                     --wordlist ../wordlists/default_creds.txt \\"
echo "                     --delay 0.5"
echo
echo "Press Enter to continue..."
read

python3 ../password_tester.py --mode web --url http://localhost:8000 \
                     --username admin \
                     --user-field username \
                     --pass-field password \
                     --success-text "Login successful" \
                     --failure-text "Invalid username" \
                     --wordlist ../wordlists/default_creds.txt \
                     --delay 0.5

echo
echo -e "${GREEN}Demo completed.${NC}"
echo
echo "Note: This demo only works with a properly configured local web server."
echo "Remember that testing should only be performed on systems you own or"
echo "have explicit permission to test."
echo
echo "Copyright (c) 2025 worksbyahamed"
