laughing-batman
===============
This is a script that splits film using the [`ffmpeg`](http://ffmpeg.org/) library.

Usage
_____
```
python main.py INPUT-FILE TIMES OUTPUT-FILE
```

where `TIMES` is a `csv` file of start times and durations such as
```
2:34, 15
3:24, 15
3:49, 15
1:09:05, 15
1:12:05, 15
1:13:52, 15
```

Notes
_____

This perhaps could have been done more efficiently and/or eloquently using `bash`. Oh well.

I'm sure there also could have been more efficient ways to use `ffmpeg`.

Overall, the way it works is:
 + create a file for each split
 + converts each split to `.mpg` container
 + join all `.mpg` files to a large `.mpg` file
 + convert `.mpg` file back to `.mp4`


