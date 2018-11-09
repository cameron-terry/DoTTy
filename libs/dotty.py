import sys

from pichandler import ImageConv

def die(message):
    print(message)
    exit(0)

leave_size = False
debug = False

if len(sys.argv) > 5:
    die('''
    Usage: python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [args]
    args: -d --> debug (print output to console)
          -l --> leave size (adjusts png minimally)
          You can combine them as follows: -dl, -ld
    ''')
elif len(sys.argv) == 5 and ((sys.argv[1] in ["-d", "-l", "-dl", "-ld"]) or (sys.argv[2] in ["-d", "-l", "-dl", "-ld"]) \
                                                                         or (sys.argv[3] in ["-d", "-l", "-dl", "-ld"])):
    die("[!] Please specify path, output file, and size before flags.")
elif len(sys.argv) == 5:
    valid_flags = sys.argv[4] in ["-d", "-l", "-dl", "-ld"]

    if not valid_flags:
            die('''
            Usage: python dotty.py <path_to_image> [output_file] [args]
            args: -d --> debug (print output to console)
                -l --> leave size (adjusts png minimally)
                You can combine them as follows: -dl, -ld.
            ''')
    else:
        try:
            leave_size = "l" in sys.argv[4]
            debug      = "d" in sys.argv[4]

            ic = ImageConv(sys.argv[1], filename=sys.argv[2], size=(int(sys.argv[3].split(",")[0]), int(sys.argv[3].split(",")[1])), leave_size=leave_size, debug=debug)
        except IOError:
            die("[!] Operation failed!\n[!] File could either not be found, opened, or created." + 
                    "\n[*] Note: dotty only supports JPEG files.")
elif len(sys.argv) == 4:
    valid_flags = sys.argv[3] in ["-d", "-l", "-dl", "-ld"]
    if not valid_flags:
        try:
            ic = ImageConv(sys.argv[1], filename=sys.argv[2], size=(int(sys.argv[3].split(",")[0]), int(sys.argv[3].split(",")[1])))
        except IOError:
            die("[!] Operation failed!\n[!] File could either not be found, opened, or created." + 
                        "\n[*] Note: dotty only supports JPEG files.")
    else:
        try:
            leave_size = "l" in sys.argv[3]
            debug      = "d" in sys.argv[3]

            ic = ImageConv(sys.argv[1], filename=sys.argv[2], leave_size=leave_size, debug=debug)
        except IOError:
            die("[!] Operation failed!\n[!] File could either not be found, opened, or created." + 
                "\n[*] Note: dotty only supports JPEG files.")
elif len(sys.argv) == 3:
    valid_flags = sys.argv[2] in ["-d", "-l", "-dl", "-ld"]
    if not valid_flags:
        try:
            ic = ImageConv(sys.argv[1], size=((int(sys.argv[2].split(",")[0]), int(sys.argv[2].split(",")[1]))))          
        except ValueError:
            try:
                ic = ImageConv(sys.argv[1], filename=sys.argv[2])
            except IOError:
                die("[!] Operation failed!\n[!] File could either not be found, opened, or created." + 
                    "\n[*] Note: dotty only supports JPEG files.")
    else:
        try:
            leave_size = "l" in sys.argv[2]
            debug      = "d" in sys.argv[2]

            ic = ImageConv(sys.argv[1], leave_size=leave_size, debug=debug)
        except IOError:
            die("[!] Operation failed!\n[!] File could either not be found, opened, or created." + 
                "\n[*] Note: dotty only supports JPEG files.")
elif len(sys.argv) == 2:    
    try:
        ic = ImageConv(sys.argv[1])
    except IOError:
        die("[!] Operation failed!\n[!] File could either not be found, opened, or created." + 
                "\n[*] Note: dotty only supports JPEG files.")
else:
    die('''
    Usage: python dotty.py <path_to_image> [output_file] [args]
    args: -d --> debug (print output to console)
          -l --> leave size (adjusts png minimally)
          You can combine them as follows: -dl, -ld.
    ''')

    

