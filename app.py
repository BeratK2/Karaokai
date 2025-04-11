from flask import Flask, render_template, jsonify, request, send_from_directory, render_template_string
from separation import separate
import os
import stat
import shutil


app = Flask(__name__)

SEPARATION_FOLDER = "./separated/htdemucs"

# --- Index HTML ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Separate instruments and vocals ---
@app.route('/separate', methods=['POST', 'GET'])
def run_separate():
    os.chdir(os.getcwd() + "/separation")

    # --- Remove files from song_input and separation folder --- 
    for f in os.listdir("./song_input"):
        file_path = os.path.join("./song_input", f)
        try:
            os.chmod(file_path, stat.S_IWRITE)
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
    
    for f in os.listdir(SEPARATION_FOLDER):
        file_path = os.path.join(SEPARATION_FOLDER, f)
        try:
            os.chmod(file_path, stat.S_IWRITE)
            shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
    
    # --- Save file that was input to song_input folder --- 
    if 'file' not in request.files:
        return "No file provided", 400

    file = request.files['file']
    if file.filename == '':
        return "No file selected", 400
    
    file_name, _ = os.path.splitext(file.filename)

    # Ensure the filename is safe (sanitize if needed)
    file_path = os.path.join("./song_input", file.filename)
    
    # Save the file
    try:
        file.save(file_path)
    except Exception as e:
        return f"Error saving file: {e}", 500

    # --- Run separate with input file passed in --- 
    separate.separate(file_path)

    # --- Get list of separated files ---
    output_folder = os.path.join("./separation/separated/htdemucs" + "/" + file_name)
    separated_files = os.listdir(output_folder)

    print(os.getcwd())

    # --- Generate HTML Response with Download Buttons ---
    return render_template_string('''
        <html>
        <head>
            <title>Download Separated Files</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
        </head>
        <body class="container mt-5">
            <h2 class="mb-3">Separation Complete!</h2>
            <p>Original File: <strong>{{ filename }}</strong></p>
            <p>Your files have been separated. Click below to download them:</p>
            <ul class="list-group">
                {% for file in files %}
                    <li class="list-group-item">
                        <a href="{{ url_for('download_file', folder=filename, filename=file) }}" class="btn btn-primary" download>{{ file }}</a>
                    </li>
                {% endfor %}
            </ul>
        </body>
        </html>
    ''', filename=file_name, files=separated_files)


# --- Cancel the operation and reset ---
@app.route('/cancel', methods=['POST'])
def cancel_operation():
    # Import the module and modify it directly
    from separation import separate
    
    # Since 'cancel_separation' doesn't exist yet, we need to add it
    # First, check if a process is running
    if hasattr(separate, 'current_process') and separate.current_process is not None:
        try:
            # Terminate the process
            separate.current_process.terminate()
            
            # Give it a moment to terminate gracefully
            import time
            time.sleep(0.5)
            
            # If it's still running, force kill it
            if separate.current_process.poll() is None:
                if os.name == 'nt':  # Windows
                    subprocess.run(['taskkill', '/F', '/T', '/PID', str(separate.current_process.pid)])
                else:  # Unix-like
                    import signal
                    os.kill(separate.current_process.pid, signal.SIGKILL)
            
            # Reset the current process
            separate.current_process = None
            canceled = True
            
        except Exception as e:
            print(f"Error canceling process: {e}")
            canceled = False
    else:
        print("No separation process is currently running")
        canceled = False
    
    # Clear song_input and separation folders
    base_dir = os.path.abspath(os.path.dirname(__file__))
    input_dir = os.path.join(base_dir, "separation", "song_input")
    separation_dir = os.path.join(base_dir, "separation", "separated", "htdemucs")
    
    # Clean up input directory
    for f in os.listdir(input_dir):
        file_path = os.path.join(input_dir, f)
        try:
            os.chmod(file_path, stat.S_IWRITE)
            os.remove(file_path)
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
    
    # Clean up separation directory
    for f in os.listdir(separation_dir):
        file_path = os.path.join(separation_dir, f)
        try:
            os.chmod(file_path, stat.S_IWRITE)
            shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error removing {file_path}: {e}")
    
    # Return a JSON response for better AJAX handling
    if canceled:
        return jsonify({"status": "success", "message": "Operation canceled successfully"})
    else:
        return jsonify({"status": "info", "message": "No operation to cancel"})


@app.route('/download/<filename>/<folder>')
def download_file(filename, folder):
    download_path = os.path.join("./separation/separated/htdemucs", folder)
    return send_from_directory(download_path, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)