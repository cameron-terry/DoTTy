import sys, os

from pichandler import ImageConv
from helpers import *

try:
    leave_size = False
    debug = False

    flags = ["-d", "-l", "-n", "s",
             "-dl", "-ld", "-nd", "-dn", "-nl", "-ln", "-ds", "-ls", "-ns", "-sn", "-sl", "-sd",
             "-dln", "-dnl", "-dsl", "-dls", "-dsn", "-dns", "-ldn", "-lnd", "-lds", "-lsd", "-lsn", "-lns",
             "-ndl", "-nld", "-nsl", "-nls", "-nds", "-nsd", "-sdl", "-sld", "-snd", "-sdn", "-sln", "-snl",
             "-d1", "-l1", "-n1", "s1",
             "-dl1", "-ld1", "-nd1", "-dn1", "-nl1", "-ln1", "-ds1", "-ls1", "-ns1", "-sn1", "-sl1", "-sd1",
             "-dln1", "-dnl1", "-dsl1", "-dls1", "-dsn1", "-dns1", "-ldn1", "-lnd1", "-lds1", "-lsd1", "-lsn1", "-lns1",
             "-ndl1", "-nld1", "-nsl1", "-nls1", "-nds1", "-nsd1", "-sdl1", "-sld1", "-snd1", "-sdn1", "-sln1", "-snl1"]

    if len(sys.argv) > 5:
        die('''
        Usage: python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [[args][res]]
        args: -d --> debug (print output to console)
              -l --> leave size (adjusts png minimally)
              -n --> no invert (inverts image colors by default)
              -s --> slow mode (old method of converting)
            You can combine them as follows: -dl, -ld, -dn, -lnd, etc...
        res: 
            1 --> self.RESOLUTION_FACTOR = 1 (no stretch)
                  self.RESOLUTION_FACTOR = 2 (transpose, default)
        ''')
    elif len(sys.argv) == 5 and ((sys.argv[1] in flags) or (sys.argv[2] in flags) \
                                                                            or (sys.argv[3] in flags)):
        die("[!] Please specify path, output file, and size before flags.")
    elif len(sys.argv) == 5:
        valid_flags = sys.argv[4] in flags

        if not valid_flags:
                die('''
                Usage: python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [args]
                args: -d --> debug (print output to console)
                    -l --> leave size (adjusts png minimally)
                    -n --> no invert (inverts image colors by default)
                    -s --> slow mode (old method of converting)
                    You can combine them as follows: -dl, -ld, -dn, -lnd, etc...
                res: 
                    1 --> self.RESOLUTION_FACTOR = 1 (no stretch)
                          self.RESOLUTION_FACTOR = 2 (transpose, default)
                ''')
        else:
            try:
                leave_size = "l" in sys.argv[4]
                debug      = "d" in sys.argv[4]
                invert     = "n" not in sys.argv[4]
                slow_mode  = "s" in sys.argv[4]
                res_mode   = 1 if "1" in sys.argv[4] else 2

                ic = ImageConv(sys.argv[1], filename=sys.argv[2], size=( int(sys.argv[3].split(",")[0]), 
                                                                        int(sys.argv[3].split(",")[1]) ), 
                                                                     leave_size=leave_size, debug=debug, invert=invert, slow_mode=slow_mode, res_mode=res_mode)
            except ValueError:
                ic = ImageConv(sys.argv[1], filename=sys.argv[3], size=( int(sys.argv[2].split(",")[0]), 
                                                                        int(sys.argv[2].split(",")[1]) ), 
                                                                     leave_size=leave_size, debug=debug, invert=invert, slow_mode=slow_mode, res_mode=res_mode)
            except IOError:
                die("[!] Operation failed!\n[!] File could not be written.\
                    \n[*] The file may have been created, and may contain partial data.")
    elif len(sys.argv) == 4:
        valid_flags = sys.argv[3] in flags
        if not valid_flags:
            try:
                ic = ImageConv( sys.argv[1], filename=sys.argv[2], size=( int(sys.argv[3].split(",")[0]), 
                                                                        int(sys.argv[3].split(",")[1]) ) )
            except ValueError:
                die("[!] Operation failed!\n[!] Bad arguments for size")
            except IOError:
                die("[!] Operation failed!\n[!] File could not be written.\
                    \n[*] The file may have been created, and may contain partial data.")
        else:
            try:
                leave_size = "l" in sys.argv[3]
                debug      = "d" in sys.argv[3]
                invert     = "n" not in sys.argv[3]
                slow_mode  = "s" in sys.argv[3]
                res_mode   = 1 if "1" in sys.argv[3] else 2

                ic = ImageConv( sys.argv[1], size=( int(sys.argv[2].split(",")[0]), 
                                                    int(sys.argv[2].split(",")[1]) ), 
                                                    leave_size=leave_size, debug=debug, invert=invert, slow_mode=slow_mode, res_mode=res_mode)
            except ValueError:
                try:
                    ic = ImageConv(sys.argv[1], filename=sys.argv[2], leave_size=leave_size, debug=debug, invert=invert, slow_mode=slow_mode, res_mode=res_mode)
                except IOError:
                    die("[!] Operation failed!\n[!] File could not be written.\
                    \n[*] The file may have been created, and may contain partial data.")           
    elif len(sys.argv) == 3:
        valid_flags = sys.argv[2] in flags
        if not valid_flags:
            try:
                ic = ImageConv( sys.argv[1], size=( (int(sys.argv[2].split(",")[0]), 
                                                    int(sys.argv[2].split(",")[1])) ) )          
            except ValueError:
                try:
                    ic = ImageConv(sys.argv[1], filename=sys.argv[2])
                except IOError:
                    die("[!] Operation failed!\n[!] File could not be written.\
                    \n[*] The file may have been created, and may contain partial data.")
        else:
            try:
                leave_size = "l" in sys.argv[2]
                debug      = "d" in sys.argv[2]
                invert     = "n" not in sys.argv[2]
                slow_mode  = "s" in sys.argv[2]
                res_mode   = 1 if "1" in sys.argv[2] else 2

                ic = ImageConv(sys.argv[1], leave_size=leave_size, debug=debug, invert=invert, slow_mode=slow_mode, res_mode=res_mode)
            except IOError:
                die("[!] Operation failed!\n[!] File could not be written.\
                    \n[*] The file may have been created, and may contain partial data.")
    elif len(sys.argv) == 2:    
        try:
            ic = ImageConv(sys.argv[1])
        except IOError:
            die("[!] Operation failed!\n[!] File could not be written.\
                    \n[*] The file may have been created, and may contain partial data.")
    else:
        die('''
        Usage: python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [args]
        args: -d --> debug (print output to console)
              -l --> leave size (adjusts png minimally)
              -n --> no invert (inverts image colors by default)
              -s --> slow mode (old method of converting)
            You can combine them as follows: -dls, -ld, -dn, -lnd, etc...
        res: 
            1 --> self.RESOLUTION_FACTOR = 1 (no stretch)
                  self.RESOLUTION_FACTOR = 2 (transpose)
        ''')
except KeyboardInterrupt:
    die("\n[!] Process killed by user")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
    

