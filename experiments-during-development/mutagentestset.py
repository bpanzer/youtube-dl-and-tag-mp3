import sys
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TDRC

path = sys.argv[1]
#tags = ID3(path)
tags = ID3(r''+path)
title = 'mytitle'
comment = "This is comment!\nline 2"
artist='Various Artists'
year='1980'
album='album'
tags["TIT2"] = TIT2(encoding=3, text=u''+title+'')
tags["TPE1"] = TPE1(encoding=3, text= u''+artist+'')
tags["TALB"] = TALB(encoding=3, text= u''+album+'')
tags["TDRC"] = TDRC(encoding=3, text= u''+year+'')
tags["COMM"] = COMM(encoding=3, text=u''+comment+'')
tags.save()
