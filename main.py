#!/usr/bin/env python
# encoding: utf-8
#
# Copyright 2010 Ricardo Niederberger Cabral
#  (ricardo at isnotworking dot com)
#
#  This file is part of Delicious Tag Cleaner.
#
#  Delicious Tag Cleaner is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Delicious Tag Cleaner is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with Delicious Tag Cleaner.  If not, see <http://www.gnu.org/licenses/>.
  
import wsgiref.handlers
import cgi

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext import db

footer = """
<hr/>
       
<div style="float: right;">
<img src="http://code.google.com/appengine/images/appengine-silver-120x30.gif"
alt="Powered by Google App Engine" />
</div>
Found it useful? Please consider donating!
<form action="https://www.paypal.com/cgi-bin/webscr" method="post">
<input type="hidden" name="cmd" value="_s-xclick">
<input type="image" src="https://www.paypal.com/en_US/i/btn/btn_donateCC_LG.gif" border="0" name="submit" alt="PayPal - The safer, easier way to pay online!">
<img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1">
<input type="hidden" name="encrypted" value="-----BEGIN PKCS7-----MIIHbwYJKoZIhvcNAQcEoIIHYDCCB1wCAQExggEwMIIBLAIBADCBlDCBjjELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAkNBMRYwFAYDVQQHEw1Nb3VudGFpbiBWaWV3MRQwEgYDVQQKEwtQYXlQYWwgSW5jLjETMBEGA1UECxQKbGl2ZV9jZXJ0czERMA8GA1UEAxQIbGl2ZV9hcGkxHDAaBgkqhkiG9w0BCQEWDXJlQHBheXBhbC5jb20CAQAwDQYJKoZIhvcNAQEBBQAEgYC2FYGMoit8Y1ROwKZ2h3h9Gvun0ye+Dk48/cxSgrDi/AAKAjvBus3fOeroeHthd7n0S4cVxxZwZkg6Y9Hgm5BOQC4x+tTO0EDvtX+4WjyZTPI5DoszYw1Xi+V5LJr5ytIbRYkP7Sk1iSZW1WK2xPJ+mbnMSschLn8Qh0B3Y4IkNjELMAkGBSsOAwIaBQAwgewGCSqGSIb3DQEHATAUBggqhkiG9w0DBwQIexIsfHpROu+Agci5gzPY4iBqhn4iOIvEiaNz7/Juk9zK8NFLpeY81JEisnGsrFGdFg8qLE5+xYFpuMALoHX1k6GAktjLQb7PmVvDNTZ/PCzi/6NZIB3gryYBnppurvU9/eMx1ec8pxNofjSpNsn6inbTr6y0MOmRtCmK8IzQc0kvlR02jnkPubKCKLJNATnkwzoTmVp2g+UpIwtChJwCZR/eAIwCI0oEAdTCEn0BZhtysWfiSih1UF9mhwhcIDiAmsSCR3DweUm1R7j68bd/NeJyyaCCA4cwggODMIIC7KADAgECAgEAMA0GCSqGSIb3DQEBBQUAMIGOMQswCQYDVQQGEwJVUzELMAkGA1UECBMCQ0ExFjAUBgNVBAcTDU1vdW50YWluIFZpZXcxFDASBgNVBAoTC1BheVBhbCBJbmMuMRMwEQYDVQQLFApsaXZlX2NlcnRzMREwDwYDVQQDFAhsaXZlX2FwaTEcMBoGCSqGSIb3DQEJARYNcmVAcGF5cGFsLmNvbTAeFw0wNDAyMTMxMDEzMTVaFw0zNTAyMTMxMDEzMTVaMIGOMQswCQYDVQQGEwJVUzELMAkGA1UECBMCQ0ExFjAUBgNVBAcTDU1vdW50YWluIFZpZXcxFDASBgNVBAoTC1BheVBhbCBJbmMuMRMwEQYDVQQLFApsaXZlX2NlcnRzMREwDwYDVQQDFAhsaXZlX2FwaTEcMBoGCSqGSIb3DQEJARYNcmVAcGF5cGFsLmNvbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAwUdO3fxEzEtcnI7ZKZL412XvZPugoni7i7D7prCe0AtaHTc97CYgm7NsAtJyxNLixmhLV8pyIEaiHXWAh8fPKW+R017+EmXrr9EaquPmsVvTywAAE1PMNOKqo2kl4Gxiz9zZqIajOm1fZGWcGS0f5JQ2kBqNbvbg2/Za+GJ/qwUCAwEAAaOB7jCB6zAdBgNVHQ4EFgQUlp98u8ZvF71ZP1LXChvsENZklGswgbsGA1UdIwSBszCBsIAUlp98u8ZvF71ZP1LXChvsENZklGuhgZSkgZEwgY4xCzAJBgNVBAYTAlVTMQswCQYDVQQIEwJDQTEWMBQGA1UEBxMNTW91bnRhaW4gVmlldzEUMBIGA1UEChMLUGF5UGFsIEluYy4xEzARBgNVBAsUCmxpdmVfY2VydHMxETAPBgNVBAMUCGxpdmVfYXBpMRwwGgYJKoZIhvcNAQkBFg1yZUBwYXlwYWwuY29tggEAMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADgYEAgV86VpqAWuXvX6Oro4qJ1tYVIT5DgWpE692Ag422H7yRIr/9j/iKG4Thia/Oflx4TdL+IFJBAyPK9v6zZNZtBgPBynXb048hsP16l2vi0k5Q2JKiPDsEfBhGI+HnxLXEaUWAcVfCsQFvd2A1sxRr67ip5y2wwBelUecP3AjJ+YcxggGaMIIBlgIBATCBlDCBjjELMAkGA1UEBhMCVVMxCzAJBgNVBAgTAkNBMRYwFAYDVQQHEw1Nb3VudGFpbiBWaWV3MRQwEgYDVQQKEwtQYXlQYWwgSW5jLjETMBEGA1UECxQKbGl2ZV9jZXJ0czERMA8GA1UEAxQIbGl2ZV9hcGkxHDAaBgkqhkiG9w0BCQEWDXJlQHBheXBhbC5jb20CAQAwCQYFKw4DAhoFAKBdMBgGCSqGSIb3DQEJAzELBgkqhkiG9w0BBwEwHAYJKoZIhvcNAQkFMQ8XDTA4MDUyMjE5NTcxMVowIwYJKoZIhvcNAQkEMRYEFI8ucvIOKnAKLKtZD/35kAkPfTe5MA0GCSqGSIb3DQEBAQUABIGAh3A5KkpJDJfKrkfy0up5Pl74xZ/I/4BcO0U42zoo/K8I9wvMaw2lzK+8j6m1t2QeNJATrQwkCz8gtO7J+HsCy/sXCpqzwfXnxVPFia6X7wQEQI5Nj3UBbjkw4hRNPkRjJ9yn+KwElActR6ZyJUVwFV5jchjBs2RiCqXhlhDu5Vg=-----END PKCS7-----
">
</form>
<p><a href='http://blog.isnotworking.com/2007/12/delicious-tag-cleaner.html'>Discuss about this tool and send feedback</a>
"""

