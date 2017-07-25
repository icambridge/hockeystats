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
import time
import string
import re

conn = http.client.HTTPSConnection("www.hockey-reference.com")


def writeCsv(player, type, years):
    if len(years) == 0:
        print("No years")
        return

    directory = "./stats/player/%s" % (player)
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


def buildPlayer(tree):
    regex = re.compile('[^A-Z]')
    postion = tree.xpath('//*[@id="meta"]/div/p[1]/text()[1]')
    handed = tree.xpath('//*[@id="meta"]/div/p[1]/text()[2]')
    name = tree.xpath('//*[@id="meta"]/div/h1/text()')
    heightWeight = tree.xpath('//*[@id="meta"]/div/p[2]/text()')
    bornField = tree.xpath('//*[@id="necro-birth"]')
    if len(bornField) > 0:
        dob = bornField[0].attrib['data-birth']
    else:
        dob = ""

    if len(handed) > 0:
        handed = handed[0]
    else:
        handed = ""
    if len(postion) > 0:
        postition = postion[0]
    else:
        postition = ""
    if len(heightWeight) > 0:
        heightWeight = heightWeight[0]
    else:
        heightWeight = ""
    if len(name) > 0:
        name = name[0]
    else:
        name = ""

    postition = postition.strip('\\n')

    return {
        "position": regex.sub("", postition),
        "handed": regex.sub("", handed),
        "name": name,
        "heigh_and_weight": heightWeight,
        "date_of_birth": dob
    }


def buildTeams(teamsPre):
    teams = []
    for c in range(len(teamsPre)):
        team = teamsPre[c]
        team = list(team)
        if len(team) == 0:
            teams.append(teamsPre[c].text)
            continue

        for counter in range(len(team)):
            teams.append(team[counter].text)
    return teams


def buildAward(awardsPre):
    awards = []
    for awardCounter in range(len(awardsPre)):
        awardList = awardsPre[awardCounter]
        awardList = list(awardList)
        yearAwards = []
        for counter in range(len(awardList)):
            award = {
                "name": awardList[counter].text,
                "link": awardList[counter].attrib['href'],
            }
            yearAwards.append(award)
        awards.append(yearAwards)
    return awards


def buildNHLBasicYears(tree):
    years = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/th')
    if len(years) > 0:
        return buildNHLPlusYears(tree)
    return buildNHLNormalYears(tree)


def buildGoalieNHLYears(tree):
    years = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/th')
    if len(years) > 0:
        return buildGoalieNHLPlusYears(tree)
    return buildGoalieNHLNormalYears(tree)


