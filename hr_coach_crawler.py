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
import time


conn = http.client.HTTPSConnection("www.hockey-reference.com")

def writeCsv(coach, years):
    if len(years) == 0:
        print("No years")
        return

    directory = "./stats/coach"
    filename = "%s/%s.csv" % (directory, coach)

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

def buildYears(tree):
    seasons = tree.xpath('//*[@id="coach"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[1]')
    teams = tree.xpath('//*[@id="coach"]/tbody/tr/td[2]/a/text()')
    leagues = tree.xpath('//*[@id="coach"]/tbody/tr/td[3]/a/text()')
    gamesPlayedPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[4]')
    winsPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[5]')
    losesPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[6]')
    tiesPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[7]')
    otLosesPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[8]')
    pointsPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[9]')
    pointsPrecentagePre = tree.xpath('//*[@id="coach"]/tbody/tr/td[10]')
    finishPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[12]')
    playoffWinsPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[13]')
    playoffLosesPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[14]')
    playoffTiesPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[15]')
    playoffWinLosePre = tree.xpath('//*[@id="coach"]/tbody/tr/td[16]')
    playoffNotesPre = tree.xpath('//*[@id="coach"]/tbody/tr/td[17]')

    ages = [x.text if x.text else 0 for x in agesPre]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    wins = [x.text if x.text else 0 for x in winsPre]
    loses = [x.text if x.text else 0 for x in losesPre]
    ties = [x.text if x.text else 0 for x in tiesPre]
    otLoses = [x.text if x.text else 0 for x in otLosesPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    pointsPercentages = [x.text if x.text else 0 for x in pointsPrecentagePre]
    finishes = [x.text if x.text else '' for x in finishPre]
    playoffWins = [x.text if x.text else 0 for x in playoffWinsPre]
    playoffLoses = [x.text if x.text else 0 for x in playoffLosesPre]
    playoffTies = [x.text if x.text else 0 for x in playoffTiesPre]
    playoffWinLose = [x.text if x.text else 0 for x in playoffWinLosePre]
    playoffNotes = [x.text if x.text else '' for x in playoffNotesPre]

    years = []
    i = 0
    while i < len(seasons):
        year = {
            "season": seasons[i],
            "leage": leagues[i],
            "team": teams[i],
            "games_played": gamesPlayed[i],
            "wins": wins[i],
            "loses": loses[i],
            "ties": ties[i],
            "overtime_loses": otLoses[i],
            "points": points[i],
            "points_percentage": pointsPercentages[i],
            "finishing_position": finishes[i],
            "playoff_note": playoffNotes[i],
            "playoff_wins": playoffWins[i],
            "playoff_loses": playoffLoses[i],
            "playoff_ties": playoffTies[i],
            "playoff_win_lose": playoffWinLose[i]
        }
        years.append(year)
        i = i + 1

    return years


def getHtml(url):
    time.sleep(2)
    conn.request("GET", url)
    response = conn.getresponse()

    print(url, response.status, response.reason)

    return response.read()

def crawlCoach(url):

    content = getHtml(url)

    coachName = url.split("/")[2].split(".")[0]
    tree = html.fromstring(content)

    years = buildYears(tree)
    writeCsv(coachName, years)

content = getHtml("/coaches/")
tree = html.fromstring(content)
unBoldCoachPages = tree.xpath('//*[@id="coaches"]/tbody/tr/th/a/@href')
boldCoachPages = tree.xpath('//*[@id="coaches"]/tbody/tr/th//strong/a/@href')
coachPages = unBoldCoachPages + boldCoachPages
numberFound = len(coachPages)

print("Found %s" % (numberFound))

for i in range(numberFound):
    crawlCoach(coachPages[i])
