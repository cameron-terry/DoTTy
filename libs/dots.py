import numpy as np
import time, sys

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
        return 1
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
        return 1
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
        return 1
    block = int(round(barLength*progress))
    text = "\rWorking: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), round(progress*100, 2), status)
    sys.stdout.write(text)
    sys.stdout.flush()
    
    return 0

class DotBlock:
    def __init__(self, x, y, img):
        # convert chunked values to braille text
        self.values = {         
            "BLANK"       : [[False, False, False, False, False, False, False, False], '⣿'],
            "8"           : [[False, False, False, False, False, False, False, True], '⡿'],
            "7"           : [[False, False, False, False, False, False, True, False], '⢿'],
            "78"          : [[False, False, False, False, False, False, True, True], '⠿'],
            "6"           : [[False, False, False, False, False, True, False, False], '⣟'],
            "68"          : [[False, False, False, False, False, True, False, True], '⡟'],
            "67"          : [[False, False, False, False, False, True, True, False], '⢟'],
            "678"         : [[False, False, False, False, False, True, True, True], '⠟'],
            "5"           : [[False, False, False, False, True, False, False, False], '⣻'],
            "58"          : [[False, False, False, False, True, False, False, True], '⡻'],
            "57"          : [[False, False, False, False, True, False, True, False], '⢻'],
            "578"         : [[False, False, False, False, True, False, True, True], '⠻'],
            "56"          : [[False, False, False, False, True, True, False, False], '⣛'],
            "568"         : [[False, False, False, False, True, True, False, True], '⡛'],
            "567"         : [[False, False, False, False, True, True, True, False], '⢛'],
            "5678"        : [[False, False, False, False, True, True, True, True], '⠛'],
            "4"           : [[False, False, False, True, False, False, False, False], '⣯'],
            "48"          : [[False, False, False, True, False, False, False, True], '⡯'],
            "47"          : [[False, False, False, True, False, False, True, False], '⢯'],
            "478"         : [[False, False, False, True, False, False, True, True], '⠯'],
            "46"          : [[False, False, False, True, False, True, False, False], '⣏'],
            "468"         : [[False, False, False, True, False, True, False, True], '⡏'],
            "467"         : [[False, False, False, True, False, True, True, False], '⢏'],
            "4678"        : [[False, False, False, True, False, True, True, True], '⠏'],
            "45"          : [[False, False, False, True, True, False, False, False], '⣫'],
            "458"         : [[False, False, False, True, True, False, False, True], '⡫'],
            "457"         : [[False, False, False, True, True, False, True, False], '⢫'],
            "4578"        : [[False, False, False, True, True, False, True, True], '⠫'],
            "456"         : [[False, False, False, True, True, True, False, False], '⣋'],
            "4568"        : [[False, False, False, True, True, True, False, True], '⡋'],
            "4567"        : [[False, False, False, True, True, True, True, False], '⢋'],
            "45678"        : [[False, False, False, True, True, True, True, True], '⠋'],
            "3"           : [[False, False, True, False, False, False, False, False], '⣽'],
            "38"          : [[False, False, True, False, False, False, False, True], '⡽'],
            "37"          : [[False, False, True, False, False, False, True, False], '⢽'],
            "378"         : [[False, False, True, False, False, False, True, True], '⠽'],
            "36"          : [[False, False, True, False, False, True, False, False], '⣝'],
            "368"         : [[False, False, True, False, False, True, False, True], '⡝'],
            "367"         : [[False, False, True, False, False, True, True, False], '⢝'],
            "3678"        : [[False, False, True, False, False, True, True, True], '⠝'],
            "35"          : [[False, False, True, False, True, False, False, False], '⣹'],
            "358"         : [[False, False, True, False, True, False, False, True], '⡹'],
            "357"         : [[False, False, True, False, True, False, True, False], '⢹'],
            "3578"        : [[False, False, True, False, True, False, True, True], '⠹'],
            "356"         : [[False, False, True, False, True, True, False, False], '⣙'],
            "3568"        : [[False, False, True, False, True, True, False, True], '⡙'],
            "3567"        : [[False, False, True, False, True, True, True, False], '⢙'],
            "35678"       : [[False, False, True, False, True, True, True, True], '⠙'],
            "34"          : [[False, False, True, True, False, False, False, False], '⣭'],
            "348"         : [[False, False, True, True, False, False, False, True], '⡭'],
            "347"         : [[False, False, True, True, False, False, True, False], '⢭'],
            "3478"        : [[False, False, True, True, False, False, True, True], '⠭'],
            "346"         : [[False, False, True, True, False, True, False, False], '⣍'],
            "3468"        : [[False, False, True, True, False, True, False, True], '⡍'],
            "3467"        : [[False, False, True, True, False, True, True, False], '⢍'],
            "34678"       : [[False, False, True, True, False, True, True, True], '⠍'],
            "345"         : [[False, False, True, True, True, False, False, False], '⣩'],
            "3458"        : [[False, False, True, True, True, False, False, True], '⡩'],
            "3457"        : [[False, False, True, True, True, False, True, False], '⢩'],
            "34578"       : [[False, False, True, True, True, False, True, True], '⠩'],
            "3456"        : [[False, False, True, True, True, True, False, False], '⣉'],
            "34568"       : [[False, False, True, True, True, True, False, True], '⡉'],
            "34567"       : [[False, False, True, True, True, True, True, False], '⢉'],
            "345678"      : [[False, False, True, True, True, True, True, True], '⠉'],
            "2"           : [[False, True, False, False, False, False, False, False], '⣷'],
            "28"          : [[False, True, False, False, False, False, False, True], '⡷'],
            "27"          : [[False, True, False, False, False, False, True, False], '⢷'],
            "278"         : [[False, True, False, False, False, False, True, True], '⠷'],
            "26"          : [[False, True, False, False, False, True, False, False], '⣗'],
            "268"         : [[False, True, False, False, False, True, False, True], '⡗'],
            "267"         : [[False, True, False, False, False, True, True, False], '⢖'],
            "2678"        : [[False, True, False, False, False, True, True, True], '⠗'],
            "25"          : [[False, True, False, False, True, False, False, False], '⣳'],
            "258"         : [[False, True, False, False, True, False, False, True], '⡳'],
            "257"         : [[False, True, False, False, True, False, True, False], '⢳'],
            "2578"        : [[False, True, False, False, True, False, True, True], '⠳'],
            "256"         : [[False, True, False, False, True, True, False, False], '⣓'],
            "2568"        : [[False, True, False, False, True, True, False, True], '⡓'],
            "2567"        : [[False, True, False, False, True, True, True, False], '⢓'],
            "25678"       : [[False, True, False, False, True, True, True, True], '⠓'],
            "24"          : [[False, True, False, True, False, False, False, False], '⣧'],
            "248"         : [[False, True, False, True, False, False, False, True], '⡧'],
            "247"         : [[False, True, False, True, False, False, True, False], '⢧'],
            "2478"        : [[False, True, False, True, False, False, True, True], '⠧'],
            "246"         : [[False, True, False, True, False, True, False, False], '⣇'],
            "2468"        : [[False, True, False, True, False, True, False, True], '⡇'],
            "2467"        : [[False, True, False, True, False, True, True, False], '⢇'],
            "24678"       : [[False, True, False, True, False, True, True, True], '⠇'],
            "245"         : [[False, True, False, True, True, False, False, False], '⣣'],
            "2458"        : [[False, True, False, True, True, False, False, True], '⡣'],
            "2457"        : [[False, True, False, True, True, False, True, False], '⢣'],
            "24578"       : [[False, True, False, True, True, False, True, True], '⠣'],
            "2456"        : [[False, True, False, True, True, True, False, False], '⣃'],
            "24568"       : [[False, True, False, True, True, True, False, True], '⡃'],
            "24567"       : [[False, True, False, True, True, True, True, False], '⢃'],
            "245678"      : [[False, True, False, True, True, True, True, True], '⠃'],
            "23"          : [[False, True, True, False, False, False, False, False], '⣵'],
            "238"         : [[False, True, True, False, False, False, False, True], '⡵'],
            "237"         : [[False, True, True, False, False, False, True, False], '⢵'],
            "2378"        : [[False, True, True, False, False, False, True, True], '⠵'],
            "236"         : [[False, True, True, False, False, True, False, False], '⣕'],
            "2368"        : [[False, True, True, False, False, True, False, True], '⡕'],
            "2367"        : [[False, True, True, False, False, True, True, False], '⢕'],
            "23678"       : [[False, True, True, False, False, True, True, True], '⠕'],
            "235"         : [[False, True, True, False, True, False, False, False], '⣱'],
            "2358"        : [[False, True, True, False, True, False, False, True], '⡱'],
            "2357"        : [[False, True, True, False, True, False, True, False], '⢱'],
            "23578"       : [[False, True, True, False, True, False, True, True], '⠱'],
            "2356"        : [[False, True, True, False, True, True, False, False], '⣑'],
            "23568"       : [[False, True, True, False, True, True, False, True], '⡑'],
            "23567"       : [[False, True, True, False, True, True, True, False], '⢑'],
            "235678"      : [[False, True, True, False, True, True, True, True], '⠑'],
            "234"         : [[False, True, True, True, False, False, False, False], '⣥'],
            "2348"        : [[False, True, True, True, False, False, False, True], '⡥'],
            "2347"        : [[False, True, True, True, False, False, True, False], '⢥'],
            "23478"       : [[False, True, True, True, False, False, True, True], '⠥'],
            "2346"        : [[False, True, True, True, False, True, False, False], '⣅'],
            "23468"       : [[False, True, True, True, False, True, False, True], '⡅'],
            "23467"       : [[False, True, True, True, False, True, True, False], '⢅'],
            "234678"      : [[False, True, True, True, False, True, True, True], '⠡'],
            "2345"        : [[False, True, True, True, True, False, False, False], '⣡'],
            "23458"       : [[False, True, True, True, True, False, False, True], '⡡'],
            "23457"       : [[False, True, True, True, True, False, True, False], '⢡'],
            "234578"      : [[False, True, True, True, True, False, True, True], '⠡'],
            "23456"       : [[False, True, True, True, True, True, False, False], '⣁'],
            "234568"      : [[False, True, True, True, True, True, False, True], '⡁'],
            "234567"      : [[False, True, True, True, True, True, True, False], '⢁'],
            "2345678"     : [[False, True, True, True, True, True, True, True], '⠁'],
            "1"           : [[True, False, False, False, False, False, False, False], '⣾'],
            "18"          : [[True, False, False, False, False, False, False, True], '⡾'],
            "17"          : [[True, False, False, False, False, False, True, False], '⢾'],
            "178"         : [[True, False, False, False, False, False, True, True], '⠾'],
            "16"          : [[True, False, False, False, False, True, False, False], '⣞'],
            "168"         : [[True, False, False, False, False, True, False, True], '⡞'],
            "167"         : [[True, False, False, False, False, True, True, False], '⢞'],
            "1678"        : [[True, False, False, False, False, True, True, True], '⠞'],
            "15"          : [[True, False, False, False, True, False, False, False], '⣺'],
            "158"         : [[True, False, False, False, True, False, False, True], '⡺'],
            "157"         : [[True, False, False, False, True, False, True, False], '⢺'],
            "1578"        : [[True, False, False, False, True, False, True, True], '⠺'],
            "156"         : [[True, False, False, False, True, True, False, False], '⣚'],
            "1568"        : [[True, False, False, False, True, True, False, True], '⡚'],
            "1567"        : [[True, False, False, False, True, True, True, False], '⢚'],
            "15678"       : [[True, False, False, False, True, True, True, True], '⠚'],
            "14"          : [[True, False, False, True, False, False, False, False], '⣮'],
            "148"         : [[True, False, False, True, False, False, False, True], '⡮'],
            "147"         : [[True, False, False, True, False, False, True, False], '⢮'],
            "1478"        : [[True, False, False, True, False, False, True, True], '⠮'],
            "146"         : [[True, False, False, True, False, True, False, False], '⣎'],
            "1468"        : [[True, False, False, True, False, True, False, True], '⡎'],
            "1467"        : [[True, False, False, True, False, True, True, False], '⢎'],
            "14678"       : [[True, False, False, True, False, True, True, True], '⠎'],
            "145"         : [[True, False, False, True, True, False, False, False], '⣪'],
            "1458"        : [[True, False, False, True, True, False, False, True], '⡪'],
            "1457"        : [[True, False, False, True, True, False, True, False], '⢪'],
            "14578"       : [[True, False, False, True, True, False, True, True], '⠪'],
            "1456"        : [[True, False, False, True, True, True, False, False], '⣊'],
            "14568"       : [[True, False, False, True, True, True, False, True], '⡊'],
            "14567"       : [[True, False, False, True, True, True, True, False], '⢊'],
            "145678"      : [[True, False, False, True, True, True, True, True], '⠊'],
            "13"          : [[True, False, True, False, False, False, False, False], '⣼'],
            "138"         : [[True, False, True, False, False, False, False, True], '⡼'],
            "137"         : [[True, False, True, False, False, False, True, False], '⢼'],
            "1378"        : [[True, False, True, False, False, False, True, True], '⠼'],
            "136"         : [[True, False, True, False, False, True, False, False], '⣜'],
            "1368"        : [[True, False, True, False, False, True, False, True], '⡜'],
            "1367"        : [[True, False, True, False, False, True, True, False], '⢜'],
            "13678"       : [[True, False, True, False, False, True, True, True], '⠜'],
            "135"         : [[True, False, True, False, True, False, False, False], '⣸'],
            "1358"        : [[True, False, True, False, True, False, False, True], '⡸'],
            "1357"        : [[True, False, True, False, True, False, True, False], '⢸'],
            "13578"       : [[True, False, True, False, True, False, True, True], '⠸'],
            "1356"        : [[True, False, True, False, True, True, False, False], '⣘'],
            "13568"       : [[True, False, True, False, True, True, False, True], '⡘'],
            "13567"       : [[True, False, True, False, True, True, True, False], '⢘'],
            "135678"      : [[True, False, True, False, True, True, True, True], '⠘'],
            "134"         : [[True, False, True, True, False, False, False, False], '⣬'],
            "1348"        : [[True, False, True, True, False, False, False, True], '⡬'],
            "1347"        : [[True, False, True, True, False, False, True, False], '⢬'],
            "13478"       : [[True, False, True, True, False, False, True, True], '⠬'],
            "1346"        : [[True, False, True, True, False, True, False, False], '⣌'],
            "13468"       : [[True, False, True, True, False, True, False, True], '⡌'],
            "13467"       : [[True, False, True, True, False, True, True, False], '⢌'],
            "134678"      : [[True, False, True, True, False, True, True, True], '⠌'],
            "1345"        : [[True, False, True, True, True, False, False, False], '⣨'],
            "13458"       : [[True, False, True, True, True, False, False, True], '⡨'],
            "13457"       : [[True, False, True, True, True, False, True, False], '⢨'],
            "134578"      : [[True, False, True, True, True, False, True, True], '⠨'],
            "13456"       : [[True, False, True, True, True, True, False, False], '⣈'],
            "134568"      : [[True, False, True, True, True, True, False, True], '⡈'],
            "134567"      : [[True, False, True, True, True, True, True, False], '⢈'],
            "1345678"     : [[True, False, True, True, True, True, True, True], '⠈'],
            "12"          : [[True, True, False, False, False, False, False, False], '⣶'],
            "128"         : [[True, True, False, False, False, False, False, True], '⡶'],
            "127"         : [[True, True, False, False, False, False, True, False], '⢶'],
            "1278"        : [[True, True, False, False, False, False, True, True], '⠶'],
            "126"         : [[True, True, False, False, False, True, False, False], '⣖'],
            "1268"        : [[True, True, False, False, False, True, False, True], '⡖'],
            "1267"        : [[True, True, False, False, False, True, True, False], '⢖'],
            "12678"       : [[True, True, False, False, False, True, True, True], '⠖'],
            "125"         : [[True, True, False, False, True, False, False, False], '⣲'],
            "1258"        : [[True, True, False, False, True, False, False, True], '⡲'],
            "1257"        : [[True, True, False, False, True, False, True, False], '⢲'],
            "12578"       : [[True, True, False, False, True, False, True, True], '⠲'],
            "1256"        : [[True, True, False, False, True, True, False, False], '⣒'],
            "12568"       : [[True, True, False, False, True, True, False, True], '⡒'],
            "12567"       : [[True, True, False, False, True, True, True, False], '⢒'],
            "125678"      : [[True, True, False, False, True, True, True, True], '⠒'],
            "124"         : [[True, True, False, True, False, False, False, False], '⣦'],
            "1248"        : [[True, True, False, True, False, False, False, True], '⡦'],
            "1247"        : [[True, True, False, True, False, False, True, False], '⢦'],
            "12478"       : [[True, True, False, True, False, False, True, True], '⠦'],
            "1246"        : [[True, True, False, True, False, True, False, False], '⣆'],
            "12468"       : [[True, True, False, True, False, True, False, True], '⡆'],
            "12467"       : [[True, True, False, True, False, True, True, False], '⢅'],
            "124678"      : [[True, True, False, True, False, True, True, True], '⠆'],
            "1245"        : [[True, True, False, True, True, False, False, False], '⣢'],
            "12458"       : [[True, True, False, True, True, False, False, True], '⡢'],
            "12457"       : [[True, True, False, True, True, False, True, False], '⢢'],
            "124578"      : [[True, True, False, True, True, False, True, True], '⠢'],
            "12456"       : [[True, True, False, True, True, True, False, False], '⣂'],
            "124568"      : [[True, True, False, True, True, True, False, True], '⡂'],
            "124567"      : [[True, True, False, True, True, True, True, False], '⢂'],
            "1245678"     : [[True, True, False, True, True, True, True, True], '⠂'],
            "123"         : [[True, True, True, False, False, False, False, False], '⣴'],
            "1238"        : [[True, True, True, False, False, False, False, True], '⡴'],
            "1237"        : [[True, True, True, False, False, False, True, False], '⢴'],
            "12378"       : [[True, True, True, False, False, False, True, True], '⠴'],
            "1236"        : [[True, True, True, False, False, True, False, False], '⣔'],
            "12368"       : [[True, True, True, False, False, True, False, True], '⡔'],
            "12367"       : [[True, True, True, False, False, True, True, False], '⢔'],
            "123678"      : [[True, True, True, False, False, True, True, True], '⠔'],
            "1235"        : [[True, True, True, False, True, False, False, False], '⣰'],
            "12358"       : [[True, True, True, False, True, False, False, True], '⡰'],
            "12357"       : [[True, True, True, False, True, False, True, False], '⢰'],
            "123578"      : [[True, True, True, False, True, False, True, True], '⠰'],
            "12356"       : [[True, True, True, False, True, True, False, False], '⣐'],
            "123568"      : [[True, True, True, False, True, True, False, True], '⡐'],
            "123567"      : [[True, True, True, False, True, True, True, False], '⢐'],
            "1235678"     : [[True, True, True, False, True, True, True, True], '⠐'],
            "1234"        : [[True, True, True, True, False, False, False, False], '⣤'],
            "12348"       : [[True, True, True, True, False, False, False, True], '⡤'],
            "12347"       : [[True, True, True, True, False, False, True, False], '⢤'],
            "123478"      : [[True, True, True, True, False, False, True, True], '⠤'],
            "12346"       : [[True, True, True, True, False, True, False, False], '⣄'],
            "123468"      : [[True, True, True, True, False, True, False, True], '⡄'],
            "123467"      : [[True, True, True, True, False, True, True, False], '⢄'],
            "1234678"     : [[True, True, True, True, False, True, True, True], '⡄'],
            "12345"       : [[True, True, True, True, True, False, False, False], '⣠'],
            "123458"      : [[True, True, True, True, True, False, False, True], '⡠'],
            "123457"      : [[True, True, True, True, True, False, True, False], '⢠'],
            "1234578"     : [[True, True, True, True, True, False, True, True], '⠠'],
            "123456"      : [[True, True, True, True, True, True, False, False], '⣀'],
            "1234568"     : [[True, True, True, True, True, True, False, True], '⡀'],
            "1234567"     : [[True, True, True, True, True, True, True, False], '⢀'],
            "12345678"    : [[True, True, True, True, True, True, True, True], ' ']
        }

        # set cols, rows
        self.X = x
        self.Y = y
        self.I = img
    
    def convert(self, filename, debug=False):
        k = 0

        with open(filename, 'w') as f:
            print("[*] Writing to {}...\n".format(filename))
            show_progress = True
            done = False
            # chunk the image
            for i in range(0, self.Y // 4): # rows of braille unicode
                for j in range(0, self.X // 2, 2): # cols of braille unicode
                    if show_progress:
                        show_progress = True if update_progress(((i*4 + 4) / self.Y)) == 0 else False
                    else:
                        if not done:
                            block = int(round(10*1))
                            status = "SUCCESS!     \r\n"
                            text = "\rWorking: [{0}] {1}% {2}".format("#"*block + "-"*(10-block), 1*100, status)
                            sys.stdout.write(text)
                            sys.stdout.flush()
                            done = True
                    '''
                    The file is analyzed in chunks: ... x x ...
                                                    ... x x ...
                                                    ... x x ...
                                                    ... x x ...
                    '''
                    k += 1
                    chunk = [
                        self.I[i * 4][j * 2],       self.I[i * 4][j * 2 + 1],
                        self.I[i * 4 + 1][j * 2], self.I[i * 4 + 1][j * 2 + 1],
                        self.I[i * 4 + 2][j * 2], self.I[i * 4 + 2][j * 2 + 1],
                        self.I[i * 4 + 3][j * 2], self.I[i * 4 + 3][j * 2 + 1],            
                    ]

                    for pattern in self.values:               
                        if np.array_equal(chunk, self.values[pattern][0]):
                            if debug:
                                print(self.values[pattern][1], end="")
                            
                            f.write(self.values[pattern][1])
                            

                if debug:
                    print("\n")
                
                f.write("\n")

        print("\n[+] Output sent to {}.".format(filename))
    