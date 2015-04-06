# This script will be packacged into a standalone Windows executable, and, after running "rake compile", the contents 
# of this entire project directory, including that executable, will be burned to a USB to produce a product that
# can be handed over to the client and executed without any command line knowledge or dependencies installed
import os
import webbrowser
from time import sleep
import thread
import SimpleHTTPServer
import SocketServer

os.chdir("site/static")

PORT = 8000

Handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)

thread.start_new_thread(httpd.serve_forever, ())
webbrowser.open("localhost:8000/home.html")
sleep(15) # enough time for appcache to cache everything
httpd.shutdown()
