from flask import Flask, render_template, jsonify, send_file, request
import json

app = Flask(__name__)

def load_commands(file_name):
    """Load commands from the specified JSON file"""
    try:
        with open(f'data/{file_name}', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Load commands from JSON files
WINDOWS_COMMANDS = load_commands('commands.json')
LINUX_COMMANDS = load_commands('linux_commands.json')

@app.route('/')
def index():
    return render_template('main_menu.html')

@app.route('/windows')
def windows():
    return render_template('commands.html', commands=WINDOWS_COMMANDS, os_type="Windows")

@app.route('/linux')
def linux():
    return render_template('commands.html', commands=LINUX_COMMANDS, os_type="Linux")

@app.route('/api/commands/<os_type>')
def get_commands(os_type):
    if os_type.lower() == 'windows':
        return jsonify(WINDOWS_COMMANDS)
    elif os_type.lower() == 'linux':
        return jsonify(LINUX_COMMANDS)
    return jsonify([])

@app.route('/api/commands/<os_type>/search')
def search_commands(os_type):
    query = request.args.get('q', '').lower()
    commands = WINDOWS_COMMANDS if os_type.lower() == 'windows' else LINUX_COMMANDS
    filtered_commands = [
        cmd for cmd in commands
        if query in cmd['command'].lower() or query in cmd['description'].lower()
    ]
    return jsonify(filtered_commands)

@app.route('/api/download/<os_type>')
def download_commands(os_type):
    """Download the commands as a JSON file"""
    filename = 'commands.json' if os_type.lower() == 'windows' else 'linux_commands.json'
    return send_file(f'data/{filename}',
                    mimetype='application/json',
                    as_attachment=True,
                    download_name=f'{os_type}_commands.json')

if __name__ == '__main__':
    app.run(debug=True)

