import socket
import threading
from . import log, UTF8, TARGET_IP, PORT, Q, Node

class Listener:
    def __init__(self, sock):
        self.sock = sock
        self.buffer = b''
    def receive(self):
        while True:
            self.buffer += self.sock.recv(1024)
            while b'\n' in self.buffer:
                line, self.buffer = self.buffer.split(b'\n', 1)
                yield line.decode(UTF8)
    def parse(self, data):
        # asyncget "\\Preset\InputMeters\SV\LeftInput" "0.0 dB"
        try:
            cmd, path, value = [x.strip() for x in data.split('"') if x.strip()]
            node = Node.parse(path, value)
        except (ValueError, IndexError):
            log.info(f'ignored message: "{data.strip()}"')
    def send_q(self):
        if not Q: return
        cmd(self.sock, *Q.pop(0))
    def run(self):
        try:
            for data in self.receive():
                self.parse(data)
                self.send_q()
        except Exception as e:
            log.exception(e)
        finally:
            self.sock.close()

def setup_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TARGET_IP, PORT)) # TODO timeout
    if sock: log.info(f"Connected to {TARGET_IP}:{PORT}")
    thread = threading.Thread(target=lambda sock: Listener(sock).run(), args=(sock,))
    thread.daemon = True
    thread.start()
    return sock, thread
def send_message(sock: socket.socket, message: str):
    #log.debug(f"send_message: {message}")
    sock.sendall(message.encode(UTF8) + b'\n')
def cmd(sock, method, message):
    if method == 'raw': # :/
        return send_message(sock, message)
    return send_message(sock, f"{method} \"{message}\"")