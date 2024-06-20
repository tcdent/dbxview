import re, math
from . import N, Q, Node, log

RE_DB = re.compile(r'(-?\d+\.\d+)dB')
def db(value: str) -> float:
    match = RE_DB.match(value)
    return float(match.group(1)) if match else 0.0
def db_int(value: str) -> int:
    return round(db(value))
def db_pc(value: str) -> float:
    return (db(value) + 120) / 120 * 100
def pc(value: str) -> float:
    value = value[:-1] if value[-1] == '%' else value
    return float(value)
def pc_int(value: str) -> int:
    return round(pc(value))
RE_HZ = re.compile(r'(\d+\.?\d*)Hz')
RE_KHZ = re.compile(r'(\d+\.?\d*)kHz')
def hz(value: str) -> float:
    try:
        return float(value)
    except ValueError: pass
    match = RE_HZ.match(value)
    if match:
        return float(match.group(1))
    match = RE_KHZ.match(value)
    if match:
        return float(match.group(1)) * 1000
LF_HZ, HF_HZ = 20, 20000 # TODO i think we go lower
LF_HZ_LOG = math.log10(LF_HZ) 
HF_HZ_LOG = math.log10(20000)
def pc_hz(value: str) -> int:
    return round(10 ** ((pc(value) / 100) * (HF_HZ_LOG - LF_HZ_LOG) + LF_HZ_LOG))
def hz_pc(value: float) -> str:
    value = max(hz(value), LF_HZ) 
    return ((math.log10(value) - LF_HZ_LOG) / (HF_HZ_LOG - LF_HZ_LOG)) * 100
def hz_int(value: str) -> int:
    value = hz(value)
    return round(value if value else 0)
def onoff(value: str) -> bool:
    return value == 'On'

def sub(nodes: list[Node]):
    Q.extend([('sub', node.path) for node in nodes])
def unsub(nodes: list[Node]):
    Q.extend([('unsub', node.path) for node in nodes])
def loop(nodes: list):
    Q.extend([('asyncget', node.path) for node in nodes])


# VAR = N['Node']['SV']['Reboot']
# VAR = N['Node']['Config']['SV']['Command']
# VAR = N['Node']['Config']['SV']['Result']
# VAR = N['Node']['Config']['SV']['Progress']
# VAR = N['Node']['Config']['SV']['Command:Status']
# VAR = N['Storage']['Presets']['SV']['CurrentPreset']
# VAR = N['Storage']['Presets']['SV']['Changed']
# VAR = N['Node']['Wizard']['SV']['WizardState']
# VAR = N['Node']['Wizard']['SV']['WizardEvent']
# VAR = N['Node']['Wizard']['SV']['WizardRunAll']
# VAR = N['Node']['Wizard']['SV']['LevelAssistOutput']

DEV = N['Node']['SV']['DeviceName']
CLASS = N['Node']['AT']['Class_Name']
INST = N['Node']['AT']['Instance_Name']
SW_VER = N['Node']['AT']['Software_Version']
HW_VER = N['Node']['SV']['HardwareVersion']
PRE = N['Storage']['Presets']['SV']['CurrentPreset']
NAME = N['Storage']['Presets']['SV']['Name_13'] # TODO 1-20
RATE = N['Node']['BLUX']['SV']['SampleRate']

VAR = N['Preset']['SignalGenerator']['SV']['Signal Generator']
VAR = N['Preset']['StereoGEQ']['SV']['GraphicEQ']
VAR = N['Preset']['LeftGEQ']['SV']['GraphicEQ']
VAR = N['Preset']['RightGEQ']['SV']['GraphicEQ']
VAR = N['Preset']['RoomEQ']['SV']['ParametricEQ']
VAR = N['Preset']['SubharmonicSynth']['SV']['SubharmonicSynth']
VAR = N['Preset']['Back Line Delay']['SV']['Delay']
VAR = N['Preset']['High Outputs PEQ']['SV']['ParametricEQ']
VAR = N['Preset']['High Outputs Limiter']['SV']['Limiter']
VAR = N['Preset']['High Outputs Delay']['SV']['Delay']
VAR = N['Preset']['Mid Outputs PEQ']['SV']['ParametricEQ']
VAR = N['Preset']['Mid Outputs Limiter']['SV']['Limiter']
VAR = N['Preset']['Mid Outputs Delay']['SV']['Delay']
VAR = N['Preset']['Low Outputs PEQ']['SV']['ParametricEQ']
VAR = N['Preset']['Low Outputs Limiter']['SV']['Limiter']
VAR = N['Preset']['Low Outputs Delay']['SV']['Delay']

