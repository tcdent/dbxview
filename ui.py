import math
import curses
from . import log, Node

str_ = str # :/

class coord:
    curses = property(lambda self: (self.y, self.x))
    def __init__(self, *coords):
        self.y, self.x = coords
    def __splat__(self):
        return self.y, self.x
class rgb:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
    def to_curses_color(self):
        def f(value): return int(value * 1000 / 255)
        return f(self.r), f(self.g), f(self.b)
class key:
    BACK = 127
    ESC = 27
    ENTER = 10
    SPACE = 32
    PERIOD = 46
    PERCENT = 37
    MINUS = 45
    @classmethod
    def is_numeric(cls, ch): return ch >= 48 and ch <= 57
    @classmethod
    def is_alpha(cls, ch): return (ch >= 65 and ch <= 90) or (ch >= 97 and ch <= 122)

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
curses.init_pair(8, curses.COLOR_WHITE, 12)

PINK = curses.color_pair(1)
BLUE = curses.color_pair(2)
GREEN = curses.color_pair(3)
YELLOW = curses.color_pair(4)
RED = curses.color_pair(5)
GREEN_REV = curses.color_pair(6)
RED_REV = curses.color_pair(7)
BLUE_REV = curses.color_pair(8)

editing = False

class Module:
    y = property(lambda self: self.coords.y)
    x = property(lambda self: self.coords.x)
    color = property(lambda self: self._color)
    def __init__(self, coords, dims, color=None):
        self.coords = coord(*coords)
        self.height, self.width = dims
        self._color = color or curses.A_NORMAL
        self._grid = None
        self.value = "" # :/
    @property
    def grid(self):
        if not self._grid: # TODO that +1 is a hack
            self._grid = curses.newwin(self.height+1, self.width, self.y, self.x)
        return self._grid
    def render(self):
        if '\n' in str_(self.value): # TODO real multiline
            lines = self.value.split('\n')
            for i, line in enumerate(lines):
                self.grid.addstr(i, 0, line, self.color)
        else:
            value = str_(self.value).ljust(self.width)[:self.width]
            self.grid.addstr(0, 0, value, self.color)
        self.grid.refresh()
    def hit(self, y, x):
        return y >= self.y and y < self.y + self.height and x >= self.x and x < self.x + self.width
    def click(self, y, x): pass
    def input(self, ch): pass
    def destroy(self):
        self.grid.erase()
        self.grid.refresh()
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
        self.render()
    def save(self):
        self.node.set_data(self.value)
        self.update(self.node)
        self.node.save()
    def destroy(self):
        if isinstance(self.node, Node):
            self.node.remove_callback(self.update)
        super().destroy()
class str(NodeModule):
    pass
class title(str):
    def render(self):
        line = "═" * len(self.value)
        self.grid.addstr(0, 0, self.value.center(self.width), self.color)
        self.grid.addstr(1, 0, line.center(self.width), self.color)
        self.grid.refresh()
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
        #self.grid.erase()
        if not isinstance(self.value, (int, float)):
            self.value = 0.0
        bar_width = min(math.floor(self.value / 100 * self.width), self.width)
        for x in range(max(bar_width, 0)):
            self.grid.addch(0, x, self.FULL, self.color)
        # if self.value % 100 >= 50:
        #     bar_width += 1
        #     self.grid.addch(0, bar_width+1, self.HALF, self.color)
        for x in range(bar_width, self.width):
            self.grid.addch(0, x, "-", BLUE)
        self.grid.refresh()
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
    def render(self):
        if self.value == True:
            self.grid.addstr(0, 0, self.ON, self.ON_COLOR)
        else:
            self.grid.addstr(0, 0, self.OFF, self.OFF_COLOR)
        self.grid.refresh()
class mute(bool):
    OFF = "○"
    ON = "●"
    OFF_COLOR = GREEN
    ON_COLOR = RED
class onoff(bool):
    OFF = " O "
    ON = " I "
    OFF_COLOR = curses.A_REVERSE
    ON_COLOR = BLUE_REV
    def click(self, y, x):
        if self.hit(y, x):
            value = not self.value
            self.value = 'On' if value else 'Off'
            self.save()
            self.render()
class edit(NodeModule):
    color = BLUE_REV
    def __init__(self, coords, dims, node, color=None, format: callable=None, filter: callable=None):
        super().__init__(coords, dims, node, color, format)
        self.filter = filter
        self.editing = False
        self.original_value = self.value
    def click(self, y, x):
        if not self.editing and self.hit(y, x):
            self.start_editing()
        elif self.editing:
            self.stop_editing()
            self.value = self.original_value
    def start_editing(self):
        global editing
        editing = True
        self.editing = True
        self.original_value = self.value
        self.color = curses.A_REVERSE
        self.render()
    def stop_editing(self):
        global editing
        editing = False
        self.editing = False
        self.color = BLUE_REV
        self.render()
    def save(self):
        if self.filter:
            self.value = self.filter(self.value)
        super().save()
    def input(self, ch):
        if not self.editing:
            return
        if key.is_alpha(ch) or key.is_numeric(ch) or ch == key.PERIOD or ch == key.MINUS:
            self.value = str_(self.value) + chr(ch)
        if ch == key.BACK:
            self.value = str_(self.value)[:-1]
        if ch == key.ESC:
            self.stop_editing()
            self.value = self.original_value
        if ch == key.ENTER:
            self.stop_editing()
            self.save()
        self.render()

class Contains:
    def append(self, module):
        self.modules.append(module)
        self.render()
    def render(self):
        for module in self.modules:
            module.render()
    def click(self, y, x):
        for module in self.modules:
            module.click(y, x)
    def input(self, ch):
        for module in self.modules:
            module.input(ch)
    def destroy(self):
        for module in self.modules:
            module.destroy()
        self.grid.erase()
        self.grid.refresh()
class box(Contains, Module):
    H, V, TL, TR, BL, BR =  "─", "│", "┌", "┐", "└", "┘"
    def __init__(self, coords, dims, modules=None, color=None):
        super().__init__(coords, dims, color)
        self.modules = []
        for module in modules or []:
            self.append(module)
    def append(self, module):
        module.coords = coord(self.y + module.y, self.x + module.x)
        super().append(module)
    def render(self):
        w, h = self.width - 1, self.height - 1
        for x in range(1, w):
            self.grid.addch(0, x, self.H)
            self.grid.addch(h, x, self.H)
        for y in range(1, h):
            self.grid.addch(y, 0, self.V)
            self.grid.addch(y, w, self.V)
        self.grid.addch(0, 0, self.TL)
        self.grid.addch(h, 0, self.BL)
        self.grid.addch(0, w, self.TR)
        self.grid.addch(h, w, self.BR)
        self.grid.refresh()
        super().render()
class view(Contains):
    def __init__(self, dims, modules=None):
        self.width, self.height = dims
        self.modules = []
        self.grid = curses.newwin(self.height, self.width, 0, 0)
        for module in modules or []:
            self.append(module)
    def init(self):
        pass
class app(Contains):
    def __init__(self, dims):
        self.width, self.height = dims
        self.modules = []
    def init(self, stdscr):
        curses.curs_set(0)
        stdscr.nodelay(True)
        stdscr.timeout(100)
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    def update(self, modules: list[view]):
        for module in modules:
            self.append(module)
    def destroy(self, module: view):
        self.modules.remove(module)
        module.destroy()
