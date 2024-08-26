from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__)

def run_sherlock(usernames, options):
    command = f"sherlock {usernames} " + " ".join(options)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    usernames = request.form['usernames']
    options = []

    if request.form.get('verbose'):
        options.append("--verbose")
    
    if request.form.get('csv'):
        options.append("--csv")
    
    if request.form.get('xlsx'):
        options.append("--xlsx")
    
    if request.form.get('output'):
        filename = request.form['filename']
        options.append(f"--output {filename}")
    
    if request.form.get('timeout'):
        timeout_value = request.form['timeout_value']
        options.append(f"--timeout {timeout_value}")
    
    if request.form.get('print_all'):
        options.append("--print-all")
    
    if request.form.get('browse'):
        options.append("--browse")
    
    output, error = run_sherlock(usernames, options)
    
    return render_template('result.html', output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
