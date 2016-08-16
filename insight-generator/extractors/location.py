GEO_TOPIC_ENDPOINT = "http://localhost:8765/api/search?"

from base import Extractor

class GeoTopicExtractor(Extractor):

  def extract(self, content):
    self.locationCountHash = self.extraction.countHash("LOCATION")
    locations = self.locationCountHash.keys()

    if len(locations) > 0:
      self.params = "&".join(map(lambda l: "s={0}".format(self.modules['urllib'].quote(l)), locations))
      self.response = self.modules['urllib2'].urlopen(GEO_TOPIC_ENDPOINT + self.params).read()
      self.info = self.modules['json'].loads(self.response)
      extractedLocations = self.getLocations()
      extractedGeoInfo = self.getInfo()
    else:
      extractedLocations = [ ]
      extractedGeoInfo   = [ ]

    self.extraction.accumulate("geo", extractedLocations)
    self.extraction.accumulate("locations", extractedGeoInfo)

    return self.extraction

  def formatInfo(self, l, rawText):
    return {
     'name': l[0]['name'],
     'rawText': rawText,
     'count': self.locationCountHash[ rawText ],
     'countryCode': l[0]['countryCode'],
     'location': {
        'lat': l[0]['latitude'],
        'lon': l[0]['longitude']
     },
     'admin1Code': l[0]['admin1Code'],
     'admin2Code': l[0]['admin2Code']
    }

  def getInfo(self):
    return map(lambda k: self.formatInfo(self.info[k], k), self.info)

  def getLocations(self):
    return map(lambda k: self.formatInfo(self.info[k], k)["location"], self.info)