Usage
-----

### How to Use
`$ python dotty.py <path_to_image> [output_file] [sizeX,sizeY] [-[args][res]]`

#### Args
| arg              | command                                              |
|:----------------:|------------------------------------------------------|
| `d`              | debug (send output to console)                       |
| `l`              | leave size unchanged (as close as possible)          |
| `n`              | no invert (inverts image by default)                 |
| `s`              | re-groups image 1 chunk at a time (old behavior)     |
| `m`              | uses merge-like algorithm to chunk / decode          |
| `1` (res)        | sets resolution to `1:1`                             |
| `2` (res)        | sets resolution to `transpose (default)`             |
| `<number>` (res) | sets resolution to `1:<number>`                      |
#### Command-line usage
The path to the image should *always* be after `dotty.py`.
The output file and size change should come after (in that order, respectively), if specified.
Finally, any flags should be specified at the end, with resolution after.

Flags can be chained together in any order.

If `sizeX,sizeY` and `-l` are used, `-l` takes precedence.

Specifying the output file is a text file is not necessary.

If there are problems with the image resolution after trying `-<number>`, try using `-s`.
Although Dotty has been optimized, there may be resolution issues when compared to the old version.
`-s` runs the original code.

#### Example uses
* Create a `240x240`-sized (60 rows, 60 columns) text file of `foo.jpg` and output to `../out/output.txt` as well as the console:
    ```sh
    $ python dotty.py ../img/user_images/foo.jpg -d
    ```

* Create a full-sized (as close as possible to original) text file of `lightbulb.jpg` and output to `../out/bulb.txt`:
    ```sh 
    $ python dotty.py ../img/examples/lightbulb.jpg bulb.txt -l
    ```

* Create a `120x60`-sized (15 rows, 30 columns) text file of `bell.jpg` and output to `../out/output.txt`:
    ```sh
    $ python dotty.py ../img/examples/bell.jpg 120,60
    ```

* Create a full-sized text file of `kingfisher.jpg` without invert and output to `../out/kingfisher.txt`:
    ```sh
    $ python dotty.py ../img/user_images/kingfisher.jpg kingfisher -ln
    ```
