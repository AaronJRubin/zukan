import os
import webbrowser
import subprocess

os.chdir("site/static")
subprocess.Popen(["python", "-m", "SimpleHTTPServer"])
webbrowser.open("localhost:8000/home.html")

