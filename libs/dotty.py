import sys, os

from pichandler import ImageConv
from helpers import *

try:
    leave_size = False
    debug = False

    flags = ["-d", "-l", "-n", 
             "-dl", "-ld", "-nd", "-dn", "-nl", "-ln",
             "-dln", "-dnl", "-ldn", "-lnd", "-ndl", "-nld"]

    if len(sys.argv) > 5:
        die('''
        Usage: python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [args]
        args: -d --> debug (print output to console)
              -l --> leave size (adjusts png minimally)
              -n --> no invert (inverts image colors by default)
            You can combine them as follows: -dl, -ld, -dn, -lnd, etc...
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
                    You can combine them as follows: -dl, -ld, -dn, -lnd, etc...
                ''')
        else:
            try:
                leave_size = "l" in sys.argv[4]
                debug      = "d" in sys.argv[4]
                invert     = "n" not in sys.argv[4]

                ic = ImageConv(sys.argv[1], filename=sys.argv[2], size=( int(sys.argv[3].split(",")[0]), 
                                                                        int(sys.argv[3].split(",")[1]) ), 
                                                                     leave_size=leave_size, debug=debug, invert=invert)
            except ValueError:
                ic = ImageConv(sys.argv[1], filename=sys.argv[3], size=( int(sys.argv[2].split(",")[0]), 
                                                                        int(sys.argv[2].split(",")[1]) ), 
                                                                     leave_size=leave_size, debug=debug, invert=invert)
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

                ic = ImageConv( sys.argv[1], size=( int(sys.argv[2].split(",")[0]), 
                                                    int(sys.argv[2].split(",")[1]) ), 
                                                    leave_size=leave_size, debug=debug, invert=invert)
            except ValueError:
                try:
                    ic = ImageConv(sys.argv[1], filename=sys.argv[2], leave_size=leave_size, debug=debug, invert=invert)
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

                ic = ImageConv(sys.argv[1], leave_size=leave_size, debug=debug, invert=invert)
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
            You can combine them as follows: -dl, -ld, -dn, -lnd, etc...
        ''')
except KeyboardInterrupt:
    die("\n[!] Process killed by user")
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)
    

