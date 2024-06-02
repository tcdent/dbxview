import math
import numpy as np
import curses
from . import log, Node

PINK = None
BLUE = None
GREEN = None
YELLOW = None
RED = None
GREEN_REV = None
RED_REV = None

str_ = str
class String(str): pass

class Module:
    color = property(lambda self: self._color)
    def __init__(self, coords, dims, color=None):
        self.x, self.y = coords
        self.width, self.height = dims
        self._color = color
        self.grid = np.full((self.height, self.width), " ", dtype=String)
    def render(self):
        return self.grid

class NodeModule(Module):
    def __init__(self, coords, dims, node, color=None, format: callable=None):
        super().__init__(coords, dims, color)
        self.node = node # can also be str
        self.value = str_(node)
        self.format = format
        if isinstance(node, Node):
            self.node.add_callback(self.update)
    def __repr__(self):
        if isinstance(self.node, Node):
            return f"{self.__class__.__name__}({self.node.name} {self.node.path}, {self.value})"
        return f"{self.__class__.__name__}({self.node})"
    def update(self, node):
        self.value = str_(node)
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
    @property
    def color(self):
        if self.value < 80:
            return BLUE
        if self.value < 90:
            return YELLOW
        return RED
    def render(self):
        self.grid.fill("-")
        if not isinstance(self.value, (int, float)):
            self.value = 0.0
        bar_width = min(math.floor(self.value / 100 * self.width), self.width)
        for i in range(self.height):
            for j in range(max(bar_width, 0)):
                self.grid[i][j] = self.FULL
            if self.value % 100 >= 50:
                self.grid[i][j+i] = self.HALF
        return self.grid
class bool(NodeModule):
    OFF = "○"
    ON = "●"
    OFF_COLOR = RED
    ON_COLOR = GREEN
    @property
    def color(self):
        if self.value == True:
            return self.ON_COLOR
        return self.OFF_COLOR
    def render(self):
        self.grid.fill(" ")
        if self.value == True:
            self.grid[0][0] = self.ON
        else:
            self.grid[0][0] = self.OFF
        return self.grid
class mute(bool):
    OFF = "M"
    ON = "M"
    OFF_COLOR = GREEN_REV
    ON_COLOR = RED_REV

class app:
    def __init__(self, width=80, height=30):
        self.width = width
        self.height = height
        self.modules = []
        self.grid = np.full((self.height, self.width), " ", dtype=String)
        self.prev_grid = np.full((self.height, self.width), " ", dtype=String)
    def init(self, stdscr):
        global PINK, BLUE, GREEN, YELLOW, RED
        curses.curs_set(0)
        curses.start_color()
        stdscr.nodelay(True)
        stdscr.timeout(100)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION) 
        # colors have to be defined after curses init
        curses.init_color(11, round(160*1000/255), round(55*1000/255), round(112*1000/255))
        curses.init_color(12, round(18*1000/255), round(109*1000/255), round(124*1000/255))
        curses.init_color(13, round(72*1000/255), round(124*1000/255), round(18*1000/255))
        curses.init_color(14, round(226*1000/255), round(175*1000/255), round(73*1000/255))
        curses.init_color(15, round(237*1000/255), round(62*1000/255), round(92*1000/255))

        curses.init_pair(1, 11, curses.COLOR_BLACK)
        curses.init_pair(2, 12, curses.COLOR_BLACK)
        curses.init_pair(3, 13, curses.COLOR_BLACK)
        curses.init_pair(4, 14, curses.COLOR_BLACK)
        curses.init_pair(5, 15, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_WHITE, 13)
        curses.init_pair(7, curses.COLOR_WHITE, 15)

        def to_curses_color(value):
            return int(value * 1000 / 255)
        colors = [
            (to_curses_color(192), to_curses_color(128), to_curses_color(255)),
            (to_curses_color(64), to_curses_color(128), to_curses_color(192)),
            (to_curses_color(128), to_curses_color(255), to_curses_color(64)),
            (to_curses_color(255), to_curses_color(192), to_curses_color(64)),
            (to_curses_color(255), to_curses_color(64), to_curses_color(128)),
            (to_curses_color(64), to_curses_color(192), to_curses_color(255)),
            (to_curses_color(128), to_curses_color(64), to_curses_color(255)),
            (to_curses_color(255), to_curses_color(255), to_curses_color(64))
        ]
        
        for i, (r, g, b) in enumerate(colors, start=20):
            curses.init_color(i, r, g, b)
            curses.init_pair(i, i, curses.COLOR_BLACK)
        
            PINK = curses.color_pair(20)
            BLUE = curses.color_pair(21)
            GREEN = curses.color_pair(22)
            YELLOW = curses.color_pair(23)
            RED = curses.color_pair(24)
            GREEN_REV = curses.color_pair(25)
            RED_REV = curses.color_pair(26)

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
            stdscr.addch(y, x, self.grid[y, x], m.color or curses.A_NORMAL)
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
