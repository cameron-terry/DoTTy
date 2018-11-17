from PIL import Image
import PIL.ImageOps    

import time
import numpy as np

from dots import DotBlock
from helpers import die, DIVIDER, next_power_of_2

VERSION = "v0.2.4"

class ImageConv:
    """
    Converts image to bilevel image, then stores the data as a `numpy` array for manipulation.

    Attributes:
        x (int): width
        y (int): height
    """
    def __init__(self, pic, filename="output.txt", size=(240, 240), leave_size=False, debug=False, invert=True, slow_mode=False, res_mode=2, float_size=False):
        """
        Initializes a `numpy` array for conversion using `DotBlock.convert()`.

        Args:
            pic (image): The original image file.

            filename (str, optional): The output file to write to. 
                Defaults to "../output.txt".

            size ((int, int), optional): The output size.
                Defaults to (240, 240).

            leave_size (boolean, optional): Keep the output size 
                as close as possible to the original size of 
                the original picture.
                Defaults to False.

            debug (boolean, optional): Print the output to the console.
                Defaults to False.

            invert (boolean, optional): Invert the image.
                Defaults to True.

            slow_mode (boolean, optional): Convert using 1 chunk
                Defaults to False.

            res_mode (int, optional): set `DotBlock.RESOLUTION_FACTOR` to original or transpose
        """
        if not isinstance(filename, str):
            die("[!] Bad filename given.")
        if not isinstance(leave_size, bool) or not isinstance(debug, bool):
            die("[!] Bad flag arguments given.")
        
        img = Image.open(pic)

        if not img.mode == 'RGB':
            img = img.convert('RGB')

        # readjust size to fit braille chars
        self.X = img.size[0] - (img.size[0] % 2)
        self.Y = img.size[1] - (img.size[1] % 4)

        if float_size:
            self.Y = next_power_of_2(self.Y)
        
        assert self.X % 2 == 0, "Rows failed to initialize."
        assert self.Y % 4 == 0, "Columns failed to initialize."

        # convert to black and white, invert colors  
        if not leave_size:
            # default resize
            self.X = size[0]
            self.Y = size[1]

        print(DIVIDER)
        print("Dotty, for pixels to Unicode .txt ({})".format(VERSION))
        print(DIVIDER)
        print("[*] Size: {rows}x{cols}".format(rows=self.X, cols=self.Y))  
        print("[*] Rows: {rows}, Cols: {cols}".format(rows=self.X // 4, cols=self.Y // 4))

        I = np.asarray(PIL.ImageOps.invert(img).convert('1').resize((self.X, self.Y), Image.ANTIALIAS)) \
            if invert else np.asarray(img.convert('1').resize((self.X, self.Y), Image.ANTIALIAS))

        db = DotBlock(self.X, self.Y, I, res_mode=res_mode)

        start_time = time.clock()
        db.convert(filename, debug=debug, slow_mode=slow_mode, float_size=float_size)
        end_time = time.clock() - start_time

        if debug:
            print("time: " + str(end_time))

if __name__ == '__main__':
    ic = ImageConv('../img/user_images/kingfisher.jpg', leave_size=True, invert=False, res_mode=1)