def buildGoaliePlayoffYears(tree):
    years = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[3]/a/text()')
    wonPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[4]')
    gamesPlayedPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[5]')
    gamesStartedPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[6]')
    winsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[7]')
    losesPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[8]')
    tiesPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[9]')
    goalsAllowedPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[10]')
    shotsAgainistPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[11]')
    savesPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[12]')
    savesPrecentagePre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[13]')
    goalsAllowedAveragePre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[14]')
    shutoutsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[15]')
    minutesPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[16]')
    goodStartsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[17]')
    goodStartsPrecentagePre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[18]')
    badStartsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[19]')
    goalsAllowedPrecentagePre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[20]')
    goalsSavedAboveAveragePre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[21]')
    goalsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[22]')
    assistsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[23]')
    pointsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[24]')
    pimPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[25]')

    ages = [x.text if x.text else '' for x in agesPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    assists = [x.text if x.text else 0 for x in assistsPre]
    goals = [x.text if x.text else 0 for x in goalsPre]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    pim = [x.text if x.text else 0 for x in pimPre]
    won = [x.text if x.text else '' for x in wonPre]

    gamesStarted = [x.text if x.text else 0 for x in gamesStartedPre]
    wins = [x.text if x.text else 0 for x in winsPre]
    loses = [x.text if x.text else 0 for x in losesPre]
    ties = [x.text if x.text else 0 for x in tiesPre]
    goalsAllowedAverage = [x.text if x.text else 0 for x in goalsAllowedAveragePre]
    goalsAllowed = [x.text if x.text else 0 for x in goalsAllowedPre]
    shotsAgainist = [x.text if x.text else 0 for x in shotsAgainistPre]
    saves = [x.text if x.text else 0 for x in savesPre]
    savesPrecentage = [x.text if x.text else 0 for x in savesPrecentagePre]
    shutouts = [x.text if x.text else 0 for x in shutoutsPre]

    minutes = [x.text if x.text else 0 for x in minutesPre]
    goodStarts = [x.text if x.text else 0 for x in goodStartsPre]
    goodStartsPrecentage = [x.text if x.text else 0 for x in goodStartsPrecentagePre]
    badStarts = [x.text if x.text else 0 for x in badStartsPre]
    goalsAllowedPrecentage = [x.text if x.text else 0 for x in goalsAllowedPrecentagePre]
    goalsSavedAboveAverage = [x.text if x.text else 0 for x in goalsSavedAboveAveragePre]

    teams = buildTeams(teamsPre)
    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "team": teams[counter],
            "games_played": gamesPlayed[counter],
            "goals": goals[counter],
            "assists": assists[counter],
            "points": points[counter],
            "pim": pim[counter],
            "games_started": gamesStarted[counter],
            "wins": wins[counter],
            "loses": loses[counter],
            "ties": ties[counter],
            "goals_allowed_average": goalsAllowedAverage[counter],
            "goals_allowed": goalsAllowed[counter],
            "shots_againist": shotsAgainist[counter],
            "saves": saves[counter],
            "saves_percentage": savesPrecentage[counter],
            "shutouts": shutouts[counter],
            "minutes": minutes[counter],
            "good_starts": goodStarts[counter],
            "good_start_precentages": goodStartsPrecentage[counter],
            "bad_start": badStarts[counter],
            "goals_allowed_precentage": goalsAllowedPrecentage[counter],
            "goals_saved_aboved_average": goalsSavedAboveAverage[counter],
            "won": won[counter],
        }
        stats.append(year)
        counter = counter + 1

    return stats


def buildGoalieOtherYears(tree):
    years = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[3]/text()')
    gamesPlayedPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[4]')
    gamesStartedPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[5]')
    winsPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[6]')
    losesPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[7]')
    tiesPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[8]')
    goalsAllowedPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[9]')
    shotsAgainistPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[10]')
    savesPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[11]')
    savesPrecentagePre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[12]')
    goalsAllowedAveragePre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[13]')
    shutoutsPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[14]')
    minutesPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[15]')
    goodStartsPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[16]')
    goodStartsPrecentagePre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[17]')
    badStartsPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[18]')
    goalsAllowedPrecentagePre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[19]')
    goalsSavedAboveAveragePre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[20]')
    goalsPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[21]')
    assistsPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[22]')
    pointsPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[23]')
    pimPre = tree.xpath('//*[@id="stats_basic_other"]/tbody/tr/td[24]')

    ages = [x.text if x.text else '' for x in agesPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    assists = [x.text if x.text else 0 for x in assistsPre]
    goals = [x.text if x.text else 0 for x in goalsPre]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    pim = [x.text if x.text else 0 for x in pimPre]

    gamesStarted = [x.text if x.text else 0 for x in gamesStartedPre]
    wins = [x.text if x.text else 0 for x in winsPre]
    loses = [x.text if x.text else 0 for x in losesPre]
    ties = [x.text if x.text else 0 for x in tiesPre]
    goalsAllowedAverage = [x.text if x.text else 0 for x in goalsAllowedAveragePre]
    goalsAllowed = [x.text if x.text else 0 for x in goalsAllowedPre]
    shotsAgainist = [x.text if x.text else 0 for x in shotsAgainistPre]
    saves = [x.text if x.text else 0 for x in savesPre]
    savesPrecentage = [x.text if x.text else 0 for x in savesPrecentagePre]
    shutouts = [x.text if x.text else 0 for x in shutoutsPre]

    minutes = [x.text if x.text else 0 for x in minutesPre]
    goodStarts = [x.text if x.text else 0 for x in goodStartsPre]
    goodStartsPrecentage = [x.text if x.text else 0 for x in goodStartsPrecentagePre]
    badStarts = [x.text if x.text else 0 for x in badStartsPre]
    goalsAllowedPrecentage = [x.text if x.text else 0 for x in goalsAllowedPrecentagePre]
    goalsSavedAboveAverage = [x.text if x.text else 0 for x in goalsSavedAboveAveragePre]

    teams = buildTeams(teamsPre)
    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "team": teams[counter],
            "games_played": gamesPlayed[counter],
            "goals": goals[counter],
            "assists": assists[counter],
            "points": points[counter],
            "pim": pim[counter],
            "games_started": gamesStarted[counter],
            "wins": wins[counter],
            "loses": loses[counter],
            "ties": ties[counter],
            "goals_allowed_average": goalsAllowedAverage[counter],
            "goals_allowed": goalsAllowed[counter],
            "shots_againist": shotsAgainist[counter],
            "saves": saves[counter],
            "saves_percentage": savesPrecentage[counter],
            "shutouts": shutouts[counter],
            "minutes": minutes[counter],
            "good_starts": goodStarts[counter],
            "good_start_precentages": goodStartsPrecentage[counter],
            "bad_start": badStarts[counter],
            "goals_allowed_precentage": goalsAllowedPrecentage[counter],
            "goals_saved_aboved_average": goalsSavedAboveAverage[counter],
        }
        stats.append(year)
        counter = counter + 1

    return stats


