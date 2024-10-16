#Settlers of Catan
#Player class implementation

from .board import *
import numpy as np
import random


#Class definition for a player
class player():
    'Class Definition for Game Player'

    #Initialize a game player, we use A, B and C to identify
    def __init__(self, playerName, playerColor, debugLog):
        self.name = playerName
        self.color = playerColor
        self.victoryPoints = 0
        self.backDevCards = 0 #裏向きで伏せられている発展カードの数

        self.settlementsLeft = 5
        self.roadsLeft = 15
        self.citiesLeft = 4
        self.resources = {'ORE':0, 'BRICK':0, 'WHEAT':0, 'WOOD':0, 'SHEEP':0}

        self.knightsPlayed = 0
        self.largestArmyFlag = False
        
        self.maxRoadLength = 0
        self.longestRoadFlag = False

        #Undirected Graph to keep track of which vertices and edges player has colonised
        #Every time a player's build graph is updated the gameBoardGraph must also be updated

        #Each of the 3 lists store vertex information - Roads are stores with tuples of vertex pairs
        self.buildGraph = {'ROADS':[], 'SETTLEMENTS':[], 'CITIES':[]}
        self.portList = [] #List of ports acquired

        #Dev cards in possession
        self.newDevCards = [] #List to keep the new dev cards draw - update the main list every turn
        self.devCards = {'KNIGHT':0, 'VP':0, 'MONOPOLY':0, 'ROADBUILDER':0, 'YEAROFPLENTY':0} 
        #self.devCardPlayedThisTurn = False gameの方で管理することにした

        self.visibleVictoryPoints = self.victoryPoints - self.devCards['VP']
        self.setupResources = [] #楽なinitialセットアップのやつ以外でつかわん

        if debugLog:
            self.debugLog = True
        else:
            self.debugLog = False

    def __str__(self):
        ret = f"{self.name}"
        ret += f"資源:{self.resources}\n"
        #ret += f"建築一覧:{self.buildGraph}\n"
        ret += f"longest:{self.longestRoadFlag}　　　largest:{self.largestArmyFlag}\n"
        ret += f"PORT一覧:{self.portList}\n"
        ret += f"発展一覧:{self.devCards}\n"
        ret += f"vp:{self.victoryPoints}"
        return ret
    

    #Function to update dev card stack with dev cards drawn from prior turn
    def updateDevCards(self):
        for newCard in self.newDevCards:
            self.devCards[newCard] += 1

        #Reset the new card list to blank
        self.newDevCards = []
    

    #無料版の道建設(ゲーム開始時と街道建設カード)
    def buildFreeRoad(self,v1,v2,board,phaseName):
        self.resources["BRICK"] += 1
        self.resources["WOOD"] += 1
        self.buildRoad(v1,v2,board,phaseName)

    #v1,v2はindexで受け取ることにしたので、ここでピクセルに変更が必要
    def buildRoad(self, v1, v2, board,phaseName):
        v1Coord = board.vertex_index_to_pixel_dict[v1]
        v2Coord = board.vertex_index_to_pixel_dict[v2]

        #初期建設の場合の、合法道チェック
        if phaseName == "firstInitialRoad" or phaseName == "secondInitialRoad":
            if (v1Coord,v2Coord) not in board.get_setup_roads(self) and (v2Coord,v1Coord) not in board.get_setup_roads(self):
                print("合法じゃない道の指定してるよ",v1,v2,phaseName)
                exit()
        #通常or街道ビルダーでの合法道チェック    
        else:
            if (v1Coord,v2Coord) not in board.get_potential_roads(self) and (v2Coord,v1Coord) not in board.get_potential_roads(self):
                print("合法じゃない道の指定してるよ",v1,v2,phaseName)
                exit()
        if(self.resources['BRICK'] <= 0 or self.resources['WOOD'] <= 0): 
            print("資源不足エラー",self.resources)
            exit()
        if self.roadsLeft <=0:
            print("道残数不足エラー",self.roadsLeft)
            exit()

        self.buildGraph['ROADS'].append((v1Coord,v2Coord))
        self.roadsLeft -= 1

        self.resources['BRICK'] -= 1
        self.resources['WOOD'] -= 1
        board.updateBoardGraph_road(v1Coord, v2Coord, self) #update the overall boardGraph

        #Calculate current max road length and update
        self.maxRoadLength = self.get_road_length(board)

        if self.debugLog:
          print(f'{self.name} Built a Road at {v1},{v2}. MaxRoadLength: {self.maxRoadLength}')


    #無料版。初期建設で使う
    def buildFreeSettlement(self,v,board,phaseName):
        self.resources["BRICK"] += 1
        self.resources["WOOD"] += 1
        self.resources["SHEEP"] += 1
        self.resources["WHEAT"] += 1
        self.buildSettlement(v,board,phaseName)

    #function to build a settlement on vertex with coordinates vCoord
    def buildSettlement(self, v, board, phaseName):
        vCoord = board.vertex_index_to_pixel_dict[v]

        #初期建設の場合の、合法開拓地チェック
        if phaseName == "firstInitialSettlement" or phaseName == "secondInitialSettlement":
            if vCoord not in board.get_setup_settlements(self):
                print("合法じゃない開拓地の指定してるよ",v,phaseName)
                exit()
        #通常での合法開拓地チェック    
        else:
            if vCoord not in board.get_potential_settlements(self):
                print("合法じゃない開拓地の指定してるよ",v,phaseName)
                exit()
        if(self.resources['BRICK'] <= 0 or self.resources['WOOD'] <= 0 or self.resources['SHEEP'] <= 0 or self.resources['WHEAT'] <= 0):
            print("開拓地のための資源足りません",self.resources)
            exit()
        if(self.settlementsLeft <= 0): #Check if player has settlements left
            print("開拓地の残数がたりません",self.settlementsLeft)
            exit()

        self.buildGraph['SETTLEMENTS'].append(vCoord)
        self.settlementsLeft -= 1

        #Update player resources
        self.resources['BRICK'] -= 1
        self.resources['WOOD'] -= 1
        self.resources['SHEEP'] -= 1
        self.resources['WHEAT'] -= 1
        
        self.victoryPoints += 1
        board.updateBoardGraph_settlement(vCoord, self) #update the overall boardGraph

        if self.debugLog:
          print(f'{self.name} Built a Settlement at {v}')
        
            #Add port to players port list if it is a new port
        if((board.boardGraph[vCoord].port != False) and (board.boardGraph[vCoord].port not in self.portList)):
            self.portList.append(board.boardGraph[vCoord].port)
            if self.debugLog:
              print("{} now has {} Port access".format(self.name, board.boardGraph[vCoord].port))


    #function to build a city on vertex v
    def buildCity(self, v, board):
        vCoord = board.vertex_index_to_pixel_dict[v]

        if not board.boardGraph[vCoord].state["Settlement"]:
            print("そこに開拓地はない",v)
            exit()
        if board.boardGraph[vCoord].state["Player"] != self:
            print("お前の開拓地じゃないだろ！",v)
            exit()
        if(self.resources['WHEAT'] < 2 or self.resources['ORE'] < 3):
            print("Insufficient Resources to Build City. Build Cost: 3 ORE, 2 WHEAT")
            exit()
        if(self.citiesLeft <= 0):
            print("都市不足")
            exit()

        'Upgrade existing settlement to city in buildGraph'
        #Check if player has resources available
            
        self.buildGraph['CITIES'].append(vCoord)
        self.settlementsLeft += 1 #Increase number of settlements and decrease number of cities
        self.citiesLeft -=1

        #Update player resources
        self.resources['ORE'] -= 3
        self.resources['WHEAT'] -= 2
        self.victoryPoints += 1

        board.updateBoardGraph_city(vCoord, self) #update the overall boardGraph
        if self.debugLog:
          print('{} Built a City'.format(self.name))

        


    
    #function to move robber to a specific hex and steal from a player
    def moveRobber(self, hexIndex, board, anotherPlayer):
        'Update boardGraph with Robber and steal resource'

        if board.hexTileDict[hexIndex].robber:
            print("そこもう盗賊おるよ","おこうとした場所",hexIndex)
            exit()

        if anotherPlayer in board.get_players_to_rob(hexIndex):
            if sum(anotherPlayer.resources.values()) > 0:
                if self.debugLog:
                  print("盗みます")
                self.steal_resource(anotherPlayer)
            else:
                if self.debugLog:
                  print("相手の資源が0なので盗めませんでした")
        else:
            if self.debugLog:
              print("盗む人はいません")

        board.updateBoardGraph_robber(hexIndex)
        return


    #Function to steal a random resource from player_2
    def steal_resource(self, player_2):        
        #Get all resources player 2 has in a list and use random list index to steal
        p2_resources = []
        for resourceName, resourceAmount in player_2.resources.items():
            p2_resources += [resourceName]*resourceAmount

        resourceStolen = random.choice(p2_resources)
        
        #Update resources of both players
        player_2.resources[resourceStolen] -= 1
        self.resources[resourceStolen] += 1
        if self.debugLog:
          print("Stole 1 {} from Player {}".format(resourceStolen, player_2.name))

        return

        
    #Function to calculate road length for longest road calculation
    #Use both player buildgraph and board graph to compute recursively
    def get_road_length(self, board):
        roadLengths = [] #List to store road lengths from each starting edge
        for road in self.buildGraph['ROADS']: #check for every starting edge
            self.road_i_lengths = [] #List to keep track of all lengths of roads resulting from this root road
            roadCount = 0
            roadArr = []
            vertexList = []
            #print("Start road:", road)
            self.check_path_length(road, roadArr, roadCount, vertexList, board.boardGraph)

            road_inverted = (road[1], road[0])
            roadCount = 0
            roadArr = []
            vertexList = []
            self.check_path_length(road_inverted, roadArr, roadCount, vertexList, board.boardGraph)
                
            roadLengths.append(max(self.road_i_lengths)) #Update roadLength with max starting from this road
            #print(self.road_i_lengths)

        #print("Road Lengths:", roadLengths, max(roadLengths))
        return max(roadLengths)

    #Function to check the path length from a current edge to all possible other vertices not yet visited by t
    def check_path_length(self, edge, edgeList, roadLength, vertexList, boardGraph):
        #Append current edge to list and increment road count
        edgeList.append(edge) #Append the road
        roadLength += 1
        vertexList.append(edge[0]) #Append the first vertex
        
        #Get new neighboring forward edges from this edge - not visited by the search yet
        road_neighbors_list = self.get_neighboring_roads(edge, boardGraph, edgeList, vertexList)
        
        #print(neighboringRoads)
        #if no neighboring roads exist append the roadLength upto this edge
        if(road_neighbors_list == []):
            #print("No new neighbors found")
            self.road_i_lengths.append(roadLength)
            return

        else:
            #check paths from left and right neighbors separately
            for neighbor_road in road_neighbors_list:
                #print("checking neighboring edge:", neighbor_road)
                self.check_path_length(neighbor_road, edgeList, roadLength, vertexList, boardGraph)



    #Helper function to get neighboring edges from this road that haven't already been explored
    #We want forward neighbors only
    def get_neighboring_roads(self, road_i, boardGraph, visitedRoads, visitedVertices):
        #print("Getting neighboring roads for current road:", road_i)
        newNeighbors = []
        #Use v1 and v2 to get the vertices to expand from
        v1 = road_i[0]
        v2 = road_i[1] 
        for edge in self.buildGraph['ROADS']:
            if(edge[1] in visitedVertices):
                edge = (edge[1], edge[0]) #flip the edge if the orientation is reversed

            if(edge not in visitedRoads): #If it is a new distinct edge
                if(boardGraph[v2].state['Player'] in [self, None]):#Add condition for vertex to be not colonised by anyone else
                    if(edge[0] == v2 and edge[0] not in visitedVertices):  #If v2 has neighbors, defined starting or finishing at v2
                        #print("Appending NEW neighbor:", edge)
                        newNeighbors.append(edge)

                    if(edge[0] == v1 and edge[0] not in visitedVertices):
                        newNeighbors.append(edge)

                    if(edge[1] == v2 and edge[1] not in visitedVertices): #If v1 has neighbors, defined starting or finishing at v2
                        newNeighbors.append((edge[1], edge[0]))

                    if(edge[1] == v1 and edge[1] not in visitedVertices):
                        newNeighbors.append((edge[1], edge[0]))

        return newNeighbors


    #Function to basic trade 4:1 with bank, or use ports to trade
    def bankTrade(self, r1, r2):
        '''Function to implement trading with bank
        r1: resource player wants to trade away
        r2: resource player wants to receive
        Automatically give player the best available trade ratio
        '''
        if r1==r2:
            print("同じ資源での交換はできませんエラー",r1)
            exit()
        #Get r1 port string
        r1_port = "2:1 " + r1
        if(r1_port in self.portList and self.resources[r1] >= 2): #Can use 2:1 port with r1
            self.resources[r1] -= 2
            self.resources[r2] += 1
            if self.debugLog:
              print("Traded 2 {} for 1 {} using {} Port".format(r1, r2, r1))
            return

        #Check for 3:1 Port
        elif('3:1 PORT' in self.portList and self.resources[r1] >= 3):
            self.resources[r1] -= 3
            self.resources[r2] += 1
            if self.debugLog:
              print("Traded 3 {} for 1 {} using 3:1 Port".format(r1, r2))
            return

        #Check 4:1 port
        elif(self.resources[r1] >= 4):
            self.resources[r1] -= 4
            self.resources[r2] += 1
            if self.debugLog:
              print("Traded 4 {} for 1 {}".format(r1, r2))
            return
        
        else:
            if self.debugLog:
                print("Insufficient resource {} to trade with Bank".format(r1))
                print(f"売{r1},買{r2}")
                print(f"PORT状況:{self.portList}")
                exit()
            return


    
    #4つ指定したリソース以外は、ランダムに捨ててしまう
    def discard(self,saveResources):
        totalResource =  sum(self.resources.values())
        if totalResource<=7:
            print("バーストしてないのに捨てようとしてますエラー",self.resources)
            exit()
        if sum(saveResources.values())!=4:
            print("saveしようとしている資源が4つじゃありません")
            print(saveResources)
            exit()

        if self.debugLog:
            print(f"Player{self.name}の破棄スタート")
            print("元",self.resources)

        #破棄すべき手札の数（きりあげでわる２）Player
        numCardsToDiscard  = totalResource//2
        
        #捨てちゃってもよいもの
        #strを捨ててもよい数分だけリストに詰めてく
        canDiscardResources = []
        for k,v in self.resources.items():
            #持ってる数-saveしたい数
            if v-saveResources[k]<0:
                print("保持したい資源が足りないエラー")
                print("持",self.resources)
                print("保持希望",saveResources)
                exit()
            for _ in range(v - saveResources[k]):
                canDiscardResources.append(k)
        #破棄する手札をランダムに決定
        discardResources = random.sample(canDiscardResources,numCardsToDiscard)

        for resource in discardResources:
            self.resources[resource] -= 1
            if self.debugLog:
                if self.resources[resource]<0:
                    print("捨てすぎエラーだよ")
                    print("捨てようとしたもの→",discardResources)
                    exit()
        if self.debugLog:
          print("後",self.resources)



    #function to draw a Development Card
    def buyDevCard(self, board):
        'Draw a random dev card from stack and update self.devcards'
        if(self.resources['WHEAT'] == 0 or self.resources['ORE'] == 0 or self.resources['SHEEP'] ==0): #Check if player has resources available
            print("発展カード購入に必要な資源が足りませんエラー")
            print("今のリソース",self.resources)
            exit()

        #Get alldev cards available
        devCardsToDraw = []
        for cardName, cardAmount in board.devCardStack.items():
            devCardsToDraw += [cardName]*cardAmount

        #IF there are no devCards left
        if(devCardsToDraw == []):
            print("発展カードもうないよエラー")
            exit()
            
        cardDrawn = random.choice(devCardsToDraw)

        #Update player resources
        self.resources['ORE'] -= 1
        self.resources['WHEAT'] -= 1
        self.resources['SHEEP'] -= 1
        self.backDevCards += 1

        #If card is a victory point apply immediately, else add to new card list
        if(cardDrawn == 'VP'):
            self.victoryPoints += 1
            board.devCardStack[cardDrawn] -= 1
            self.devCards[cardDrawn] += 1
            self.visibleVictoryPoints = self.victoryPoints - self.devCards['VP']
        
        else:#Update player dev card and the stack
            self.newDevCards.append(cardDrawn)
            board.devCardStack[cardDrawn] -= 1
   
        if self.debugLog:
          print("{} drew a {} from Development Card Stack".format(self.name, cardDrawn))


    def useKnight(self):
        if self.devCards["KNIGHT"]==0:
            print("騎士カード不足エラー")
            exit()
        self.devCards["KNIGHT"] -= 1
        self.knightsPlayed += 1
        self.backDevCards -= 1

    def useRoadBuilder(self):
        if self.devCards["ROADBUILDER"]==0:
            print("街道ビルダーカード不足エラー")
            exit()
        self.devCards["ROADBUILDER"] -= 1
        self.backDevCards -= 1

    def useYear(self,getResources):
        if self.devCards["YEAROFPLENTY"]==0:
            print("収穫カード不足エラー")
            exit()
        for k,v in getResources.items():
            self.resources[k] += v
            if self.debugLog:
              if v>0:
                  print(f"収穫により、{k}を{v}個獲得しました。")
        self.devCards["YEAROFPLENTY"] -= 1
        self.backDevCards -= 1



    def useMonopoly(self,resource,anotherPlayer):
        if self.devCards["MONOPOLY"] == 0:
            print("独占カード不足エラー")
            exit()
        self.devCards["MONOPOLY"] -= 1
        self.backDevCards -= 1

        numResource = anotherPlayer.resources[resource]
        self.resources[resource] += numResource
        anotherPlayer.resources[resource] = 0
        if self.debugLog:
          print(f"{self.name}は{anotherPlayer.name}から{numResource}個の{resource}を奪いました")