import curses
from . import N, Q, ui, state, net, TARGET_IP
from .state import *

EPOCH = 3

def main(stdscr):
    LABEL = (4, 1)
    METER = (22, 1)
    LEVEL = (8, 1)

    grid = ui.app(80, 30)
    grid.init(stdscr)
    sock, listener = net.setup_tcp()
    state.sub()

    grid.append(ui.title((0, 0), (80, 3), NAME))
    grid.append(ui.str((0, 3), (80, 1), DEV))
    grid.append(ui.str((65, 28), (20, 1), f"{TARGET_IP}"))
    grid.append(ui.str((0, 28), (65, 1), f" [q]uit  [r]esub"))

    grid.append(ui.box((0, 6), (40, 7), [
        ui.str((6, 0), (6, 2), "┤Left├"),
        ui.str((2, 2), LABEL, "IN"),
        ui.str((2, 3), LABEL, "HIGH"),
        ui.str((2, 4), LABEL, "MID"),
        ui.str((2, 5), LABEL, "LOW"),
        ui.bar((7, 2), METER, L_IN),
        ui.bar((7, 3), METER, L_HIGH),
        ui.bar((7, 4), METER, L_MID),
        ui.bar((7, 5), METER, L_LOW),
        ui.str((30, 2), LEVEL, L_IN),
        ui.str((30, 3), LEVEL, L_HIGH),
        ui.str((30, 4), LEVEL, L_MID),
        ui.str((30, 5), LEVEL, L_LOW),
        ui.str((35, 2), (5, 1), L_IN_CLIP),
        ui.str((35, 3), (5, 1), MUTE_L_HIGH),
        ui.str((35, 4), (5, 1), MUTE_L_MID),
        ui.str((35, 5), (5, 1), MUTE_L_LOW),
    ]))

    grid.append(ui.box((40, 6), (40, 7), [
        ui.str((6, 0), (7, 2), "┤Right├"),
        ui.str((2, 2), LABEL, "IN"),
        ui.str((2, 3), LABEL, "HIGH"),
        ui.str((2, 4), LABEL, "MID"),
        ui.str((2, 5), LABEL, "LOW"),
        ui.bar((7, 2), METER, R_IN),
        ui.bar((7, 3), METER, R_HIGH),
        ui.bar((7, 4), METER, R_MID),
        ui.bar((7, 5), METER, R_LOW),
        ui.str((30, 2), LEVEL, R_IN),
        ui.str((30, 3), LEVEL, R_HIGH),
        ui.str((30, 4), LEVEL, R_MID),
        ui.str((30, 5), LEVEL, R_LOW),
        ui.str((35, 2), (5, 1), R_IN_CLIP),
        ui.str((35, 3), (5, 1), MUTE_R_HIGH),
        ui.str((35, 4), (5, 1), MUTE_R_MID),
        ui.str((35, 5), (5, 1), MUTE_R_LOW),
    ]))

    grid.append(ui.box((0, 13), (40, 9), [
        ui.str((6, 0), (24, 2), SS, format=lambda n: f"┤Subharmonic Synth {n}├"),
        ui.str((2, 1), LABEL, "%"),
        ui.str((2, 2), LABEL, "LEVEL", color=ui.PINK),
        ui.str((2, 3), LABEL, "UPP"),
        ui.str((2, 4), LABEL, "LOW"),
        ui.str((2, 5), LABEL, "24-36"),
        ui.str((2, 6), LABEL, "36-56"),
        ui.bar((7, 1), METER, SH),
        ui.bar((7, 2), METER, SS_LEVEL, color=ui.PINK),
        ui.bar((7, 3), METER, SS_UPPER),
        ui.bar((7, 4), METER, SS_LOWER),
        ui.bar((7, 5), METER, SS_24),
        ui.bar((7, 6), METER, SS_36),
        ui.str((30, 1), LEVEL, SH),
        ui.str((30, 2), LEVEL, SS_LEVEL),
        ui.str((30, 3), LEVEL, SS_UPPER),
        ui.str((30, 4), LEVEL, SS_LOWER),
        ui.str((30, 5), LEVEL, SS_24),
        ui.str((30, 6), LEVEL, SS_36),
    ]))

    ctx = 0
    while True:
        ctx += 1
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            stdscr.addstr(y, x, '▒')
            grid.click(y, x)
        if key == ord('q'):
            break
        elif key == ord('r'):
            state.sub()
        if ctx == EPOCH:
            ctx = 0
            state.loop()
        grid.display(stdscr)

curses.wrapper(main)