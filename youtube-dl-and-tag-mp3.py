from __future__ import unicode_literals
import re
import requests
import sys
import json
import argparse
import glob, os
import youtube_dl
#import time
#from datetime import datetime, timezone
from mutagen.id3 import ID3, TIT2, TALB, TPE1, TPE2, COMM, TDRC

parser = argparse.ArgumentParser(prog='youtube-dl-and-tag-mp3',description='save audio from youtube as mp3 and tag it.')
parser.add_argument('yt_url', help='youtube-url to download')
parser.add_argument('-p', '--printonly', help="just print the tags, don't download the mp3", action='store_true')
args = parser.parse_args()

regex_https_url = '^https:\/\/.+'
urlmatch = re.search(regex_https_url, args.yt_url, re.DOTALL)
if not urlmatch:
	sys.exit("error: yt_url is invalid")

regex_Provided_to_Youtube_videoDetails = '"videoDetails":\{"videoId":"[a-zA-Z0-9]+","title":".+","lengthSeconds":"[0-9]*","keywords":\[.*\],"channelId":"[a-zA-Z0-9_\-]+","isOwnerViewing":.+,"shortDescription":"Provided to YouTube (.+)Auto-generated by YouTube.","isCrawlable":.+,"thumbnail":\{"thumbnails":\[\{"url":'	# work on line 20
regex_Provided_to_Youtube_description = '"embed":\{"iframeUrl":"https:\/\/www\.youtube\.com/.+","width":[0-9]*,"height":[0-9]*\},"title":\{"simpleText":".*"\},"description":\{"simpleText":"Provided to YouTube (.+)Auto-generated by YouTube."\},"lengthSeconds"'	# work on line 20
regex_Provided_to_Youtube_attributedDescription = '"attributedDescription":\{"content":"Provided to YouTube by (.+)Auto-generated by YouTube."\}\}\},\{"itemSectionRenderer":'	# work on line 74
regex_Provided_to_Youtube_attributedDescriptionBodyText = '"attributedDescriptionBodyText":\{"content":"Provided to YouTube by (.+)Auto-generated by YouTube."\}\}\}\]\}\}'	# work on line 74
regex_Provided_to_Youtube_inner_line0a = 'by (.+)'
regex_Provided_to_Youtube_inner_line0b = '(.+)'
regex_Provided_to_Youtube_inner_line2 = '(.+) · (.+)'
regex_Provided_to_Youtube_inner_line4 = '(.+)'
regex_Provided_to_Youtube_inner_line6 = '℗ ([0-9]{4}) (.+)'
regex_TableFormat = '\[\{"infoRowRenderer":\{"title":\{"simpleText":"TITEL"\},"defaultMetadata":\{"runs":\[\{"text":"(.+)","navigationEndpoint":\{"clickTrackingParams":".*","commandMetadata":\{"webCommandMetadata":\{"url":".*","webPageType":".*","rootVe":.*\}\},"watchEndpoint":\{"videoId":".*","watchEndpointSupportedOnesieConfig":\{"html5PlaybackOnesieConfig":\{"commonConfig":\{"url":".*"\}\}\}\}\}\}\]\},"trackingParams":".*"\}\},\{"infoRowRenderer":\{"title":\{"simpleText":"INTERPRET"\},"defaultMetadata":\{"simpleText":"(.+)"\},"trackingParams":".*","infoRowExpandStatusKey":"structured-description-music-section-artists-row-state-id"\}\},\{"infoRowRenderer":\{"title":\{"simpleText":"ALBUM"\},"defaultMetadata":\{"simpleText":"(.+)"\},"trackingParams":".*"\}\},\{"infoRowRenderer":\{"title":\{"simpleText":"LIZENZEN"\}'
foo01 = '"videoDetails":\{"videoId":"[a-zA-Z0-9]+","title":".+","lengthSeconds":"[0-9]*","keywords":\[.*\],"channelId":"[a-zA-Z0-9_\-]+","isOwnerViewing":.+,"shortDescription":"P'
teststr1 = 'asdadas"videoDetails":{"videoId":"op9ApJJyhD4","title":"Dance with Me","lengthSeconds":"180","keywords":["Orleans","Dance With Me: The Best Of Orleans","Dance with Me"],"channelId":"UCL37WcHfgaSthoMcwiXEdYQ","isOwnerViewing":false,"shortDescription":"Provided to YouTube by Rhino/Elektra\n\nDance with Me · Orleans\n\nDance With Me: The Best Of Orleans\n\n℗ 1975 Elektra/Asylum Records for the United States and WEA International for the world outside of the United States.\n\nTrumpet: Blue Mitchell\nProducer: Chuck Plotkin\nDrums: Jerry Marotta\nGuitar, Vocals: John Hall\nBass  Guitar: Lance Hopper\nVocals: Lance Hopper\nSaxophone: Michael Brecker\nDrums, Piano: Wells Kelly\nComposer, Writer: Johanna D. Hall\nComposer, Writer: John Joseph Hall\nComposer: Wolfgang Amadeus Mozart\n\nAuto-generated by YouTube.","isCrawlable":true,"thumbnail":{"thumbnails":[{"url":asdasasdaasdasda'
useragent = 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'
filenamemp3 = ""

