import numpy as np
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
            self.values = json.load(fp)

        # set cols, rows, image
        if isinstance(x, float):
            x = int(x)
        if not isinstance(x, int):
            die("[!] Width must be an int")
        if isinstance(y, float):
            y = int(y)
        if not isinstance(y, int):
            die("[!] Height must be an int")
        if not isinstance(img, np.ndarray):
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
            return self.values[key][1]
        except KeyError:
            return self.values["BLANK"][1]

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
    def convert_chunk(self, chunks):
        """
        Converts chunks to Braille symbols.

        Args:
            chunks (bool[][]): The chunks to decode

        Returns:
            A string representing a row of Braille symbols
        """
        # init array to hold values
        converted = []

        # iterate through, decoding each chunk
        for chunk in chunks:
            key = self.gen_key(chunk)
            chunk_true = len(key)

            self.stats[chunk_true] += 1

            # lookup value to append -- O(1)
            converted.append(self.values["BLANK"][1]) if chunk_true == 0 else converted.append(self.lookup(key))                           

        # return decoded string        
        return "".join(converted)
    
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
                chunk = self.lookup(self.gen_key([
                    self.I[_ * 4][0],     self.I[_ * 4][1],
                    self.I[_ * 4 + 1][0], self.I[_ * 4 + 1][1],
                    self.I[_ * 4 + 2][0], self.I[_ * 4 + 2][1],
                    self.I[_ * 4 + 3][0], self.I[_ * 4 + 3][1],            
                ]))
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

        # chunk section
        for _ in range(len(chunks)):
            try:
                chunks[_] = [chunks[_][0]] + [self.lookup(self.gen_key([
                    self.I[(_ * 4)][0 + (2 * j)],     self.I[(_ * 4)][1 + (2 * j)],
                    self.I[(_ * 4 + 1)][0 + (2 * j)], self.I[(_ * 4 + 1)][1 + (2 * j)],
                    self.I[(_ * 4 + 2)][0 + (2 * j)], self.I[(_ * 4 + 2)][1 + (2 * j)],
                    self.I[(_ * 4 + 3)][0 + (2 * j)], self.I[(_ * 4 + 3)][1 + (2 * j)],            
                ])) for j in range(0, self.X // 2, self.RESOLUTION_FACTOR)]
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
    
    # O(n^2)
    def decode_chunks(self, chunks, longest_message, debug, clock=-1):
        """
        Convert chunks to Braille symbols.

        Args:
            chunks(int): Re-grouped image data

            longest_message (str): Longest message displayed on console

            debug (bool): Show additional information

            clock (float, optional): Show operation times. Defaults to -1 which means no info will be shown.
        
        Returns:
            outfile (Unicode[]): Array of braille symbols

            td: Clock information
        """
        show_progress = True

        outfile = []
        message = "[*] Decoding..."

        # chunk the image
        for c in range(len(chunks)): # rows of braille unicode
            row = self.convert_chunk(chunks[c])
            outfile.append(row)

            # update progress
            if show_progress:
                current_progress = c / (len(chunks) - 1)
                show_progress = show_current_progress(current_progress, message, debug=debug)
        
        if clock != -1:
            td = time.clock()
            return outfile, out_success(message, longest_message, clock, td)
        
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
                # generate chunks: O(n)
                td = self.generate_chunks(chunks, longest_message, debug=debug, clock=td)
                
                # initialize chunks: O(n^2)
                td = self.initialize_chunks(chunks, longest_message, debug=debug, clock=td)

                # reassemble: O(n)
                outfile, td = self.reassemble(chunks, longest_message, debug=debug, clock=td)

                # write to file: O(n)
                self.write_to_file(filename, len(chunks), outfile, longest_message, debug=debug, clock=td)                        
            
                if debug:
                    print_stats(self.stats)
            # merge decode: O(n log 2n^2)
            else:
                merge = self.merge_chunk(self.I)
                td2 = time.clock()

                td2 = out_success("[*] Merge chunking...", longest_message, td, td2)
                merge = [merge[i:i+(self.X // 2)] for i in range(0, len(merge), self.X // 2)]
                merge, td2 = self.reassemble(merge, longest_message, debug=debug, clock=td)

                show_progress = True
                message = "[*] Writing to file..."
                # write to file -- O(n)
                with open(filename, "w") as f:
                    for line in range(len(merge)):
                        f.write(merge[line] + "\n")
                    
                        # update progress
                        if show_progress:
                            current_progress = line / (len(merge) - 1)
                            show_progress = show_current_progress(current_progress, message, debug=debug)
                
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
                            chunk = self.lookup(self.gen_key([
                                self.I[i * 4][j * 2],     self.I[i * 4][j * 2 + 1],
                                self.I[i * 4 + 1][j * 2], self.I[i * 4 + 1][j * 2 + 1],
                                self.I[i * 4 + 2][j * 2], self.I[i * 4 + 2][j * 2 + 1],
                                self.I[i * 4 + 3][j * 2], self.I[i * 4 + 3][j * 2 + 1],            
                            ]))
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
    