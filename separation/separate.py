import os
import subprocess

def separate(song): 
    subprocess.run(["demucs", "--two-stems=vocals", song])
    os.chdir("../")

    print("Song separated successfully!")