def getYtContentFromInternet(url):
    headers = {'User-agent': useragent}
    response = requests.get(url, headers=headers)
    if response:
        #print(response.text)
        lines = response.text.splitlines()
        #return lines[linenumber]
        return "".join(lines)	# line breaks vary, so rather join them into one line
    else:
	    print("could not load yt page")
	    return ""

def saveYtContentLineByLine(url):	# used for development only
    headers = {'User-agent': useragent}
    response = requests.get(url, headers=headers)
    if response:
        lines = response.text.splitlines()
        linenr = 0
        for line in lines:
            filename="./line"+str(linenr)
            linenr = linenr+1
            with open(filename, 'w') as f:
                f.write(line)
    else:
	    print("could not load yt page")

def formatAsJson(tags,indent):
    result = {
    "label": tags["label"],
    "title": tags["title"],
    "artist": tags["artist"],
    "album": tags["album"],
    "year": tags["year"],
    "company": tags["company"]
    }
    return json.dumps(result,indent=indent)
    

def getYtContentFromFile(filename):
    f = open(filename,"r")
    lines = f.readlines()
    return "".join(lines) # the file ought to contain just one line, but just in case join them

def getDummyTags(lines):
    result = {}
    result["title"]     = "title"
    result["artist"]    = "artist"
    result["album"]     = "album"
    result["label"]     = "label"
    result["year"]      = "2000"
    result["company"]   = "company"
    return result

def scrapForMetatags_Provided_to_Youtube(line):
    #substr = line[318000:323000]	# indexes for joined line
    outermatch = re.search(regex_Provided_to_Youtube_videoDetails, line, re.DOTALL)	# works on line 20 with regex_Provided_to_Youtube_inner_line0a
    #substr = line[322000:328000]	# indexes for joined line
    #outermatch = re.search(regex_Provided_to_Youtube_description, line, re.DOTALL)	# works on line 20 with regex_Provided_to_Youtube_inner_line0a
    #substr = line[578000:780000]	# indexes for joined line
    #outermatch = re.search(regex_Provided_to_Youtube_attributedDescription, line, re.DOTALL)	# works on line 74 with regex_Provided_to_Youtube_inner_line0b
    #substr = line[790000:1060000]	# indexes for joined line
    #outermatch = re.search(regex_Provided_to_Youtube_attributedDescriptionBodyText, line, re.DOTALL)	# works on line 74 with regex_Provided_to_Youtube_inner_line0b
    #outermatch = re.search(regex_Provided_to_Youtube_videoDetails, teststr1, re.DOTALL)
    if outermatch:
        #print("scrapForMetatags_Provided_to_Youtube: outer regex matches at position ", outermatch.start())
        desctext = outermatch.group(1)	# group(0) would be the entire match
        desclines = desctext.split('\\n') # workaround because I can't apply a regex to the whole text due to the line breaks (\n)
        #print(desclines)
        result = {}
        innermatch = re.search(regex_Provided_to_Youtube_inner_line0a, desclines[0])
        if innermatch:
            result["label"]   = innermatch.group(1)
        innermatch = re.search(regex_Provided_to_Youtube_inner_line2, desclines[2])
        if innermatch:
            result["title"]   = innermatch.group(1)
            result["artist"]  = innermatch.group(2)
        innermatch = re.search(regex_Provided_to_Youtube_inner_line4, desclines[4])
        if innermatch:
            result["album"]   = innermatch.group(1)
        innermatch = re.search(regex_Provided_to_Youtube_inner_line6, desclines[6])
        if innermatch:
            result["year"]    = innermatch.group(1)
            result["company"] = innermatch.group(2)
        return result
    #else:
    #    print("scrapForMetatags_Provided_to_Youtube: outer regex doesn't match")
    return None

