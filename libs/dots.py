from numpy import ndarray
import time, sys
import json

from helpers import *

# TODO: there is significant error as the sizes increase (much detail is lost)

class DotBlock:
    """
    Holds image data and can convert image to a series of Braille symbols.

    Attributes:
        x (int): The width of the output image.
        y (int): The height of the output image.
        img (np.array): The image data (black and white).
    """
    def __init__(self, x, y, img, res_mode=2):
        # convert chunked values to braille text
        """
        Initialize size and image data.

        Args:
            x (int): The width of the output image.
            y (int): The height of the output image.

            img(np.array): The image data (black and white).

        The values are organized as follows:\n
        ``... 1 2 ...``\n
        ``... 3 4 ...``\n
        ``... 5 6 ...``\n
        ``... 7 8 ...``\n
        """
        
        with open('unicode_lookup.json', 'r') as fp:
            self.u_braille = json.load(fp)

        # set cols, rows, image
        if isinstance(x, float):
            x = int(x)
        if not isinstance(x, int):
            die("[!] Width must be an int")
        if isinstance(y, float):
            y = int(y)
        if not isinstance(y, int):
            die("[!] Height must be an int")
        if not isinstance(img, ndarray):
            die("[!] Image was not converted properly")

        self.X = x
        self.Y = y
        self.I = img

        self.RESOLUTION_FACTOR = res_mode  # change this to affect how the picture is scaled
        self.CHUNK_SIZE = 8 # constant

        self.stats = [0, 0, 0, 0, 0, 0, 0, 0, 0] # used for statistics
        self.GLOBAL_MERGE_COUNT = 0 # used for merge

    # O(1)
    def gen_key(self, chunk):
        """
        Generates a key.

        Args:
            chunk (bool[]) -- chunk to find key for

        Returns:
            A key in the Unicode dictionary
        """
        # build key
        lookup = ""

        # generate lookup key -- every number either appears once or none     
        lookup = "".join([lookup + str(value+1) if chunk[value] else lookup + "" for value in range(self.CHUNK_SIZE)])
        return lookup

    # O(1)
    def lookup(self, key):
        """
        Gets a Unicode Braille symbol for a given key.

        Args:
            key (str): The symbol's key in unicode_lookup.json

        Returns:
            Unicode Braille symbol
        """
        try:
            chunk_true = len(key) - 1 if len(key) > 0 else 0
            self.stats[chunk_true] += 1
            return self.u_braille[key][1]
        except KeyError:
            return self.u_braille["BLANK"][1]

    # O(1)
    def decode(self, chunk):
        return self.lookup(self.gen_key(chunk))

    # O(n)
    def reassemble(self, chunks, longest_message, debug, clock=-1):
        if clock != -1:
            clock = time.clock()

        show_progress = True
    
        message = "[*] Reassembling..."

        reassembled = []
        for chunk in range(len(chunks)):
            reassembled.append("".join(chunks[chunk]))

            # update progress
            if show_progress:
                current_progress = chunk / (len(chunks) - 1)
                show_progress = show_current_progress(current_progress, message, debug=debug)

        if clock != -1:
            td = time.clock()
            return reassembled, out_success(message, longest_message, clock, td)
        
        return -1

    # O(n)
    def generate_chunks(self, chunks, longest_message, debug, clock=-1):
        """
        Create `n` chunks to semi-parallelize re-grouping an `np.array`.

        Args:
            chunks(int): Re-grouped image data

            longest_message (str): Longest message displayed on console

            debug (bool): Show additional information

            clock (float, optional): Show operation times. Defaults to -1 which means no info will be shown.
        
        Returns:
            td: Clock information
        """
        if clock != -1:
            clock = time.clock()

        show_progress = True

        message = "[*] Creating chunks..."
        # chunk the image
        for _ in range(self.Y // 4): # rows of braille unicode
            '''
            The file is analyzed in chunks: ... x x ...
                                            ... x x ...
                                            ... x x ...
                                            ... x x ...
            '''           
            # chunk section
            try:
                chunk = self.decode([
                    self.I[_ * 4][0],     self.I[_ * 4][1],
                    self.I[_ * 4 + 1][0], self.I[_ * 4 + 1][1],
                    self.I[_ * 4 + 2][0], self.I[_ * 4 + 2][1],
                    self.I[_ * 4 + 3][0], self.I[_ * 4 + 3][1],            
                ])
            except IndexError:
                die("[-] Stupid bugs.")

            chunks.append([chunk])

            # update progress
            if show_progress:
                current_progress = _ / (self.Y // 4) - 1
                show_progress = show_current_progress(current_progress, message, debug=debug)
        
        if clock != -1:
            td = time.clock()
            return out_success(message, longest_message, clock, td)

        return -1
    
    # O(n^2)
    def initialize_chunks(self, chunks, longest_message, debug, clock=-1):
        """
        Create the rest of the chunks.

        Args:
            chunks(int): Re-grouped image data

            longest_message (str): Longest message displayed on console

            debug (bool): Show additional information

            clock (float, optional): Show operation times. Defaults to -1 which means no info will be shown.
        
        Returns:
            td: Clock information
        """
        if clock != -1:
            clock = time.clock()

        show_progress = True
    
        message = "[*] Initializing..."

        # horizontal iteration
        for _ in range(len(chunks)):
            try:
                chunks[_] = [chunks[_][0]] + [self.decode([
                    self.I[(_ * 4)][0 + (2 * j)],     self.I[(_ * 4)][1 + (2 * j)],
                    self.I[(_ * 4 + 1)][0 + (2 * j)], self.I[(_ * 4 + 1)][1 + (2 * j)],
                    self.I[(_ * 4 + 2)][0 + (2 * j)], self.I[(_ * 4 + 2)][1 + (2 * j)],
                    self.I[(_ * 4 + 3)][0 + (2 * j)], self.I[(_ * 4 + 3)][1 + (2 * j)],            
                ]) for j in range(0, self.X // 2, self.RESOLUTION_FACTOR)]
            except IndexError:
                die("[-] Stupid bugs.")

            # update progress
            if show_progress:
                current_progress = _ / (len(chunks) - 1)
                show_progress = show_current_progress(current_progress, message, debug=debug)

        if clock != -1:
            td = time.clock()
            return out_success(message, longest_message, clock, td)
        
        return -1

    # O(n)
    def write_to_file(self, filename, chunk_length, outfile, longest_message, debug, clock=-1):
        if clock != -1:
            clock = time.clock()
        """
        Write decoded image to file.

        Args:
            filename (str): The file to write to

            chunk_length (int): Number of chunks

            outfile (Unicode[]): Array of braille symbols

            longest_message (str): Longest message displayed on console

            debug (bool): Show additional information

            clock (float, optional): Show operation times. Defaults to -1 which means no info will be shown.
        """
        show_progress = True

        message = "[*] Writing to file..."
        with open(filename, 'w') as f:
            for _ in range(chunk_length):
                f.write(outfile[_])
                f.write("\n")    

                # update progress
                if show_progress:
                    current_progress = _ / (chunk_length - 1)
                    show_progress = show_current_progress(current_progress, message, debug=debug)
        
        if clock != -1:
            td = time.clock()
            out_success(message, longest_message, clock, td)

    # O(n^2) with speed and quality differences depending on version ran
    def convert(self, filename, debug=False, slow_mode=False, float_size=False):
        """
        Convert image data to Braille symbols and save to .txt file.

        Args:
            filename (str): The output file to write to.

            debug (boolean, optional): Prints output to console. Defaults to False.

            slow_mode (boolean, optional): Chunks 1 at a time. Defaults to False.

        """
        filename = "../out/" + filename if "../out/" not in filename else filename

        if filename[-4:] != ".txt":
            filename += ".txt"

        
        if not slow_mode:     
            longest_message = "[*] Creating chunks..."

            chunks = []
            print("[*] Resolution: [1:{}]".format(self.RESOLUTION_FACTOR))
            print(DIVIDER)
            print("[*] Writing to {}...".format(filename))
            print(DIVIDER)

            # start clock for timing
            td = time.clock()
            
            # process is O(n) + O(n^2) + O(n) + O(n) = O(n^2 + 3n)
            if not float_size:                
                # generate starting chunks: O(n)
                td = self.generate_chunks(chunks, longest_message, debug=debug, clock=td)
                
                # initialize remaining chunks: O(n^2)
                td = self.initialize_chunks(chunks, longest_message, debug=debug, clock=td)

                # reassemble: O(n)
                outfile, td = self.reassemble(chunks, longest_message, debug=debug, clock=td)

                # write to file: O(n)
                self.write_to_file(filename, len(chunks), outfile, longest_message, debug=debug, clock=td)                        
            
                if debug:
                    print_stats(self.stats)
            # merge decode: O(n)???
            else:
                current_progress = 0
                show_current_progress(current_progress, "[*] Merge decoding...")
                out = self.recur_decode(self.I)
                td2 = time.clock()

                td2 = out_success("[*] Merge decoding...", longest_message, td, td2)

                show_progress = True
                message = "[*] Writing to file..."
                
                with open(filename, "w") as f:    
                    # update progress
                    f.writelines(out)
                                  
                td = time.clock()
                out_success("[*] Writing to file...", longest_message, td2, td)
        # -s (estimated runtime-complexity O(3n^2 + 2n)
        else:
            print("\n[*] Slow mode enabled, now chunking 1 at a time.")
            td = time.clock()
            with open(filename, 'w') as f:
                print("[*] Writing to {}...".format(filename))
                print(DIVIDER)

                show_progress = True
                done = False

                message = "[*] Working..."
                longest_message = message
                # chunk the image
                for i in range(0, self.Y // 4): # rows of braille unicode
                    chunks = []
                    for j in range(0, self.X // 2, 2): # cols of braille unicode
                        # update progress
                        current_progress = (i*4 + 4) / self.Y
                        if show_progress and not debug:
                            show_progress = True if update_progress(current_progress, message, longest_message=longest_message) == 0 else False
                        else:
                            if not done and not debug:
                                block = int(round(10))
                                status = "SUCCESS!     \r\n"
                                text = "\r{0} [{1}] {2}% {3}".format(message, " "*(len(longest_message) - len(message)) + "#"*block + "-"*(10-block), 100, status)

                                sys.stdout.write(text)
                                sys.stdout.flush()

                                done = True
                        
                        # chunk section
                        try:
                            chunk = self.decode([
                                self.I[i * 4][j * 2],     self.I[i * 4][j * 2 + 1],
                                self.I[i * 4 + 1][j * 2], self.I[i * 4 + 1][j * 2 + 1],
                                self.I[i * 4 + 2][j * 2], self.I[i * 4 + 2][j * 2 + 1],
                                self.I[i * 4 + 3][j * 2], self.I[i * 4 + 3][j * 2 + 1],            
                            ])
                        except IndexError:
                            die("[-] Stupid bugs.")

                        chunks.append(chunk)

                    out = "".join(chunks)

                    if debug:
                        print(out)

                    f.write(out) 

                    if debug:
                        print("\n")
                    
                    f.write("\n")

                td_2 = time.clock()
                print("time: " + str(td_2 - td))

        print(DIVIDER)
        print("[+] Output sent to {}.".format(filename))
    
    ## Experimental algorithms

    def recur_decode(self, arr):
        # base cases
        if len(arr) == 4:
            # base case -- have a chunk
            if len(arr[0]) == 2:
                self.GLOBAL_MERGE_COUNT += 1
                return self.decode([
                    arr[0][0], arr[0][1],
                    arr[1][0], arr[1][1],
                    arr[2][0], arr[2][1],
                    arr[3][0], arr[3][1]
                ])

            # semi base case, the row -- can't divide length wise anymore
            # split columns in 2

            # can split in half
            if (len(arr[0]) // 2) % 2 == 0:
                arr_1 = [row[:len(arr[0]) // 2] for row in arr] # first half
                arr_2 = [row[len(arr[0]) // 2:] for row in arr] # second half
                result_l = self.recur_decode(arr_1)
                result_r = self.recur_decode(arr_2)
                # check size of reassembled list
                return result_l + result_r if len(arr[0]) != self.X else result_l + result_r + "\n"
            # cannot split directly in half -- remove the middle and split the other two
            else:
                # [:(n-d)/2], [(n-d)/2:n/2], [n/2:], n = len(row), d = 2
                arr_1  = [row[:(len(row) - 2) // 2] for row in arr] # first portion
                middle = [row[(len(row) - 2) // 2:(len(row) + 2) // 2] for row in arr] # middle
                arr_2  = [row[(len(row) + 2) // 2:] for row in arr] # second portion
                result_l = self.recur_decode(arr_1)
                try:
                    result_m = self.decode([
                        middle[0][0], middle[0][1],
                        middle[1][0], middle[1][1],
                        middle[2][0], middle[2][1],
                        middle[3][0], middle[3][1],
                    ])
                except IndexError:
                    print(arr_1)
                    print(middle)
                    print(arr_2)
                    exit(0)
                result_r = self.recur_decode(arr_2)
                # check size of reassembled list
                return result_l + result_m + result_r if len(arr[0]) != self.X else result_l + result_r + "\n"
        # split rows in 4
        elif len(arr) > 4:
            # can split in half
            if (len(arr) // 4) % 2 == 0:
                arr_1 = arr[:len(arr) // 2] # first half
                arr_2 = arr[len(arr) // 2:] # second half                
                result_l = self.recur_decode(arr_1)
                result_r = self.recur_decode(arr_2)               
                return result_l + result_r
            # cannot split directly in half -- remove the middle and split the other two
            else:
                # [:(n-d)/2], [(n-d)/2:n/2], [n/2:], n = len(row), d = 4
                arr_1  = arr[:(len(arr) - 4) // 2]
                middle = arr[(len(arr) - 4) // 2:(len(arr) + 4) // 2]
                arr_2  = arr[(len(arr) + 4) // 2:]
                result_l = self.recur_decode(arr_1)
                middle = self.recur_decode(middle)
                result_r = self.recur_decode(arr_2)
                return result_l + middle + result_r
        else:
            print(len(arr), len(arr[0]))
            die("Error")
    
    # O(n)
    def merge_chunk_row(self, arr):
        try:
            return [self.lookup(self.gen_key([
                    arr[0][0 + (2 * j)], arr[0][1 + (2 * j)],
                    arr[1][0 + (2 * j)], arr[1][1 + (2 * j)],
                    arr[2][0 + (2 * j)], arr[2][1 + (2 * j)],
                    arr[3][0 + (2 * j)], arr[3][1 + (2 * j)],            
                ])) for j in range(len(arr[0]) // 2)]
        except IndexError:
            die("[-] Stupid bugs.")

    # O(n^2)
    def merge_chunk(self, arr, first_run=True):
        """
        Converts chunks to Braille symbols recursively.

        Args:
            arr (bool[]): The chunks to decode

        Returns:
            A grid of Braille symbols
        """
        # return chunk
        if len(arr) == 4:           
            self.GLOBAL_MERGE_COUNT += 1

            # O(n)
            return self.merge_chunk_row(arr)            
        # split array
        elif len(arr) > 4:
            left = self.merge_chunk(arr[:len(arr)//2], first_run=False)
            right = self.merge_chunk(arr[len(arr)//2:], first_run=False)

            current_progress = self.GLOBAL_MERGE_COUNT / (self.Y // 4)
            
            show_current_progress(current_progress, "[*] Merge chunking...")
            merge = left + right

            return merge
        # shouldn't be here, something went wrong during initialization
        else:
            die("[!] Underflow")