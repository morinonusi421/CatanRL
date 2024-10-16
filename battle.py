import random
from CatanImplements.Catan import *
from CatanImplements.Controller import *
from sb3_contrib.ppo_mask import MaskablePPO
from CustomPolicies import CustomMaskableActorCriticPolicy , CrossCNNPolicy, CrossGraphPolicy
import os
from CatanImplements.Environment import EnvironmentWithCNNFeature,EnvironmentWithGraphFeature
from CatanImplements.Bots import HeuristicBot


EVAL_LOG_PATH = "./cnn_eval/"
EVAL_LOG_PATH_GRAPH = "./graph_eval/"

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

    env_cnn = EnvironmentWithCNNFeature(opponetAgent=HeuristicBot(cnn_or_graph="cnn"),hande=0)
    model_cnn = MaskablePPO(CrossCNNPolicy, env_graph, verbose=1,)
    model_cnn.set_parameters(os.path.join(EVAL_LOG_PATH, f"best_model_0.zip"))

    env_graph = EnvironmentWithGraphFeature(opponetAgent=HeuristicBot(cnn_or_graph="graph"),hande=0)
    model_graph = MaskablePPO(CrossGraphPolicy, env_graph, verbose=1,)
    model_graph.set_parameters(os.path.join(EVAL_LOG_PATH_GRAPH, f"best_model_0.zip"))

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
