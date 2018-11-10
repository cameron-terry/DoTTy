About
=====

![Dotty output screenshot](/img/ss/dotty_ss.png)

Dotty takes image files and outputs a text file with the image transformed into a grid of Braille symbols.

Dotty scans the image in 4x2 chunks, creating a Braille symbol for each chunk.
The output is stored in the `out/` directory.

Requirements
------------
+ Python 3
+ Numpy -- https://scipy.org/install.html
+ Pillow -- https://pillow.readthedocs.io/en/3.0.x/installation.html

Usage
-----

### How to Use
`$ python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [args]`

#### Args
| arg  | command                                     |
|------|---------------------------------------------|
| `-d` | debug (send output to console)              |
| `-l` | leave size unchanged (as close as possible) |
| `-n` | no invert (inverts image by default)        |

#### Command-line usage
The path to the image should *always* be after `dotty.py`.
The output file and size change should come after (in that order, respectively), if specified.
Finally, any flags should be specified at the end.

Flags can be chained together in any order.

Specifying the output file is a text file is not necessary.

#### Example uses
* Create a `240x240`-sized (60 rows, 60 columns) text file of `foo.jpg` and output to `../out/output.txt` as well as the console:
    > `$ python dotty.py ../img/user_images/foo.jpg -d`

* Create a full-sized (as close as possible to original) text file of `lightbulb.jpg` and output to `../out/bulb.txt`:
    > `$ python dotty.py ../img/examples/lightbulb.jpg bulb.txt -l`

* Create a `120x60`-sized (15 rows, 30 columns) text file of `bell.jpg` and output to `../out/output.txt`:
    > `$ python dotty.py ../img/examples/bell.jpg 120,60`

* Create a full-sized text file of `foo.jpeg` without invert and output to `../out/bar.txt`:
    > `$ python dotty.py ../img/user_images/foo.jpeg bar -ln`

Sample Runs
===========

Marilyn Monroe (1200 × 1200)
----------------------------
![Marilyn Monroe](/img/ss/dotty_ss3.png)

Starry Night -- Vincent Van Gogh (1280 x 1014)
----------------------------------------------
![Starry Night -- Vincent Van Gogh](/img/ss/dotty_ss2.png)

The Great Wave off Kanagawa -- Hokusai (2000 × 1345)
----------------------------------------------------
![The Great Wave off Kanagawa -- Hokusai](/img/ss/dotty_ss6.png)

Manhattan (1242 × 810)
----------------------
![Manhattan](/img/ss/dotty_ss4.png)

Chevy '57 (1000 × 750)
----------------------
![Chevy '57](/img/ss/dotty_ss5.png)

Mount Everest (2004 × 1800)
---------------------------
![Mount Everest](/img/ss/dotty_ss7.png)