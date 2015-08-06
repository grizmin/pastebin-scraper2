import sys, os, re, random, time, urllib2, socket, httplib, argparse, gzip, urlparser

class scraper(object):

  def __init__(self):
    # Load resources

    # User Agents
    try:
      with open("Data/User-Agents.txt","r") as f:
        self._agents = [a.strip() for a in f.readlines() if a.strip() is not "" and a.strip().isspace() is False]
    except(IOError):
      print("User-Agents.txt not found!")
      sys.exit()

    # Proxies
    try:
      with open("Data/Proxies.txt","r") as f:
        self._proxies = [p.strip() for p in f.readlines() if p.strip() is not "" and a.strip().isspace() is False]
      if(self._outOfProxies()):
        raise ValueError
    except(IOError):
      print("Proxies.txt not found!")
      sys.exit()
    except(ValueError):
      print("Not enough proxies to continue!")
      sys.exit()

    self._alreadyVisitedPasties = []

  def run(self,sleepTimer = 10):
    """
    Starts the process of scraping pastebin for pasties, sleeping for a passed amount of time
    """

    while 1:
      try:
        # obtain the source of pastebin and filter it 
        source = self._getSource("http://pastebin.com/archive")
        while(source is False or source is None):
          source = self._getSource("http://pastebin.com/archive")
        

        myParser = urlparser.pastebinParser()
        myParser.parse(source)
        loop = False
        print myParser.getPasties()
        # obtain the urls from the filtered source and make requests to the urls
        for url,title in myParser.getPasties():
          if("http://pastebin.com/raw.php?i="+url in self._alreadyVisitedPasties):
            if not loop: sys.stdout.write("\033[93mSkipping pastie. It\'s already downloaded: \033[0m")
            loop = True
            if loop: sys.stdout.write("%s " % url)
            continue
          print("\nGetting %s  Title: %s" % (url,title))  
          pastie = self._getSource("http://pastebin.com/raw.php?i="+url)
            
          if pastie is None:
            print ("DEBUG: URL:  %s, TITLE:" %s(url, title))
            print source
            raise NameError("Pastie is empty!")

          self._saveToFile(pastie, url, doArchive)
        
        self._sleep(sleepTimer)
      except(NameError,KeyboardInterrupt,EOFError) as e:
        sys.exit(e)
    
    return

  def _sleep(self, seconds):
    print("\n\033[94mGoing to sleep for {0} seconds...Zzz\033[0m".format(seconds))
    time.sleep(seconds)
    return

  def _getSource(self, url):
    """
    Establishes a connection to the URL
    """

    # prepare for the connection
    self._setProxy()
    req = urllib2.Request(url)
    req.add_header("User-Agent",self._randomAgent())

    try:
      # make the connection and check for the status
      request = urllib2.urlopen(req,None,timeout=5)
      if(request.code != 200):
        print("Status code "+request.code+"recieved!")
        return
      source = urllib2.unquote(request.read())
      
      # some proxies redirect to a login page or similar, with a simple check we can bypass this problem
      if(url is "http://pastebin.com/archive"  and "#1 paste tool since 2002" not in source):
        raise socket.error
      
      return source

    except(urllib2.HTTPError, urllib2.URLError):
      self._removeDeadProxy(self._curProxy)

    except(socket.timeout,socket.error,httplib.BadStatusLine):
      self._removeDeadProxy(self._curProxy)

  def _filterPasties(self, pastie, filters=['minecraft']):
    
    " Remove pasties with certain strings like \'minecraft\' "

    pattern = re.compile(r'\b(?:%s)\b' % '|'.join(filters), re.IGNORECASE)
    match = pattern.search(pastie)
    if match:
      pastie = "Filtered pastie found: \'%s\'. Deleting data." % match.group()
    
    return pastie


  def _saveToFile(self, data, name, doArchive=False):

    """
    Saves extracted data to file with a passed name
    """
    
    timeString = time.strftime("%d-%m-%Y", time.localtime())
    filename = doArchive and "%s.txt.gz" % name  or "%s.txt" % name
    directory = "Data/Results/%s/" % timeString
    
    data = self._filterPasties(data)

    # make sure we don't add duplicates to the visited list
    if("http://pastebin.com/raw.php?i="+name not in self._alreadyVisitedPasties and not os.path.isfile(directory + filename)):
      self._alreadyVisitedPasties.append("http://pastebin.com/raw.php?i="+name)
    
    # create the directory we want to save our data in
    if(os.path.isdir(directory) is False):
      os.makedirs(directory)
    
    opener =  doArchive and gzip.open or open
    print ("Saving data to file %s" % directory + filename)
    with opener(directory + filename, "w") as fs:
      fs.write(data)
    
    return

  def _randomAgent(self):
    """
    Returns a random user agent 
    """
    r = random.randint(0,len(self._agents)-1)
    return self._agents[r]

  def _setProxy(self):
    """
    Installs a ProxyHandler
    """
    proxy = urllib2.ProxyHandler({"http":self._randomProxy()})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    return

  def _randomProxy(self):
    """
    Returns a random proxy and sets it as current proxy
    """
    if(self._outOfProxies()):
      print("We ran out of proxies!")
      sys.exit()

    r = random.randint(0,len(self._proxies)-1)
    self._curProxy = self._proxies[r]
    print("Using proxy: "+self._curProxy)
    return self._proxies[r]

  def _removeDeadProxy(self,proxy):
    """
    Removes the passed proxy from the proxy pool
    """
    if(self._outOfProxies()):
      print("Not enough proxies left!")
      sys.exit()

    print("Removing dead proxy {0}".format(proxy))
    self._proxies.remove(proxy)
    return

  def _saveFilteredProxyList(self):
    """
    Saves the modified list of proxies to file
    """
    
    if(self._outOfProxies() is False):
      print("Saving proxy list...")

    # write changes to file
    with open("Data/Proxies.txt","w") as f:
      for p in self._proxies:
        f.write(p+os.linesep)
    return

  def _outOfProxies(self):
    return len(self._proxies) <= 0

  def __del__(self):
    # quickly save our changed proxy list
    self._saveFilteredProxyList()

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument("-s","--sleep",type=int,help="Seconds to sleep between scraping",required=False,default=10)
  parser.add_argument("--gzip","-gz",help="Saves compressed files",required=False,default=False,action="store_true")
  args = parser.parse_args()

  if(args.sleep < 0):
    print("Adjusting sleep timer to 1 second")
    args.sleep = 1
  
  doArchive = args.gzip
  
  s = scraper()
  s.run(args.sleep)
