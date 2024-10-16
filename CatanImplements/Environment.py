from .Catan import *
from .Controller import *
import random
from .Bots import *

import gymnasium as gym
from gymnasium import spaces
import numpy as np


#vectorの特徴→51
#boardの特徴→ 19*11*21 


        
class EnvironmentWithCNNFeature(gym.Env):
    def __init__(self,opponetAgent,debugLog=False,fixed=True,hande=0):
        super().__init__()

        # Observation space definition
        self.observation_space = spaces.Dict({
            "matrix": spaces.Box(low=0, high=1, shape=(24, 11, 21), dtype=np.float32), 
            "vector": spaces.Box(low=0, high=1, shape=(53,), dtype=np.float32)    
        })

        self.action_space = spaces.Discrete(1039) 

        self.opponentAgent = opponetAgent
        self.hande = hande
        self.catan = Catan(viewMode=False,debugLog=debugLog,fixed=fixed)
        #trueなら自分が先手、falseならopponetAgentが先手
        self.firstMove = random.choice([True,False])
        if self.firstMove:
            self.catan.playerList[0].name = "A2C"
            self.catan.playerList[1].name = "bot"
            self.catan.playerList[0].victoryPoints = self.hande
        else:
            self.catan.playerList[0].name = "bot"
            self.catan.playerList[1].name = "A2C"
            self.catan.playerList[1].victoryPoints = self.hande
        return
    
    #今が学習したいエージェントのturnならTrue
    #opponetAgentのturnならFalse
    def isMainAgentTurn(self):
        catan = self.catan
        #mainが先手
        if self.firstMove:
            if catan.nowPlayer == catan.playerList[0]:
                return True
            else:
                return False
        #mainが後手
        else:
            if catan.nowPlayer == catan.playerList[0]:
                return False
            else:
                return True

    def reset(self,seed=0):
        catan = self.catan
        #catanの状況をリセット
        catan.reset()
        #今後必要になればopponetAgentに関しても何かしらの処理
        self.firstMove = random.choice([True,False])
        if self.firstMove:
            self.catan.playerList[0].name = "A2C"
            self.catan.playerList[1].name = "bot"
            self.catan.playerList[0].victoryPoints = self.hande
        else:
            self.catan.playerList[0].name = "bot"
            self.catan.playerList[1].name = "A2C"
            self.catan.playerList[1].victoryPoints = self.hande

        #mainの手番になるまで進める
        while(not self.isMainAgentTurn()):
            #ゲームを渡して、行動を選択させる
            action = self.opponentAgent.choiceAction(catan)
            actionInfo = actionController(action)
            _,_ = catan.step(actionInfo)

        vector_obs = getVectorFeature(catan)
        cnn_obs = getBoardCNNFeature(catan)
        obs = {"matrix":cnn_obs,"vector":vector_obs}

        #次の状況での合法手も一緒に返す
        return obs,{}
    
    def step(self,action):
        catan = self.catan
        actionInfo = actionController(action)
        done,self_reward = self.catan.step(actionInfo)

        #自分の行動でゲーム終了
        if done:
            vector_obs = getVectorFeature(catan)
            cnn_obs = getBoardCNNFeature(catan)
            obs = {"matrix":cnn_obs,"vector":vector_obs}
            return obs,self_reward,done,False,{"is_success":True}
        
        #もう一度自分のターンがくるまで、相手エージェントに行動させる
        while(not self.isMainAgentTurn()):
            opponentAction = self.opponentAgent.choiceAction(catan)
            opponentActionInfo = actionController(opponentAction)
            done,op_reward = catan.step(opponentActionInfo)
            #相手の行動でゲーム終了
            if done:
                vector_obs = getVectorFeature(catan)
                cnn_obs = getBoardCNNFeature(catan)
                obs = {"matrix":cnn_obs,"vector":vector_obs}
                #敵ターンで終了　＝　負けてるのでマイナス報酬
                return obs,-op_reward+self_reward,done,False,{"is_success":False}
            
        vector_obs = getVectorFeature(catan)
        cnn_obs = getBoardCNNFeature(catan)
        obs = {"matrix":cnn_obs,"vector":vector_obs}
        return obs,self_reward,False,False,{}

    def action_masks(self):
        return getLegalMask(self.catan)
    


