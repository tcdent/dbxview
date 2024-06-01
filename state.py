from . import N, Q

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

def sub():
    Q.append(('sub', DEV.path))
    Q.append(('sub', PRE.path))
    Q.append(('sub', NAME.path))
    Q.append(('sub', CURR_PRE.path))
    Q.append(('sub', L_IN.path))
    Q.append(('sub', R_IN.path))
    Q.append(('asyncget', L_IN_CLIP.path))
    Q.append(('asyncget', R_IN_CLIP.path))

    Q.append(('sub', SH.path))
    Q.append(('sub', SH_.path))
    Q.append(('sub', SS.path))
    Q.append(('sub', SS_.path))
    Q.append(('sub', SS_24.path))
    Q.append(('sub', SS_24_.path))
    Q.append(('sub', SS_36.path))
    Q.append(('sub', SS_36_.path))
    Q.append(('sub', SS_LEVEL.path))
    Q.append(('sub', SS_UPPER.path))
    Q.append(('sub', SS_LOWER.path))
    

    Q.append(('sub', L_HIGH.path))
    Q.append(('sub', MUTE_L_HIGH.path))
    Q.append(('sub', R_HIGH.path))
    Q.append(('sub', MUTE_R_HIGH.path))
    Q.append(('asyncget', LMT_HIGH.path))
    Q.append(('sub', L_MID.path))
    Q.append(('sub', MUTE_L_MID.path))
    Q.append(('sub', R_MID.path))
    Q.append(('sub', MUTE_R_MID.path))
    Q.append(('asyncget', LMT_MID.path))
    Q.append(('sub', L_LOW.path))
    Q.append(('sub', MUTE_L_LOW.path))
    Q.append(('sub', R_LOW.path))
    Q.append(('sub', MUTE_R_LOW.path))
    Q.append(('asyncget', LMT_LOW.path))

def loop():
    #Q.append(('asyncget', SS.path))
    #Q.append(('asyncget', SS_.path))
    Q.append(('asyncget', SS_LEVEL.path))
    Q.append(('asyncget', SS_UPPER.path))
    Q.append(('asyncget', SS_LOWER.path))
