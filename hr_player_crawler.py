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

def writeCsv(player, type, years):
    if len(years) == 0:
        print("No years")
        return

    directory = "./stats/player/%" % (player)
    filename = "%s/%s.csv" % (directory, type)

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
    conn.request("GET", url)
    response = conn.getresponse()

    print(url, response.status, response.reason)

    return response.read()

def buildNHLYears(tree):
        year = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/th')
        agesPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[1]')
        teams = tree.xpath('//*[@id="skaters"]/tbody/tr/td[2]/a/text()')
        leagues = tree.xpath('//*[@id="skaters"]/tbody/tr/td[3]/a/text()')
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
        totalShotsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[19]')
        totalIceTimePre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[20]')
        averageIceTimePre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[21]')
        foWinsPre  = tree.xpath('//*[@id="skaters"]/tbody/tr/td[22]')
        foLosesPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[23]')
        foPrecentagePre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[24]')
        hitsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[25]')
        blocksPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[26]')
        takeawaysPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[27]')
        giveawaysPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[28]')
        awardsPre = tree.xpath('//*[@id="skaters"]/tbody/tr/td[29]')

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
        totalShots = [x.text if x.text else 0 for x in totalShotsPre]

        foWins = [x.text if x.text else 0 for x in foWinsPre]
        foLoses = [x.text if x.text else 0 for x in foLosesPre]
        foPercentage = [x.text if x.text else 0 for x in foPercentagePre]

        totalIceTime = [x.text if x.text else '' for x in totalIceTimePre]
        averageIceTime = [x.text if x.text else '' for x in averageIceTimePre]

        hits = [x.text if x.text else 0 for x in foWinsPre]
        blocks = [x.text if x.text else 0 for x in foLosesPre]
        takeaways = [x.text if x.text else 0 for x in foWinsPre]
        giveaways = [x.text if x.text else 0 for x in foLosesPre]
        awards = []

        for awardCounter in range(len(awardsPre)):
            awardList = awardsPre[awardCounter]
            awardList = list(awardList)
            yearAwards = []
            for counter in range(len(awardList)):
                awards = {
                    "name": awardList[counter].text,
                    "link": awardList[counter].attrib['href'],
                }
                yearAwards.append(awards)

            awards.append(yearAwards)

        years = []
        count = len(names)
        counter = 0
        while counter < count:

            year = {
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
                "total_shots": totalShots[counter],
                "shotsPercentage": shotsPercentage[counter],
                "total_ice_time": totalIceTime[counter],
                "average_ice_time": averageIceTime[counter],
                "faceoff_wins": foWins[counter],
                "faceoff_loses": foLoses[counter],
                "faceoff_percentage": foPercentage[counter],
                "hits": hits[counter],
                "blocks": blocks[counter],
                "takeaways": takeaways[counter],
                "giveaways": giveaways[counter],
                "awards": awards[counter]
            }
            years.append(year)
            counter = counter + 1

        return years

def crawlPlayer(url):

    content = getHtml(url)

    playerName = url.split("/")[2].split(".")[0]
    tree = html.fromstring(content)

    years = buildNHLYears(tree)
    writeCsv(playerName, "nhl", years)


letters = list(string.ascii_lowercase)


for a in range(len(letters)):
    content = getHtml("/players/"+letters[a]+"/")
    tree = html.fromstring(content)
    unBoldPlayerPages = tree.xpath('//*[@id="div_players"]/p/a/@href')
    boldPlayerPages = tree.xpath('//*[@id="div_players"]/p/strong/a/@href')
    playersPages = unBoldPlayerPages + boldPlayerPages
    numberFound = len(playersPages)

    print("Found %s" % (numberFound))

    for i in range(numberFound):
        crawlPlayer(playersPages[i])
