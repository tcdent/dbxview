import curses
from . import N, Q, ui, state, net, TARGET_IP
from .state import *

class meters(ui.view):
    subs = (
        L_IN, R_IN, L_IN_CLIP, R_IN_CLIP,
        SH, SS, SS_24, SS_36, SS_LEVEL, SS_UPPER, SS_LOWER,
        L_HIGH, MUTE_L_HIGH, R_HIGH, MUTE_R_HIGH, LMT_HIGH,
        L_MID, MUTE_L_MID, R_MID, MUTE_R_MID, LMT_MID,
        L_LOW, MUTE_L_LOW, R_LOW, MUTE_R_LOW, LMT_LOW,
    )
    loops = (
        SS_LEVEL, SS_UPPER, SS_LOWER, 
    )
    def init(self):
        LABEL = (1, 4)
        METER = (1, 22)
        LEVEL = (1, 4)

        self.modules = [
            ui.box((6, 0), (7, 40), [
                ui.str((0, 6), (2, 6), "┤Left├"),
                ui.str((2, 2), LABEL, "IN", color=ui.YELLOW),
                ui.str((3, 2), LABEL, "HIGH"),
                ui.str((4, 2), LABEL, "MID"),
                ui.str((5, 2), LABEL, "LOW"),
                ui.bar((2, 7), METER, L_IN, format=state.db_pc),
                ui.bar((3, 7), METER, L_HIGH, format=state.db_pc),
                ui.bar((4, 7), METER, L_MID, format=state.db_pc),
                ui.bar((5, 7), METER, L_LOW, format=state.db_pc),
                ui.str((1, 31), LABEL, "dB"),
                ui.str((2, 30), LEVEL, L_IN, format=state.db_str, color=curses.A_REVERSE),
                ui.str((3, 30), LEVEL, L_HIGH, format=state.db_str),
                ui.str((4, 30), LEVEL, L_MID, format=state.db_str),
                ui.str((5, 30), LEVEL, L_LOW, format=state.db_str),
                ui.str((1, 35), (1, 1), "C", color=curses.A_REVERSE),
                ui.bool((2, 35), (1, 1), L_IN_CLIP, format=state.onoff),
                ui.str((1, 37), (1, 1), "M"),
                ui.mute((3, 37), (1, 1), MUTE_L_HIGH, format=state.onoff),
                ui.mute((4, 37), (1, 1), MUTE_L_MID, format=state.onoff),
                ui.mute((5, 37), (1, 1), MUTE_L_LOW, format=state.onoff),
            ]),
            ui.box((6, 40), (7, 40), [
                ui.str((0, 6), (2, 7), "┤Right├"),
                ui.str((2, 2), LABEL, "IN", color=ui.YELLOW),
                ui.str((3, 2), LABEL, "HIGH"),
                ui.str((4, 2), LABEL, "MID"),
                ui.str((5, 2), LABEL, "LOW"),
                ui.bar((2, 7), METER, R_IN, format=state.db_pc),
                ui.bar((3, 7), METER, R_HIGH, format=state.db_pc),
                ui.bar((4, 7), METER, R_MID, format=state.db_pc),
                ui.bar((5, 7), METER, R_LOW, format=state.db_pc),
                ui.str((2, 30), LEVEL, R_IN, format=state.db_str),
                ui.str((3, 30), LEVEL, R_HIGH, format=state.db_str),
                ui.str((4, 30), LEVEL, R_MID, format=state.db_str),
                ui.str((5, 30), LEVEL, R_LOW, format=state.db_str),
                ui.str((1, 35), LABEL, "C"),
                ui.bool((2, 35), (1, 1), R_IN_CLIP, format=state.onoff),
                ui.str((1, 37), LABEL, "M"),
                ui.mute((3, 37), (1, 1), MUTE_R_HIGH, format=state.onoff),
                ui.mute((4, 37), (1, 1), MUTE_R_MID, format=state.onoff),
                ui.mute((5, 37), (1, 1), MUTE_R_LOW, format=state.onoff),
            ]),
            ui.box((13, 0), (9, 40), [
                ui.str((0, 6), (2, 24), SS, format=lambda n: f"┤Subharmonic Synth {n}├"),
                ui.str((1, 2), LABEL, "%"),
                ui.str((2, 2), LABEL, "LEVEL"),
                ui.str((3, 2), LABEL, "UPP"),
                ui.str((4, 2), LABEL, "LOW"),
                ui.str((5, 2), LABEL, "24-36"),
                ui.str((6, 2), LABEL, "36-56"),
                ui.bar((1, 7), METER, SH, format=state.pc),
                ui.bar((2, 7), METER, SS_LEVEL, format=state.db_pc),
                ui.bar((3, 7), METER, SS_UPPER, format=state.db_pc),
                ui.bar((4, 7), METER, SS_LOWER, format=state.db_pc),
                ui.bar((5, 7), METER, SS_24, format=state.pc),
                ui.bar((6, 7), METER, SS_36, format=state.pc),
                ui.str((1, 30), LEVEL, SH),
                ui.str((2, 30), LEVEL, SS_LEVEL, format=state.db_str),
                ui.str((3, 30), LEVEL, SS_UPPER, format=state.db_str),
                ui.str((4, 30), LEVEL, SS_LOWER, format=state.db_str),
                ui.str((5, 30), LEVEL, SS_24),
                ui.str((6, 30), LEVEL, SS_36),
            ]),
        ]
