import http.server, ssl, os,re

import re._constants;
host = 'localhost';
port = 4443;
httpd = http.server.HTTPServer((host, port), http.server.SimpleHTTPRequestHandler);
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);
ssl_context.load_cert_chain(certfile='localhost.pem', keyfile='localhost-key.pem');
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


print(f'Server running at https://{host}:{port}/');
httpd.serve_forever()