L_IN = N['Preset']['InputMeters']['SV']['LeftInput']
R_IN = N['Preset']['InputMeters']['SV']['RightInput']
L_IN_CLIP = N['Preset']['InputMeters']['SV']['LeftInputClip']
R_IN_CLIP = N['Preset']['InputMeters']['SV']['RightInputClip']

L_HIGH = N['Preset']['OutputMeters']['SV']['HighLeftOutput']
L_MID = N['Preset']['OutputMeters']['SV']['MidLeftOutput']
L_LOW = N['Preset']['OutputMeters']['SV']['LowLeftOutput']
R_HIGH = N['Preset']['OutputMeters']['SV']['HighRightOutput']
R_MID = N['Preset']['OutputMeters']['SV']['MidRightOutput']
R_LOW = N['Preset']['OutputMeters']['SV']['LowRightOutput']

MUTE_L_HIGH = N['Preset']['OutputGains']['SV']['HighLeftOutputMute']
MUTE_L_MID = N['Preset']['OutputGains']['SV']['MidLeftOutputMute']
MUTE_L_LOW = N['Preset']['OutputGains']['SV']['LowLeftOutputMute']
MUTE_R_HIGH = N['Preset']['OutputGains']['SV']['HighRightOutputMute']
MUTE_R_MID = N['Preset']['OutputGains']['SV']['MidRightOutputMute']
MUTE_R_LOW = N['Preset']['OutputGains']['SV']['LowRightOutputMute']

LMT_LOW = N['Preset']['Low Outputs Limiter']['SV']['ThresholdMeter']
LMT_MID = N['Preset']['Mid Outputs Limiter']['SV']['ThresholdMeter']
LMT_HIGH = N['Preset']['High Outputs Limiter']['SV']['ThresholdMeter']

# Delay
DLY_LOW = N['Preset']['Low Outputs Delay']['SV']['Amount']
DLY_LOW_ = N['Preset']['Low Outputs Delay']['SV']['Amount']['%']
DLY_MID = N['Preset']['Mid Outputs Delay']['SV']['Amount']
DLY_MID_ = N['Preset']['Mid Outputs Delay']['SV']['Amount']['%']
DLY_HIGH = N['Preset']['High Outputs Delay']['SV']['Amount']
DLY_HIGH_ = N['Preset']['High Outputs Delay']['SV']['Amount']['%']

# Crossover
XO_BANDS = N['Preset']['Crossover']['AT']['NumBands']
XO_MONOSUB = N['Preset']['Crossover']['AT']['MonoSub']
XO_INVERT = N['Preset']['Crossover']['SV']['Inverted']
XO_NORMAL = N['Preset']['Crossover']['SV']['Normal']