def buildGoalieOtherPlayoffYears(tree):
    years = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[3]/text()')
    gamesPlayedPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[4]')
    gamesStartedPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[5]')
    winsPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[6]')
    losesPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[7]')
    tiesPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[8]')
    goalsAllowedPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[9]')
    shotsAgainistPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[10]')
    savesPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[11]')
    savesPrecentagePre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[12]')
    goalsAllowedAveragePre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[13]')
    shutoutsPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[14]')
    minutesPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[15]')
    goodStartsPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[16]')
    goodStartsPrecentagePre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[17]')
    badStartsPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[18]')
    goalsAllowedPrecentagePre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[19]')
    goalsSavedAboveAveragePre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[20]')
    goalsPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[21]')
    assistsPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[22]')
    pointsPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[23]')
    pimPre = tree.xpath('//*[@id="stats_playoffs_other"]/tbody/tr/td[24]')

    ages = [x.text if x.text else '' for x in agesPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    assists = [x.text if x.text else 0 for x in assistsPre]
    goals = [x.text if x.text else 0 for x in goalsPre]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    pim = [x.text if x.text else 0 for x in pimPre]

    gamesStarted = [x.text if x.text else 0 for x in gamesStartedPre]
    wins = [x.text if x.text else 0 for x in winsPre]
    loses = [x.text if x.text else 0 for x in losesPre]
    ties = [x.text if x.text else 0 for x in tiesPre]
    goalsAllowedAverage = [x.text if x.text else 0 for x in goalsAllowedAveragePre]
    goalsAllowed = [x.text if x.text else 0 for x in goalsAllowedPre]
    shotsAgainist = [x.text if x.text else 0 for x in shotsAgainistPre]
    saves = [x.text if x.text else 0 for x in savesPre]
    savesPrecentage = [x.text if x.text else 0 for x in savesPrecentagePre]
    shutouts = [x.text if x.text else 0 for x in shutoutsPre]

    minutes = [x.text if x.text else 0 for x in minutesPre]
    goodStarts = [x.text if x.text else 0 for x in goodStartsPre]
    goodStartsPrecentage = [x.text if x.text else 0 for x in goodStartsPrecentagePre]
    badStarts = [x.text if x.text else 0 for x in badStartsPre]
    goalsAllowedPrecentage = [x.text if x.text else 0 for x in goalsAllowedPrecentagePre]
    goalsSavedAboveAverage = [x.text if x.text else 0 for x in goalsSavedAboveAveragePre]

    teams = buildTeams(teamsPre)
    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "team": teams[counter],
            "games_played": gamesPlayed[counter],
            "goals": goals[counter],
            "assists": assists[counter],
            "points": points[counter],
            "pim": pim[counter],
            "games_started": gamesStarted[counter],
            "wins": wins[counter],
            "loses": loses[counter],
            "ties": ties[counter],
            "goals_allowed_average": goalsAllowedAverage[counter],
            "goals_allowed": goalsAllowed[counter],
            "shots_againist": shotsAgainist[counter],
            "saves": saves[counter],
            "saves_percentage": savesPrecentage[counter],
            "shutouts": shutouts[counter],
            "minutes": minutes[counter],
            "good_starts": goodStarts[counter],
            "good_start_precentages": goodStartsPrecentage[counter],
            "bad_start": badStarts[counter],
            "goals_allowed_precentage": goalsAllowedPrecentage[counter],
            "goals_saved_aboved_average": goalsSavedAboveAverage[counter],
        }
        stats.append(year)
        counter = counter + 1

    return stats


