from PIL import Image
import PIL.ImageOps    

import numpy as np

from dots import DotBlock

class ImageConv:
    def __init__(self, pic, filename="../output.txt", size=(240, 240), leave_size=False, debug=False):
        img = Image.open(pic)

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
        print("[*] Rows: {rows}, Cols: {cols}".format(rows=self.X // 2, cols=self.Y // 4))

        I = np.asarray(PIL.ImageOps.invert(img).convert('1').resize((self.X, self.Y), Image.ANTIALIAS))

        db = DotBlock(self.X, self.Y, I)

        db.convert(filename, debug=debug)

if __name__ == '__main__':
    ic = ImageConv('../img/pepe.jpg', leave_size=True)