XO_HIGH = N['Preset']['Crossover']['SV']['Band_1_Gain']
XO_HIGH_ = N['Preset']['Crossover']['SV']['Band_1_Gain']['%']
XO_HIGH_POL = N['Preset']['Crossover']['SV']['Band_1_Polarity']
XO_HIGH_LP = N['Preset']['Crossover']['SV']['Band_1_LPFrequency']
XO_HIGH_LP_ = N['Preset']['Crossover']['SV']['Band_1_LPFrequency']['%']
XO_HIGH_LP_TYPE = N['Preset']['Crossover']['SV']['Band_1_LPType']
XO_HIGH_LP_MAX = N['Preset']['Crossover']['SV']['Band_1_LPType']['Max']
XO_HIGH_LP_MIN = N['Preset']['Crossover']['SV']['Band_1_LPType']['Min']
XO_HIGH_LP_EN = N['Preset']['Crossover']['SV']['Band_1_LPType']['EN']
XO_HIGH_HP = N['Preset']['Crossover']['SV']['Band_1_HPFrequency']
XO_HIGH_HP_ = N['Preset']['Crossover']['SV']['Band_1_HPFrequency']['%']
XO_HIGH_HP_TYPE = N['Preset']['Crossover']['SV']['Band_1_HPType']
XO_HIGH_HP_MAX = N['Preset']['Crossover']['SV']['Band_1_HPType']['Max']
XO_HIGH_HP_MIN = N['Preset']['Crossover']['SV']['Band_1_HPType']['Min']
XO_HIGH_HP_EN = N['Preset']['Crossover']['SV']['Band_1_HPType']['EN']

XO_MID = N['Preset']['Crossover']['SV']['Band_2_Gain']
XO_MID_ = N['Preset']['Crossover']['SV']['Band_2_Gain']['%']
XO_MID_POL = N['Preset']['Crossover']['SV']['Band_2_Polarity']
XO_MID_LP = N['Preset']['Crossover']['SV']['Band_2_LPFrequency']
XO_MID_LP_ = N['Preset']['Crossover']['SV']['Band_2_LPFrequency']['%']
XO_MID_LP_TYPE = N['Preset']['Crossover']['SV']['Band_2_LPType']
XO_MID_LP_MAX = N['Preset']['Crossover']['SV']['Band_2_LPType']['Max']
XO_MID_LP_MIN = N['Preset']['Crossover']['SV']['Band_2_LPType']['Min']
XO_MID_LP_EN = N['Preset']['Crossover']['SV']['Band_2_LPType']['EN']
XO_MID_HP = N['Preset']['Crossover']['SV']['Band_2_HPFrequency']
XO_MID_HP_ = N['Preset']['Crossover']['SV']['Band_2_HPFrequency']['%']
XO_MID_HP_TYPE = N['Preset']['Crossover']['SV']['Band_2_HPType']
XO_MID_HP_MAX = N['Preset']['Crossover']['SV']['Band_2_HPType']['Max']
XO_MID_HP_MIN = N['Preset']['Crossover']['SV']['Band_2_HPType']['Min']
XO_MID_HP_EN = N['Preset']['Crossover']['SV']['Band_2_HPType']['EN']

XO_LOW = N['Preset']['Crossover']['SV']['Band_3_Gain']
XO_LOW_ = N['Preset']['Crossover']['SV']['Band_3_Gain']['%']
XO_LOW_POL = N['Preset']['Crossover']['SV']['Band_3_Polarity']
XO_LOW_LP = N['Preset']['Crossover']['SV']['Band_3_LPFrequency']
XO_LOW_LP_ = N['Preset']['Crossover']['SV']['Band_3_LPFrequency']['%']
XO_LOW_LP_TYPE = N['Preset']['Crossover']['SV']['Band_3_LPType']
XO_LOW_LP_MAX = N['Preset']['Crossover']['SV']['Band_3_LPType']['Max']
XO_LOW_LP_MIN = N['Preset']['Crossover']['SV']['Band_3_LPType']['Min']
XO_LOW_LP_EN = N['Preset']['Crossover']['SV']['Band_3_LPType']['EN']
XO_LOW_HP = N['Preset']['Crossover']['SV']['Band_3_HPFrequency']
XO_LOW_HP_ = N['Preset']['Crossover']['SV']['Band_3_HPFrequency']['%']
XO_LOW_HP_TYPE = N['Preset']['Crossover']['SV']['Band_3_HPType']
XO_LOW_HP_MAX = N['Preset']['Crossover']['SV']['Band_3_HPType']['Max']
XO_LOW_HP_MIN = N['Preset']['Crossover']['SV']['Band_3_HPType']['Min']
XO_LOW_HP_EN = N['Preset']['Crossover']['SV']['Band_3_HPType']['EN']

