import re, math
from . import N, Q, Node, log

"""
unsub \"\\\\Preset\\SignalGenerator\\SV\\Signal Generator\\\"\n"
unsub \"\\\\Preset\\Afs\\SV\\AFS\\\"\n
unsub \"\\\\Preset\\StereoGEQ\\SV\\GraphicEQ\\\"\n
unsub \"\\\\Preset\\LeftGEQ\\SV\\GraphicEQ\\\"\n"
unsub \"\\\\Storage\\Presets\\SV\\Name_13\\\"\n"
unsub \"\\\\Preset\\RightGEQ\\SV\\GraphicEQ\\\"\n
unsub \"\\\\Preset\\RoomEQ\\SV\\ParametricEQ\\\"\n
unsub \"\\\\Preset\\SubharmonicSynth\\SV\\SubharmonicSynth\\\"\n"
unsub \"\\\\Preset\\Compressor\\SV\\Compressor\\\"\n
unsub \"\\\\Preset\\Back Line Delay\\SV\\Delay\\\"\n
unsub \"\\\\Preset\\High Outputs PEQ\\SV\\ParametricEQ\\\"\n"
unsub \"\\\\Preset\\High Outputs Limiter\\SV\\Limiter\\\"\n
unsub \"\\\\Preset\\High Outputs Delay\\SV\\Delay\\\"\n
unsub \"\\\\Preset\\Mid Outputs PEQ\\SV\\ParametricEQ\\\"\n
unsub \"\\\\Preset\\Mid Outputs Limiter\\SV\\Limiter\\\"\n
unsub \"\\\\Preset\\Mid Outputs Delay\\SV\\Delay\\\"\n
unsub \"\\\\Preset\\Low Outputs PEQ\\SV\\ParametricEQ\\\"\n
unsub \"\\\\Preset\\Low Outputs Limiter\\SV\\Limiter\\\"\n
unsub \"\\\\Preset\\Low Outputs Delay\\SV\\Delay\\\"\n"

sub \"\\\\Preset\\SubharmonicSynth\\SV\\Subharmonics\\\"\n"
sub \"\\\\Preset\\SubharmonicSynth\\SV\\Subharmonics\\%\"\n"
sub \"\\\\Preset\\SubharmonicSynth\\SV\\Synthesis Level 36-56Hz\\\"\n"
subr "\\Preset\SubharmonicSynth\SV\SubharmonicSynth" "On"
set "\\Preset\SubharmonicSynth\SV\SubharmonicSynth" "Off"
set "\\Preset\SubharmonicSynth\SV\SubharmonicSynth" "On"
"""

DEV = N['Node']['SV']['DeviceName']
PRE = N['Storage']['Presets']['SV']['CurrentPreset']
NAME = N['Storage']['Presets']['SV']['Name_13'] # TODO
CURR_PRE = N['Storage']['Presets']['SV']['CurrentPreset']

L_IN = N['Preset']['InputMeters']['SV']['LeftInput']
R_IN = N['Preset']['InputMeters']['SV']['RightInput']
L_IN_CLIP = N['Preset']['InputMeters']['SV']['LeftInputClip']
R_IN_CLIP = N['Preset']['InputMeters']['SV']['RightInputClip']

L_HIGH = N['Preset']['OutputMeters']['SV']['HighLeftOutput']
MUTE_L_HIGH = N['Preset']['OutputGains']['SV']['HighLeftOutputMute']
R_HIGH = N['Preset']['OutputMeters']['SV']['HighRightOutput']
MUTE_R_HIGH = N['Preset']['OutputGains']['SV']['HighRightOutputMute']
LMT_HIGH = N['Preset']['HighOutputsLimiter']['SV']['ThresholdMeter']
L_MID = N['Preset']['OutputMeters']['SV']['MidLeftOutput']
MUTE_L_MID = N['Preset']['OutputGains']['SV']['MidLeftOutputMute']
R_MID = N['Preset']['OutputMeters']['SV']['MidRightOutput']
MUTE_R_MID = N['Preset']['OutputGains']['SV']['MidRightOutputMute']
LMT_MID = N['Preset']['MidOutputsLimiter']['SV']['ThresholdMeter']
L_LOW = N['Preset']['OutputMeters']['SV']['LowLeftOutput']
MUTE_L_LOW = N['Preset']['OutputGains']['SV']['LowLeftOutputMute']
R_LOW = N['Preset']['OutputMeters']['SV']['LowRightOutput']
MUTE_R_LOW = N['Preset']['OutputGains']['SV']['LowRightOutputMute']
LMT_LOW = N['Preset']['LowOutputsLimiter']['SV']['ThresholdMeter']

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

# High Parametic EQ
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

# Mid Parametic EQ
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

# Low Parametic EQ
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

# ie. -117.4dB
RE_DB = re.compile(r'(-?\d+\.\d+)dB')
def db(value: str) -> float:
    match = RE_DB.match(value)
    return float(match.group(1)) if match else 0.0
def db_int(value: str) -> int:
    return round(db(value))
def db_pc(value: str) -> float:
    return (db(value) + 120) / 120 * 100
def pc(value: str) -> float:
    return float(value[:-1])
RE_HZ = re.compile(r'(\d+\.\d+)Hz')
def hz(value: str) -> float:
    match = RE_HZ.match(value)
    return float(match.group(1)) if match else 0.0
def pc_hz(value: str) -> int:
    return round(10 ** ((pc(value) / 100) * (math.log10(20000) - math.log10(20)) + math.log10(20)))
def hz_pc(value: float) -> str:
    return (math.log10(float(value)) - math.log10(20)) / (math.log10(20000) - math.log10(20)) * 100
def onoff(value: str) -> bool:
    return value == 'On'

def sub(nodes: list[Node]):
    Q.extend([('sub', node.path) for node in nodes])
def unsub(nodes: list[Node]):
    Q.extend([('unsub', node.path) for node in nodes])
def loop(nodes: list):
    Q.extend([('asyncget', node.path) for node in nodes])