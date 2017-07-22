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

teams = [
            "ANA",
            "PHX",
            "BOS",
            "BUF",
            "CGY",
            "COL",
            "DAL",
            "CAR",
            "CHI",
            "CBJ",
            "DET",
            "EDM",
            "FLA",
            "LAK",
            "MIN",
            "MTL",
            "NSH",
            "NJD",
            "NYI",
            "NYR",
            "OTT",
            "PHI",
            "PIT",
            "SJS",
            "STL",
            "TBL",
            "TOR",
            "VAN",
            "VEG",
            "WSH",
            "WPG",
          ]

conn = http.client.HTTPSConnection("www.hockey-reference.com")

def writeCsv(team, years):
    if len(years) == 0:
        print("No years")
        return

    directory = "./stats/team/%s" % (team)
    filename = "%s/overall.csv" % (directory)

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

def getHtml(team):

    url = "/teams/%s/" % (team)

    conn.request("GET", url)
    response = conn.getresponse()

    print(team, response.status, response.reason)

    return response.read()

def buildYears(team, tree):
    seasons = tree.xpath('//*[@id="'+team+'"]/tbody/tr/th/a/text()')
    seasonsLinks = tree.xpath('//*[@id="'+team+'"]/tbody/tr/th/a/@href')
    leagues = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[1]/a/text()')
    teamName = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[2]/a/text()')
    gamesPlayedPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[3]')
    winsPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[4]')
    losesPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[5]')
    tiesPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[6]')
    otLosesPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[7]')
    pointsPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[8]')
    pointsPrecentagePre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[9]')
    finishPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[12]')
    playoffsPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[13]')
    coachesPre = tree.xpath('//*[@id="'+team+'"]/tbody/tr/td[14]')

    code = [x.split("/")[2] for x in seasonsLinks]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    wins = [x.text if x.text else 0 for x in winsPre]
    loses = [x.text if x.text else 0 for x in losesPre]
    ties = [x.text if x.text else 0 for x in tiesPre]
    otLoses = [x.text if x.text else 0 for x in otLosesPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    pointsPercentages = [x.text if x.text else 0 for x in pointsPrecentagePre]
    finishes = [x.text if x.text else '' for x in finishPre]
    playoffs = [x.text if x.text else '' for x in playoffsPre]
    coaches = []

    for coachListCounter in range(len(coachesPre)):
        coachList = coachesPre[coachListCounter]
        coachList = list(coachList)
        yearCoaches = []
        for counter in range(len(coachList)):
            yearCoaches.append(coachList[counter].text)

        coaches.append(yearCoaches)

    years = []
    i = 0
    while i < len(seasons):
        year = {
            "code": code[i],
            "season": seasons[i],
            "leage": leagues[i],
            "team_name": teamName[i],
            "games_played": gamesPlayed[i],
            "wins": wins[i],
            "loses": loses[i],
            "ties": ties[i],
            "overtime_loses": otLoses[i],
            "points": points[i],
            "points_percentage": pointsPercentages[i],
            "finishing_position": finishes[i],
            "playoff_result": playoffs[i],
            "coaches": coaches[i]
        }
        years.append(year)
        i = i + 1

    return years


for i in range(len(teams)):

        content = getHtml(teams[i])
        tree = html.fromstring(content)

        years = buildYears(teams[i], tree)
        writeCsv(teams[i], years)