def buildGoalieNHLNormalYears(tree):
    years = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[3]/a/text()')
    gamesPlayedPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[4]')
    gamesStartedPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[5]')
    winsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[6]')
    losesPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[7]')
    tiesPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[8]')
    goalsAllowedPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[9]')
    shotsAgainistPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[10]')
    savesPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[11]')
    savesPrecentagePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[12]')
    goalsAllowedAveragePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[13]')
    shutoutsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[14]')
    minutesPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[15]')
    goodStartsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[16]')
    goodStartsPrecentagePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[17]')
    badStartsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[18]')
    goalsAllowedPrecentagePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[19]')
    goalsSavedAboveAveragePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[20]')
    goaliePointSharePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[21]')
    goalsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[22]')
    assistsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[23]')
    pointsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[24]')
    pimPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[25]')
    awardsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[26]')

    ages = [x.text if x.text else '' for x in agesPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    assists = [x.text if x.text else 0 for x in assistsPre]
    goals = [x.text if x.text else 0 for x in goalsPre]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    pim = [x.text if x.text else 0 for x in pimPre]

    gamesStarted = [x.text if x.text else 0 for x in gamesStartedPre]
    wins = [x.text if x.text else 0 for x in winsPre]
    loses = [x.text if x.text else 0 for x in losesPre]
    ties = [x.text if x.text else 0 for x in tiesPre]
    goalsAllowedAverage = [x.text if x.text else 0 for x in goalsAllowedAveragePre]
    goalsAllowed = [x.text if x.text else 0 for x in goalsAllowedPre]
    shotsAgainist = [x.text if x.text else 0 for x in shotsAgainistPre]
    saves = [x.text if x.text else 0 for x in savesPre]
    savesPrecentage = [x.text if x.text else 0 for x in savesPrecentagePre]
    shutouts = [x.text if x.text else 0 for x in shutoutsPre]

    minutes = [x.text if x.text else 0 for x in minutesPre]
    goodStarts = [x.text if x.text else 0 for x in goodStartsPre]
    goodStartsPrecentage = [x.text if x.text else 0 for x in goodStartsPrecentagePre]
    badStarts = [x.text if x.text else 0 for x in badStartsPre]
    goalsAllowedPrecentage = [x.text if x.text else 0 for x in goalsAllowedPrecentagePre]
    goalsSavedAboveAverage = [x.text if x.text else 0 for x in goalsSavedAboveAveragePre]
    goaliePointShare = [x.text if x.text else 0 for x in goaliePointSharePre]

    awards = buildAward(awardsPre)
    teams = buildTeams(teamsPre)
    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "team": teams[counter],
            "games_played": gamesPlayed[counter],
            "goals": goals[counter],
            "assists": assists[counter],
            "points": points[counter],
            "pim": pim[counter],
            "awards": awards[counter],
            "games_started": gamesStarted[counter],
            "wins": wins[counter],
            "loses": loses[counter],
            "ties": ties[counter],
            "goals_allowed_average": goalsAllowedAverage[counter],
            "goals_allowed": goalsAllowed[counter],
            "shots_againist": shotsAgainist[counter],
            "saves": saves[counter],
            "saves_percentage": savesPrecentage[counter],
            "shutouts": shutouts[counter],
            "minutes": minutes[counter],
            "good_starts": goodStarts[counter],
            "good_start_precentages": goodStartsPrecentage[counter],
            "bad_start": badStarts[counter],
            "goals_allowed_precentage": goalsAllowedPrecentage[counter],
            "goals_saved_aboved_average": goalsSavedAboveAverage[counter],
            "goalie_point_share": goaliePointShare[counter],
        }
        stats.append(year)
        counter = counter + 1

    return stats


