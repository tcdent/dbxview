import math
import curses
from . import log, Node

class rgb:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def to_curses_color(self):
        def f(value): return int(value * 1000 / 255)
        return f(self.r), f(self.g), f(self.b)

curses.initscr()
curses.start_color()
curses.init_color(11, *rgb(160, 55, 112).to_curses_color())
curses.init_color(12, *rgb(18, 109, 124).to_curses_color())
curses.init_color(13, *rgb(72, 124, 18).to_curses_color())
curses.init_color(14, *rgb(226, 175, 73).to_curses_color())
curses.init_color(15, *rgb(237, 62, 92).to_curses_color())

curses.init_pair(1, 11, curses.COLOR_BLACK)
curses.init_pair(2, 12, curses.COLOR_BLACK)
curses.init_pair(3, 13, curses.COLOR_BLACK)
curses.init_pair(4, 14, curses.COLOR_BLACK)
curses.init_pair(5, 15, curses.COLOR_BLACK)
curses.init_pair(6, curses.COLOR_WHITE, 13)
curses.init_pair(7, curses.COLOR_WHITE, 15)

PINK = curses.color_pair(1)
BLUE = curses.color_pair(2)
GREEN = curses.color_pair(3)
YELLOW = curses.color_pair(4)
RED = curses.color_pair(5)
GREEN_REV = curses.color_pair(6)
RED_REV = curses.color_pair(7)

str_ = str # :/
class String(str): pass

class Module:
    x = property(lambda self: self._x + self._offset[1])
    y = property(lambda self: self._y + self._offset[0])
    color = property(lambda self: self._color)
    def __init__(self, coords, dims, color=None):
        self.set_coords(coords)
        self.width, self.height = dims
        self.set_offset()
        self._color = color or curses.A_NORMAL
        self.value = "" # :/
        self.grid = curses.newwin(self.height, self.width, self.y, self.x)
    def set_coords(self, coords):
        self._x, self._y = coords
    def set_offset(self, offset=(0, 0)):
        self._offset = offset
    def render(self, grid: curses.window, offset=(0, 0)):
        self.set_offset(offset)
        grid.addstr(self.y, self.x, self.value, self.color)
        grid.refresh()
    def destroy(self):
        self.grid.clear()
        self.grid.refresh()
        del self.grid

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
        self.value = str_(node)[:self.width]
        if self.format:
            self.value = self.format(self.value)

class box(Module):
    H, V, TL, TR, BL, BR =  "─", "│", "┌", "┐", "└", "┘"
    def __init__(self, coords, dims, modules=None, color=None):
        super().__init__(coords, dims, color)
        self.modules = modules or []
    def append(self, module):
        self.modules.append(module)
    def render(self, grid: curses.window, offset=(0, 0)):
        self.set_offset(offset)
        w, h = self.width - 1, self.height - 1
        offset = (self.y, self.x)
        for x in range(1, w):
            grid.addch(self.y, self.x + x, self.H)
            grid.addch(self.y + h, self.x + x, self.H)
        for y in range(1, h):
            grid.addch(self.y + y, self.x, self.V)
            grid.addch(self.y + y, self.x + w, self.V)
        grid.addch(self.y, self.x, self.TL)
        grid.addch(self.y + h, self.x, self.BL)
        grid.addch(self.y, self.x + w, self.TR)
        grid.addch(self.y + h, self.x + w, self.BR)
        for module in self.modules:
            module.render(grid, offset)
        grid.refresh()
        return self.grid
class str(NodeModule): pass
class title(str):
    def render(self, grid: curses.window, offset=(0, 0)):
        self.set_offset(offset)
        line = "═" * len(self.value)
        grid.addstr(self.y, self.x, self.value.center(self.width), self.color)
        grid.addstr(self.y + 1, self.x, line.center(self.width), self.color)
        grid.refresh()
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
    def render(self, grid: curses.window, offset=(0, 0)):
        self.set_offset(offset)
        if not isinstance(self.value, (int, float)):
            self.value = 0.0
        bar_width = min(math.floor(self.value / 100 * self.width), self.width)
        for i in range(self.height):
            for j in range(max(bar_width, 0)):
                grid.addch(i + self.y, j + self.x, self.FULL, self.color)
            if self.value % 100 >= 50:
                grid.addch(i + self.y, bar_width + self.x, self.HALF, self.color)
                bar_width += 1
            for j in range(bar_width, self.width):
                grid.addch(i + self.y, j + self.x, "-", self.color)
class bool(NodeModule):
    OFF = "○"
    ON = "●"
    OFF_COLOR = curses.A_DIM
    ON_COLOR = RED
    @property
    def color(self):
        if self.value == True:
            return self.ON_COLOR
        return self.OFF_COLOR
    def render(self, grid: curses.window, offset=(0, 0)):
        self.set_offset(offset)
        if self.value == True:
            grid.addstr(self.y, self.x, self.ON, self.ON_COLOR)
        else:
            grid.addstr(self.y, self.x, self.OFF, self.OFF_COLOR)
class mute(bool):
    OFF = "○"
    ON = "●"
    OFF_COLOR = GREEN
    ON_COLOR = RED
class view:
    def __init__(self, dims, modules=None):
        self.width, self.height = dims
        self.modules = modules or []
        self.grid = curses.newwin(self.height, self.width, 0, 0)
    def append(self, module):
        self.modules.append(module)
    def render(self):
        for module in self.modules:
            module.render(self.grid)
        self.grid.refresh()
    def init(self): pass
    def destroy(self): pass
            
class app:
    def __init__(self, dims):
        self.width, self.height = dims
        self.views = []
    def init(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(100)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    def append(self, module):
        self.views.append(module)
    def update(self, modules):
        self.views.update(modules)
    def render(self):
        for view in self.views:
            view.render()
    def click(self, y, x):
        pass
