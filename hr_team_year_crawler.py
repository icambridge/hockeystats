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
from datetime import datetime
import csv
import os

teams = {
            "ANA" : {"start": 2007},
            "MDA" : {"start": 1994, "end": 2006},
            "WIN" : {"start": 1980, "end": 1996},
            "PHX" : {"start": 1997, "end": 2014},
            "ARI" : {"start": 2016},
            "BOS" : {"start": 1925},
            "BUF" : {"start": 1971},
            "ATF" : {"start": 1973, "end": 1980},
            "CGY" : {"start": 1981},
            "QUE" : {"start": 1980, "end": 1995},
            "COL" : {"start": 1996},
            "MNS" : {"start": 1968, "end": 1993},
            "DAL" : {"start": 1994},
            "HAR" : {"start": 1980, "end": 1997},
            "CAR" : {"start": 1998},
            "CHB" : {"start": 1970, "end": 1926},
            "CHI" : {"start": 1987},
            "CBJ" : {"start": 2001},
            "DET" : {"start": 1933},
            "DTF" : {"start": 1931, "end": 1932},
            "DTC" : {"start": 1927, "end": 1930},
            "EDM" : {"start": 1980},
            "FLA" : {"start": 1994},
            "LAK" : {"start": 1968},
            "MIN" : {"start": 2001},
            "MTL" : {"start": 1917},
            "NSH" : {"start": 1999},
            "NJD" : {"start": 1983},
            "CLR" : {"start": 1977, "end": 1982},
            "KCS" : {"start": 1975, "end": 1796},
            "NYI" : {"start": 1973},
            "NYR" : {"start": 1927},
            "OTT" : {"start": 1993},
            "PHI" : {"start": 1968},
            "PIT" : {"start": 1968},
            "SJS" : {"start": 1992},
            "STL" : {"start": 1968},
            "TBL" : {"start": 1993},
            "TOR" : {"start": 1927},
            "TRS" : {"start": 1920, "end": 1926},
            "TRA" : {"start": 1918, "end": 1919},
            "VAN" : {"start": 1983},
            "VEG" : {"start": 2018},
            "WSH" : {"start": 1975},
            "WPG" : {"start": 2012},
            "ATL" : {"start": 2000, "end": 2011},
          }
d = datetime.today()

conn = http.client.HTTPSConnection("www.hockey-reference.com")

def writeCsv(team, year, skaters):
    if len(skaters) == 0:
        return

    directory = "./stats/team/%s" % (team)
    filename = "%s/%s.csv" % (directory, year)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = []
        for fieldname in skaters[0]:
            fieldnames.append(fieldname)

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i in range(len(skaters)):
            writer.writerow(skaters[i])

def buildSkaters(tree, team, year):
    names = tree.xpath('//*[@id="skaters"]/tbody/tr/td[1]/a/text()')
    links = tree.xpath('//*[@id="skaters"]/tbody/tr/td[1]/a/@href')
    agesPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[2]')
    positionsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[3]')
    gamesPlayedPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[4]')
    goalsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[5]')
    assistsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[6]')
    pointsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[7]')
    plusMinusPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[8]')
    pimPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[9]')
    evenGoalsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[10]')
    ppGoalsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[11]')
    shGoalsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[12]')
    gwGoalsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[13]')
    evenAssistsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[14]')
    ppAssistsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[15]')
    shAssistsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[16]')
    shotsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[17]')
    shotsPercentagePre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[18]')
    totalIceTimePre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[19]')
    averageIceTimePre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[20]')
    opsPre  = tree.xpath('//*[@id="skaters"]/tbody/tr/td[21]')
    dpsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[22]')
    psPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[23]')

    # to protect againist empty values
    positions = [x.text if x.text else '' for x in positionsPre]
    ages = [x.text if x.text else '' for x in agesPre]

    plusMinus = [x.text if x.text else 0 for x in plusMinusPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    assists = [x.text if x.text else 0 for x in assistsPre]
    goals = [x.text if x.text else 0 for x in goalsPre]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    pim = [x.text if x.text else 0 for x in pimPre]

    evenGoals = [x.text if x.text else 0 for x in evenGoalsPre]
    ppGoals = [x.text if x.text else 0 for x in ppGoalsPre]
    shGoals = [x.text if x.text else 0 for x in shGoalsPre]
    gwGoals = [x.text if x.text else 0 for x in gwGoalsPre]
    evenAssists = [x.text if x.text else 0 for x in evenAssistsPre]
    ppAssists = [x.text if x.text else 0 for x in ppAssistsPre]
    shAssists = [x.text if x.text else 0 for x in shAssistsPre]
    shots = [x.text if x.text else 0 for x in shotsPre]
    shotsPercentage = [x.text if x.text else 0 for x in shotsPercentagePre]

    ops = [x.text if x.text else 0 for x in opsPre]
    dps = [x.text if x.text else 0 for x in dpsPre]
    ps = [x.text if x.text else 0 for x in psPre]

    totalIceTime = [x.text if x.text else '' for x in totalIceTimePre]
    shotsPercentage = [x.text if x.text else '' for x in shotsPercentagePre]
    totalIceTime = [x.text if x.text else '' for x in totalIceTimePre]
    averageIceTime = [x.text if x.text else '' for x in averageIceTimePre]

    skaters = []
    count = len(names)
    counter = 0
    while counter < count:

        skater = {
            "name": names[counter],
            "link": links[counter],
            "age":  ages[counter],
            "positions": positions[counter],
            "games_played": gamesPlayed[counter],
            "goals": goals[counter],
            "assists": assists[counter],
            "points": points[counter],
            "plus_minus": plusMinus[counter],
            "pim": pim[counter],
            "even_strength_goals": evenGoals[counter],
            "power_play_goals": ppGoals[counter],
            "shorthanded_goals": shGoals[counter],
            "game_winning_goals": gwGoals[counter],
            "even_strength_assists": evenAssists[counter],
            "power_play_assists": ppAssists[counter],
            "shorthanded_assists": shAssists[counter],
            "shots": shots[counter],
            "shotsPercentage": shotsPercentage[counter],
            "total_ice_time": totalIceTime[counter],
            "average_ice_time": averageIceTime[counter],
            "offensive_point_share": ops[counter],
            "defensive_point_share": dps[counter],
            "overall_point_share": ps[counter],
            "team": team,
            "year": year
        }
        skaters.append(skater)
        counter = counter + 1

    return skaters

def getHtml(team, year):

    url = "/teams/%s/%d.html" % (team, year)

    conn.request("GET", url)
    response = conn.getresponse()

    print(team, year, response.status, response.reason)

    return response.read()


for team in teams:
    dates = teams[team]
    if "end" in dates:
        endDate = dates["end"]
    else:
        endDate = d.year

    year = dates["start"]

    while year <= endDate:

        content = getHtml(team, year)
        tree = html.fromstring(content)

        skaters = buildSkaters(tree, team, year)
        writeCsv(team, year, skaters)

        year = year + 1