def buildGoalieNHLPlusYears(tree):
    years = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[3]/a/text()')
    gamesPlayedPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[4]')
    gamesStartedPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[5]')
    winsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[6]')
    losesPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[7]')
    tiesPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[8]')
    goalsAllowedPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[9]')
    shotsAgainistPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[10]')
    savesPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[11]')
    savesPrecentagePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[12]')
    goalsAllowedAveragePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[13]')
    shutoutsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[14]')
    minutesPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[15]')
    goodStartsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[16]')
    goodStartsPrecentagePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[17]')
    badStartsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[18]')
    goalsAllowedPrecentagePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[19]')
    goalsSavedAboveAveragePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[20]')
    goaliePointSharePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[21]')
    goalsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[22]')
    assistsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[23]')
    pointsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[24]')
    pimPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[25]')
    awardsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[26]')

    ages = [x.text if x.text else '' for x in agesPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    assists = [x.text if x.text else 0 for x in assistsPre]
    goals = [x.text if x.text else 0 for x in goalsPre]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    pim = [x.text if x.text else 0 for x in pimPre]

    gamesStarted = [x.text if x.text else 0 for x in gamesStartedPre]
    wins = [x.text if x.text else 0 for x in winsPre]
    loses = [x.text if x.text else 0 for x in losesPre]
    ties = [x.text if x.text else 0 for x in tiesPre]
    goalsAllowedAverage = [x.text if x.text else 0 for x in goalsAllowedAveragePre]
    goalsAllowed = [x.text if x.text else 0 for x in goalsAllowedPre]
    shotsAgainist = [x.text if x.text else 0 for x in shotsAgainistPre]
    saves = [x.text if x.text else 0 for x in savesPre]
    savesPrecentage = [x.text if x.text else 0 for x in savesPrecentagePre]
    shutouts = [x.text if x.text else 0 for x in shutoutsPre]

    minutes = [x.text if x.text else 0 for x in minutesPre]
    goodStarts = [x.text if x.text else 0 for x in goodStartsPre]
    goodStartsPrecentage = [x.text if x.text else 0 for x in goodStartsPrecentagePre]
    badStarts = [x.text if x.text else 0 for x in badStartsPre]
    goalsAllowedPrecentage = [x.text if x.text else 0 for x in goalsAllowedPrecentagePre]
    goalsSavedAboveAverage = [x.text if x.text else 0 for x in goalsSavedAboveAveragePre]
    goaliePointShare = [x.text if x.text else 0 for x in goaliePointSharePre]

    awards = buildAward(awardsPre)
    teams = buildTeams(teamsPre)
    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "team": teams[counter],
            "games_played": gamesPlayed[counter],
            "goals": goals[counter],
            "assists": assists[counter],
            "points": points[counter],
            "pim": pim[counter],
            "awards": awards[counter],
            "games_started": gamesStarted[counter],
            "wins": wins[counter],
            "loses": loses[counter],
            "ties": ties[counter],
            "goals_allowed_average": goalsAllowedAverage[counter],
            "goals_allowed": goalsAllowed[counter],
            "shots_againist": shotsAgainist[counter],
            "saves": saves[counter],
            "saves_percentage": savesPrecentage[counter],
            "shutouts": shutouts[counter],
            "minutes": minutes[counter],
            "good_starts": goodStarts[counter],
            "good_start_precentages": goodStartsPrecentage[counter],
            "bad_start": badStarts[counter],
            "goals_allowed_precentage": goalsAllowedPrecentage[counter],
            "goals_saved_aboved_average": goalsSavedAboveAverage[counter],
            "goalie_point_share": goaliePointShare[counter],
        }
        stats.append(year)
        counter = counter + 1

    return stats