class MergeTransaction(db.Model):
  old = db.StringProperty()
  new = db.StringProperty() 
  count = db.IntegerProperty(default=1)
  
class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""<html><head><title>del.icio.us tag cleaner</title></head><body>
        <div style="float: right; border-left-style: solid;">
        <img src="img/sc1.png"
        alt="Sample screenshot" title="Sample screenshot" />
        </div>
        
        <p>This is a tool for removing unnecessary tags from your <a href='http://del.icio.us'>del.icio.us</a> bookmarks.

        <p>If you're like me, you probably have thousands of bookmarks collected over years and years of web surfing and hundreds of tags used to describe them. 
        But the thing is that over these years you haven't been able to come up with a consistent taxonomy for your tags.

        <p>You might have, for example, dozens of different tags for expressing links related to software development: "dev", "devel", "development" etc.

        <p>This tool can suggest you tags to be merged together, so you can choose one by one and have it merge the chosen tags on your del.icio.us account.
        
        <p>Examples of suggested merges: “book”, “books” and “ebooks” tags into a single “book” tag.
        <hr/>
        <form action="/tag_trivia" method="post">
                <div>del.icio.us username: <INPUT type="text" name="username"></div>
                <div>password: <INPUT type="password" name="pw"></div><p><b>Terms of service:</b> Use at your own risk. This service doesn't store user-specific data. Your del.icio.us username and password will be transmitted over a non-secure connection, thus subject to interception by malicious third parties on your network.
                <br/><div><input type="submit" value="Suggest me tags to be cleaned!"></div>
        </form>

        %s
        
        <script type="text/javascript">
        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
        document.write(unescape("%%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%%3E%%3C/script%%3E"));
        </script>
        <script type="text/javascript">
        var pageTracker = _gat._getTracker("UA-63372-22");
        pageTracker._initData();
        pageTracker._trackPageview();
        </script>
        </body></html>
             """% footer)

import base64
from xml.etree import ElementTree as et

from cachedata import sampledata
from BeautifulSoup import BeautifulSoup

class RenameTagHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("""NOK""")
    
    def post(self):
        username = cgi.escape(self.request.get('username'))
        pw = cgi.escape(self.request.get('pw'))
        encoded = base64.b64encode(username + ':' + pw)
        #self.response.out.write( username + ':' + pw)
        authstr = "Basic "+encoded
        #self.response.out.write( authstr)
        old = cgi.escape(self.request.get('old'))
        new = cgi.escape(self.request.get('new'))
        url = "https://api.del.icio.us/v1/tags/rename?new=%s&old=%s" % (new,old)
        #self.response.out.write( url)
        mheaders = {'Authorization':authstr,
                    "User-Agent" : "del.icio.us tag cleaner",
                    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                    "Keep-Alive": "300",
                    "Connection": "keep-alive",
                    "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                    "Cache-Control": "max-age=0",    
        }
        
        # store user preference
        query = db.GqlQuery("SELECT * FROM MergeTransaction WHERE old = :old AND new = :new",old=old, new=new)
        results = query.fetch(1)
        if results:
            tx = results[0]
            tx.count += 1
            tx.put()
        else:
            tx = MergeTransaction()
            tx.old = old
            tx.new = new
            tx.put()
        try:
            result = urlfetch.fetch(url,headers = mheaders)
        except:
            self.response.out.write('NOK')
            return
            
        #self.response.out.write(result.content)
        #self.response.out.write(result.status_code)        
        if result.status_code == 200:
            data = result.content
            #self.response.out.write(data)        
            if data.find('<result>done</result>') != -1:
                self.response.out.write('OK')        
                return
                    
        self.response.out.write('NOK')

class FetchTagsHandler(webapp.RequestHandler):
    def get(self):
        self.redirect("/")
        
    def post(self):
        username = cgi.escape(self.request.get('username'))
        pw = cgi.escape(self.request.get('pw'))
        encoded = base64.b64encode(username + ':' + pw)
        authstr = "Basic "+encoded
        url = "https://api.del.icio.us/v1/tags/get"

        self.response.out.write("""<html><head><title>Cleaning del.icio.us tags for %s</title>
        <script src="http://www.google.com/jsapi"></script>
        <script type="text/javascript">
        // Load jQuery
        google.load("jquery", "1");
        </script>
        <script type="text/javascript" src="/js/jquery.blockUI.js"></script>                
        <script type="text/javascript">
        function rename(oldt,newt)
        {
        
            jQuery.blockUI({ fadeOut: 200, css: { 
                border: 'none', 
                padding: '15px', 
                backgroundColor: '#000', 
                '-webkit-border-radius': '10px', 
                '-moz-border-radius': '10px', 
                opacity: '.5', 
                color: '#fff' 
            } });
            setTimeout(jQuery.unblockUI, 5000);
            $.post("/rename", { username: "%s", pw: "%s", old: oldt, new: newt},
              function(data){
                if (data == 'OK') {
                     $('#'+oldt+newt).fadeOut("slow");
                } else {
                    alert("Sorry. Your operation couldn't be completed because del.icio.us won't allow this service to run too many commands at once. Please tell them (feedback@del.icio.us) to increase our limit!");
                }                

                jQuery.unblockUI( {fadeOut: 0});
              });
        }        
        </script>
        </head><body>""" % (username, username, pw))
        
        self.response.out.write('<div style="float: right; margin-right: 30px;"><h1>Your top tags</h1>')

        data = None

        mheaders = {'Authorization':authstr,
                    "User-Agent" : "del.icio.us tag cleaner",
                    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                    "Keep-Alive": "300",
                    "Connection": "keep-alive",
                    "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                    "Cache-Control": "max-age=0",    
        }

        if 1:
            result = urlfetch.fetch(url,headers = mheaders)    
            if result.status_code == 200 and len(result.content) > 10:
                data = result.content
            else:
                self.response.out.write("Sorry. Your operation couldn't be completed because del.icio.us won't allow this service to run too many commands at once. Please tell them (feedback@del.icio.us) to increase our limit!</body></html>")
                return
        else:
            data = sampledata

        soup = BeautifulSoup(data)

        tags = [[tag['tag'], int(tag['count'])] for tag in soup.findAll('tag')]
        tags.sort(lambda x,y: cmp(y[1],x[1]))
        
        tag_popularity = {}
        for tag in tags:
            tag_popularity[tag[0]] = int(tag[1])
        
        for tag in tags[:20]:
            self.response.out.write('<li><a href="http://del.icio.us/%s/%s">%s</a> (%s)'% (username, tag[0], tag[0], tag[1]))

        self.response.out.write("""</div><h1>Merge candidates</h1><p>Click on the right arrow button (<img src='img/rarrow.gif'/>) to rename a tag as suggested. Due to del.icio.us limitations, you may need to click a few times before it finally works and the selected pair of tags disappears.</p>""")

        tomerge_tags = [] # list of tuples (old,new)
        for tag in tags:
            for tagp in tags:
                old = tagp[0]
                new = tag[0]
                if new in old and new != old and len(new) > 3:
                    tomerge_tags.append([old, new])
        
        tomerge_tags.sort(lambda y,x: cmp(tag_popularity[x[1]],tag_popularity[y[1]]))
        
        tomerge_tags_shorten = []
        tomerge_tags_plural = []        

        for tag in tomerge_tags:
            if  tag[0] == tag[1]+'s' or \
                tag[0] == tag[1]+'es' or \
                tag[0] == tag[1][:-1]+'ies':
                tomerge_tags_plural.append(tag)
            else:
                tomerge_tags_shorten.append(tag)

        def write_tag(tag):
            id = tag[0] + tag[1]
            self.response.out.write("""<li id='%s'>%s <img onclick="rename('%s','%s');" src='img/rarrow.gif'/ title="rename" border='0' style='cursor: pointer;'> %s</li>""" % (id,tag[0], tag[0], tag[1], tag[1]))

        if tomerge_tags_plural:
            self.response.out.write('<h2>Remove plural</h2>')
        for tag in tomerge_tags_plural:
            write_tag(tag)

        if tomerge_tags_shorten:
            self.response.out.write('<h2>Shorten</h2>')                        
        for tag in tomerge_tags_shorten:
            write_tag(tag)
            
        self.response.out.write(footer+'</body></html>')

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/tag_trivia', FetchTagsHandler),
                                        ('/rename', RenameTagHandler)],
                                       debug=False)
  wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
  main()