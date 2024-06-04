import sys
if __name__ == '__main__':
    if '--discover' in sys.argv:
        from .discover import yolo
        yolo()
        sys.exit(0)

import curses
from . import N, Q, ui, state, net, TARGET_IP
from .state import *

class meters(ui.view):
    subs = (
        L_IN_CLIP, R_IN_CLIP,
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
                ui.str((2, 30), LEVEL, L_IN, format=state.db_int),
                ui.str((3, 30), LEVEL, L_HIGH, format=state.db_int),
                ui.str((4, 30), LEVEL, L_MID, format=state.db_int),
                ui.str((5, 30), LEVEL, L_LOW, format=state.db_int),
                ui.str((1, 35), (1, 1), "C"),
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
                ui.str((2, 30), LEVEL, R_IN, format=state.db_int),
                ui.str((3, 30), LEVEL, R_HIGH, format=state.db_int),
                ui.str((4, 30), LEVEL, R_MID, format=state.db_int),
                ui.str((5, 30), LEVEL, R_LOW, format=state.db_int),
                ui.str((1, 35), (1, 1), "C"),
                ui.bool((2, 35), (1, 1), R_IN_CLIP, format=state.onoff),
                ui.str((1, 37), (1, 1), "M"),
                ui.mute((3, 37), (1, 1), MUTE_R_HIGH, format=state.onoff),
                ui.mute((4, 37), (1, 1), MUTE_R_MID, format=state.onoff),
                ui.mute((5, 37), (1, 1), MUTE_R_LOW, format=state.onoff),
            ]),
            ui.box((14, 0), (6, 40), [
                ui.str((0, 6), (2, 19), "┤Subharmonic Synth├"),
                ui.onoff((0, 2), (1, 4), SS, format=state.onoff),
                ui.str((2, 2), LABEL, "LVL"),
                ui.str((3, 2), LABEL, "UP"),
                ui.str((4, 2), LABEL, "LOW"),
                #ui.str((1, 2), LABEL, "%"),
                #ui.str((5, 2), LABEL, "24-36"),
                #ui.str((6, 2), LABEL, "36-56"),
                ui.bar((2, 7), METER, SS_LEVEL, format=state.db_pc),
                ui.bar((3, 7), METER, SS_UPPER, format=state.db_pc),
                ui.bar((4, 7), METER, SS_LOWER, format=state.db_pc),
                #ui.bar((1, 7), METER, SH, format=state.pc),
                #ui.bar((5, 7), METER, SS_24, format=state.pc),
                #ui.bar((6, 7), METER, SS_36, format=state.pc),
                ui.str((2, 30), LEVEL, SS_LEVEL, format=state.db_int),
                ui.str((3, 30), LEVEL, SS_UPPER, format=state.db_int),
                ui.str((4, 30), LEVEL, SS_LOWER, format=state.db_int),
                #ui.str((1, 30), LEVEL, SH),
                #ui.str((5, 30), LEVEL, SS_24),
                #ui.str((6, 30), LEVEL, SS_36),
            ]),
        ]