# Limiters
VAR = N['Preset']['High Outputs Limiter']['SV']['GainReductionMeter']
VAR = N['Preset']['High Outputs Limiter']['SV']['OverEasy']
VAR = N['Preset']['High Outputs Limiter']['SV']['Threshold']
VAR = N['Preset']['High Outputs Limiter']['SV']['Threshold']['%']
VAR = N['Preset']['High Outputs Limiter']['SV']['OverEasy']['%']
VAR = N['Preset']['Mid Outputs Limiter']['SV']['GainReductionMeter']
VAR = N['Preset']['Mid Outputs Limiter']['SV']['OverEasy']
VAR = N['Preset']['Mid Outputs Limiter']['SV']['Threshold']
VAR = N['Preset']['Mid Outputs Limiter']['SV']['Threshold']['%']
VAR = N['Preset']['Mid Outputs Limiter']['SV']['OverEasy']['%']
VAR = N['Preset']['Low Outputs Limiter']['SV']['GainReductionMeter']
VAR = N['Preset']['Low Outputs Limiter']['SV']['OverEasy']
VAR = N['Preset']['Low Outputs Limiter']['SV']['Threshold']
VAR = N['Preset']['Low Outputs Limiter']['SV']['Threshold']['%']
VAR = N['Preset']['Low Outputs Limiter']['SV']['OverEasy']['%']

# Subharmonic Synth
SH = N['Preset']['SubharmonicSynth']['SV']['Subharmonics']
SH_ = N['Preset']['SubharmonicSynth']['SV']['Subharmonics']['%']
SS = N['Preset']['SubharmonicSynth']['SV']['SubharmonicSynth']
SS_ = N['Preset']['SubharmonicSynth']['SV']['SubharmonicSynth']['%']
SS_24 = N['Preset']['SubharmonicSynth']['SV']['Synthesis Level 24-36Hz']
SS_24_ = N['Preset']['SubharmonicSynth']['SV']['Synthesis Level 24-36Hz']['%']
SS_36 = N['Preset']['SubharmonicSynth']['SV']['Synthesis Level 36-56Hz']
SS_36_ = N['Preset']['SubharmonicSynth']['SV']['Synthesis Level 36-56Hz']['%']
SS_LEVEL = N['Preset']['SubharmonicSynth']['SV']['SubSynthLevel']
SS_UPPER = N['Preset']['SubharmonicSynth']['SV']['UpperBandLevel']
SS_LOWER = N['Preset']['SubharmonicSynth']['SV']['LowerBandLevel']

# Parametic EQ
PEQ_HIGH = N['Preset']['High Outputs PEQ']['SV']['ParametricEQ']
PEQ_HIGH_MANUAL = N['Preset']['High Outputs PEQ']['SV']['Manual']
PEQ_HIGH_AUTO = N['Preset']['High Outputs PEQ']['SV']['AutoEQ']
PEQ_HIGH_LO = N['Preset']['High Outputs PEQ']['SV']['Low Shelf']
PEQ_HIGH_HS = N['Preset']['High Outputs PEQ']['SV']['High Shelf']
PEQ_HIGH_FL = N['Preset']['High Outputs PEQ']['SV']['Flatten']
PEQ_HIGH_BELL = N['Preset']['High Outputs PEQ']['SV']['Bell']
PEQ_HIGH_BAND = [None] * 9
for i in range(1, 9):
    PEQ_HIGH_BAND[i] = {
        'type': N['Preset']['High Outputs PEQ']['SV'][f'Band_{i}_Type'],
        'q': N['Preset']['High Outputs PEQ']['SV'][f'Band_{i}_Q'],
        'gain': N['Preset']['High Outputs PEQ']['SV'][f'Band_{i}_Gain'],
        'freq': N['Preset']['High Outputs PEQ']['SV'][f'Band_{i}_Frequency']['%'],
    }

