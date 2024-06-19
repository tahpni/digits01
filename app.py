from flask import Flask, render_template, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute_draw', methods=['POST'])
def execute_draw():
    # Run the draw script
    result = subprocess.run(['python', 'draw.py'])
    return jsonify({'output': result.stdout})

@app.route('/executeneural', sub.run(“./neuraldigits.cpp”, shell=True)

if __name__ == '__main__':
    app.run(debug=True)
