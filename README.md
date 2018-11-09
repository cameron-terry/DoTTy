# About
![Dotty output screenshot](/img/dotty_ss.png)

Dotty takes `.JPEG` files and outputs a text file with the image transformed into a grid of Braille symbols.
Dotty scans the `.JPEG` in 4x2 chunks, creating a Braille symbol for each chunk.

### How to Use
`$ python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [args]`

| arg  | command                        |
|------|--------------------------------|
| `-d` | debug (send output to console) |
| `-l` | leave size unchanged           |

The path to the image should *always* be after `dotty.py`.
The output file and size change should come after (in that order, respectively), if specified.
Finally, any flags should be specified at the end.

`-d` and `-l` can be chained together in either order.

### Example uses
* Create a 240x240 text file of pepe.jpg and output to ../out/output.txt as well as the console:
    `$ python dotty.py ../img/pepe.jpg -d`

* create a full-sized (as close as possible to original) text file of pepe.jpg and output to ../out/pepe_braille.txt:
    `$ python dotty.py ../img/pepe.jpg ../out/pepe_braille.txt -l`

* create a 120x60 text file of bell.jpg and output to ../out/output.txt
    `$ python dotty.py ../img/bell.jpg 120,60`
