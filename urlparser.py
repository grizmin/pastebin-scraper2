from  sgmllib import SGMLParser
import base64, re

#Sample data
#                        <tr>
#                               <td><img src="/i/t.gif"  class="i_p0" alt="" border="0" /><a href="/u5ptkyLS">Marco's Crackshot</a></td>
#                               <td>21 sec ago</td>
#                               <td align="right"><a href="/archive/text">None</a></td>
#                        </tr>

class pastebinParser(SGMLParser):
  
  pastie = ()
  _debug = False
  _sanitarize = False
  def parse(self, s):
    self.feed(s)
    self.close()

  def reset(self):
    SGMLParser.reset(self)
    self.pasties = []
    self.intr = False
    self.intd = False
    self.ina = False
    self.title = []
    self.indata = False

  def start_a(self,attributes):
    if self.intd:
      for key, value in attributes:
        if "archive" not in value:
          self.ina = True
          self.indata = True
          self.pastie = self.pastie + (value.strip("/"),)

  def start_td(self, attributes):
    self.intd = True
  
  def end_td(self):
    self.intd = False
  
  def start_tr(self, attributes):
    self.intr = True
  
  def end_tr(self):
    self.intr = False

  def end_a(self):
    self.ina = False
    if self.title:
      self.pastie += (''.join(self.title),)
    if self.pastie:
      self.pasties.append(self.pastie)
    self.pastie = ()
    self.title = []

  def handle_data(self, data):
    if self.intr and self.intd and self.ina:
      if self._sanitarize: data = self.sanitarize(data)
      if self._debug: print "DEBUG: %s,%s" % (self.pastie,data)
      if self.indata:
        self.title.append(data)
        self.indata = False
      else:
        self.title[-1] += data

  def print_pasties(self):
    for k,v in self.pasties:
      print "url: %s Title: %s" % (k,v)

  def getPasties(self):
    if self._debug: print self.pasties
    return self.pasties

  def sanitarize(self, data):
     p = re.compile('(\'|\"|`|>|<|\%)', re.VERBOSE)
     match = p.search(data)
     if match:
       data = ''
     return data
