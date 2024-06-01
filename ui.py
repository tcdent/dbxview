import math
import numpy as np
import curses
from . import log, Node

PINK = None
BLUE = None

class String(str): pass

class Module:
    def __init__(self, coords, dims, color=None):
        self.x, self.y = coords
        self.width, self.height = dims
        self.color = color or curses.COLOR_WHITE
        self.grid = np.full((self.height, self.width), " ", dtype=String)
    def render(self):
        return self.grid

class NodeModule(Module):
    def __init__(self, coords, dims, node, color=None, format: callable=None):
        super().__init__(coords, dims, color)
        self.node = node # can also be str
        self.value = String(node)
        self.format = format
        if isinstance(node, Node):
            self.node.add_callback(self.update)
    def __repr__(self):
        if isinstance(self.node, Node):
            return f"{self.__class__.__name__}({self.node.name} {self.node.path}, {self.value})"
        return f"{self.__class__.__name__}({self.node})"
    def update(self, node):
        self.value = String(node)
        if self.format:
            self.value = self.format(self.value)

class box(Module):
    H, V, TL, TR, BL, BR =  "─", "│", "┌", "┐", "└", "┘"
    def __init__(self, coords, dims, modules=None, color=None):
        super().__init__(coords, dims, color)
        self.modules = modules or []
    def append(self, module):
        self.modules.append(module)
    def render_module(self, module):
        grid = module.render()
        for y, x in zip(*np.where(grid)):
            if 0 <= module.y + y < self.height and 0 <= module.x + x < self.width:
                self.grid[module.y + y, module.x + x] = grid[y, x]
    def render(self):
        self.grid.fill(" ")
        w, h = self.width - 1, self.height - 1
        for x in range(1, w):
            self.grid[0, x] = self.H
            self.grid[h, x] = self.H
        for y in range(1, h):
            self.grid[y, 0] = self.V
            self.grid[y, w] = self.V
        self.grid[0, 0] = self.TL
        self.grid[0, w] = self.TR
        self.grid[h, 0] = self.BL
        self.grid[h, w] = self.BR
        for module in self.modules:
            self.render_module(module)
        return self.grid
    def lookup(self, y, x):
        for m in self.modules:
            if m.y <= y < m.y + m.height and m.x <= x < m.x + m.width:
                return m
        return self

class str(NodeModule):
    def render(self):
        self.grid.fill(" ")
        lines = self.value.split('\n')
        for i, line in enumerate(lines):
            if i < self.height:
                for j, char in enumerate(line):
                    if j < self.width:
                        self.grid[i][j] = char
        return self.grid

class title(str):
    def render(self):
        grid = super().render()
        under = "═" * len(self.value)
        grid[0] = [c for c in self.value.center(self.width)]
        grid[1] = [c for c in under.center(self.width)]
        return grid

class bar(NodeModule):
    FULL = "█"
    HALF = "▌"
    def update(self, node: Node):
        value = float(String(node)[:-2]) or 0
        self.value = round((value + 120) / 120 * 100)
    def render(self):
        self.grid.fill("-")
        if not isinstance(self.value, int):
            self.value = 0
        bar_width = min(math.floor(self.value / 100 * self.width), self.width)
        for i in range(self.height):
            for j in range(max(bar_width, 0)):
                self.grid[i][j] = self.FULL
            if self.value % 100 >= 50:
                self.grid[i][j+i] = self.HALF
        return self.grid

class app:
    def __init__(self, width=80, height=30):
        self.width = width
        self.height = height
        self.modules = []
        self.grid = np.full((self.height, self.width), " ", dtype=String)
        self.prev_grid = np.full((self.height, self.width), " ", dtype=String)
    def init(self, stdscr):
        global PINK, BLUE

        curses.curs_set(0)
        curses.start_color()
        stdscr.nodelay(True)
        stdscr.timeout(100)
        curses.mousemask(curses.ALL_MOUSE_EVENTS)

        curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        PINK = curses.color_pair(1)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        BLUE = curses.color_pair(2)
    def append(self, module):
        self.modules.append(module)
    def render(self):
        self.grid.fill(" ")
        for m in self.modules:
            grid = m.render()
            # TODO compare `grid` to `self.grid` but module coords are relative
            for y, x in zip(*np.where(grid)):
                if 0 <= m.y + y < self.height and 0 <= m.x + x < self.width:
                    self.grid[m.y + y, m.x + x] = grid[y, x]
    def display(self, stdscr):
        self.render()
        for y, x in zip(*np.where(self.grid != self.prev_grid)):
            m = self.lookup(y, x) # :/
            stdscr.addch(y, x, self.grid[y, x], m.color)
        stdscr.refresh()
        np.copyto(self.prev_grid, self.grid)
    def lookup(self, y, x):
        for m in self.modules:
            if m.y <= y < m.y + m.height and m.x <= x < m.x + m.width:
                if hasattr(m, 'lookup'):
                    return m.lookup(y - m.y, x - m.x)
                return m
        return None
    def click(self, y, x):
        module = self.lookup(y, x)
        if module:
            log.info(f"click: {module}")
