laughing-batman
===============
This is a script that splits film using the [`ffmpeg`](http://ffmpeg.org/) library.

##Usage

```
python main.py INPUT-FILE TIMES-FILE OUTPUT-FILE
```

where `TIMES-FILE` is a `csv` file of start times and durations such as
```
17:35, 8
21:50, 8
27:55, 12
37:50, 9
39:30, 12
```

##Notes


This perhaps could have been done more efficiently and/or eloquently using `bash` instead of `python`. Oh well.

I'm sure there also could have been more efficient ways to use `ffmpeg`.

##Workflow

```
# create a file for each split
ffmpeg -ss 100 -i emerson.mp4 -t 15 input1.mp4
ffmpeg -ss 204 -i emerson.mp4 -t 15 input2.mp4

# convert splits to .mpg
ffmpeg -i input1.mp4 -qscale:v 1 intermediate1.mpg
ffmpeg -i input2.mp4 -qscale:v 1 intermediate2.mpg

# join videos
cat intermediate1.mpg intermediate2.mpg > intermediate_all.mpg

# convert back to .mp4
ffmpeg -i intermediate_all.mpg -qscale:v 2 output.mp4

# clean up
rm input*
rm intermediate_all.mpg
```




