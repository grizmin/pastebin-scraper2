from  sgmllib import SGMLParser

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

  def handle_data(self, data):
    if self.intd and self.ina:
      self.pastie += (data,)

  def print_pasties(self):
    for k,v in self.pasties:
      print "url: %s Title: %s" % (k,v)

  def getPasties(self):
    return self.pasties

