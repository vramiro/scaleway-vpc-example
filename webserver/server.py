from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json

SERVER_HOST = 'localhost';
SERVER_PORT = 8080;
QOTD_SERVER = 'localhost';
QOTD_PORT = 4242;

html_stub = """
<html>
  <head>
   <title>Quote of the day</title>
   <style>
      .myButton {
        box-shadow:inset 0px 1px 0px 0px #bbdaf7;
        background:linear-gradient(to bottom, #79bbff 5%, #378de5 100%);
        background-color:#79bbff;
        border-radius:6px;
        border:1px solid #84bbf3;
        display:inline-block;
        cursor:pointer;
        color:#ffffff;
        font-family:Arial;
        font-size:15px;
        font-weight:bold;
        padding:6px 24px;
        text-decoration:none;
        text-shadow:0px 1px 0px #528ecc;
      }
      .myButton:hover {
        background:linear-gradient(to bottom, #378de5 5%, #79bbff 100%);
        background-color:#378de5;
      }
      .myButton:active {
        position:relative;
        top:1px;
      }
    </style>
    <script>
      function qotd(){
        fetch('/qotd')
          .then(response => response.json())
          .then(jsonData => displayQOTD(jsonData))
        }

      function displayQOTD(data){
        console.log(data);
        document.getElementById("quote").innerText = data.quote;
        document.getElementById("author").innerText = data.author;
      }
    </script>
  </head>
  <body>
   <div align="center">
    <h1>Quote of the Day</h1>
    <a onclick="qotd()" class="myButton">next</a>
    <div>
      <p><h3 id='quote'>...</h3></p>
      <p><h4 id='author'></h4></p>
    </div>
   </div>
  </body>
</html>
"""

class QOTDServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/qotd':
            self.do_qotd()
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(html_stub, "utf-8"))

    def do_qotd(self):
        # Connect to the Database server
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((QOTD_SERVER, QOTD_PORT));

        # Receive data, parse and transform to JSON
        s = client.recv(1024).decode('utf-8').split('|');
        json_data = json.dumps({'id': s[0], 'quote': s[1], 'author': s[2]}).encode('utf-8')
        print(json_data)

        # Send JSON response
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json_data))

if __name__ == "__main__":
    s = HTTPServer((SERVER_HOST, SERVER_PORT), QOTDServer)
    print("Server started http://%s:%s" % (SERVER_HOST, SERVER_PORT))
    s.serve_forever()
