#!/bin/bash
for f in ./*.ref; do
    # strip leading "./" and trailing ".ref":
    tmp=${f#./}
    videoid=${tmp:0:${#tmp}-4}
    #echo $videoid
    python3 ../youtube-dl-and-tag-mp3.py -p https://www.youtube.com/watch?v=${videoid} > ./${videoid}.test
    diff ./${videoid}.test ./${videoid}.ref
done
rm *.test
