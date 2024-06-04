import os, sys
from pathlib import Path
from . import Node, N

packets = """
0000  00 0f d7 05 3e b2 cc 08 fa ab ab 92 08 00 45 00   ....>.........E.
0010  00 69 00 00 40 00 40 06 b5 c1 c0 a8 01 93 c0 a8   .i..@.@.........
0020  01 ea df f2 4b 48 9b 28 cc 4e 95 44 c6 42 80 18   ....KH.(.N.D.B..
0030  08 00 70 e7 00 00 01 01 08 0a 08 a5 5e 2d 00 00   ..p.........^-..
0040  00 ae 61 73 79 6e 63 67 65 74 20 22 5c 5c 50 72   ..asyncget "\\Pr
0050  65 73 65 74 5c 4f 75 74 70 75 74 4d 65 74 65 72   eset\OutputMeter
0060  73 5c 53 56 5c 48 69 67 68 52 69 67 68 74 4f 75   s\SV\HighRightOu
0070  74 70 75 74 5c 22 0a                              tput\".

0000  cc 08 fa ab ab 92 00 0f d7 05 3e b2 08 00 45 00   ..........>...E.
0010  00 34 9a ba 40 00 40 06 1b 3c c0 a8 01 ea c0 a8   .4..@.@..<......
0020  01 93 4b 48 df f2 95 44 c6 42 9b 28 cc 4e 80 10   ..KH...D.B.(.N..
0030  82 f8 19 40 00 00 01 01 08 0a 00 00 00 ae 08 a5   ...@............
0040  5e 2a                                             ^*

0000  00 0f d7 05 3e b2 cc 08 fa ab ab 92 08 00 45 00   ....>.........E.
0010  00 67 00 00 40 00 40 06 b5 c3 c0 a8 01 93 c0 a8   .g..@.@.........
0020  01 ea df f2 4b 48 9b 28 cc 83 95 44 c6 42 80 18   ....KH.(...D.B..
0030  08 00 f8 06 00 00 01 01 08 0a 08 a5 5e 2d 00 00   ............^-..
0040  00 ae 61 73 79 6e 63 67 65 74 20 22 5c 5c 50 72   ..asyncget "\\Pr
0050  65 73 65 74 5c 4f 75 74 70 75 74 4d 65 74 65 72   eset\OutputMeter
0060  73 5c 53 56 5c 4d 69 64 4c 65 66 74 4f 75 74 70   s\SV\MidLeftOutp
0070  75 74 5c 22 0a                                    ut\".

0000  00 0f d7 05 3e b2 cc 08 fa ab ab 92 08 00 45 00   ....>.........E.
0010  00 dd 00 00 40 00 40 06 b5 4d c0 a8 01 93 c0 a8   ....@.@..M......
0020  01 ea df f2 4b 48 9b 28 cd e0 95 44 c6 42 80 18   ....KH.(...D.B..
0030  08 00 06 2d 00 00 01 01 08 0a 08 a5 5e 3d 00 00   ...-........^=..
0040  00 ae 61 73 79 6e 63 67 65 74 20 22 5c 5c 50 72   ..asyncget "\\Pr
0050  65 73 65 74 5c 49 6e 70 75 74 4d 65 74 65 72 73   eset\InputMeters
0060  5c 53 56 5c 52 69 67 68 74 49 6e 70 75 74 43 6c   \SV\RightInputCl
0070  69 70 5c 22 0a 61 73 79 6e 63 67 65 74 20 22 5c   ip\".asyncget "\
0080  5c 50 72 65 73 65 74 5c 4d 69 64 20 4f 75 74 70   \Preset\Mid Outp
0090  75 74 73 20 4c 69 6d 69 74 65 72 5c 53 56 5c 54   uts Limiter\SV\T
00a0  68 72 65 73 68 6f 6c 64 4d 65 74 65 72 5c 22 0a   hresholdMeter\".
00b0  61 73 79 6e 63 67 65 74 20 22 5c 5c 50 72 65 73   asyncget "\\Pres
00c0  65 74 5c 4d 69 64 20 4f 75 74 70 75 74 73 20 4c   et\Mid Outputs L
00d0  69 6d 69 74 65 72 5c 53 56 5c 54 68 72 65 73 68   imiter\SV\Thresh
00e0  6f 6c 64 4d 65 74 65 72 5c 22 0a                  oldMeter\".
"""

DIR = Path(os.path.dirname(__file__))

def yolo():
    #handle = packets.split('\n')
    handle = open(DIR/'packets.txt', 'r')
    data = ""
    cmds = []
    for line in handle:
        try:
            data += line[56:74].replace("\n", '')
        except IndexError:
            pass
    P, paths = [], []
    for cmdish in data.split('.'):
        if not cmdish: continue
        if len(cmdish) < 5: continue
        print(cmdish)
        cmd, path, value, keys = None, None, None, None
        try:
            cmd, path, value = [x.strip() for x in cmdish.split('"') if x.strip()]
            keys = path.split('\\')[2:]
        except (ValueError, IndexError) as e:
            try:
                cmd, path = [x.strip() for x in cmdish.split('"') if x.strip()]
                keys = path.split('\\')[2:]
            except (ValueError, IndexError) as e:
                print(f"ignored: {cmdish}")
                continue
        except KeyError:
            print(f"ignored: {cmdish}")
        if keys and not path in paths:
            paths.append(path)
            P.append(keys)
    for p in P:
        pp = "']['".join(p)
        print(f"VAR = N['{pp}']")
