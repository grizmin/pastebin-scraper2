from  sgmllib import SGMLParser
import base64, re

class pastebinParser(SGMLParser):
  
  pastie = ()
  
  def parse(self, s):
    self.feed(s)
    self.close()

  def reset(self):
    SGMLParser.reset(self)
    self.pasties = []
    self.intd = False
    self.ina = False
    self.title = ''

  def start_a(self,attributes):
    if self.intd:
      for key, value in attributes:
        if "archive" not in value:
          self.ina = True
          self.pastie = self.pastie + (value.strip("/"),)

  def start_td(self, attributes):
    self.intd = True
  
  def end_td(self):
    self.intd = False
  
  def end_a(self):
    self.ina = False
    if self.pastie:
      self.pasties.append(self.pastie)
    self.pastie = ()
    self.title = ''

  def handle_data(self, data):
    if self.intd and self.ina:
      data = self.sanitarize(data)
      self.title += str(data)
      self.pastie += (self.title,)
      self.ina = False
      
  def print_pasties(self):
    for k,v in self.pasties:
      print "url: %s Title: %s" % (k,v)

  def getPasties(self):
    return self.pasties
    self.indata = True

  def sanitarize(self, data):
     p = re.compile('(\'|\"|`|>|<|\%)', re.VERBOSE)
     match = p.search(data)
     if match:
       data = ''
     return data
