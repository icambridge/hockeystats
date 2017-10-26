#!/usr/bin/env python
# Copyright 2017-present Iain Cambridge.
#
# Licensed under the MIT License(the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     https://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import http.client
from lxml import html
import csv
import os
import sys
import time
import string
import re

if len(sys.argv) != 3:
    print( "Usage: %s id name" % (sys.argv[0]))
    exit(-1)


conn = http.client.HTTPConnection("www.eliteprospects.com")

def writeCsv(player, years):
    if len(years) == 0:
        print("No years")
        return

    directory = "./stats/eliteprospect/player/"
    filename = "%s/%s.csv" % (directory, player)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = []
        for fieldname in years[0]:
            fieldnames.append(fieldname)

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i in range(len(years)):
            writer.writerow(years[i])


def getHtml(url):
    time.sleep(2)
    conn.request("GET", url, None, {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"})
    response = conn.getresponse()

    print(url, response.status, response.reason)

    return response.read()

id = sys.argv[1]
name = sys.argv[2]
content = getHtml("/%s?player=%s" % ("player.php", id))
content = str(content).replace("\\n", "").replace("\\t", "")
r =re.compile('<span id=\"fontSections\">CAREER STATISTICS</span>(.*?)<span id=\"fontSections\">CAREER TOTALS<\/span>', re.MULTILINE + re.S)
m = r.search(content)
tree = html.fromstring(m.group())

tables = tree.xpath('table')

yearsPre = tree.xpath('table/tr/td[1]/font')
teams = tree.xpath('table/tr/td[2]/font/text()')
leagues = tree.xpath('table/tr/td[3]/font/text()')
gamesPlayedPre = tree.xpath('table/tr/td[4]/font')
goalsPre = tree.xpath('table/tr/td[5]/font')
assistsPre = tree.xpath('table/tr/td[6]/font')
totalPointsPre = tree.xpath('table/tr/td[7]/strong/font')
plusMinsPre = tree.xpath('table/tr/td[8]/font')
pimPre = tree.xpath('table/tr/td[9]/font')

years = [x.text if x.text else '' for x in yearsPre]
gamesPlayed = [x.text if x.text else '' for x in gamesPlayedPre]
goals = [x.text if x.text else '' for x in goalsPre]
assists = [x.text if x.text else '' for x in assistsPre]
totalPoints = [x.text if x.text else '' for x in totalPointsPre]
plusMinus = [x.text if x.text else '' for x in plusMinsPre]
pim = [x.text if x.text else '' for x in pimPre]

stats = []

count = len(years)
counter = 0
while counter < count:
    year = {
        "year": years[counter].lstrip(),
        "league": leagues[counter].lstrip(),
        "team": teams[counter].lstrip(),
        "games_played": gamesPlayed[counter],
        "goals": goals[counter],
        "assists": assists[counter],
        "points": totalPoints[counter],
        "plus_minus": plusMinus[counter],
        "pim": pim[counter],
    }
    stats.append(year)
    counter = counter + 1

writeCsv(name, stats)