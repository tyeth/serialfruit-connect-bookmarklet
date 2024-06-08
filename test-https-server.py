import http.server, ssl, os,re, signal, sys
import re._constants;

# ssl_args = {'certfile':'127.0.0.1.pem', 'keyfile':'127.0.0.1-key.pem'}
# host = '127.0.0.1';
ssl_args = {'certfile':'localhost.pem', 'keyfile':'localhost-key.pem'}
host = 'localhost';

port = 4443;

def signal_handler(signal, frame):
    print('\nShutting down the server...')
    httpd.server_close()
    sys.exit(0)

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Access-Control-Allow-Credentials', 'false')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()


httpd = http.server.ThreadingHTTPServer((host, port), CORSRequestHandler);
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);
ssl_context.load_cert_chain(**ssl_args);
httpd.socket = ssl_context.wrap_socket(httpd.socket, server_side=True);
# load all files from src folder and copy into /localhost-src folder with replacements for jsdelivr lines
print('Loading files from src folder and copying into localhost folder with replacements for jsdelivr lines');
if not os.path.exists('localhost-src'):
    os.makedirs('localhost-src');
for file in os.listdir('src'):
    with open('src/' + file, 'r') as f:
        # replace this line using a regex as version can vary even being main instead of a version:
        # https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@v0.0.62/src goes to https://{host}:{port}/localhost-src
        regex_to_match = r'https://cdn.jsdelivr.net/gh/tyeth/serialfruit-connect@.*?/src';
        localhost_to_substitute = f'https://{host}:{port}/localhost-src';
        content = re.sub(regex_to_match, localhost_to_substitute, f.read(),count=0 , flags=re.MULTILINE | re.IGNORECASE | re.DOTALL);
        with open('localhost-src/' + file, 'w',encoding='utf-8') as f:
            f.write(content);


# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)

print(f'Server running at https://{host}:{port}/');
httpd.serve_forever()
