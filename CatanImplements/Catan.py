#Settlers of Catan
#Gameplay class with pygame with AI players

from .board import *
from .gameView import *
from .player import *
import numpy as np
import matplotlib.pyplot as plt

from .Phase import *

#viewMode 画面の表示モード。消すと速くなる
#debugLog  Trueだと、合法手意外で少し速くなるはず。
class Catan():
    #Create new gameboard
    def __init__(self,viewMode,debugLog=False,fixed=True,stepReward=True):
        self.board = catanBoard(fixed) #fixed=Trueの場合、毎回同じ初期配置にする
        self.fixed = fixed
        self.turn = 0
        playerColors = ['black','orange1','darkslateblue', 'magenta4',]
        self.playerList = []
        for i in range(2):
            newPlayer = player("abcd"[i],playerColors[i],debugLog = debugLog)
            self.playerList.append(newPlayer)        
        self.phase = Phase.firstInitialSettlement
        self.hasRoled = False
        self.hasDevCardPlayed = False
        self.nowPlayer = self.playerList[0]
        self.anotherPlayer = self.playerList[1]
        #discardのために、一時的にphaseをもらっている状態
        self.tempAnotherPlayerPhase = False

        #Initialize boardview object
        if viewMode:
          self.viewMode = True
          self.boardView = catanGameView(self.board, self)
        else:
            self.viewMode = False

        self.debugLog = debugLog
        self.stepReward = stepReward
        self.playerChanged = False #このターンにプレイヤーチェンジ呼び出したか
        
        return None
    
    def reset(self):
        self.board = catanBoard(self.fixed)
        self.turn = 0
        playerColors = ['black','orange1','darkslateblue', 'magenta4',]
        self.playerList = []
        for i in range(2):
            newPlayer = player("abcd"[i],playerColors[i],debugLog = self.debugLog)
            self.playerList.append(newPlayer)        
        self.phase = Phase.firstInitialSettlement
        self.hasRoled = False
        self.hasDevCardPlayed = False
        self.nowPlayer = self.playerList[0]
        self.anotherPlayer = self.playerList[1]
        #discardのために、一時的にphaseをもらっている状態
        self.tempAnotherPlayerPhase = False
        

    #Function to roll dice 
    def getDiceNum(self):
        dice_1 = np.random.randint(1,7)
        dice_2 = np.random.randint(1,7)
        diceNum= dice_1 + dice_2
        if self.debugLog:
          print("Dice Roll = ", diceNum, "{", dice_1, dice_2, "}")
        return diceNum
    
    def playerChange(self):
        self.nowPlayer,self.anotherPlayer = self.anotherPlayer,self.nowPlayer
        self.playerChanged = True

    #Function to update resources for all players
    def update_playerResources(self, diceRoll):
        if diceRoll == 7:
            print("7のときは資源獲得関数呼び出さないでほしかった")
            exit()

        #First get the hex or hexes corresponding to diceRoll
        hexResourcesRolled = self.board.getHexResourceRolled(diceRoll)
        #print('Resources rolled this turn:', hexResourcesRolled)
        #Check for each player
        for player_i in self.playerList:
            #Check each settlement the player has
            for settlementCoord in player_i.buildGraph['SETTLEMENTS']:
                for adjacentHex in self.board.boardGraph[settlementCoord].adjacentHexList: #check each adjacent hex to a settlement
                    if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False): #This player gets a resource if hex is adjacent and no robber
                        resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                        player_i.resources[resourceGenerated] += 1
                        if self.debugLog:
                          print("{} collects 1 {} from Settlement".format(player_i.name, resourceGenerated))
            
            #Check each City the player has
            for cityCoord in player_i.buildGraph['CITIES']:
                for adjacentHex in self.board.boardGraph[cityCoord].adjacentHexList: #check each adjacent hex to a settlement
                    if(adjacentHex in hexResourcesRolled and self.board.hexTileDict[adjacentHex].robber == False): #This player gets a resource if hex is adjacent and no robber
                        resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                        player_i.resources[resourceGenerated] += 2
                        if self.debugLog:
                          print("{} collects 2 {} from City".format(player_i.name, resourceGenerated))
        

    #function to check if a player has the longest road - after building latest road
    def check_longest_road(self, player_i):
        if(player_i.maxRoadLength >= 5): #Only eligible if road length is at least 5
            longestRoad = True
            for p in self.playerList:
                if(p.maxRoadLength >= player_i.maxRoadLength and p != player_i): #Check if any other players have a longer road
                    longestRoad = False
            
            if(longestRoad and player_i.longestRoadFlag == False): #if player_i takes longest road and didn't already have longest road
                #Set previous players flag to false and give player_i the longest road points
                prevPlayer = ''
                for p in self.playerList:
                    if(p.longestRoadFlag):
                        p.longestRoadFlag = False
                        p.victoryPoints -= 2
                        prevPlayer = 'from Player ' + p.name
    
                player_i.longestRoadFlag = True
                player_i.victoryPoints += 2
                if self.debugLog:
                  print("Player {} takes Longest Road {}".format(player_i.name, prevPlayer))

    #function to check if a player has the largest army - after playing latest knight
    def check_largest_army(self, player_i):
        if(player_i.knightsPlayed >= 3): #Only eligible if at least 3 knights are player
            largestArmy = True
            for p in self.playerList:
                if(p.knightsPlayed >= player_i.knightsPlayed and p != player_i): #Check if any other players have more knights played
                    largestArmy = False
            
            if(largestArmy and player_i.largestArmyFlag == False): #if player_i takes largest army and didn't already have it
                #Set previous players flag to false and give player_i the largest points
                prevPlayer = ''
                for p in self.playerList:
                    if(p.largestArmyFlag):
                        p.largestArmyFlag = False
                        p.victoryPoints -= 2
                        prevPlayer = 'from Player ' + p.name
    
                player_i.largestArmyFlag = True
                player_i.victoryPoints += 2
                if self.debugLog:
                  print("Player {} takes Largest Army {}".format(player_i.name, prevPlayer))

   
    
    def step_moveThief(self,actionInfo):
        if self.phase != Phase.moveThief:
            print("盗賊動かしフェイズ以外で、盗賊動かそうとしてるエラー")
            print(self.phase,actionInfo)
            exit()
        if self.debugLog:
          print(f"{self.nowPlayer.name}が盗賊を動かします")
        hexIndex = actionInfo["hexIndex"]
        self.nowPlayer.moveRobber(hexIndex,self.board,self.anotherPlayer)
        self.phase = Phase.normal

    def step_buildSettlement(self,actionInfo):
        v = actionInfo["v"]    

        if self.phase == Phase.firstInitialSettlement:
            self.nowPlayer.buildFreeSettlement(v, self.board, self.phase.name)
            self.phase = Phase.firstInitialRoad

        elif self.phase == Phase.secondInitialSettlement:
            self.nowPlayer.buildFreeSettlement(v, self.board, self.phase.name)
            self.phase = Phase.secondInitialRoad

            #初期手札の処理はここでやる
            for adjacentHex in self.board.boardGraph[self.nowPlayer.buildGraph['SETTLEMENTS'][-1]].adjacentHexList:
                resourceGenerated = self.board.hexTileDict[adjacentHex].resource.type
                if(resourceGenerated != 'DESERT'):
                    self.nowPlayer.resources[resourceGenerated] += 1
                    if self.debugLog:
                      print("{} collects 1 {} from Settlement".format(self.nowPlayer.name, resourceGenerated))

        elif self.phase == Phase.normal:
            if not self.hasRoled:
                print("サイコロ前に開拓地建設エラー",self.phase)
                exit()
            self.nowPlayer.buildSettlement(v, self.board, self.phase.name)
        else:
            print("変なフェーズで開拓地建設エラー")
            print(self,actionInfo,"phaseは",self.phase)
            exit()

    #初期道、通常購入、ビルダー使用時　全部これでいける
    def step_buildRoad(self,actionInfo):
        v1,v2 = actionInfo["v1"],actionInfo["v2"]

        #最初に建てる道
        if self.phase == Phase.firstInitialRoad:
            self.nowPlayer.buildFreeRoad(v1,v2,self.board,self.phase.name)
            if self.nowPlayer == self.playerList[0]:
                self.phase = Phase.firstInitialSettlement
                self.playerChange() #1221の12の部分
            else:
                self.phase = Phase.secondInitialSettlement
                #1221の22の部分
        #２個目に建てる道
        elif self.phase == Phase.secondInitialRoad:
            self.nowPlayer.buildFreeRoad(v1,v2,self.board,self.phase.name)
            if self.nowPlayer == self.playerList[1]:
                self.phase = Phase.secondInitialSettlement
                self.playerChange() #1221の21の部分
            else:
                self.phase = Phase.normal #1221のラストの１の部分

        #街道ビルダーで作る一つ目の道
        elif self.phase == Phase.roadBuilderFirst:
            self.nowPlayer.buildFreeRoad(v1,v2,self.board,self.phase.name)
            #次に建てられる道がないなら、通常フェーズに戻る
            
            if len(self.board.get_potential_roads(self.nowPlayer)) == 0:
                self.phase = Phase.normal
            else:
                self.phase = Phase.roadBuilderSecond
        

        #街道ビルダーの二つ目の道
        elif self.phase == Phase.roadBuilderSecond:
            self.nowPlayer.buildFreeRoad(v1,v2,self.board,self.phase.name)
            self.phase = Phase.normal

        #通常時。購入して道を作る
        elif self.phase == Phase.normal:
            if not self.hasRoled:
                print("サイコロ前に道建設エラー",self.phase)
                exit()
            self.nowPlayer.buildRoad(v1,v2,self.board, self.phase.name)
        else:
            print("変なフェーズで道建設エラー")
            print(self,actionInfo,"phaseは",self.phase)
            exit()

        self.check_longest_road(self.nowPlayer)

    def step_buildCity(self,actionInfo):
        if self.phase != Phase.normal:
            print("変なフェーズで都市建設エラー",self.phase)
            exit()
        if not self.hasRoled:
            print("サイコロ前に都市建設エラー",self.phase)
            exit()
        
        v = actionInfo["v"]
        #購入、ポイントプラス、、ビルドグラフの更新までこれで終わる
        self.nowPlayer.buildCity(v, self.board)

    #ズルしてサイコロの目を指定。デバッグよう
    def step_cheatRollDice(self,diceNum):
        if self.phase != Phase.normal:
            print("変なフェーズでサイコロ振ってるエラー",self.phase)
            exit()
        if self.hasRoled:
            print("2回もふれません")
            exit()
        if diceNum == 7:
            #自分がクラッシュ→破棄フェイズへ
            #その後、破棄フェイズからもう一つの破棄や盗賊フェイズに移動
            if sum(self.nowPlayer.resources.values())>7:
                if self.debugLog:
                  print("手番プレイヤーの破棄フェイズに移ります")
                self.phase = Phase.discard
            #相手のみクラッシュ→一時的に相手のターンにして破棄フェイズへ
            elif sum(self.anotherPlayer.resources.values())>7:
                self.phase = Phase.discard
                if self.debugLog:
                  print("非手番プレイヤーの破棄フェイズに移ります")
                self.tempAnotherPlayerPhase = True
                self.playerChange()
            #誰もクラッシュしない→すぐに盗賊フェイズに移動
            else:
                self.phase = Phase.moveThief
                if self.debugLog:
                  print("盗賊の移動フェイズに移ります")
        else:
            self.update_playerResources(diceNum)
        self.hasRoled = True
        return False,0

    def step_rollDice(self):
        if self.phase != Phase.normal:
            print("変なフェーズでサイコロ振ってるエラー",self.phase)
            exit()
        if self.hasRoled:
            print("2回サイコロふれませんエラー")
            exit()
        diceNum = self.getDiceNum()
        if diceNum == 7:
            #自分がクラッシュ→破棄フェイズへ
            #その後、破棄フェイズからもう一つの破棄や盗賊フェイズに移動
            if sum(self.nowPlayer.resources.values())>7:
                if self.debugLog:
                  print("手番プレイヤーの破棄フェイズに移ります")
                self.phase = Phase.discard
            #相手のみクラッシュ→一時的に相手のターンにして破棄フェイズへ
            elif sum(self.anotherPlayer.resources.values())>7:
                self.phase = Phase.discard
                if self.debugLog:
                  print("非手番プレイヤーの破棄フェイズに移ります")
                self.tempAnotherPlayerPhase = True
                self.playerChange()
            #誰もクラッシュしない→すぐに盗賊フェイズに移動
            else:
                self.phase = Phase.moveThief
                if self.debugLog:
                  print("盗賊の移動フェイズに移ります")
        else:
            self.update_playerResources(diceNum)
        self.hasRoled = True

    def step_discard(self,actionInfo):
        if self.phase != Phase.discard:
            print("変なフェーズで破棄しようとしてます",self.phase)
            exit()
        saveResources = actionInfo["saveResources"]
        self.nowPlayer.discard(saveResources)

        #破棄のため一時的に主プレイヤーを渡していた
        #プレイヤーを本来の人に戻し、盗賊移動フェイズへ
        if self.tempAnotherPlayerPhase:
            self.tempAnotherPlayerPhase = False
            self.playerChange()
            self.phase = Phase.moveThief

        #主プレイヤーの破棄をしたが、相手の破棄も必要
        #相手に一時的にプレイヤー権を渡す
        elif sum(self.anotherPlayer.resources.values())>7:
            if self.debugLog:
              print("非手番プレイヤーの破棄フェイズに移ります")
            self.phase = Phase.discard
            self.tempAnotherPlayerPhase = True
            self.playerChange()

        #主プレイヤーのみの破棄を終了
        else:
            self.phase = Phase.moveThief

    def step_endTurn(self):
        if not self.hasRoled:
            print("さいころ降らずにターン終われません")
            exit()
        if self.phase != Phase.normal:
            print("変なフェーズでターン終了宣言してる",self.phase)
            exit()
        #プレイヤーをチェンジし、ターンはじめの処理
        self.playerChange()
        if self.debugLog:
          print(f"{self.nowPlayer.name}のターンです")
        self.nowPlayer.updateDevCards()
        self.hasDevCardPlayed = False
        self.hasRoled = False
        self.turn += 1

    def step_bankTrade(self,actionInfo):
        if self.phase != Phase.normal:
            print("変なフェーズで銀行取引を呼び出してるよ",self.phase)
            exit()
        if not self.hasRoled:
            print("サイコロ降る前に銀行取引してるエラー",actionInfo)
            exit()
        buyResource,sellResource = actionInfo["buyResource"],actionInfo["sellResource"]
        self.nowPlayer.bankTrade(sellResource, buyResource)
        
    def step_buyDevCard(self):
        if self.phase != Phase.normal:
            print("変なフェーズで発展購入を呼び出してるよ",self.phase)
            exit()
        if not self.hasRoled:
            print("サイコロ振る前に発展購入呼び出してるよ",self.phase)
            exit()
        self.nowPlayer.buyDevCard(self.board)

    def step_useKnight(self):
        if self.phase != Phase.normal:
            print("変なフェイズで騎士使用の宣言エラー",self.phase)
            exit()
        if self.hasDevCardPlayed:
            print("発展カード2回目エラー",self.phase)
            exit()
        self.hasDevCardPlayed = True
        self.nowPlayer.useKnight()
        self.check_largest_army(self.nowPlayer)
        self.phase = Phase.moveThief

    def step_useRoadBuilder(self):
        if self.phase != Phase.normal:
            print("変なフェイズでビルダー使用宣言エラー",self.phase)
            exit()
        if self.hasDevCardPlayed:
            print("発展カード2回目エラー",self.phase)
            exit()
        self.hasDevCardPlayed = True
        self.nowPlayer.useRoadBuilder()
        self.phase = Phase.roadBuilderFirst

    def step_useYear(self,actionInfo):
        if self.phase != Phase.normal:
            print("変なフェイズで収穫宣言エラー",self.phase)
            exit()
        if self.hasDevCardPlayed:
            print("発展カード2回目エラー",self.phase)
            exit()
        getResources = actionInfo["getResources"]
        self.nowPlayer.useYear(getResources)
        self.hasDevCardPlayed = True

    def step_useMonopoly(self,actionInfo):
        resource = actionInfo["resource"]
        if self.phase != Phase.normal:
            print("変なフェーズで独占使用エラー",self.phase)
            exit()
        if self.hasDevCardPlayed:
            print("発展カード2回目エラー",self.phase)
            exit()
        self.hasDevCardPlayed = True
        self.nowPlayer.useMonopoly(resource,self.anotherPlayer)
        


        






    #actioninfoは辞書
    #合法手のみを想定
    def step(self,actionInfo):
        done,reward = False,0
        name = actionInfo["name"]
        beforePoints = self.nowPlayer.victoryPoints
        self.playerChanged = False

        if name == "moveThief":
            self.step_moveThief(actionInfo)

        elif name == "buildSettlement":
            self.step_buildSettlement(actionInfo)

        elif name == "buildRoad":
            self.step_buildRoad(actionInfo)

        elif name == "buildCity":
            self.step_buildCity(actionInfo)

        elif name == "discard":
            self.step_discard(actionInfo)

        elif name == "rollDice":
            self.step_rollDice()

        elif name == "endTurn":
            self.step_endTurn()

        elif name == "bankTrade":
            self.step_bankTrade(actionInfo)

        elif name == "buyDevCard":
            self.step_buyDevCard()

        elif name == "useKnight":
            self.step_useKnight()

        elif name == "useRoadBuilder":
            self.step_useRoadBuilder()

        elif name == "useYear":
            self.step_useYear(actionInfo)

        elif name == "useMonopoly":
            self.step_useMonopoly(actionInfo)

        else:
            print("知らないアクションエラー")
            print(actionInfo)
            exit()

        if self.viewMode:
          self.boardView.displayGameScreen()

        if self.nowPlayer.victoryPoints >= 10:
            if self.debugLog:
              print(f"{self.nowPlayer.name} WIN!")
            reward = 0.75 + 0.02*(self.nowPlayer.victoryPoints - self.anotherPlayer.victoryPoints)
            done = True
        if self.anotherPlayer.victoryPoints >= 10:
            print("ここ呼ばれるのおかしいかも")
            if self.debugLog:
              print(f"{self.anotherPlayer.name} WIN!")
            reward = -0.75 - 0.02*(self.anotherPlayer.victoryPoints - self.nowPlayer.victoryPoints)
            done = True
            exit()

        afterPoints = self.nowPlayer.victoryPoints


        #今回の行動で得られた勝利点で報酬に色をつける
        #プレイヤーチェンジするような行動ではstep報酬はつかないの
        if not done and not self.playerChanged:
            if self.phase not in [Phase.firstInitialRoad,Phase.secondInitialRoad,Phase.firstInitialSettlement,Phase.secondInitialSettlement]:
              reward = (afterPoints - beforePoints)*0.1

        return done,reward

