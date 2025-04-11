import os
import subprocess
import time

# Global variable to store the current process
current_process = None

def separate(song): 
    global current_process
    start_time = time.time()

    # Start the process and store it in the global variable
    current_process = subprocess.Popen(["demucs", "--two-stems=vocals", song])
    
    # Wait for the process to complete
    current_process.wait()
    
    # Reset the current process
    current_process = None
    
    os.chdir("../")

    end_time = time.time()
    duration = end_time - start_time

    print("Song separated successfully!")
    print(f"Time taken: {duration:.2f} seconds")