from PIL import Image
import PIL.ImageOps    

import numpy as np

from dots import DotBlock
from helpers import *

class ImageConv:
    """
    Converts image to bilevel image, then stores the data as a `numpy` array for manipulation.

    Attributes:
        x (int): width
        y (int): height
    """
    def __init__(self, pic, filename="output.txt", size=(240, 240), leave_size=False, debug=False, invert=True):
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
        
        assert self.X % 2 == 0, "Rows failed to initialize."
        assert self.Y % 4 == 0, "Columns failed to initialize."

        # convert to black and white, invert colors  
        if not leave_size:
            # default resize
            self.X = size[0]
            self.Y = size[1]

        print("[*] Size: {rows}x{cols}".format(rows=self.X, cols=self.Y))  
        print("[*] Rows: {rows}, Cols: {cols}".format(rows=self.X // 4, cols=self.Y // 4))

        I = np.asarray(PIL.ImageOps.invert(img).convert('1').resize((self.X, self.Y), Image.ANTIALIAS)) \
            if invert else np.asarray(img.convert('1').resize((self.X, self.Y), Image.ANTIALIAS))

        db = DotBlock(self.X, self.Y, I)

        db.convert(filename, debug=debug)

if __name__ == '__main__':
    ic = ImageConv('../img/pepe.jpg', leave_size=True)
