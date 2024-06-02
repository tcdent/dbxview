import curses
from . import N, Q, ui, state, net, TARGET_IP
from .state import *

EPOCH = 3

def main(stdscr):
    LABEL = (4, 1)
    METER = (22, 1)
    LEVEL = (4, 1)

    grid = ui.app(80, 30)
    grid.init(stdscr)
    sock, listener = net.setup_tcp()
    state.sub()

    grid.append(ui.title((0, 0), (80, 3), NAME))
    grid.append(ui.str((0, 3), (80, 1), DEV))
    grid.append(ui.box((0, 6), (40, 7), [
        ui.str((6, 0), (6, 2), "┤Left├"),
        ui.str((2, 2), LABEL, "IN", color=ui.YELLOW),
        ui.str((2, 3), LABEL, "HIGH"),
        ui.str((2, 4), LABEL, "MID"),
        ui.str((2, 5), LABEL, "LOW"),
        ui.bar((7, 2), METER, L_IN, format=state.db_pc),
        ui.bar((7, 3), METER, L_HIGH, format=state.db_pc),
        ui.bar((7, 4), METER, L_MID, format=state.db_pc),
        ui.bar((7, 5), METER, L_LOW, format=state.db_pc),
        ui.str((31, 1), LABEL, "dB"),
        ui.str((30, 2), LEVEL, L_IN, format=state.db_str),
        ui.str((30, 3), LEVEL, L_HIGH, format=state.db_str),
        ui.str((30, 4), LEVEL, L_MID, format=state.db_str),
        ui.str((30, 5), LEVEL, L_LOW, format=state.db_str),
        ui.str((35, 1), (1, 1), "C"),
        ui.bool((35, 2), (1, 1), L_IN_CLIP, format=state.onoff),
        ui.str((37, 1), (1, 1), "M"),
        ui.mute((37, 3), (1, 1), MUTE_L_HIGH, format=state.onoff),
        ui.mute((37, 4), (1, 1), MUTE_L_MID, format=state.onoff),
        ui.mute((37, 5), (1, 1), MUTE_L_LOW, format=state.onoff),
    ]))
    grid.append(ui.box((40, 6), (40, 7), [
        ui.str((6, 0), (7, 2), "┤Right├"),
        ui.str((2, 2), LABEL, "IN", color=ui.YELLOW),
        ui.str((2, 3), LABEL, "HIGH"),
        ui.str((2, 4), LABEL, "MID"),
        ui.str((2, 5), LABEL, "LOW"),
        ui.bar((7, 2), METER, R_IN, format=state.db_pc),
        ui.bar((7, 3), METER, R_HIGH, format=state.db_pc),
        ui.bar((7, 4), METER, R_MID, format=state.db_pc),
        ui.bar((7, 5), METER, R_LOW, format=state.db_pc),
        ui.str((30, 2), LEVEL, R_IN, format=state.db_str),
        ui.str((30, 3), LEVEL, R_HIGH, format=state.db_str),
        ui.str((30, 4), LEVEL, R_MID, format=state.db_str),
        ui.str((30, 5), LEVEL, R_LOW, format=state.db_str),
        ui.str((35, 1), LABEL, "C"),
        ui.bool((35, 2), (1, 1), R_IN_CLIP, format=state.onoff),
        ui.str((37, 1), LABEL, "M"),
        ui.mute((37, 3), (1, 1), MUTE_R_HIGH, format=state.onoff),
        ui.mute((37, 4), (1, 1), MUTE_R_MID, format=state.onoff),
        ui.mute((37, 5), (1, 1), MUTE_R_LOW, format=state.onoff),
    ]))
    grid.append(ui.box((0, 13), (40, 9), [
        ui.str((6, 0), (24, 2), SS, format=lambda n: f"┤Subharmonic Synth {n}├"),
        ui.str((2, 1), LABEL, "%"),
        ui.str((2, 2), LABEL, "LEVEL"),
        ui.str((2, 3), LABEL, "UPP"),
        ui.str((2, 4), LABEL, "LOW"),
        ui.str((2, 5), LABEL, "24-36"),
        ui.str((2, 6), LABEL, "36-56"),
        ui.bar((7, 1), METER, SH, format=state.pc),
        ui.bar((7, 2), METER, SS_LEVEL, format=state.db_pc),
        ui.bar((7, 3), METER, SS_UPPER, format=state.db_pc),
        ui.bar((7, 4), METER, SS_LOWER, format=state.db_pc),
        ui.bar((7, 5), METER, SS_24, format=state.pc),
        ui.bar((7, 6), METER, SS_36, format=state.pc),
        ui.str((30, 1), LEVEL, SH),
        ui.str((30, 2), LEVEL, SS_LEVEL, format=state.db_str),
        ui.str((30, 3), LEVEL, SS_UPPER, format=state.db_str),
        ui.str((30, 4), LEVEL, SS_LOWER, format=state.db_str),
        ui.str((30, 5), LEVEL, SS_24),
        ui.str((30, 6), LEVEL, SS_36),
    ]))
    grid.append(ui.str((65, 28), (20, 1), f"{TARGET_IP}"))
    grid.append(ui.str((0, 28), (65, 1), f" [q]uit  [r]econnect"))

    ctx = 0
    while True:
        ctx += 1
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            stdscr.addstr(y, x, '▒', curses.A_REVERSE)
            #grid.click(y, x)
        if key == ord('q'):
            break
        elif key == ord('r'):
            sock.close()
            sock, listener = net.setup_tcp()
            state.sub()
        if ctx == EPOCH:
            ctx = 0
            state.loop()
        grid.display(stdscr)

curses.wrapper(main)