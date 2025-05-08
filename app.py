from flask import Flask, render_template_string, request

app = Flask(__name__)

# Very simple template for demonstration
login_html = '''
<!doctype html>
<title>Login</title>
<h2>Login Form</h2>
<form method="POST">
  <label>Username:</label>
  <input type="text" name="username" required><br>
  <label>Password:</label>
  <input type="password" name="password" required><br>
  <input type="submit" value="Login">
</form>
{% if message %}
  <p>{{ message }}</p>
{% endif %}
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # For demo: username=admin, password=password
        if username == 'admin' and password == 'password':
            message = 'Welcome'
        else:
            message = 'Invalid'
    return render_template_string(login_html, message=message)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
