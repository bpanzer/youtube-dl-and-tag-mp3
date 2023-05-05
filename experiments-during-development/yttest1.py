from __future__ import unicode_literals
import youtube_dl


class MyLogger(object):		# keep this in order to avoid status messages on stdout
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def ytdl_hook(d):
    if d['status'] == 'finished':
        print('Done downloading '+d['filename']+', now converting ...')

ytdl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logger': MyLogger(),
    'progress_hooks': [ytdl_hook],
}

def foo():
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download(['https://www.youtube.com/watch?v=op9ApJJyhD4'])

foo()
