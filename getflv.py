#!/usr/bin/env python
# -*- coding: utf-8 -*-

#龙斌大话电影 
#http://video.56.com/opera/22121.html
#<a title="20131104" class="" href="http://www.56.com/u78/v_OTk4NzI0OTk.html" 

import os, sys, time, random, re
import requests
import urllib, urllib2
import wget
from wgety import Wgety
reload(sys);sys.setdefaultencoding('utf-8')



__version__ = '1.0'
__author__  = 'Yang Sen C <Sen.b.Yang@alcatel-sbell.com.cn>'
__date__    = "2014-02-18"
__license__ = "GNU Lesser General Public License (LGPL)"



link_pattern = re.compile('href=', re.MULTILINE) # re.IGNORECASE


class get_FLV:
	def __init__( self, weburl, outputdir, time_out = 2, proxies=None ):
		self.url = weburl
		self.dir = outputdir
		self.jsoncallbackValue = "jQuery171024871149915270507_"
		self.timeout = time_out
		self.dict = {}
		os.chdir( self.dir )

	def get_flv_downlink_url(self, webpageUrl, format="high"):
		#format: super > high > normal
		#http://www.flvcd.com/parse.php?kw=&flag=one&format=high
		#http://www.flvcd.com/parse.php?kw=http%3A%2F%2Fwww.56.com%2Fu57%2Fv_MTA0MzI0ODM4.html&flag=one&format=super
		flvcd_url = "http://www.flvcd.com/parse.php?kw=%s&flag=one&format=high" % webpageUrl
		headers = {'host':'www.flvcd.com',
		           'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0) Gecko/20100101 Firefox/4.0',
		           'Accept-Language':'en-us,en;q=0.5',
		           'Accept-Encoding':'gzip, deflate',
		           'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
		           'Keep-Alive':'115'}
		try:
			content = requests.get( flvcd_url, allow_redirects=False, timeout=self.timeout, headers=headers )
		except:
			return
		pattern=re.compile(r'href=".*" target="_blank" class="link" onclick=')
		downlink = pattern.findall(content.text)[0]
		downlink_url = re.compile('href="(.*)"\s+target').match(downlink).group(1)
		return downlink_url
		#<a href="http://f4.r.56.com/f4.c87.56.com/flvdownload/15/12/139236092976hd.flv?v=1&t=Fic-6sYet8oRBsQwk90S4A&r=838&e=1392726908&tt=641&sz=24357038&vid=106532824" target="_blank" class="link" onclick='_alert()
	def call_back(self, a, b, c):
		per = 100.0 * a * b / c
		if per > 100: per = 100
		print '%.2f%%' % per

	def download_flv_to_localdisk(self, downlink, localfile):
		#http://www.nowamagic.net/academy/detail/1302861
		urllib.urlretrieve(downlink, localfile, self.call_back)


	def run( self ):
		try:
			req = requests.get( self.url, allow_redirects=False, timeout=self.timeout )
		except:
			return

		if( req.status_code == requests.codes.ok ):
			regex = re.compile(r'title="\d+" class="" href=".*"\s+target')
			for i in regex.findall(req.text):
				array = i.split(" ")
				title = re.compile('title="(\d+)"').match(array[0]).group(1)
				link  = re.compile('href="(.*)"').match(array[2]).group(1)
				self.dict[title] = link

		for key in self.dict.keys():
			print "KEY=%s, Link=%s" % (key,self.dict[key])
			localfilename = key + ".flv"
			if os.path.exists (localfilename):
				continue
			downlinkurl = self.get_flv_downlink_url(self.dict[key])
			print downlinkurl
			if downlinkurl != None:
				print "Begin to Download %s\n" % localfilename
				self.download_flv_to_localdisk( downlinkurl, localfilename )

			time.sleep( 5 ) 


if __name__ == '__main__':
	#http://blog.csdn.net/wind__fantasy/article/details/6989356
	#http://www.nowamagic.net/academy/detail/1302861
	#http://blog.5d13.cn/resources/goweb/03.1.html
	LongBinTalkShow_56WebURL = "http://video.56.com/opera/22121.html"
	OutputDir = r"C:/temp/FLV"
	if not os.path.exists( OutputDir ):
		os.makedirs( OutputDir,0771 )

	t = get_FLV( LongBinTalkShow_56WebURL, OutputDir )
	t.run()