class EnvironmentWithGraphFeature(gym.Env):
    def __init__(self,opponetAgent,debugLog=False,fixed=True,hande=0):
        super().__init__()

        # Observation space definition
        self.observation_space = spaces.Dict({
            "hex": spaces.Box(low=0, high=1, shape=(19,6), dtype=np.float32),  
            "vertex": spaces.Box(low=0, high=1, shape=(54, 15), dtype=np.float32),  
            "road": spaces.Box(low=0, high=1, shape=(72, 2), dtype=np.float32),  
            "vector": spaces.Box(low=0, high=1, shape=(53,), dtype=np.float32)    
        })

        self.action_space = spaces.Discrete(314) 

        self.opponentAgent = opponetAgent
        self.hande = hande
        self.catan = Catan(viewMode=False,debugLog=debugLog,fixed=fixed)
        #trueなら自分が先手、falseならopponetAgentが先手
        self.firstMove = random.choice([True,False])
        if self.firstMove:
            self.catan.playerList[0].name = "A2C"
            self.catan.playerList[1].name = "bot"
            self.catan.playerList[0].victoryPoints = self.hande
        else:
            self.catan.playerList[0].name = "bot"
            self.catan.playerList[1].name = "A2C"
            self.catan.playerList[1].victoryPoints = self.hande
        return
    
    #今が学習したいエージェントのturnならTrue
    #opponetAgentのturnならFalse
    def isMainAgentTurn(self):
        catan = self.catan
        #mainが先手
        if self.firstMove:
            if catan.nowPlayer == catan.playerList[0]:
                return True
            else:
                return False
        #mainが後手
        else:
            if catan.nowPlayer == catan.playerList[0]:
                return False
            else:
                return True

    def reset(self,seed=0):
        catan = self.catan
        #catanの状況をリセット
        catan.reset()
        #今後必要になればopponetAgentに関しても何かしらの処理
        self.firstMove = random.choice([True,False])
        if self.firstMove:
            self.catan.playerList[0].name = "A2C"
            self.catan.playerList[1].name = "bot"
            self.catan.playerList[0].victoryPoints = self.hande
        else:
            self.catan.playerList[0].name = "bot"
            self.catan.playerList[1].name = "A2C"
            self.catan.playerList[1].victoryPoints = self.hande

        #mainの手番になるまで進める
        while(not self.isMainAgentTurn()):
            #ゲームを渡して、行動を選択させる
            action = self.opponentAgent.choiceAction(catan)
            actionInfo = actionControllerGraph(action)
            _,_ = catan.step(actionInfo)

        vector_obs = getVectorFeature(catan)
        hex_obs, vertex_obs, road_obs  = getGraphFeature(catan)
        obs = {"hex":hex_obs, "vertex":vertex_obs, "road":road_obs, "vector":vector_obs}

        #次の状況での合法手も一緒に返す
        return obs,{}
    
    def step(self,action):
        catan = self.catan
        actionInfo = actionControllerGraph(action)
        done,self_reward = self.catan.step(actionInfo)

        #自分の行動でゲーム終了
        if done:
            vector_obs = getVectorFeature(catan)
            hex_obs, vertex_obs, road_obs  = getGraphFeature(catan)
            obs = {"hex":hex_obs, "vertex":vertex_obs, "road":road_obs, "vector":vector_obs}
            return obs,self_reward,done,False,{"is_success":True}
        
        #もう一度自分のターンがくるまで、相手エージェントに行動させる
        while(not self.isMainAgentTurn()):
            opponentAction = self.opponentAgent.choiceAction(catan)
            opponentActionInfo = actionControllerGraph(opponentAction)
            done,op_reward = catan.step(opponentActionInfo)
            #相手の行動でゲーム終了
            if done:
                vector_obs = getVectorFeature(catan)
                hex_obs, vertex_obs, road_obs  = getGraphFeature(catan)
                obs = {"hex":hex_obs, "vertex":vertex_obs, "road":road_obs, "vector":vector_obs}
                #敵ターンで終了　＝　負けてるのでマイナス報酬
                return obs,-op_reward+self_reward,done,False,{"is_success":False}
            
        vector_obs = getVectorFeature(catan)
        hex_obs, vertex_obs, road_obs  = getGraphFeature(catan)
        obs = {"hex":hex_obs, "vertex":vertex_obs, "road":road_obs, "vector":vector_obs}
        return obs,self_reward,False,False,{}

    def action_masks(self):
        return getLegalMaskGraph(self.catan)

