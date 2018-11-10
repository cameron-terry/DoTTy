# About
![Dotty output screenshot](/img/ss/dotty_ss.png)

Dotty takes image files and outputs a text file with the image transformed into a grid of Braille symbols.

Dotty scans the image in 4x2 chunks, creating a Braille symbol for each chunk.
The output is stored in the `out/` directory.

Dotty runs on Python 3.

### How to Use
`$ python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [args]`

#### Args
| arg  | command                                    |
|------|--------------------------------------------|
| `-d` | debug (send output to console)             |
| `-l` | leave size unchanged (as close as possible |
| `-n` | no invert (inverts image by default)       |

#### Command-line usage
The path to the image should *always* be after `dotty.py`.
The output file and size change should come after (in that order, respectively), if specified.
Finally, any flags should be specified at the end.

Flags can be chained together in any order.

Specifying the output file is a text file is not necessary.

#### Example uses
* Create a `240x240`-sized (60 rows, 60 columns) text file of `pepe.jpg` and output to `../out/output.txt` as well as the console:
    > `$ python dotty.py ../img/examples/pepe.jpg -d`

* Create a full-sized (as close as possible to original) text file of `marilyn_monroe.jpg` and output to `../out/marilyn.txt`:
    > `$ python dotty.py ../img/examples/pepe.jpg marilyn.txt -l`

* Create a `120x60`-sized (15 rows, 30 columns) text file of `bell.jpg` and output to `../out/output.txt`:
    > `$ python dotty.py ../img/examples/bell.jpg 120,60`

* Create a full-sized text file of `chevy57.jpeg` without invert and output to `../out/chevy57.txt`:
    > `$ python dotty.py ../img/examples/chevy57.jpeg chevy57 -ln`

# Sample Runs
![Marilyn Monroe](/img/ss/dotty_ss3.png)
![Starry Night -- Vincent Van Gogh](/img/ss/dotty_ss2.png)
![Manhattan](/img/ss/dotty_ss4.png)
![Chevy '57](/img/ss/dotty_ss5.png)