def buildOtherYears(tree, type):
    years = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[3]/text()')
    gamesPlayedPre = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[4]')
    goalsPre = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[5]')
    assistsPre = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[6]')
    pointsPre = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[7]')
    plusMinusPre = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[8]')
    pimPre = tree.xpath('//*[@id="stats_'+type+'_other"]/tbody/tr/td[9]')  # to protect againist empty values
    ages = [x.text if x.text else '' for x in agesPre]

    plusMinus = [x.text if x.text else 0 for x in plusMinusPre]
    points = [x.text if x.text else 0 for x in pointsPre]
    assists = [x.text if x.text else 0 for x in assistsPre]
    goals = [x.text if x.text else 0 for x in goalsPre]
    gamesPlayed = [x.text if x.text else 0 for x in gamesPlayedPre]
    pim = [x.text if x.text else 0 for x in pimPre]

    teams = buildTeams(teamsPre)
    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "team": teams[counter],
            "games_played": gamesPlayed[counter],
            "goals": goals[counter],
            "assists": assists[counter],
            "points": points[counter],
            "plus_minus": plusMinus[counter],
            "pim": pim[counter],
        }
        stats.append(year)
        counter = counter + 1

    return stats


def buildNHLPlayoffYears(tree):
    years = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[3]/a/text()')
    winsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[4]')
    gamesPlayedPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[5]')
    goalsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[6]')
    assistsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[7]')
    pointsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[8]')
    plusMinusPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[9]')
    pimPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[10]')
    evenGoalsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[11]')
    ppGoalsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[12]')
    shGoalsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[13]')
    gwGoalsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[14]')
    shotsPre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[15]')
    shotsPercentagePre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[16]')
    totalIceTimePre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[17]')
    averageIceTimePre = tree.xpath('//*[@id="stats_playoffs_nhl"]/tbody/tr/td[18]')

    # to protect againist empty values
    ages = [x.text if x.text else '' for x in agesPre]
    wins = [x.text if x.text else '' for x in winsPre]

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
    shots = [x.text if x.text else 0 for x in shotsPre]
    shotsPercentage = [x.text if x.text else 0 for x in shotsPercentagePre]

    totalIceTime = [x.text if x.text else '' for x in totalIceTimePre]
    averageIceTime = [x.text if x.text else '' for x in averageIceTimePre]

    teams = buildTeams(teamsPre)

    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "win": wins[counter],
            "team": teams[counter],
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
            "shots": shots[counter],
            "shotsPercentage": shotsPercentage[counter],
            "total_ice_time": totalIceTime[counter],
            "average_ice_time": averageIceTime[counter],
        }
        stats.append(year)
        counter = counter + 1

    return stats


def buildNHLNormalYears(tree):
    years = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[3]/a/text()')
    gamesPlayedPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[4]')
    goalsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[5]')
    assistsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[6]')
    pointsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[7]')
    plusMinusPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[8]')
    pimPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[9]')
    evenGoalsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[10]')
    ppGoalsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[11]')
    shGoalsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[12]')
    gwGoalsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[13]')
    evenAssistsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[14]')
    ppAssistsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[15]')
    shAssistsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[16]')
    shotsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[17]')
    shotsPercentagePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[18]')
    totalIceTimePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[19]')
    averageIceTimePre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[20]')
    awardsPre = tree.xpath('//*[@id="stats_basic_nhl"]/tbody/tr/td[21]')

    # to protect againist empty values
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

    totalIceTime = [x.text if x.text else '' for x in totalIceTimePre]
    averageIceTime = [x.text if x.text else '' for x in averageIceTimePre]

    teams = buildTeams(teamsPre)
    awards = buildAward(awardsPre)

    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "team": teams[counter],
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
            "awards": awards[counter]
        }
        stats.append(year)
        counter = counter + 1

    return stats


