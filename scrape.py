#!/usr/bin/env python
import re

import requests
from bs4 import BeautifulSoup

from owslib.wfs import WebFeatureService

PROXY_URL = "https://consultation.lgbce.org.uk/OLProxy/Gateway.php"

def get_wfs_url_from_proxy(proxy_url):
    req = requests.get("{}?SERVICE=WMS&request=GetCapabilities".format(
        proxy_url
    ))
    soup = BeautifulSoup(req.text, "lxml")
    url = soup.find_all(
        True, {'xlink:href': re.compile('geoserver/LGBCE')})[0]['xlink:href']
    url = url.replace('WMS', 'WFS')
    return url


url = get_wfs_url_from_proxy(PROXY_URL)
# url = "http://lgbce-mapping-production-180789741.eu-west-1.elb.amazonaws.com:8080/geoserver/LGBCE/ows?SERVICE=WFS"


wfs11 = WebFeatureService(url=url, version='2.0.0')

# import ipdb; ipdb.set_trace()

for key, info in wfs11.contents.items():
    layer_url = "{}&version=1.0.0&request=GetFeature&typeName={}&maxFeatures=500&outputFormat=application/json".format(url, key)
    req = requests.get(layer_url)
    print(key)
    with open('data/{}.geojson'.format(key.replace(':', '-')), 'wb') as f:
        f.write(req.content)



# http://lgbce-mapping-production-180789741.eu-west-1.elb.amazonaws.com:8080/geoserver/LGBCE/ows?SERVICE=WFS&
# http://lgbce-mapping-production-180789741.eu-west-1.elb.amazonaws.com:8080/geoserver/LGBCE/ows?service=WFS&
