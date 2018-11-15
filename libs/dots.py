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

        self.stats = [0, 0, 0, 0, 0, 0, 0, 0, 0] # used for statistics

    # O(n)
    def convert_chunk(self, chunks):
        """
        Converts chunks to Braille symbols.

        Args:
            chunks (bool[]): The chunks to decode

        Returns:
            A string representing a row of Braille symbols
        """
        CHUNK_LENGTH = 8 # constant
        converted = []

        for chunk in chunks:
            # look for matching pattern
            lookup = ""
            chunk_true = 0

            # create lookup string, O(8) -- every number either appears once or none 
            for value in range(CHUNK_LENGTH):
                chunk_true = chunk_true + 1 if chunk[value] else chunk_true
                lookup += str(value+1) if chunk[value] else ""

            self.stats[chunk_true] += 1

            # lookup value to append -- O(1)
            converted.append(self.values["BLANK"][1]) if chunk_true == 0 else converted.append(self.values[lookup][1])                           
                
        return "".join(converted)
    
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
            chunk = [
                self.I[_ * 4][0],     self.I[_ * 4][1],
                self.I[_ * 4 + 1][0], self.I[_ * 4 + 1][1],
                self.I[_ * 4 + 2][0], self.I[_ * 4 + 2][1],
                self.I[_ * 4 + 3][0], self.I[_ * 4 + 3][1],            
            ]

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
        for j in range(0, self.X // 2, self.RESOLUTION_FACTOR): # cols of braille unicode
            # chunk section
            for _ in range(len(chunks)):
                chunks[_].append([
                    self.I[(_ * 4)][0 + (2 * j)],     self.I[(_ * 4)][1 + (2 * j)],
                    self.I[(_ * 4 + 1)][0 + (2 * j)], self.I[(_ * 4 + 1)][1 + (2 * j)],
                    self.I[(_ * 4 + 2)][0 + (2 * j)], self.I[(_ * 4 + 2)][1 + (2 * j)],
                    self.I[(_ * 4 + 3)][0 + (2 * j)], self.I[(_ * 4 + 3)][1 + (2 * j)],            
                ])

            # update progress
            if show_progress:
                current_progress = j / ((self.X // 2) - 1)
                show_progress = show_current_progress(current_progress, message, debug=debug)

        if clock != -1:
            td = time.clock()
            return out_success(message, longest_message, clock, td)
        
        return -1
    
    # O(n^2)
    def decode(self, chunks, longest_message, debug, clock=-1):
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

    def convert(self, filename, debug=False, slow_mode=False):
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

        DIVIDER = "="*48

        # process is O(n) + O(n^2) + O(n) + O(n) = O(n^2) + O(3n) = O(n^2 + 3n)
        if not slow_mode:     
            longest_message = "[*] Creating chunks..."

            chunks = []
            print("[*] Resolution: [1:{}]".format(self.RESOLUTION_FACTOR))
            print(DIVIDER)
            print("[*] Writing to {}...".format(filename))
            print(DIVIDER)

            # start clock for timing
            td = time.clock()
            
            # generate chunks: O(n)
            td = self.generate_chunks(chunks, longest_message, debug=debug, clock=td)
            
            # initialize chunks: O(n^2)
            td = self.initialize_chunks(chunks, longest_message, debug=debug, clock=td)

            # decode chunks: O(n)
            outfile, td = self.decode(chunks, longest_message, debug=debug, clock=td)

            # write to file: O(n)
            self.write_to_file(filename, len(chunks), outfile, longest_message, debug=debug, clock=td)                        
           
            if debug:
                print_stats(self.stats)
        # -s (estimated runtime-complexity O(8n^3 + n^2))
        else:
            print("\n[*] Slow mode enabled, now chunking 1 at a time.")
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
                            show_progress = True if update_progress(current_progress, message) == 0 else False
                        else:
                            if not done and not debug:
                                block = int(round(10))
                                status = "SUCCESS!     \r\n"
                                text = "\r{0} [{1}] {2}% {3}".format(message, " "*(len(longest_message) - len(message)) + "#"*block + "-"*(10-block), 100, status)

                                sys.stdout.write(text)
                                sys.stdout.flush()

                                done = True
                        
                        # chunk section
                        chunk = [
                            self.I[i * 4][j * 2],     self.I[i * 4][j * 2 + 1],
                            self.I[i * 4 + 1][j * 2], self.I[i * 4 + 1][j * 2 + 1],
                            self.I[i * 4 + 2][j * 2], self.I[i * 4 + 2][j * 2 + 1],
                            self.I[i * 4 + 3][j * 2], self.I[i * 4 + 3][j * 2 + 1],            
                        ]

                        chunks.append(chunk)

                    out = self.convert_chunk(chunks)
                    f.write(out) 

                    if debug:
                        print("\n")
                    
                    f.write("\n")

        print(DIVIDER)
        print("[+] Output sent to {}.".format(filename))
    