class equalizers(ui.view):
    subs = (
        PEQ_HIGH, PEQ_HIGH_FL, PEQ_HIGH_HS, PEQ_HIGH_LO, PEQ_HIGH_BELL, PEQ_HIGH_AUTO, PEQ_HIGH_MANUAL,
        PEQ_MID, PEQ_MID_FL, PEQ_MID_HS, PEQ_MID_LO, PEQ_MID_BELL, PEQ_MID_AUTO, PEQ_MID_MANUAL,
        PEQ_LOW, PEQ_LOW_FL, PEQ_LOW_HS, PEQ_LOW_LO, PEQ_LOW_BELL, PEQ_LOW_AUTO, PEQ_LOW_MANUAL,
    ) + \
        tuple(PEQ_HIGH_BAND[i][key] for i in range(1, 9) for key in ('type', 'q', 'gain', 'freq')) + \
        tuple(PEQ_MID_BAND[i][key] for i in range(1, 9) for key in ('type', 'q', 'gain', 'freq')) + \
        tuple(PEQ_LOW_BAND[i][key] for i in range(1, 9) for key in ('type', 'q', 'gain', 'freq'))
    loops = ()
    def init(self):
        COL_W = 8
        LABEL = (1, 4)
        BAND = (1, 6)
        high = ui.box((6, 0), (7, 80), [
            ui.str((0, 6), (2, 10), "┤High PEQ├"),
            ui.onoff((0, 2), (1, 4), PEQ_HIGH, format=state.onoff),
            ui.str((2, 2), LABEL, "  Hz"),
            ui.str((3, 2), LABEL, "  dB"),
            ui.str((4, 2), LABEL, "   Q"),
            ui.str((5, 2), LABEL, "Type"),
        ])
        for i in range(1, 9):
            high.append(ui.str((1, i * COL_W), BAND, str(i).center(BAND[1])))
            high.append(ui.edit((2, i * COL_W), BAND, PEQ_HIGH_BAND[i]['freq'], format=state.pc_hz, filter=state.hz_pc))
            high.append(ui.edit((3, i * COL_W), BAND, PEQ_HIGH_BAND[i]['gain'], format=state.db))
            high.append(ui.edit((4, i * COL_W), BAND, PEQ_HIGH_BAND[i]['q']))
            high.append(ui.str((5, i * COL_W), (1, 6), PEQ_HIGH_BAND[i]['type']))
        mid = ui.box((13, 0), (7, 80), [
            ui.str((0, 6), (2, 9), "┤Mid PEQ├"),
            ui.onoff((0, 2), (1, 4), PEQ_MID, format=state.onoff),
            ui.str((2, 2), LABEL, "  Hz"),
            ui.str((3, 2), LABEL, "  dB"),
            ui.str((4, 2), LABEL, "   Q"),
            ui.str((5, 2), LABEL, "Type"),
        ])
        for i in range(1, 9):
            mid.append(ui.str((1, i * COL_W), BAND, str(i).center(BAND[1])))
            mid.append(ui.edit((2, i * COL_W), BAND, PEQ_MID_BAND[i]['freq'], format=state.pc_hz, filter=state.hz_pc))
            mid.append(ui.edit((3, i * COL_W), BAND, PEQ_MID_BAND[i]['gain'], format=state.db))
            mid.append(ui.edit((4, i * COL_W), BAND, PEQ_MID_BAND[i]['q']))
            mid.append(ui.str((5, i * COL_W), (1, 6), PEQ_MID_BAND[i]['type']))
        low = ui.box((20, 0), (7, 80), [
            ui.str((0, 6), (2, 9), "┤Low PEQ├"),
            ui.onoff((0, 2), (1, 4), PEQ_LOW, format=state.onoff),
            ui.str((2, 2), LABEL, "  Hz"),
            ui.str((3, 2), LABEL, "  dB"),
            ui.str((4, 2), LABEL, "   Q"),
            ui.str((5, 2), LABEL, "Type"),
        ])
        for i in range(1, 9):
            low.append(ui.str((1, i * COL_W), BAND, str(i).center(BAND[1])))
            low.append(ui.edit((2, i * COL_W), BAND, PEQ_LOW_BAND[i]['freq'], format=state.pc_hz, filter=state.hz_pc))
            low.append(ui.edit((3, i * COL_W), BAND, PEQ_LOW_BAND[i]['gain'], format=state.db))
            low.append(ui.edit((4, i * COL_W), BAND, PEQ_LOW_BAND[i]['q']))
            low.append(ui.str((5, i * COL_W), (1, 6), PEQ_LOW_BAND[i]['type']))
        self.modules = [high, mid, low]