class equalizers(ui.view):
    subs = (
        PEQ_MID, PEQ_MID_MANUAL, PEQ_MID_AUTO, PEQ_MID_LO, PEQ_MID_HS, PEQ_MID_FL, PEQ_MID_BELL,
        PEQ_MID_B1_TYPE, PEQ_MID_B1_Q, PEQ_MID_B1_GAIN, PEQ_MID_B1_FREQ, 
    )
    loops = ()
    def init(self):
        # band | 1 | 2 | 3 | 4 | ... | 8
        # freq |   |   |   |   | ... |
        # gain |   |   |   |   | ... |
        # q    |   |   |   |   | ... |
        # type |   |   |   |   | ... |
        # bands horiozntally
        self.modules = [
            ui.box((6, 0), (7, 80), [
                ui.str((0, 6), (2, 24), PEQ_MID, format=lambda n: f"┤Mid Outputs PEQ {n}├"),
                ui.str((1, 2), (1, 6), "Manual"),
                ui.str((1, 8), (1, 6), "Auto"),
                ui.str((1, 14), (1, 6), "Low Shelf"),
                ui.str((1, 20), (1, 6), "High Shelf"),
                ui.str((1, 26), (1, 6), "Flatten"),
                ui.str((1, 32), (1, 6), "Bell"),
            ]), 
            ui.box((13, 0), (9, 80), [
                ui.str((0, 6), (2, 24), PEQ_MID, format=lambda n: f"┤Mid Outputs PEQ {n}├"),
                ui.str((1, 2), (1, 6), "Band 1"),
                ui.str((1, 8), (1, 6), "Band 2"),
                ui.str((1, 14), (1, 6), "Band 3"),
                ui.str((1, 20), (1, 6), "Band 4"),
                ui.str((1, 26), (1, 6), "Band 5"),
                ui.str((1, 32), (1, 6), "Band 6"),
                ui.str((1, 38), (1, 6), "Band 7"),
                ui.str((1, 44), (1, 6), "Band 8"),
                ui.str((2, 2), (1, 6), "Freq"),
                ui.str((3, 2), (1, 6), "Gain"),
                ui.str((4, 2), (1, 6), "Q"),
                ui.str((5, 2), (1, 6), "Type"),
                ui.str((2, 8), (1, 6), PEQ_MID_B1_FREQ, format=state.db_str),
                ui.str((3, 8), (1, 6), PEQ_MID_B1_GAIN, format=state.db_str),
                ui.str((4, 8), (1, 6), PEQ_MID_B1_Q, format=state.db_str),
                ui.str((5, 8), (1, 6), PEQ_MID_B1_TYPE),
            ]),
        ]
def main(stdscr):
    dims = (80, 30)
    grid = ui.app(dims)
    view = None
    net.setup_tcp()
    def setup(stdscr):
        grid.init(stdscr)
        grid.append(ui.view(dims, [
            ui.title((0, 0), (2, 80), NAME),
            ui.str((3, 0), (1, 80), DEV),
            ui.str((28, 65), (1, 20), f"{TARGET_IP}"),
            ui.str((28, 0), (1, 65), f" [q]uit [m]eters [e]qualizers"),
        ]))
        grid.render()
        state.sub((DEV, PRE, NAME, CURR_PRE,))
    def load_view(view_cls):
        nonlocal view
        if view:
            state.unsub(view.subs)
            grid.destroy(view)
            view = None
        view = view_cls(dims)
        view.init()
        grid.append(view)
        grid.render() # render static
        state.sub(view.subs)
    setup(stdscr)
    load_view(meters)
    while True:
        key = stdscr.getch()
        if key == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            stdscr.addstr(y, x, '▒', curses.A_REVERSE)
            grid.click(y, x)
        if key == ord('q'):
            break
        elif key == ord('m'):
            load_view(meters)
        elif key == ord('e'):
            load_view(equalizers)
        if view:
            state.loop(view.loops)

curses.wrapper(main)