PEQ_MID = N['Preset']['Mid Outputs PEQ']['SV']['ParametricEQ']
PEQ_MID_MANUAL = N['Preset']['Mid Outputs PEQ']['SV']['Manual']
PEQ_MID_AUTO = N['Preset']['Mid Outputs PEQ']['SV']['AutoEQ']
PEQ_MID_LO = N['Preset']['Mid Outputs PEQ']['SV']['Low Shelf']
PEQ_MID_HS = N['Preset']['Mid Outputs PEQ']['SV']['High Shelf']
PEQ_MID_FL = N['Preset']['Mid Outputs PEQ']['SV']['Flatten']
PEQ_MID_BELL = N['Preset']['Mid Outputs PEQ']['SV']['Bell']
PEQ_MID_BAND = [None] * 9
for i in range(1, 9):
    PEQ_MID_BAND[i] = {
        'type': N['Preset']['Mid Outputs PEQ']['SV'][f'Band_{i}_Type'],
        'q': N['Preset']['Mid Outputs PEQ']['SV'][f'Band_{i}_Q'],
        'gain': N['Preset']['Mid Outputs PEQ']['SV'][f'Band_{i}_Gain'],
        'freq': N['Preset']['Mid Outputs PEQ']['SV'][f'Band_{i}_Frequency']['%'],
    }

PEQ_LOW = N['Preset']['Low Outputs PEQ']['SV']['ParametricEQ']
PEQ_LOW_MANUAL = N['Preset']['Low Outputs PEQ']['SV']['Manual']
PEQ_LOW_AUTO = N['Preset']['Low Outputs PEQ']['SV']['AutoEQ']
PEQ_LOW_LO = N['Preset']['Low Outputs PEQ']['SV']['Low Shelf']
PEQ_LOW_HS = N['Preset']['Low Outputs PEQ']['SV']['High Shelf']
PEQ_LOW_FL = N['Preset']['Low Outputs PEQ']['SV']['Flatten']
PEQ_LOW_BELL = N['Preset']['Low Outputs PEQ']['SV']['Bell']
PEQ_LOW_BAND = [None] * 9
for i in range(1, 9):
    PEQ_LOW_BAND[i] = {
        'type': N['Preset']['Low Outputs PEQ']['SV'][f'Band_{i}_Type'],
        'q': N['Preset']['Low Outputs PEQ']['SV'][f'Band_{i}_Q'],
        'gain': N['Preset']['Low Outputs PEQ']['SV'][f'Band_{i}_Gain'],
        'freq': N['Preset']['Low Outputs PEQ']['SV'][f'Band_{i}_Frequency']['%'],
    }

# Graphic EQ
VAR = N['Preset']['StereoGEQ']['SV']['Manual']
VAR = N['Preset']['StereoGEQ']['SV']['DJ']
VAR = N['Preset']['StereoGEQ']['SV']['PerformanceVenue']
VAR = N['Preset']['StereoGEQ']['SV']['Speech']
VAR = N['Preset']['StereoGEQ']['SV']['MyBand']
VAR = N['Preset']['StereoGEQ']['SV']['Flat']
VAR = N['Preset']['StereoGEQ']['SV']['QuickCurve']
VAR = N['Preset']['StereoGEQ']['SV']['20 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['25 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['31']
VAR = N['Preset']['StereoGEQ']['SV']['40 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['50 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['63 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['80 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['100 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['125 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['160 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['200 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['250 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['315 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['400 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['500 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['630 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['800 Hz']
VAR = N['Preset']['StereoGEQ']['SV']['1']
VAR = N['Preset']['StereoGEQ']['SV']['2']
VAR = N['Preset']['StereoGEQ']['SV']['3']
VAR = N['Preset']['StereoGEQ']['SV']['4']
VAR = N['Preset']['StereoGEQ']['SV']['5']
VAR = N['Preset']['StereoGEQ']['SV']['6']
VAR = N['Preset']['StereoGEQ']['SV']['8']
VAR = N['Preset']['StereoGEQ']['SV']['10']
VAR = N['Preset']['StereoGEQ']['SV']['12']
VAR = N['Preset']['StereoGEQ']['SV']['16']
VAR = N['Preset']['StereoGEQ']['SV']['20']