def buildNHLPlusYears(tree):
    years = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/th/text()')
    agesPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[1]')
    teamsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[2]')
    leagues = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[3]/a/text()')
    gamesPlayedPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[4]')
    goalsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[5]')
    assistsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[6]')
    pointsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[7]')
    plusMinusPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[8]')
    pimPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[9]')
    evenGoalsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[10]')
    ppGoalsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[11]')
    shGoalsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[12]')
    gwGoalsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[13]')
    evenAssistsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[14]')
    ppAssistsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[15]')
    shAssistsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[16]')
    shotsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[17]')
    shotsPercentagePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[18]')
    totalShotsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[19]')
    totalIceTimePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[20]')
    averageIceTimePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[21]')
    foWinsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[22]')
    foLosesPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[23]')
    foPrecentagePre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[24]')
    hitsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[25]')
    blocksPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[26]')
    takeawaysPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[27]')
    giveawaysPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[28]')
    awardsPre = tree.xpath('//*[@id="stats_basic_plus_nhl"]/tbody/tr/td[29]')

    # to protect againist empty values
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
    foPercentage = [x.text if x.text else 0 for x in foPrecentagePre]

    totalIceTime = [x.text if x.text else '' for x in totalIceTimePre]
    averageIceTime = [x.text if x.text else '' for x in averageIceTimePre]

    hits = [x.text if x.text else 0 for x in hitsPre]
    blocks = [x.text if x.text else 0 for x in blocksPre]
    takeaways = [x.text if x.text else 0 for x in takeawaysPre]
    giveaways = [x.text if x.text else 0 for x in giveawaysPre]

    awards = buildAward(awardsPre)
    teams = buildTeams(teamsPre)

    stats = []
    count = len(years)
    counter = 0
    while counter < count:
        year = {
            "year": years[counter],
            "age": ages[counter],
            "league": leagues[counter],
            "team": teams[counter],
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
        stats.append(year)
        counter = counter + 1

    return stats


def crawlPlayer(url):
    content = getHtml(url)

    playerName = url.split("/")[3].split(".")[0]
    # Done because they hide stats inside comments
    content = str(content).replace("<!--", "").replace("-->", "")
    tree = html.fromstring(content)

    player = buildPlayer(tree)
    writeCsv(playerName, "overall", [player])

    if player["position"] != "G":
        scrapeSkater(playerName, tree)
    else:
        scrapeGoalie(playerName, tree)


def scrapeSkater(playerName, tree):
    years = buildNHLBasicYears(tree)
    writeCsv(playerName, "skater_nhl_basic", years)

    years = buildNHLPlayoffYears(tree)
    writeCsv(playerName, "skater_nhl_playoffs", years)

    years = buildOtherYears(tree, "basic")
    writeCsv(playerName, "skater_other_basic", years)

    years = buildOtherYears(tree, "playoffs")
    writeCsv(playerName, "skater_other_playoff", years)


def scrapeGoalie(playerName, tree):
    years = buildGoalieNHLYears(tree)
    writeCsv(playerName, "goalie_nhl_basic", years)

    years = buildGoaliePlayoffYears(tree)
    writeCsv(playerName, "goalie_nhl_playoffs", years)

    years = buildGoalieOtherYears(tree)
    writeCsv(playerName, "goalie_other_basic", years)

    years = buildGoalieOtherPlayoffYears(tree)
    writeCsv(playerName, "goalie_other_playoffs", years)


letters = list(string.ascii_lowercase)
a = 7
while a < len(letters):
    content = getHtml("/players/" + letters[a] + "/")
    tree = html.fromstring(content)
    unBoldPlayerPages = tree.xpath('//*[@id="div_players"]/p/a/@href')
    boldPlayerPages = tree.xpath('//*[@id="div_players"]/p/strong/a/@href')
    playersPages = unBoldPlayerPages + boldPlayerPages
    numberFound = len(playersPages)

    print("Found %s for %s" % (numberFound, letters[a]))
    i = 0
    while i < numberFound:
        try:
            crawlPlayer(playersPages[i])
        except http.client.RemoteDisconnected:
            os.wait(10)
            conn = http.client.HTTPSConnection("www.hockey-reference.com")
            continue
        except ConnectionResetError:
            os.wait(10)
            conn = http.client.HTTPSConnection("www.hockey-reference.com")
            continue
        i = i + 1

print("Finished")