import re
import requests
import sys

if len(sys.argv)!=2:
	print("syntax is: "+sys.argv[0]+" <yt-url>")
url = sys.argv[1]
regex_Provided_to_Youtube_videoDetails = '"videoDetails":\{"videoId":"[a-zA-Z0-9]+","title":".+","lengthSeconds":"[0-9]*","keywords":\[.*\],"channelId":"[a-zA-Z0-9_\-]+","isOwnerViewing":.+,"shortDescription":"Provided to YouTube (.+)Auto-generated by YouTube.","isCrawlable":.+,"thumbnail":\{"thumbnails":\[\{"url":'
foo01 = '"videoDetails":\{"videoId":"[a-zA-Z0-9]+","title":".+","lengthSeconds":"[0-9]*","keywords":\[.*\],"channelId":"[a-zA-Z0-9_\-]+","isOwnerViewing":.+,"shortDescription":"Provided to YouTube (.+)'
foo02 = '"videoDetails":\{"videoId":"[a-zA-Z0-9]+","title":".+","lengthSeconds":"[0-9]*","keywords":\[.*\],"channelId":"[a-zA-Z0-9_\-]+","isOwnerViewing":.+,"shortDescription":"Provided to YouTube (.+)Auto-generated by YouTube.","isCrawlable":.+,"thumbnail":\{"thumbnails":\[\{"url":'
teststr1 = '"videoDetails":{"videoId":"op9ApJJyhD4","title":"Dance with Me","lengthSeconds":"180","keywords":["Orleans","Dance With Me: The Best Of Orleans","Dance with Me"],"channelId":"UCL37WcHfgaSthoMcwiXEdYQ","isOwnerViewing":false,"shortDescription":"Provided to YouTube by Rhino/Elektra\n\nDance with Me · Orleans\n\nDance With Me: The Best Of Orleans\n\n℗ 1975 Elektra/Asylum Records for the United States and WEA International for the world outside of the United States.\n\nTrumpet: Blue Mitchell\nProducer: Chuck Plotkin\nDrums: Jerry Marotta\nGuitar, Vocals: John Hall\nBass  Guitar: Lance Hopper\nVocals: Lance Hopper\nSaxophone: Michael Brecker\nDrums, Piano: Wells Kelly\nComposer, Writer: Johanna D. Hall\nComposer, Writer: John Joseph Hall\nComposer: Wolfgang Amadeus Mozart\n\nAuto-generated by YouTube.","isCrawlable":true,"thumbnail":{"thumbnails":[{"url":'
teststr2 = '"videoDetails":{"videoId":"op9ApJJyhD4","title":"Dance with Me","lengthSeconds":"180","keywords":["Orleans","Dance With Me: The Best Of Orleans","Dance with Me"],"channelId":"UCL37WcHfgaSthoMcwiXEdYQ","isOwnerViewing":false,"shortDescription":"Provided to YouTube by Rhino/Elektra\nAuto-generated by YouTube.","isCrawlable":true,"thumbnail":{"thumbnails":[{"url":'

#print(response.text)
#print(regex_Provided_to_Youtube_videoDetails)
#substr1 = response.text[600000:1200000]
x = re.search(foo02, teststr1, re.DOTALL)
if x!=None:
	print("start position:", x.start())
else:
	print("not found")
