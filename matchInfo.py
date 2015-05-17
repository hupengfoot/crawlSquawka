# -*- coding: utf-8 -*-
import MySQLdb
from DBUtils.PooledDB import PooledDB
import requests
import json
import codecs
from bs4 import BeautifulSoup

mysqlConfig = {
    'Host':'127.0.0.1',
    'User':'root',
    'Port':3306,
    'Passwd':'',
    'Db':'squawka',
    'LeastConns':5
}

#url = 'http://s3-irl-laliga.squawka.com/match/6?time=259&_=1430452315203' 
url = 'http://s3-irl-laliga.squawka.com/dp/ingame/'
matchesDir = './matches/'

class myDbPool:
    pool = None
    def __init__(self):
        print 'init myDbPool'

    def mysqlInit(self):
        self.pool = PooledDB(MySQLdb,mysqlConfig['LeastConns'],host=mysqlConfig['Host'],user=mysqlConfig['User'],passwd=mysqlConfig['Passwd'],db=mysqlConfig['Db'],port=mysqlConfig['Port'])
    
    def myInsert(self, sql):
        conn = self.pool.connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            print 'insert success'
        except:
            print 'insert fail!'
            conn.rollback()
        conn.close()

    
#get one Match Page url
def getMatchUrl(url, matchNum):
    return url + str(matchNum)

def onlyDownloadPage(url, matchNum):
    response = requests.get(url)
    soup = creatSoup(response.text)
    temp = soup.prettify()
    matchName = matchesDir + str(matchNum)
    f = codecs.open(matchName, 'w', 'utf-8')
    f.write(temp);
    f.close();

#download page
def downloadpage(url):
    response = requests.get(url)
    #temp = soup.prettify()
    return creatSoup(response.text)

#read page from local file
def readDownloadPage():
    f = open('./squawka', 'r')
    content = f.read();
    f.close();
    return creatSoup(content)

#creat soup 
def creatSoup(content):
    soup = BeautifulSoup(content)
    return soup 

#creat teams info array
def creatTeams(soup):
    teams = []
    iteams = soup.find_all('team')
    homeTeam = {} 
    homeTeam['team_id'] = iteams[0]['id']
    homeTeam['team_name'] = iteams[0].long_name.contents[1]
    teams.append(homeTeam)
    awayTeam = {}
    awayTeam['team_id'] = iteams[1]['id']
    awayTeam['team_name'] = iteams[1].long_name.contents[1]
    teams.append(awayTeam)
    sql1 = "insert into tbTeamInfo (iTeamID, szTeamName) values('{}','{}')".format(homeTeam['team_id'].encode('utf-8'), homeTeam['team_name'].encode('utf-8'))
    sql2 = "insert into tbTeamInfo (iTeamID, szTeamName) values('{}','{}')".format(awayTeam['team_id'].encode('utf-8'), awayTeam['team_name'].encode('utf-8'))
    mydbpool.myInsert(sql1)
    mydbpool.myInsert(sql2)
    return teams

#creat player info
def creatPlayers(soup):
    players = {}
    iPlayers = soup.find_all('player')
    for one in iPlayers:
        player = {}
        player['id'] = one['id']
        player['team_id'] = one['team_id']
        player['first_name'] = one.first_name.contents[1]
        player['last_name'] = one.last_name.contents[1]
        player['name'] = player['first_name'] + " " + player['last_name']
        player['photo'] = one.photo.contents[1]
        player['position'] = one.position.contents[1]
        player['team_name'] = one.team_name.contents[1]
        player['dob'] = getSplitStr(one.dob.contents[0])
        player['weight'] = getSplitStr(one.weight.contents[0])
        player['height'] = getSplitStr(one.height.contents[0])
        player['shirt_num'] = getSplitStr(one.shirt_num.contents[0])
        player['country'] = one.country.contents[1]
        player['age'] = getSplitStr(one.age.contents[0])
        players[player['id']] = player
        sql = "insert into tbPlayerInfo(iPlayerID, iTeamID, szFirstName, szLastName, szName, szTeamName, szPhotoUrl, szPosition, szBirthDay, iWeight, iHeight, iShirtNum, szCountry, iAge) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(player['id'].encode('utf-8'), player['team_id'].encode('utf-8'), player['first_name'].encode('utf-8'), player['last_name'].encode('utf-8'), player['name'].encode('utf-8'), player['team_name'].encode('utf-8'), player['photo'].encode('utf-8'), player['position'].encode('utf-8'), player['dob'].encode('utf-8'), player['weight'].encode('utf-8'), player['height'].encode('utf-8'), player['shirt_num'].encode('utf-8'), player['country'].encode('utf-8'), player['age'].encode('utf-8'))
        mydbpool.myInsert(sql)
    return players

