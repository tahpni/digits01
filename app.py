from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_intro', methods=['POST'])
def execute_intro():
    # Run the intro maker script
    result = subprocess.run(['python', 'intromaker.py'], capture_output=True, text=True)
    return jsonify({'output': result.stdout})

@app.route('/execute_draw', methods=['POST'])
def execute_draw():
    # Run the draw script
    result = subprocess.run(['python', 'draw.py'], capture_output=True, text=True)
    return jsonify({'output': result.stdout})

if __name__ == '__main__':
    app.run(debug=True)