class VSEnvironment():
    def __init__(self,mainAgent,opponetAgent,cnn_or_graph,debugLog=False,fixed=True,hande_main=0,hande_op=0):
        self.mainAgent = mainAgent
        self.opponentAgent = opponetAgent
        self.catan = Catan(viewMode=False,debugLog=debugLog,fixed=fixed)
        #trueならメインが先手、falseならopponetAgentが先手
        self.firstMove = random.choice([True,False])
        self.cnn_or_graph = cnn_or_graph

        if self.firstMove:
            self.catan.playerList[0].name = "main"
            self.catan.playerList[1].name = "op"
            self.catan.playerList[0].victoryPoints = hande_main
            self.catan.playerList[1].victoryPoints = hande_op
            
        else:
            self.catan.playerList[0].name = "op"
            self.catan.playerList[1].name = "main"
            self.catan.playerList[1].victoryPoints = hande_main
            self.catan.playerList[0].victoryPoints = hande_op
        return
    
    #mainエージェントのturnならTrue
    #opponetAgentのturnならFalse
    def isMainAgentTurn(self):
        catan = self.catan
        #mainが先手
        if self.firstMove:
            if catan.nowPlayer == catan.playerList[0]:
                return True
            else:
                return False
        #mainが後手
        else:
            if catan.nowPlayer == catan.playerList[0]:
                return False
            else:
                return True
            
    def battle(self):
        catan = self.catan
        done = False
        while (not done):
            if self.isMainAgentTurn():
                action = self.mainAgent.choiceAction(catan)
            else:
                action = self.opponentAgent.choiceAction(catan)

            if self.cnn_or_graph == "cnn":
                actionInfo = actionControllerGraph(action)
            else:
                actionInfo = actionControllerGraph(action)

            done,reward = catan.step(actionInfo)

        if done:
            if self.isMainAgentTurn():
                return "main"
            else:
                return "opponent"
            
    def onestep(self):
        if self.isMainAgentTurn():
            action = self.mainAgent.choiceAction(self.catan)
        else:
            action = self.opponentAgent.choiceAction(self.catan)

        if self.cnn_or_graph == "cnn":
            actionInfo = actionController(action)
        else:
            actionInfo = actionControllerGraph(action)
        done,reward = self.catan.step(actionInfo)

        return action,done

    def reset(self):
        self.catan.reset()
        


if __name__ == "__main__":


    #from stable_baselines3.common.env_checker import check_env
    #env = EnvironmentWithCNNFeature(opponetAgent=HeuristicBot(cnn_or_graph="cnn"))
    #check_env(env)


    
    mainwin,opwin = 0,0
    for i in range(1):
        env = VSEnvironment( HeuristicBot("graph",random=True))
        result = env.battle()
        if result == "main":
            mainwin += 1
        else:
            opwin += 1

    print("mainwin",mainwin)
    print("opwin",opwin)

    
