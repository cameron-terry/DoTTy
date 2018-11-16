import sys, os

from pichandler import ImageConv
from helpers import die

try:
    leave_size = False
    debug = False

    with open('flags.txt', 'r') as f:
        flags = [line.replace('\n', '') for line in f]

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
        valid_flags = sys.argv[4][:-1] in flags

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
                find_res   = [x for x in range(1,10) if str(x) in sys.argv[4]]
                res_mode   = find_res[0] if len(find_res) != 0 else 2
                    
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
        valid_flags = sys.argv[3][:-1] in flags
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
                find_res   = [x for x in range(1,10) if str(x) in sys.argv[3]]
                res_mode   = find_res[0] if len(find_res) != 0 else 2

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
        valid_flags = sys.argv[2][:-1] in flags
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
                find_res   = [x for x in range(1,10) if str(x) in sys.argv[2]]
                res_mode   = find_res[0] if len(find_res) != 0 else 2

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
    