def scrapForMetatagsTableFormat(line):
    #substr = line[800000:11100000]	# indexes for joined line
    match = re.search(regex_TableFormat, line)
    if match:
        #print("scrapForMetatagsTableFormat: regex matches at position ", match.start())
        result = {}
        result["title"]     = match.group(1)
        result["artist"]    = match.group(2)
        result["album"]     = match.group(3)
        result["label"]     = ""
        result["year"]      = ""
        result["company"]   = ""
        return result
    #else:
    #    print("scrapForMetatagsTableFormat: regex doesn't match")
    return None

def getTags(url): # get YT page and extract the tags
    ytcode = getYtContentFromInternet(url)
    #ytcode = getYtContentFromFile("./lines_op9ApJJyhD4/line74")	# Provided_to_Youtube
    #ytcode = getYtContentFromFile("./lines_PDvRZtbTqPk/line74")	# Provided_to_Youtube
    #ytcode = getYtContentFromFile("./lines_hgIc3fj9iuU/line74")	# table format
    #tags = getDummyTags("")
    tags = scrapForMetatags_Provided_to_Youtube(ytcode)
    if not tags:
        tags = scrapForMetatagsTableFormat(ytcode)
    return tags

class MyLogger(object):		# keep this in order to avoid status messages on stdout
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)

def saveMp3Tags(filename, tagvalues):
    taghandle = ID3(filename)	# or ID3(r''+filename)?
    if len(tagvalues["title"])>0:
        taghandle["TIT2"] = TIT2(encoding=3, text=u''+tagvalues["title"]+'')
    if len(tagvalues["artist"])>0:
        taghandle["TPE1"] = TPE1(encoding=3, text=u''+tagvalues["artist"]+'')
    if len(tagvalues["album"])>0:
        taghandle["TALB"] = TALB(encoding=3, text=u''+tagvalues["album"]+'')
    if len(tagvalues["year"])>0:
        taghandle["TDRC"] = TDRC(encoding=3, text=u''+tagvalues["year"]+'')
    #if len(tagvalues["asd"])>0:
    #taghandle["COMM"] = COMM(encoding=3, text=u''+comment+'')
    taghandle.save()

def ytdl_hook(d):
	# post-processing is done after this function, so we can't tag the mp3 from here
	# errors in this function will prevent the execution of post-processing
    if d['status'] == 'finished':
        filename = d['filename']
        print('download of file '+filename+' completed, now converting ...')

if not args.printonly:
    # then download the mp3 first
    #print("starting download")
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
    with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download([args.yt_url])
    # when this lines is reached, the download and conversation has been finished
    filenamemp3 = max(glob.glob("./*.mp3"), key=os.path.getctime)	# dirty workaround as I can't get the filename directly # or maybe getatime
    #for f in glob.glob("./*.mp3"):
    #    print(f+" "+datetime.fromtimestamp(os.path.getmtime(f), tz=timezone.utc).isoformat()+" "+datetime.fromtimestamp(os.path.getctime(f), tz=timezone.utc).isoformat()+" "+datetime.fromtimestamp(os.path.getatime(f), tz=timezone.utc).isoformat()+" ")
    print("setting tags on file "+filenamemp3)
    tags = getTags(args.yt_url)
    if tags:
        saveMp3Tags(filenamemp3, tags)
    else:
        print("could not get tag information")
else:
    # then don't download the mp3, just print the tags
    #saveYtContentLineByLine(args.yt_url)
    #tags=False
    tags = getTags(args.yt_url)
    if tags:
        print(formatAsJson(tags,None))
    else:
        print("could not get tag information")

