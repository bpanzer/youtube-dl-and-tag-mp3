import sys
from mutagen.id3 import ID3, TIT2

#path = '/home/bpanzer/Musik/ARovin.mp3'
path = sys.argv[1]
tags = ID3(path)
print(tags.pprint())
