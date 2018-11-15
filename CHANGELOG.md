Changelog 
==========

(v0.2.1) -- 2018-11-15
======================
dots.py:DotBlock.convert()
--------------------------
### Changed
* decoding (converting chunk row data to Braille symbols) operation is now `O(n)`
  * full DotBlock.convert() process is approximately `2 * O(n^2 + n)`
    * chunk + init + decode + write: `O(n) + O(n^2) + O(n^2) + O(n)` with init (re-grouping of data) depending on two ints
* largest deciding factor on running speed is grouping time --> resolution size: `O(n^2)`
* Should see decreased run times of `> ~95%`

### Added
* resolution option (squish image by `<number>`)

dots.py:DotBlock.convert_chunk()
--------------------------------
### Changed
* Lookup time is now `O(1)`
  * removed `np.array_equal` comparison, instead build key in constant time for lookup
  * `lookup` holds the key and is used when `chunk_true` is not 0 ~~or 8~~
    * initialized at the same time as `chunk_true`, in constant time (`sizeof chunk = 8`)
* Run times:
  ```sh
      $ python dotty.py ../img/user_images/kingfisher.jpg m2 -lnd
      ...
      time: 0.26288
  ```
        
  ```sh
      $ python dotty.py ../img/user_images/kingfisher.jpg m2 -lnd1
      ...
      time: 0.653989
  ```
        
  ```sh
      $ python dotty.py ../img/user_images/manhattan.jpg m2 -lnd
      ...
      time: 0.504448
  ```
        
  ```sh
      $ python dotty.py ../img/user_images/manhattan.jpg m2 -lnd1
      ...
      time: 0.7596529
  ```
  
Image quality is unaffected from v0.2.

v(0.2) -- 2018-11-14
====================
dots.py:DotBlock.convert()
--------------------------
* old code looked up every symbol, 1 at a time (`O(n)` lookup, `O(n^2)` image resolution = `O(n^3)`!)
    * process was approximately `O(8n^3 + n^2)`
    * not sure if `np.array_equal()` short-circuits
      > Neither allclose() nor array_equal() actually short-circuits when doing the real check. 
      > They only short-circuit in the all() function/method call, which is already too late. 
      > These two functions can be especially deceiving.
   
      *congma*, https://github.com/numpy/numpy/issues/6909

### Changed
* new code creates `size.X / 4` chunks and fills them simultaneously
* separated operations into different sections
    * chunk creation: `O(n)`
    * initialization (filling the rest of the chunks in): `O(n^2)`
    * decoding (converting chunk row data to Braille symbols): `O(n^2)`
    * writing to file: `O(n)`
    * sum of operations: `O(n^2)`

### Added
* old version as option (slow_mode): `-s`
* variable RESOLUTION_FACTOR to change how image is stretched/squished
    * ~~not reachable by user yet~~

dots.py:DotBlock.convert_chunk()
--------------------------------
### Added
* variable `chunk_true` to quickly identify all `black/white` chunks
    * `chunk_true` tells how many pixels are white in a chunk 
        * 0 = `black`, 8 = `white` (unique combinations) -- can be resolved in `O(1)` time
* short-circuiting searching through `self.values` via `chunk_true`
    * only check values that match the number of white pixels
    * distribution of values:
     
         | white pixels   | percentage          |
         |:--------------:|:-------------------:|
         |       1        | 0.031               |
         |       2        | 0.11                |
         |       3        | 0.22                |
         |       4        | 0.275               |
         |       5        | 0.224               |
         |       6        | 0.11                |
         |       7        | 0.031               |
    * following from this,
        * if a chunk contains `4` pixels, the other `72.5%` do not need to be compared
        * if a chunk contains `1` pixel, the other `96.9%` do not need to be compared
    
    * example: `kingfisher.jpg`
        
        | white pixels | percentage           |
        |--------------|----------------------|
        |       0      | 0.0084 |
        |       1      | 0.0189 |
        |       2      | 0.0324 |
        |       3      | 0.0409 |
        |       4      | 0.0801 |
        |       5      | 0.3145 |
        |       6      | 0.4044 |
        |       7      | 0.0950 |
        |       8      | 0.0053 | 
         
        * around `1.5%` of chunks are resolved in `O(1)` time
        * searching through the largest basket occured `8.01%` of the time
        * `40.44%` of the chunks only needed to be compared with `11%` of possible comparisons
        * `31.45%` of the chunks only needed to be compared with `22.5%` of possible comparisons
        * `71.89%` of the chunks only needed to be compared with `33.5%` of possible comparisons
    * example: `manhattan.jpg`
        
        | white pixels | percentage |
        |--------------|------------|
        |       0      | 0.0378     |
        |       1      | 0.1779     |
        |       2      | 0.2428     |
        |       3      | 0.1624     |
        |       4      | 0.1759     |
        |       5      | 0.0756     |
        |       6      | 0.0601     |
        |       7      | 0.0590     |
        |       8      | 0.0085     |
        
        * around `4.65%` of chunks are resolved in `O(1)` time
        * searching through the largest basket occured `17.59%` of the time
        * `24.28%` of the chunks only needed to be compared with `3.24%` of possible comparisons
        * `75.89%` of the chunks needed to be compared with `63.6%` of possible comparisons

    * Run times:
        ```sh
            $ python dotty.py ../img/user_images/kingfisher.jpg m2 -lnd
            ...
            time: 14.260033
        ```
        ```sh
            $ python dotty.py ../img/user_images/kingfisher.jpg m2 -lnds
            ...
            time: 83.920389
        ```
        ![Kingfisher comparison](/img/ss/dotty_nvs.png)
        Running without slow mode resulted in an `83%` running-time decrease without significant loss of quality (`0.22%` difference in word count, `18.95%` difference in bytes). Slow time roughly follows `8t^3 + t^2`.
        ```sh
            $ python dotty.py ../img/user_images/manhattan.jpg m2 -lnd
            ...
            time: 19.734783999999998
        ```
        ```sh
            $ python dotty.py ../img/user_images/manhattan.jpg m2 -lnds
            ...
            time: 138.215585
        ```
        Assuming `t=4.44s:` 
        * `3t^3 / 2 = 131.292s` which is under the actual time by `5.05%`.
        ![Manhattan comparison -- resolution set to 2](/img/ss/dotty_nvs2.png)
        To improve the definition, change `self.RESOLUTION_FACTOR` to `1`, and re-run:
        ```sh
            $ python dotty.py ../img/user_images/manhattan.jpg m2 -lnd1
            ...
            time: 39.194958 (roughly double)
        ```
      Running without slowmode and increasing the definition resulted in a `71.6%` running-time decrease, `0.38%` difference in word count, `18.47%` difference in bytes
        
           | white pixels | percentage |
           |--------------|------------|
           |       0      | 0.0363     |
           |       1      | 0.1762     |
           |       2      | 0.2452     |
           |       3      | 0.1641     |
           |       4      | 0.1751     |
           |       5      | 0.0756     |
           |       6      | 0.0598     |
           |       7      | 0.0588     |
           |       8      | 0.0088     |
        
         Note the distribution is roughly the same.
        ![Manhattan comparison -- resolution set to 1](/img/ss/dotty_nvs3.png)