class crossover(ui.view):
    subs = (
        XO_HIGH, XO_HIGH_, XO_MID, XO_MID_, XO_LOW, XO_LOW_,
        XO_HIGH_LP_TYPE, XO_HIGH_HP_TYPE, XO_MID_LP_TYPE, XO_MID_HP_TYPE, XO_LOW_LP_TYPE, XO_LOW_HP_TYPE,
        XO_HIGH_LP_, XO_HIGH_HP_, XO_MID_LP_, XO_MID_HP_, XO_LOW_LP_, XO_LOW_HP_, 
        XO_HIGH_LP, XO_HIGH_HP, XO_MID_LP, XO_MID_HP, XO_LOW_LP, XO_LOW_HP,
        XO_HIGH_POL, XO_MID_POL, XO_LOW_POL,
    )
    loops = ()
    def init(self):
        high = ui.box((6, 0), (7, 26), [
            ui.str((0, 6), (2, 6), "┤High├"),
            ui.str((2, 2), (1, 4), "dB"),
            ui.str((3, 2), (1, 4), "LP"),
            ui.str((4, 2), (1, 4), "HP"),
            ui.str((5, 2), (1, 4), " ø"),
        ])
        high.append(ui.edit((2, 6), (1, 8), XO_HIGH, format=state.db))
        high.append(ui.edit((3, 6), (1, 8), XO_HIGH_LP, format=state.hz_int))
        high.append(ui.edit((3, 16), (1, 6), XO_HIGH_LP_TYPE))
        high.append(ui.edit((4, 6), (1, 8), XO_HIGH_HP, format=state.hz_int))
        high.append(ui.edit((4, 16), (1, 6), XO_HIGH_HP_TYPE))
        high.append(ui.str((5, 6), (1, 6), XO_HIGH_POL))

        mid = ui.box((6, 27), (7, 26), [
            ui.str((0, 6), (2, 5), "┤Mid├"),
            ui.str((2, 2), (1, 4), "dB"),
            ui.str((3, 2), (1, 4), "LP"),
            ui.str((4, 2), (1, 4), "HP"),
            ui.str((5, 2), (1, 4), " ø"),
        ])
        mid.append(ui.edit((2, 6), (1, 8), XO_MID, format=state.db))
        mid.append(ui.edit((3, 6), (1, 8), XO_MID_LP, format=state.hz_int))
        mid.append(ui.edit((3, 16), (1, 6), XO_MID_LP_TYPE))
        mid.append(ui.edit((4, 6), (1, 8), XO_MID_HP, format=state.hz_int))
        mid.append(ui.edit((4, 16), (1, 6), XO_MID_HP_TYPE))
        mid.append(ui.str((5, 6), (1, 6), XO_MID_POL))

        low = ui.box((6, 54), (7, 26), [
            ui.str((0, 6), (2, 5), "┤Low├"),
            ui.str((2, 2), (1, 4), "dB"),
            ui.str((3, 2), (1, 4), "LP"),
            ui.str((4, 2), (1, 4), "HP"),
            ui.str((5, 2), (1, 4), " ø"),
        ])
        low.append(ui.edit((2, 6), (1, 8), XO_LOW, format=state.db))
        low.append(ui.edit((3, 6), (1, 8), XO_LOW_LP, format=state.hz_int))
        low.append(ui.edit((3, 16), (1, 6), XO_LOW_LP_TYPE))
        low.append(ui.edit((4, 6), (1, 8), XO_LOW_HP, format=state.hz_int))
        low.append(ui.edit((4, 16), (1, 6), XO_LOW_HP_TYPE))
        low.append(ui.str((5, 6), (1, 6), XO_LOW_POL))

        self.modules = [high, mid, low]
class settings(ui.view):
    subs = (
        NAME, DEV, CLASS, SW_VER, PRE, 
    )
    loops = ()
    def init(self):
        self.modules = [
            ui.box((6, 0), (9, 80), [
                ui.str((0, 6), (1, 10), "┤Settings├"),
                ui.str((2, 4), (1, 12), "Device Name"),
                ui.str((3, 4), (1, 12), "     Preset"),
                ui.str((4, 4), (1, 12), "Preset Name"),
                ui.str((5, 4), (1, 12), "Device Class"),
                ui.str((6, 4), (1, 12), "Software Ver"),

                ui.edit((2, 20), (1, 20), DEV),
                ui.edit((3, 20), (1, 20), PRE),
                ui.edit((4, 20), (1, 20), NAME),
                ui.str((5, 20), (1, 20), CLASS),
                ui.str((6, 20), (1, 20), SW_VER),
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
            ui.str((0, 0), (1, 20), CLASS),
            ui.str((1, 0), (1, 20), SW_VER),
            ui.title((0, 27), (2, 27), NAME),
            ui.str((1, 65), (1, 20), DEV),
            ui.str((0, 65), (1, 15), TARGET_IP),
            
            ui.str((28, 0), (1, 65), f" [q]uit [m]eters [e]qualizers [c]rossover [s]ettings"),
        ]))
        grid.render()
        state.sub((L_IN, R_IN, DEV, PRE, NAME, CLASS, SW_VER))
    def load_view(view_cls):
        nonlocal view
        if view:
            state.unsub(view.subs)
            grid.destroy(view)
            view = None
        view = view_cls(dims)
        view.init()
        grid.append(view)
        state.sub(view.subs)
    setup(stdscr)
    load_view(meters)
    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_MOUSE:
            _, x, y, _, _ = curses.getmouse()
            grid.click(y, x)
        if not ui.editing:
            if ch == ord('q'):
                break
            elif ch == ord('m'):
                load_view(meters)
            elif ch == ord('e'):
                load_view(equalizers)
            elif ch == ord('c'):
                load_view(crossover)
            elif ch == ord('s'):
                load_view(settings)
        if view:
            if ch != -1:
                view.input(ch)
            state.loop(view.loops)

curses.wrapper(main)