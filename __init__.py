import os
import socket
import threading
import logging

UTF8 = 'utf-8'
APP_PATH = os.path.dirname(os.path.abspath(__file__))
PORT = 19272
TARGET_IP = '192.168.1.234'

log = logging.getLogger('dbxview')
log.setLevel(logging.DEBUG)
log.addHandler(logging.FileHandler(os.path.join(APP_PATH, 'dbxview.log')))

UPDATE_COMMANDS = ('set', 'get', 'subr', 'setr',)
LOG_COMMANDS = ('sub', 'unsub', )
class Node:
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.children = {}
        self.parent = None
        self.callbacks = []
        self.formatters = []
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
        return str(self.data) if self.data else str(0)
    def add_callback(self, callback):
        self.callbacks.append(callback)
    def remove_callback(self, callback):
        self.callbacks.remove(callback)
    def set_data(self, data):
        self.data = data
        for callback in self.callbacks:
            callback(self)
    def save(self):
        global Q
        log.info(f'set "{self.path}" "{self.data}"')
        Q.append(('set', f'{self.path}" "{self.data}'))
    @property
    def path(self):
        node, path = self, [self.name]
        while node.parent:
            path.append(node.parent.name)
            node = node.parent
        path.reverse()
        return '\\'.join(path) + '\\'
    @classmethod
    def parse_raw(cls, data) -> 'Node':
        try:
            # asyncget "\\Preset\InputMeters\SV\LeftInput" "0.0 dB"
            cmd, path, value = [x.strip() for x in data.split('"') if x.strip()]
            if cmd in LOG_COMMANDS:
                log.info(f'{cmd} "{path}" "{value}"')
            if cmd in UPDATE_COMMANDS:
                return cls.parse(path, value)
        except (ValueError, IndexError) as e:
            log.info(f"ignored: {data}")
    @classmethod
    def parse(cls, path: str, data) -> 'Node':
        global N
        node, keys = N, path.split('\\')[2:]
        for key in keys:
            node = node.children[key]
        node.set_data(data)
        return node

N = Node('\\') # localstore
Q = [ # outgoing message queue
    ('raw', "connect administrator administrator"), 
]