#get split str
def getSplitStr(str):
    return str.split("\n")[1][4:]

def getScore(soup):
    temp = soup.squawka.data_panel.system.headline.contents[1].split(" ")
    iteams = soup.find_all('team')
    score = {}
    score['homeScore'] = temp[1]
    score['awayScore'] = temp[3]
    score['homeTeamID'] = iteams[0]['id']
    score['awayTeamID'] = iteams[1]['id']
    return score

def getKickOff(soup):
    return getSplitStr(soup.squawka.data_panel.game.kickoff.contents[0])

def creatMatchInfo(soup, matchID):
    score = getScore(soup)
    kickoff = getKickOff(soup)
    sql = "insert into tbMatchInfo(iMatchID, tStart, iHomeTeamID, iAwayTeamID, iHomeScore, iAwayScore) values('{}', '{}', '{}', '{}', '{}', '{}')".format(matchID, kickoff, score['homeTeamID'], score['awayTeamID'], score['homeScore'], score['awayScore'])
    mydbpool.myInsert(sql)

def getSwapPlayers(soup, matchID):
    swapPlayers = []
    swapEvents = soup.find_all('swap_players') 
    for oneSwap in swapEvents:
        swap = {}
        swap['mins'] = oneSwap['min']
        swap['minsec'] = oneSwap['minsec']
        swap['secs'] = 0
        try:
            if oneSwap['injurytime_play'] == None:
                swap['injurytime_play'] = 0
            else:
                swap['injurytime_play'] = oneSwap['injurytime_play']
        except:
            swap['injurytime_play'] = 0
        swap['sub_to_player'] = oneSwap.sub_to_player['player_id']
        swap['player_to_sub'] = oneSwap.player_to_sub['player_id']
        swap['type'] = 1
        swap['team_id'] = oneSwap['team_id']
        sql = "insert into tbMatchEvent(iMatchID, iMins, iMinsec, iSecs, iInjurytime_play, iPlayer1ID, iPlayer2ID, iType, iTeamID, szEventContent) values('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(matchID, swap['mins'], swap['minsec'], swap['secs'], swap['injurytime_play'], swap['sub_to_player'], swap['player_to_sub'], swap['type'], swap['team_id'], '')
        print sql
        mydbpool.myInsert(sql)
        swapPlayers.append(swap)
    return swapPlayers
    
def getCards(soup):
    cards = []
    cardsList = soup.find_all('card')
    for oneCard in cardsList:
        card = {}
        card['type'] = getSplitStr(oneCard.contents[0])
        card['player_id'] = oneCard.parent['player_id']
        card['mins'] = oneCard.parent['mins']
        cards.append(card)
    return cards

def getGoals(soup):
    goals = []
    goals_attempts = soup.squawka.data_panel.filters.goals_attempts
    goalEvents = goals_attempts.find_all('event')
    for oneEvent in goalEvents:
        goalEvent = {}
        if oneEvent['type'] == 'goal':
            goalEvent['team_id'] = oneEvent['team_id']
            goalEvent['player_id'] = oneEvent['player_id']
            goalEvent['mins'] = oneEvent['mins']
            if oneEvent.assist_1:
                goalEvent['assist'] = getSplitStr(oneEvent.assist_1.contents[0])
            goals.append(goalEvent)
    return goals

def getCorners(soup):
    corners = []
    cornerLists = soup.squawka.data_panel.filters.corners
    cornerEvents = cornerLists.find_all('event')
    for oneEvent in cornerEvents:
        cornerEvent = {}
        cornerEvent['team_id'] = oneEvent['team']
        cornerEvent['player_id'] = oneEvent['player_id']
        cornerEvent['mins'] = oneEvent['mins']
        cornerEvent['type'] = oneEvent['type']
        corners.append(cornerEvent)
    return corners

def getPenalties(soup):
    penalties = []
    return penalties 

#parse page
def parseXMl(soup, matchID):
    teams = creatTeams(soup)
    players = creatPlayers(soup)
    creatMatchInfo(soup, matchID)
    swapPlayers = getSwapPlayers(soup, matchID)
    cards = getCards(soup)
    #goals = getGoals(soup)
    #corners = getCorners(soup)
    #penalties = getPenalties(soup)
    #print corners


if __name__ == '__main__':
    mydbpool = myDbPool()
    mydbpool.mysqlInit()
    #for i in range(10300, 10333):
    #    finalUrl = getMatchUrl(url, i)
    #    print finalUrl
    #    onlyDownloadPage(finalUrl, i)
    #soup = downloadpage(url)
    soup = readDownloadPage()
    parseXMl(soup, 10332)
    #f = codecs.open('./squawka', 'w', 'utf-8')
    #f.write(temp);
    #f.close();

