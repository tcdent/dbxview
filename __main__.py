import os
import math
import time
import re
import socket
import threading
import logging
import textual.app
import textual.widgets

UTF8 = 'utf-8'
APP_PATH = os.path.dirname(os.path.abspath(__file__))
PORT = 19272
TARGET_IP = '192.168.1.234'

log = logging.getLogger("dbx")
log.setLevel(logging.DEBUG)
log.addHandler(logging.FileHandler(os.path.join(APP_PATH, 'dbx.log')))
log.debug('-'*80)

class Node:
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.children = {}
        self.parent = None
        self.callbacks = []
    def __getitem__(self, key):
        if not key in self.children:
            self.children[key] = Node(key)
            self.children[key].parent = self
        return self.children[key]
    def __setitem__(self, key, value):
        if not key in self.children:
            self.children[key] = Node(key)
            self.children[key].parent = self
        self.children[key] = value
    def __contains__(self, key):
        return key in self.children
    def __repr__(self):
        return f"Node({self.path}, {self.data}, {self.children})"
    def __str__(self):
        """Used in the public user interface to display the contents of the node."""
        return str(self.data)
    def add_callback(self, callback):
        self.callbacks.append(callback)
    def set_data(self, data):
        self.data = data
        for callback in self.callbacks:
            callback(self)
    @property
    def path(self):
        path, node = [self.name], self
        while node.parent:
            path.append(node.parent.name)
            node = node.parent
        path.reverse()
        return '\\'.join(path)
    @classmethod
    def parse(cls, path: str, data):
        global N
        node, keys = N, path.split('\\')[2:]
        for key in keys:
            node = node.children[key]
        node.set_data(data)
        return node

N = Node('\\') # localstore

def send_message(sock: socket.socket, message: str):
    sock.sendall(message.encode(UTF8) + b'\n')
def asyncget(sock: socket.socket, node: Node):
    send_message(sock, f"asyncget {node.path}")
def sub(sock: socket.socket, node: Node):
    send_message(sock, f"sub {node.path}")

Q = [
    (send_message, "connect administrator administrator"),
    (sub, N['Preset']['InputMeters']['SV']['LeftInput']),
    (sub, N['Preset']['InputMeters']['SV']['RightInput']), 
    (sub, N['Preset']['InputMeters']['SV']['LeftInput']),
    (sub, N['Preset']['InputMeters']['SV']['RightInput']), 
    (sub, N['Preset']['OutputMeters']['SV']['HighLeftOutput']), 
    (sub, N['Preset']['OutputMeters']['SV']['HighRightOutput']),
    (sub, N['Preset']['OutputMeters']['SV']['MidLeftOutput']),
    (sub, N['Preset']['OutputMeters']['SV']['MidRightOutput']),
    (sub, N['Preset']['OutputMeters']['SV']['LowLeftOutput']),
    (sub, N['Preset']['OutputMeters']['SV']['LowRightOutput']),
]

def listener(sock):
    buffer = b''
    def receive(sock: socket.socket):
        nonlocal buffer
        while True:
            buffer += sock.recv(1024)
            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                yield line.decode(UTF8)
    def parse(data):
        # asyncget "\\Preset\InputMeters\SV\LeftInput" "0.0 dB"
        try:
            cmd, path, value = [x.strip() for x in data.split('"') if x.strip()]
            node = Node.parse(path, value)
        except (ValueError, IndexError):
            log.info(f'ignored message: "{data.strip()}"')
    def send_q(sock):
        if not Q: return
        tx_cmd = Q.pop(0)
        tx_cmd[0](sock, tx_cmd[1])
    try:
        for data in receive(sock):
            parse(data)
            send_q(sock)
    except Exception as e:
        log.exception(e)
    finally:
        sock.close()

def setup_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TARGET_IP, PORT)) # TODO timeout
    if sock: log.info(f"Connected to {TARGET_IP}:{PORT}")
    thread = threading.Thread(target=listener, args=(sock,))
    thread.daemon = True
    thread.start()
    return sock, thread

class NodeDisplay(textual.widgets.Static):
    def __init__(self, node: Node):
        super().__init__()
        self.node = node
        self.node.add_callback(self.update)
    def update(self, node: Node):
        super().update(str(node))
class Meter(textual.widgets.ProgressBar):
    def __init__(self, node: Node):
        self.node = node
        self.node.add_callback(self._update)
        super().__init__()
    def _update(self, node: Node):
        value = float(str(node)[:-2])
        perc = round((value + 120) / 120 * 100)
        self.update(total=100, progress=perc)
class Channel(textual.widgets.Static):
    def __init__(self, title: str, node: Node):
        super().__init__()
        self.title = title
        self.node = node
    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Static(self.title)
        self.number_display = NodeDisplay(self.node)
        self.meter_display = Meter(self.node)
        yield self.number_display
        yield self.meter_display

class App(textual.app.App):
    CSS = """
Screen {
    layout: grid;
    grid-size: 4;
    grid-columns: 1fr;
    width: 80;
    height: 80;
}
Vertical {
    height: 30;
}
Channel {
    height: 3;
}
    """
    def run(self):
        super().run()
    def on_mount(self):
        self.sock, self.listener = setup_tcp()
    def compose(self) -> textual.app.ComposeResult:
        yield textual.widgets.Header()
        yield textual.widgets.Footer()
        with textual.containers.Vertical():
            yield Channel("Left Input", N['Preset']['InputMeters']['SV']['LeftInput'])
            yield Channel("Left High Output", N['Preset']['OutputMeters']['SV']['HighLeftOutput'])
            yield Channel("Left Mid Output", N['Preset']['OutputMeters']['SV']['MidLeftOutput'])
            yield Channel("Left Low Output", N['Preset']['OutputMeters']['SV']['LowLeftOutput'])
        
        with textual.containers.Vertical():
            yield Channel("Right Input", N['Preset']['InputMeters']['SV']['RightInput'])
            yield Channel("Right High Output", N['Preset']['OutputMeters']['SV']['HighRightOutput'])
            yield Channel("Right Mid Output", N['Preset']['OutputMeters']['SV']['MidRightOutput'])
            yield Channel("Right Low Output", N['Preset']['OutputMeters']['SV']['LowRightOutput'])
        
        self.log_view = textual.widgets.Static("Log")
        yield self.log_view

if __name__ == "__main__":
    App().run()