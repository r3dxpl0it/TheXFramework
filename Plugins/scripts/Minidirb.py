import sys
import urllib2
import ssl
import thread
import requests
def __url_maker__(url , method = 'best'):
        if method is 'best' : 
            if 'https://' in url : 
                url = url.split('https://')
                url = url[1]
            elif  'http://' in url : 
                url = url.split('http://')
                url = url[1]
            try : 
                furl = requests.get('https://' + url)
                furl = 'https://' + url
            except : 
                try : 
                    furl = requests.get('http://' + url) 
                    furl = 'http://' + url
                except : 
                    furl = url 
        return furl

def pybuster(url, depth, max_depth, dir_list , verbose = False):
    if (depth > max_depth):
        return
    depth = depth +1

    for d in dir_list:
        new_url = url + "/" + d
        try:
            # make a SSL handler that ignores SSL CERT issues
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE

            response = urllib2.urlopen(new_url, context=ctx)
            if response and response.getcode() == 200:
                print response.getcode(), "[+] FOUND %s" % (new_url)
                thread.start_new_thread(pybuster, (new_url, depth, max_depth, dir_list, ))
        except urllib2.HTTPError, e:
            if e.code == 401:
                print e.code , "[!] Authorization Required %s " % (new_url)
            elif e.code == 403 :
                if verbose is True  : 
                    print e.code , "[!] Forbidden %s " % (new_url)
            elif e.code == 404 and verbose:
                if verbose is True  : 
                    print e.code , "[-] Not Found %s " % (new_url)
            elif e.code == 503 :
                if verbose is True  : 
                    print e.code , "[!] Service Unavailable %s " % (new_url)
            else:
                if verbose is True  : 
                    print e.code , "[?] Unknwon %s %s" % (new_url , e.code)  

def load_file(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

# -----------------------------------------------------------------------------
# main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    try : 
        def usage():
            print "%s <url> <depth> <dirlist filename> <-v/-vv> " % (sys.argv[0])
        if len(sys.argv) <> 5:
            usage()
            sys.exit(0)

        url = __url_maker__(sys.argv[1])
        depth = int(sys.argv[2])
        dir_file = sys.argv[3]
        dir_list = load_file(dir_file)
        print(url)
        if 'vv' in sys.argv[4] : 
            pybuster(url, 0, depth, dir_list , True)
        else : 
            pybuster(url, 0, depth, dir_list , False)

        print "\n Max Depth Reached \n"
    except KeyboardInterrupt :
        exit()