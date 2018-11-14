Change Log (v0.2)
-----------------

convert()
=========
* old code looked up every symbol, 1 at a time (`O(n)` lookup, `O(n^2)` image resolution = `O(n^3)`!)
   * not sure if `np.array_equal()` short-circuits
* new code creates `size.X / 4` chunks and fills them simultaneously
* separated operations into different sections
    * chunk creation: `O(n)`
    * initialization (filling the rest of the columns in): `O(n^2)`
    * decoding (converting chunk data to Braille symbol): `O(n^2)`
    * writing to file: `O(n)`
    * sum of operations: `O(n^2)`
* added old version as option (slow_mode): `-s`
* added variable RESOLUTION_FACTOR to change how image is stretched/squished
   * ~~not reachable by user yet~~

convert_chunk()
===============
* added `chunk_true` to quickly identify all `black/white` chunks
    * `chunk_true` tells how many pixels are white in a chunk 
        * 0 = `black`, 8 = `white` (unique combinations) -- can be resolved in `O(1)` time
* added short circuit to searching through `self.values` via `chunk_true`
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
            $ python dotty.py ../img/user_images/kingfisher.jpg m2 -ln
            ...
            time: 14.260033
        ```
        ```sh
            $ python dotty.py ../img/user_images/kingfisher.jpg m2 -lns
            ...
            time: 83.920389
        ```
        ![Kingfisher comparison](/img/ss/dotty_nvs.png)
        Running without slow mode resulted in an `83%` running-time decrease without significant loss of quality. Assuming `t=3.8s, t^2=14.44s, t^3=54.87s`: slow time roughly follows `3t^3 / 2`.
        ```sh
            $ python dotty.py ../img/user_images/manhattan.jpg m2 -ln
            ...
            time: 19.734783999999998
        ```
        ```sh
            $ python dotty.py ../img/user_images/manhattan.jpg m2 -lns
            ...
            time: 138.215585
        ```
        Assuming `t=4.44s:` 
        * `3t^3 / 2 = 131.292s` which is under the actual time by `5.05%`.
        ![Manhattan comparison -- resolution set to 2](/img/ss/dotty_nvs2.png)
        To improve the definition, change `self.RESOLUTION_FACTOR` to `1`, and re-run:
        ```sh
            $ python dotty.py ../img/user_images/manhattan.jpg m2 -ln1
            ...
            time: 39.194958 (roughly double)
        ```
        Running without slowmode and increasing the definition resulted in a `71.6%` running-time decrease.
        
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
