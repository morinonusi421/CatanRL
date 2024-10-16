#ランダム行動botと，ヒューリステックボット

import random
from .Controller import *
from .Phase import *
import copy
#actionInfo→アクション番号の逆引き
reverse_actionController = {"{'name': 'rollDice'}": 0, "{'name': 'endTurn'}": 1, "{'name': 'discard', 'saveResources': {'ORE': 4, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 2, "{'name': 'discard', 'saveResources': {'ORE': 3, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 3, "{'name': 'discard', 'saveResources': {'ORE': 3, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 4, "{'name': 'discard', 'saveResources': {'ORE': 3, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 5, "{'name': 'discard', 'saveResources': {'ORE': 3, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 6, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 7, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 8, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 9, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 10, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 0}}": 11, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 0}}": 12, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 1}}": 13, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 0}}": 14, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 1}}": 15, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 2}}": 16, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 3, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 17, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 2, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 18, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 19, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 20, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 0}}": 21, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 0}}": 22, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 1}}": 23, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 0}}": 24, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 1}}": 25, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 2}}": 26, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 3, 'WOOD': 0, 'SHEEP': 0}}": 27, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 1, 'SHEEP': 0}}": 28, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 1}}": 29, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 2, 'SHEEP': 0}}": 30, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 1}}": 31, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 2}}": 32, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 3, 'SHEEP': 0}}": 33, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 1}}": 34, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 2}}": 35, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 3}}": 36, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 4, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 37, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 3, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 38, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 3, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 39, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 3, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 40, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 0}}": 41, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 0}}": 42, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 1}}": 43, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 0}}": 44, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 1}}": 45, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 2}}": 46, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 3, 'WOOD': 0, 'SHEEP': 0}}": 47, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 2, 'WOOD': 1, 'SHEEP': 0}}": 48, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 1}}": 49, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 2, 'SHEEP': 0}}": 50, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 1}}": 51, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 2}}": 52, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 3, 'SHEEP': 0}}": 53, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 1}}": 54, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 2}}": 55, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 3}}": 56, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 4, 'WOOD': 0, 'SHEEP': 0}}": 57, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 3, 'WOOD': 1, 'SHEEP': 0}}": 58, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 3, 'WOOD': 0, 'SHEEP': 1}}": 59, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 2, 'SHEEP': 0}}": 60, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 1, 'SHEEP': 1}}": 61, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 2}}": 62, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 3, 'SHEEP': 0}}": 63, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 2, 'SHEEP': 1}}": 64, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 2}}": 65, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 3}}": 66, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 4, 'SHEEP': 0}}": 67, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 3, 'SHEEP': 1}}": 68, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 2}}": 69, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 3}}": 70, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 4}}": 71, "{'name': 'bankTrade', 'buyResource': 'ORE', 'sellResource': 'BRICK'}": 72, "{'name': 'bankTrade', 'buyResource': 'ORE', 'sellResource': 'WHEAT'}": 73, "{'name': 'bankTrade', 'buyResource': 'ORE', 'sellResource': 'WOOD'}": 74, "{'name': 'bankTrade', 'buyResource': 'ORE', 'sellResource': 'SHEEP'}": 75, "{'name': 'bankTrade', 'buyResource': 'BRICK', 'sellResource': 'ORE'}": 76, "{'name': 'bankTrade', 'buyResource': 'BRICK', 'sellResource': 'WHEAT'}": 77, "{'name': 'bankTrade', 'buyResource': 'BRICK', 'sellResource': 'WOOD'}": 78, "{'name': 'bankTrade', 'buyResource': 'BRICK', 'sellResource': 'SHEEP'}": 79, "{'name': 'bankTrade', 'buyResource': 'WHEAT', 'sellResource': 'ORE'}": 80, "{'name': 'bankTrade', 'buyResource': 'WHEAT', 'sellResource': 'BRICK'}": 81, "{'name': 'bankTrade', 'buyResource': 'WHEAT', 'sellResource': 'WOOD'}": 82, "{'name': 'bankTrade', 'buyResource': 'WHEAT', 'sellResource': 'SHEEP'}": 83, "{'name': 'bankTrade', 'buyResource': 'WOOD', 'sellResource': 'ORE'}": 84, "{'name': 'bankTrade', 'buyResource': 'WOOD', 'sellResource': 'BRICK'}": 85, "{'name': 'bankTrade', 'buyResource': 'WOOD', 'sellResource': 'WHEAT'}": 86, "{'name': 'bankTrade', 'buyResource': 'WOOD', 'sellResource': 'SHEEP'}": 87, "{'name': 'bankTrade', 'buyResource': 'SHEEP', 'sellResource': 'ORE'}": 88, "{'name': 'bankTrade', 'buyResource': 'SHEEP', 'sellResource': 'BRICK'}": 89, "{'name': 'bankTrade', 'buyResource': 'SHEEP', 'sellResource': 'WHEAT'}": 90, "{'name': 'bankTrade', 'buyResource': 'SHEEP', 'sellResource': 'WOOD'}": 91, "{'name': 'buyDevCard'}": 92, "{'name': 'useKnight'}": 93, "{'name': 'useRoadBuilder'}": 94, "{'name': 'useYear', 'getResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 95, "{'name': 'useYear', 'getResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 96, "{'name': 'useYear', 'getResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 97, "{'name': 'useYear', 'getResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 98, "{'name': 'useYear', 'getResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 99, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 100, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 101, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 102, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 103, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 0}}": 104, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 0}}": 105, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 1}}": 106, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 0}}": 107, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 1}}": 108, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 2}}": 109, "{'name': 'useMonopoly', 'resource': 'ORE'}": 110, "{'name': 'useMonopoly', 'resource': 'BRICK'}": 111, "{'name': 'useMonopoly', 'resource': 'WHEAT'}": 112, "{'name': 'useMonopoly', 'resource': 'WOOD'}": 113, "{'name': 'useMonopoly', 'resource': 'SHEEP'}": 114, "{'name': 'moveThief', 'hexIndex': 17}": 142, "{'name': 'moveThief', 'hexIndex': 18}": 146, "{'name': 'moveThief', 'hexIndex': 7}": 150, "{'name': 'moveThief', 'hexIndex': 16}": 182, "{'name': 'moveThief', 'hexIndex': 6}": 186, "{'name': 'moveThief', 'hexIndex': 1}": 190, "{'name': 'moveThief', 'hexIndex': 8}": 194, "{'name': 'moveThief', 'hexIndex': 15}": 222, "{'name': 'moveThief', 'hexIndex': 5}": 226, "{'name': 'moveThief', 'hexIndex': 0}": 230, "{'name': 'moveThief', 'hexIndex': 2}": 234, "{'name': 'moveThief', 'hexIndex': 9}": 238, "{'name': 'moveThief', 'hexIndex': 14}": 266, "{'name': 'moveThief', 'hexIndex': 4}": 270, "{'name': 'moveThief', 'hexIndex': 3}": 274, "{'name': 'moveThief', 'hexIndex': 10}": 278, "{'name': 'moveThief', 'hexIndex': 13}": 310, "{'name': 'moveThief', 'hexIndex': 12}": 314, "{'name': 'moveThief', 'hexIndex': 11}": 318, "{'name': 'buildRoad', 'v1': 51, 'v2': 52}": 351, "{'name': 'buildRoad', 'v1': 50, 'v2': 51}": 353, "{'name': 'buildRoad', 'v1': 50, 'v2': 53}": 355, "{'name': 'buildRoad', 'v1': 27, 'v2': 53}": 357, "{'name': 'buildRoad', 'v1': 26, 'v2': 27}": 359, "{'name': 'buildRoad', 'v1': 25, 'v2': 26}": 361, "{'name': 'buildRoad', 'v1': 48, 'v2': 52}": 371, "{'name': 'buildRoad', 'v1': 22, 'v2': 50}": 375, "{'name': 'buildRoad', 'v1': 8, 'v2': 27}": 379, "{'name': 'buildRoad', 'v1': 24, 'v2': 25}": 383, "{'name': 'buildRoad', 'v1': 48, 'v2': 49}": 391, "{'name': 'buildRoad', 'v1': 23, 'v2': 48}": 393, "{'name': 'buildRoad', 'v1': 22, 'v2': 23}": 395, "{'name': 'buildRoad', 'v1': 9, 'v2': 22}": 397, "{'name': 'buildRoad', 'v1': 8, 'v2': 9}": 399, "{'name': 'buildRoad', 'v1': 7, 'v2': 8}": 401, "{'name': 'buildRoad', 'v1': 7, 'v2': 24}": 403, "{'name': 'buildRoad', 'v1': 24, 'v2': 29}": 405, "{'name': 'buildRoad', 'v1': 45, 'v2': 49}": 411, "{'name': 'buildRoad', 'v1': 19, 'v2': 23}": 415, "{'name': 'buildRoad', 'v1': 2, 'v2': 9}": 419, "{'name': 'buildRoad', 'v1': 6, 'v2': 7}": 423, "{'name': 'buildRoad', 'v1': 28, 'v2': 29}": 427, "{'name': 'buildRoad', 'v1': 45, 'v2': 46}": 431, "{'name': 'buildRoad', 'v1': 20, 'v2': 45}": 433, "{'name': 'buildRoad', 'v1': 19, 'v2': 20}": 435, "{'name': 'buildRoad', 'v1': 3, 'v2': 19}": 437, "{'name': 'buildRoad', 'v1': 2, 'v2': 3}": 439, "{'name': 'buildRoad', 'v1': 1, 'v2': 2}": 441, "{'name': 'buildRoad', 'v1': 1, 'v2': 6}": 443, "{'name': 'buildRoad', 'v1': 6, 'v2': 11}": 445, "{'name': 'buildRoad', 'v1': 11, 'v2': 28}": 447, "{'name': 'buildRoad', 'v1': 28, 'v2': 31}": 449, "{'name': 'buildRoad', 'v1': 46, 'v2': 47}": 451, "{'name': 'buildRoad', 'v1': 20, 'v2': 21}": 455, "{'name': 'buildRoad', 'v1': 3, 'v2': 4}": 459, "{'name': 'buildRoad', 'v1': 0, 'v2': 1}": 463, "{'name': 'buildRoad', 'v1': 10, 'v2': 11}": 467, "{'name': 'buildRoad', 'v1': 30, 'v2': 31}": 471, "{'name': 'buildRoad', 'v1': 43, 'v2': 47}": 473, "{'name': 'buildRoad', 'v1': 21, 'v2': 43}": 475, "{'name': 'buildRoad', 'v1': 16, 'v2': 21}": 477, "{'name': 'buildRoad', 'v1': 4, 'v2': 16}": 479, "{'name': 'buildRoad', 'v1': 4, 'v2': 5}": 481, "{'name': 'buildRoad', 'v1': 0, 'v2': 5}": 483, "{'name': 'buildRoad', 'v1': 0, 'v2': 12}": 485, "{'name': 'buildRoad', 'v1': 10, 'v2': 12}": 487, "{'name': 'buildRoad', 'v1': 10, 'v2': 32}": 489, "{'name': 'buildRoad', 'v1': 30, 'v2': 32}": 491, "{'name': 'buildRoad', 'v1': 43, 'v2': 44}": 495, "{'name': 'buildRoad', 'v1': 16, 'v2': 17}": 499, "{'name': 'buildRoad', 'v1': 5, 'v2': 14}": 503, "{'name': 'buildRoad', 'v1': 12, 'v2': 13}": 507, "{'name': 'buildRoad', 'v1': 32, 'v2': 33}": 511, "{'name': 'buildRoad', 'v1': 40, 'v2': 44}": 517, "{'name': 'buildRoad', 'v1': 17, 'v2': 40}": 519, "{'name': 'buildRoad', 'v1': 17, 'v2': 18}": 521, "{'name': 'buildRoad', 'v1': 14, 'v2': 18}": 523, "{'name': 'buildRoad', 'v1': 14, 'v2': 15}": 525, "{'name': 'buildRoad', 'v1': 13, 'v2': 15}": 527, "{'name': 'buildRoad', 'v1': 13, 'v2': 34}": 529, "{'name': 'buildRoad', 'v1': 33, 'v2': 34}": 531, "{'name': 'buildRoad', 'v1': 40, 'v2': 41}": 539, "{'name': 'buildRoad', 'v1': 18, 'v2': 38}": 543, "{'name': 'buildRoad', 'v1': 15, 'v2': 36}": 547, "{'name': 'buildRoad', 'v1': 34, 'v2': 35}": 551, "{'name': 'buildRoad', 'v1': 41, 'v2': 42}": 561, "{'name': 'buildRoad', 'v1': 38, 'v2': 42}": 563, "{'name': 'buildRoad', 'v1': 38, 'v2': 39}": 565, "{'name': 'buildRoad', 'v1': 36, 'v2': 39}": 567, "{'name': 'buildRoad', 'v1': 36, 'v2': 37}": 569, "{'name': 'buildRoad', 'v1': 35, 'v2': 37}": 571, "{'name': 'buildSettlement', 'v': 52}": 581, "{'name': 'buildSettlement', 'v': 51}": 583, "{'name': 'buildSettlement', 'v': 50}": 585, "{'name': 'buildSettlement', 'v': 53}": 587, "{'name': 'buildSettlement', 'v': 27}": 589, "{'name': 'buildSettlement', 'v': 26}": 591, "{'name': 'buildSettlement', 'v': 25}": 593, "{'name': 'buildSettlement', 'v': 49}": 621, "{'name': 'buildSettlement', 'v': 48}": 623, "{'name': 'buildSettlement', 'v': 23}": 625, "{'name': 'buildSettlement', 'v': 22}": 627, "{'name': 'buildSettlement', 'v': 9}": 629, "{'name': 'buildSettlement', 'v': 8}": 631, "{'name': 'buildSettlement', 'v': 7}": 633, "{'name': 'buildSettlement', 'v': 24}": 635, "{'name': 'buildSettlement', 'v': 29}": 637, "{'name': 'buildSettlement', 'v': 46}": 661, "{'name': 'buildSettlement', 'v': 45}": 663, "{'name': 'buildSettlement', 'v': 20}": 665, "{'name': 'buildSettlement', 'v': 19}": 667, "{'name': 'buildSettlement', 'v': 3}": 669, "{'name': 'buildSettlement', 'v': 2}": 671, "{'name': 'buildSettlement', 'v': 1}": 673, "{'name': 'buildSettlement', 'v': 6}": 675, "{'name': 'buildSettlement', 'v': 11}": 677, "{'name': 'buildSettlement', 'v': 28}": 679, "{'name': 'buildSettlement', 'v': 31}": 681, "{'name': 'buildSettlement', 'v': 47}": 703, "{'name': 'buildSettlement', 'v': 43}": 705, "{'name': 'buildSettlement', 'v': 21}": 707, "{'name': 'buildSettlement', 'v': 16}": 709, "{'name': 'buildSettlement', 'v': 4}": 711, "{'name': 'buildSettlement', 'v': 5}": 713, "{'name': 'buildSettlement', 'v': 0}": 715, "{'name': 'buildSettlement', 'v': 12}": 717, "{'name': 'buildSettlement', 'v': 10}": 719, "{'name': 'buildSettlement', 'v': 32}": 721, "{'name': 'buildSettlement', 'v': 30}": 723, "{'name': 'buildSettlement', 'v': 44}": 747, "{'name': 'buildSettlement', 'v': 40}": 749, "{'name': 'buildSettlement', 'v': 17}": 751, "{'name': 'buildSettlement', 'v': 18}": 753, "{'name': 'buildSettlement', 'v': 14}": 755, "{'name': 'buildSettlement', 'v': 15}": 757, "{'name': 'buildSettlement', 'v': 13}": 759, "{'name': 'buildSettlement', 'v': 34}": 761, "{'name': 'buildSettlement', 'v': 33}": 763, "{'name': 'buildSettlement', 'v': 41}": 791, "{'name': 'buildSettlement', 'v': 42}": 793, "{'name': 'buildSettlement', 'v': 38}": 795, "{'name': 'buildSettlement', 'v': 39}": 797, "{'name': 'buildSettlement', 'v': 36}": 799, "{'name': 'buildSettlement', 'v': 37}": 801, "{'name': 'buildSettlement', 'v': 35}": 803, "{'name': 'buildCity', 'v': 52}": 812, "{'name': 'buildCity', 'v': 51}": 814, "{'name': 'buildCity', 'v': 50}": 816, "{'name': 'buildCity', 'v': 53}": 818, "{'name': 'buildCity', 'v': 27}": 820, "{'name': 'buildCity', 'v': 26}": 822, "{'name': 'buildCity', 'v': 25}": 824, "{'name': 'buildCity', 'v': 49}": 852, "{'name': 'buildCity', 'v': 48}": 854, "{'name': 'buildCity', 'v': 23}": 856, "{'name': 'buildCity', 'v': 22}": 858, "{'name': 'buildCity', 'v': 9}": 860, "{'name': 'buildCity', 'v': 8}": 862, "{'name': 'buildCity', 'v': 7}": 864, "{'name': 'buildCity', 'v': 24}": 866, "{'name': 'buildCity', 'v': 29}": 868, "{'name': 'buildCity', 'v': 46}": 892, "{'name': 'buildCity', 'v': 45}": 894, "{'name': 'buildCity', 'v': 20}": 896, "{'name': 'buildCity', 'v': 19}": 898, "{'name': 'buildCity', 'v': 3}": 900, "{'name': 'buildCity', 'v': 2}": 902, "{'name': 'buildCity', 'v': 1}": 904, "{'name': 'buildCity', 'v': 6}": 906, "{'name': 'buildCity', 'v': 11}": 908, "{'name': 'buildCity', 'v': 28}": 910, "{'name': 'buildCity', 'v': 31}": 912, "{'name': 'buildCity', 'v': 47}": 934, "{'name': 'buildCity', 'v': 43}": 936, "{'name': 'buildCity', 'v': 21}": 938, "{'name': 'buildCity', 'v': 16}": 940, "{'name': 'buildCity', 'v': 4}": 942, "{'name': 'buildCity', 'v': 5}": 944, "{'name': 'buildCity', 'v': 0}": 946, "{'name': 'buildCity', 'v': 12}": 948, "{'name': 'buildCity', 'v': 10}": 950, "{'name': 'buildCity', 'v': 32}": 952, "{'name': 'buildCity', 'v': 30}": 954, "{'name': 'buildCity', 'v': 44}": 978, "{'name': 'buildCity', 'v': 40}": 980, "{'name': 'buildCity', 'v': 17}": 982, "{'name': 'buildCity', 'v': 18}": 984, "{'name': 'buildCity', 'v': 14}": 986, "{'name': 'buildCity', 'v': 15}": 988, "{'name': 'buildCity', 'v': 13}": 990, "{'name': 'buildCity', 'v': 34}": 992, "{'name': 'buildCity', 'v': 33}": 994, "{'name': 'buildCity', 'v': 41}": 1022, "{'name': 'buildCity', 'v': 42}": 1024, "{'name': 'buildCity', 'v': 38}": 1026, "{'name': 'buildCity', 'v': 39}": 1028, "{'name': 'buildCity', 'v': 36}": 1030, "{'name': 'buildCity', 'v': 37}": 1032, "{'name': 'buildCity', 'v': 35}": 1034}
reverse_actionControllerGraph = {"{'name': 'rollDice'}": 0, "{'name': 'endTurn'}": 1, "{'name': 'discard', 'saveResources': {'ORE': 4, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 2, "{'name': 'discard', 'saveResources': {'ORE': 3, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 3, "{'name': 'discard', 'saveResources': {'ORE': 3, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 4, "{'name': 'discard', 'saveResources': {'ORE': 3, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 5, "{'name': 'discard', 'saveResources': {'ORE': 3, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 6, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 7, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 8, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 9, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 10, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 0}}": 11, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 0}}": 12, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 1}}": 13, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 0}}": 14, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 1}}": 15, "{'name': 'discard', 'saveResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 2}}": 16, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 3, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 17, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 2, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 18, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 19, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 20, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 0}}": 21, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 0}}": 22, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 1}}": 23, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 0}}": 24, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 1}}": 25, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 2}}": 26, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 3, 'WOOD': 0, 'SHEEP': 0}}": 27, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 1, 'SHEEP': 0}}": 28, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 1}}": 29, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 2, 'SHEEP': 0}}": 30, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 1}}": 31, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 2}}": 32, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 3, 'SHEEP': 0}}": 33, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 1}}": 34, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 2}}": 35, "{'name': 'discard', 'saveResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 3}}": 36, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 4, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 37, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 3, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 38, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 3, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 39, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 3, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 40, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 0}}": 41, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 0}}": 42, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 1}}": 43, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 0}}": 44, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 1}}": 45, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 2}}": 46, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 3, 'WOOD': 0, 'SHEEP': 0}}": 47, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 2, 'WOOD': 1, 'SHEEP': 0}}": 48, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 1}}": 49, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 2, 'SHEEP': 0}}": 50, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 1}}": 51, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 2}}": 52, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 3, 'SHEEP': 0}}": 53, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 1}}": 54, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 2}}": 55, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 3}}": 56, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 4, 'WOOD': 0, 'SHEEP': 0}}": 57, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 3, 'WOOD': 1, 'SHEEP': 0}}": 58, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 3, 'WOOD': 0, 'SHEEP': 1}}": 59, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 2, 'SHEEP': 0}}": 60, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 1, 'SHEEP': 1}}": 61, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 2}}": 62, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 3, 'SHEEP': 0}}": 63, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 2, 'SHEEP': 1}}": 64, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 2}}": 65, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 3}}": 66, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 4, 'SHEEP': 0}}": 67, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 3, 'SHEEP': 1}}": 68, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 2}}": 69, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 3}}": 70, "{'name': 'discard', 'saveResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 4}}": 71, "{'name': 'bankTrade', 'buyResource': 'ORE', 'sellResource': 'BRICK'}": 72, "{'name': 'bankTrade', 'buyResource': 'ORE', 'sellResource': 'WHEAT'}": 73, "{'name': 'bankTrade', 'buyResource': 'ORE', 'sellResource': 'WOOD'}": 74, "{'name': 'bankTrade', 'buyResource': 'ORE', 'sellResource': 'SHEEP'}": 75, "{'name': 'bankTrade', 'buyResource': 'BRICK', 'sellResource': 'ORE'}": 76, "{'name': 'bankTrade', 'buyResource': 'BRICK', 'sellResource': 'WHEAT'}": 77, "{'name': 'bankTrade', 'buyResource': 'BRICK', 'sellResource': 'WOOD'}": 78, "{'name': 'bankTrade', 'buyResource': 'BRICK', 'sellResource': 'SHEEP'}": 79, "{'name': 'bankTrade', 'buyResource': 'WHEAT', 'sellResource': 'ORE'}": 80, "{'name': 'bankTrade', 'buyResource': 'WHEAT', 'sellResource': 'BRICK'}": 81, "{'name': 'bankTrade', 'buyResource': 'WHEAT', 'sellResource': 'WOOD'}": 82, "{'name': 'bankTrade', 'buyResource': 'WHEAT', 'sellResource': 'SHEEP'}": 83, "{'name': 'bankTrade', 'buyResource': 'WOOD', 'sellResource': 'ORE'}": 84, "{'name': 'bankTrade', 'buyResource': 'WOOD', 'sellResource': 'BRICK'}": 85, "{'name': 'bankTrade', 'buyResource': 'WOOD', 'sellResource': 'WHEAT'}": 86, "{'name': 'bankTrade', 'buyResource': 'WOOD', 'sellResource': 'SHEEP'}": 87, "{'name': 'bankTrade', 'buyResource': 'SHEEP', 'sellResource': 'ORE'}": 88, "{'name': 'bankTrade', 'buyResource': 'SHEEP', 'sellResource': 'BRICK'}": 89, "{'name': 'bankTrade', 'buyResource': 'SHEEP', 'sellResource': 'WHEAT'}": 90, "{'name': 'bankTrade', 'buyResource': 'SHEEP', 'sellResource': 'WOOD'}": 91, "{'name': 'buyDevCard'}": 92, "{'name': 'useKnight'}": 93, "{'name': 'useRoadBuilder'}": 94, "{'name': 'useYear', 'getResources': {'ORE': 2, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 95, "{'name': 'useYear', 'getResources': {'ORE': 1, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 96, "{'name': 'useYear', 'getResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 97, "{'name': 'useYear', 'getResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 98, "{'name': 'useYear', 'getResources': {'ORE': 1, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 99, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 2, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 0}}": 100, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 0}}": 101, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 0}}": 102, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 1, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 1}}": 103, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 2, 'WOOD': 0, 'SHEEP': 0}}": 104, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 1, 'SHEEP': 0}}": 105, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 1, 'WOOD': 0, 'SHEEP': 1}}": 106, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 2, 'SHEEP': 0}}": 107, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 1, 'SHEEP': 1}}": 108, "{'name': 'useYear', 'getResources': {'ORE': 0, 'BRICK': 0, 'WHEAT': 0, 'WOOD': 0, 'SHEEP': 2}}": 109, "{'name': 'useMonopoly', 'resource': 'ORE'}": 110, "{'name': 'useMonopoly', 'resource': 'BRICK'}": 111, "{'name': 'useMonopoly', 'resource': 'WHEAT'}": 112, "{'name': 'useMonopoly', 'resource': 'WOOD'}": 113, "{'name': 'useMonopoly', 'resource': 'SHEEP'}": 114, "{'name': 'moveThief', 'hexIndex': 0}": 115, "{'name': 'moveThief', 'hexIndex': 1}": 116, "{'name': 'moveThief', 'hexIndex': 2}": 117, "{'name': 'moveThief', 'hexIndex': 3}": 118, "{'name': 'moveThief', 'hexIndex': 4}": 119, "{'name': 'moveThief', 'hexIndex': 5}": 120, "{'name': 'moveThief', 'hexIndex': 6}": 121, "{'name': 'moveThief', 'hexIndex': 7}": 122, "{'name': 'moveThief', 'hexIndex': 8}": 123, "{'name': 'moveThief', 'hexIndex': 9}": 124, "{'name': 'moveThief', 'hexIndex': 10}": 125, "{'name': 'moveThief', 'hexIndex': 11}": 126, "{'name': 'moveThief', 'hexIndex': 12}": 127, "{'name': 'moveThief', 'hexIndex': 13}": 128, "{'name': 'moveThief', 'hexIndex': 14}": 129, "{'name': 'moveThief', 'hexIndex': 15}": 130, "{'name': 'moveThief', 'hexIndex': 16}": 131, "{'name': 'moveThief', 'hexIndex': 17}": 132, "{'name': 'moveThief', 'hexIndex': 18}": 133, "{'name': 'buildSettlement', 'v': 0}": 134, "{'name': 'buildSettlement', 'v': 1}": 135, "{'name': 'buildSettlement', 'v': 2}": 136, "{'name': 'buildSettlement', 'v': 3}": 137, "{'name': 'buildSettlement', 'v': 4}": 138, "{'name': 'buildSettlement', 'v': 5}": 139, "{'name': 'buildSettlement', 'v': 6}": 140, "{'name': 'buildSettlement', 'v': 7}": 141, "{'name': 'buildSettlement', 'v': 8}": 142, "{'name': 'buildSettlement', 'v': 9}": 143, "{'name': 'buildSettlement', 'v': 10}": 144, "{'name': 'buildSettlement', 'v': 11}": 145, "{'name': 'buildSettlement', 'v': 12}": 146, "{'name': 'buildSettlement', 'v': 13}": 147, "{'name': 'buildSettlement', 'v': 14}": 148, "{'name': 'buildSettlement', 'v': 15}": 149, "{'name': 'buildSettlement', 'v': 16}": 150, "{'name': 'buildSettlement', 'v': 17}": 151, "{'name': 'buildSettlement', 'v': 18}": 152, "{'name': 'buildSettlement', 'v': 19}": 153, "{'name': 'buildSettlement', 'v': 20}": 154, "{'name': 'buildSettlement', 'v': 21}": 155, "{'name': 'buildSettlement', 'v': 22}": 156, "{'name': 'buildSettlement', 'v': 23}": 157, "{'name': 'buildSettlement', 'v': 24}": 158, "{'name': 'buildSettlement', 'v': 25}": 159, "{'name': 'buildSettlement', 'v': 26}": 160, "{'name': 'buildSettlement', 'v': 27}": 161, "{'name': 'buildSettlement', 'v': 28}": 162, "{'name': 'buildSettlement', 'v': 29}": 163, "{'name': 'buildSettlement', 'v': 30}": 164, "{'name': 'buildSettlement', 'v': 31}": 165, "{'name': 'buildSettlement', 'v': 32}": 166, "{'name': 'buildSettlement', 'v': 33}": 167, "{'name': 'buildSettlement', 'v': 34}": 168, "{'name': 'buildSettlement', 'v': 35}": 169, "{'name': 'buildSettlement', 'v': 36}": 170, "{'name': 'buildSettlement', 'v': 37}": 171, "{'name': 'buildSettlement', 'v': 38}": 172, "{'name': 'buildSettlement', 'v': 39}": 173, "{'name': 'buildSettlement', 'v': 40}": 174, "{'name': 'buildSettlement', 'v': 41}": 175, "{'name': 'buildSettlement', 'v': 42}": 176, "{'name': 'buildSettlement', 'v': 43}": 177, "{'name': 'buildSettlement', 'v': 44}": 178, "{'name': 'buildSettlement', 'v': 45}": 179, "{'name': 'buildSettlement', 'v': 46}": 180, "{'name': 'buildSettlement', 'v': 47}": 181, "{'name': 'buildSettlement', 'v': 48}": 182, "{'name': 'buildSettlement', 'v': 49}": 183, "{'name': 'buildSettlement', 'v': 50}": 184, "{'name': 'buildSettlement', 'v': 51}": 185, "{'name': 'buildSettlement', 'v': 52}": 186, "{'name': 'buildSettlement', 'v': 53}": 187, "{'name': 'buildCity', 'v': 0}": 188, "{'name': 'buildCity', 'v': 1}": 189, "{'name': 'buildCity', 'v': 2}": 190, "{'name': 'buildCity', 'v': 3}": 191, "{'name': 'buildCity', 'v': 4}": 192, "{'name': 'buildCity', 'v': 5}": 193, "{'name': 'buildCity', 'v': 6}": 194, "{'name': 'buildCity', 'v': 7}": 195, "{'name': 'buildCity', 'v': 8}": 196, "{'name': 'buildCity', 'v': 9}": 197, "{'name': 'buildCity', 'v': 10}": 198, "{'name': 'buildCity', 'v': 11}": 199, "{'name': 'buildCity', 'v': 12}": 200, "{'name': 'buildCity', 'v': 13}": 201, "{'name': 'buildCity', 'v': 14}": 202, "{'name': 'buildCity', 'v': 15}": 203, "{'name': 'buildCity', 'v': 16}": 204, "{'name': 'buildCity', 'v': 17}": 205, "{'name': 'buildCity', 'v': 18}": 206, "{'name': 'buildCity', 'v': 19}": 207, "{'name': 'buildCity', 'v': 20}": 208, "{'name': 'buildCity', 'v': 21}": 209, "{'name': 'buildCity', 'v': 22}": 210, "{'name': 'buildCity', 'v': 23}": 211, "{'name': 'buildCity', 'v': 24}": 212, "{'name': 'buildCity', 'v': 25}": 213, "{'name': 'buildCity', 'v': 26}": 214, "{'name': 'buildCity', 'v': 27}": 215, "{'name': 'buildCity', 'v': 28}": 216, "{'name': 'buildCity', 'v': 29}": 217, "{'name': 'buildCity', 'v': 30}": 218, "{'name': 'buildCity', 'v': 31}": 219, "{'name': 'buildCity', 'v': 32}": 220, "{'name': 'buildCity', 'v': 33}": 221, "{'name': 'buildCity', 'v': 34}": 222, "{'name': 'buildCity', 'v': 35}": 223, "{'name': 'buildCity', 'v': 36}": 224, "{'name': 'buildCity', 'v': 37}": 225, "{'name': 'buildCity', 'v': 38}": 226, "{'name': 'buildCity', 'v': 39}": 227, "{'name': 'buildCity', 'v': 40}": 228, "{'name': 'buildCity', 'v': 41}": 229, "{'name': 'buildCity', 'v': 42}": 230, "{'name': 'buildCity', 'v': 43}": 231, "{'name': 'buildCity', 'v': 44}": 232, "{'name': 'buildCity', 'v': 45}": 233, "{'name': 'buildCity', 'v': 46}": 234, "{'name': 'buildCity', 'v': 47}": 235, "{'name': 'buildCity', 'v': 48}": 236, "{'name': 'buildCity', 'v': 49}": 237, "{'name': 'buildCity', 'v': 50}": 238, "{'name': 'buildCity', 'v': 51}": 239, "{'name': 'buildCity', 'v': 52}": 240, "{'name': 'buildCity', 'v': 53}": 241, "{'name': 'buildRoad', 'v1': 0, 'v2': 1}": 242, "{'name': 'buildRoad', 'v1': 0, 'v2': 5}": 243, "{'name': 'buildRoad', 'v1': 0, 'v2': 12}": 244, "{'name': 'buildRoad', 'v1': 1, 'v2': 2}": 245, "{'name': 'buildRoad', 'v1': 1, 'v2': 6}": 246, "{'name': 'buildRoad', 'v1': 2, 'v2': 3}": 247, "{'name': 'buildRoad', 'v1': 2, 'v2': 9}": 248, "{'name': 'buildRoad', 'v1': 3, 'v2': 4}": 249, "{'name': 'buildRoad', 'v1': 3, 'v2': 19}": 250, "{'name': 'buildRoad', 'v1': 4, 'v2': 5}": 251, "{'name': 'buildRoad', 'v1': 4, 'v2': 16}": 252, "{'name': 'buildRoad', 'v1': 5, 'v2': 14}": 253, "{'name': 'buildRoad', 'v1': 6, 'v2': 7}": 254, "{'name': 'buildRoad', 'v1': 6, 'v2': 11}": 255, "{'name': 'buildRoad', 'v1': 7, 'v2': 8}": 256, "{'name': 'buildRoad', 'v1': 7, 'v2': 24}": 257, "{'name': 'buildRoad', 'v1': 8, 'v2': 9}": 258, "{'name': 'buildRoad', 'v1': 8, 'v2': 27}": 259, "{'name': 'buildRoad', 'v1': 9, 'v2': 22}": 260, "{'name': 'buildRoad', 'v1': 10, 'v2': 11}": 261, "{'name': 'buildRoad', 'v1': 10, 'v2': 12}": 262, "{'name': 'buildRoad', 'v1': 10, 'v2': 32}": 263, "{'name': 'buildRoad', 'v1': 11, 'v2': 28}": 264, "{'name': 'buildRoad', 'v1': 12, 'v2': 13}": 265, "{'name': 'buildRoad', 'v1': 13, 'v2': 15}": 266, "{'name': 'buildRoad', 'v1': 13, 'v2': 34}": 267, "{'name': 'buildRoad', 'v1': 14, 'v2': 15}": 268, "{'name': 'buildRoad', 'v1': 14, 'v2': 18}": 269, "{'name': 'buildRoad', 'v1': 15, 'v2': 36}": 270, "{'name': 'buildRoad', 'v1': 16, 'v2': 17}": 271, "{'name': 'buildRoad', 'v1': 16, 'v2': 21}": 272, "{'name': 'buildRoad', 'v1': 17, 'v2': 18}": 273, "{'name': 'buildRoad', 'v1': 17, 'v2': 40}": 274, "{'name': 'buildRoad', 'v1': 18, 'v2': 38}": 275, "{'name': 'buildRoad', 'v1': 19, 'v2': 20}": 276, "{'name': 'buildRoad', 'v1': 19, 'v2': 23}": 277, "{'name': 'buildRoad', 'v1': 20, 'v2': 21}": 278, "{'name': 'buildRoad', 'v1': 20, 'v2': 45}": 279, "{'name': 'buildRoad', 'v1': 21, 'v2': 43}": 280, "{'name': 'buildRoad', 'v1': 22, 'v2': 23}": 281, "{'name': 'buildRoad', 'v1': 22, 'v2': 50}": 282, "{'name': 'buildRoad', 'v1': 23, 'v2': 48}": 283, "{'name': 'buildRoad', 'v1': 24, 'v2': 25}": 284, "{'name': 'buildRoad', 'v1': 24, 'v2': 29}": 285, "{'name': 'buildRoad', 'v1': 25, 'v2': 26}": 286, "{'name': 'buildRoad', 'v1': 26, 'v2': 27}": 287, "{'name': 'buildRoad', 'v1': 27, 'v2': 53}": 288, "{'name': 'buildRoad', 'v1': 28, 'v2': 29}": 289, "{'name': 'buildRoad', 'v1': 28, 'v2': 31}": 290, "{'name': 'buildRoad', 'v1': 30, 'v2': 31}": 291, "{'name': 'buildRoad', 'v1': 30, 'v2': 32}": 292, "{'name': 'buildRoad', 'v1': 32, 'v2': 33}": 293, "{'name': 'buildRoad', 'v1': 33, 'v2': 34}": 294, "{'name': 'buildRoad', 'v1': 34, 'v2': 35}": 295, "{'name': 'buildRoad', 'v1': 35, 'v2': 37}": 296, "{'name': 'buildRoad', 'v1': 36, 'v2': 37}": 297, "{'name': 'buildRoad', 'v1': 36, 'v2': 39}": 298, "{'name': 'buildRoad', 'v1': 38, 'v2': 39}": 299, "{'name': 'buildRoad', 'v1': 38, 'v2': 42}": 300, "{'name': 'buildRoad', 'v1': 40, 'v2': 41}": 301, "{'name': 'buildRoad', 'v1': 40, 'v2': 44}": 302, "{'name': 'buildRoad', 'v1': 41, 'v2': 42}": 303, "{'name': 'buildRoad', 'v1': 43, 'v2': 44}": 304, "{'name': 'buildRoad', 'v1': 43, 'v2': 47}": 305, "{'name': 'buildRoad', 'v1': 45, 'v2': 46}": 306, "{'name': 'buildRoad', 'v1': 45, 'v2': 49}": 307, "{'name': 'buildRoad', 'v1': 46, 'v2': 47}": 308, "{'name': 'buildRoad', 'v1': 48, 'v2': 49}": 309, "{'name': 'buildRoad', 'v1': 48, 'v2': 52}": 310, "{'name': 'buildRoad', 'v1': 50, 'v2': 51}": 311, "{'name': 'buildRoad', 'v1': 50, 'v2': 53}": 312, "{'name': 'buildRoad', 'v1': 51, 'v2': 52}": 313}


class RandomBot():
    def __init__(self):
        self.selectedActions = [0]*1039

    def choiceAction(self,catan):
        actionWeight = [random.random() for i in range(1039)]
        legalMask = getLegalMask(catan)
        actionWeight = [actionWeight[i] * legalMask[i] for i in range(1039)]
        selectAction = random.choices([i for i in range(1039)],actionWeight)[0]
        self.selectedActions[selectAction] += 1
        return selectAction
    
#グラフネットワークの方に適応しただけ
class RandomBot2():
    def __init__(self):
        self.selectedActions = [0]*314
    def choiceAction(self,catan):
        actionWeight = [random.random() for i in range(314)]
        legalMask = getLegalMaskGraph(catan)
        actionWeight = [actionWeight[i] * legalMask[i] for i in range(314)]
        selectAction = random.choices([i for i in range(314)],actionWeight)[0]
        self.selectedActions[selectAction] += 1
        return selectAction
    
class HeuristicBot():

    def __init__(self,cnn_or_graph,random=True):
        if cnn_or_graph == "cnn":
            self.cnn_or_graph = "cnn"
        elif cnn_or_graph == "graph":
            self.cnn_or_graph = "graph"
        else:
            print("ヒューリステックAI初期化ミス")
            exit()
        #もう持ってる資源　新しい資源にボーナスをつけるため
        self.yetHaveResources = set()
        self.diceRoll_expectation = {2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1, None:0}
        self.resourceName = ['ORE','BRICK','WHEAT','WOOD','SHEEP'] 
        self.random = random

    #与えられた頂点の評価
    def getVertexValue(self,catan,vCoord):
        board = catan.board
        vertexValue = 0
        newHaveResources = copy.deepcopy(self.yetHaveResources)
        for adjacentHexIndex in board.boardGraph[vCoord].adjacentHexList:
            resourceType = board.hexTileDict[adjacentHexIndex].resource.type
            resourceNum = board.hexTileDict[adjacentHexIndex].resource.num
            vertexValue += self.diceRoll_expectation[resourceNum]
            if resourceType != "DESERT":
              newHaveResources.add(resourceType)

        #新しく確保した資源種類ごとに2.5のボーナス
        diffHaveResources = len(newHaveResources) - len(self.yetHaveResources)
        vertexValue += 2.5*(diffHaveResources)
        #if catan.debugLog:
        #    print(f"ヒュ：{board.boardGraph[vCoord].vertexIndex}の評価は{vertexValue}")
        return vertexValue
    
    #全てのhexの盗賊を置いた際の嬉しさを計算する
    def getHexValues(self,catan):
        board = catan.board
        hexValues = [0]*19 #各hexの盗賊を置いた時の嬉しさ
        for vIndex in range(54):
            vCoord = board.vertex_index_to_pixel_dict[vIndex]
            v = board.boardGraph[vCoord]
            for hexIndex in v.adjacentHexList:
                resourceNum = board.hexTileDict[hexIndex].resource.num
                if resourceNum != None:
                    resourceExpect = self.diceRoll_expectation[resourceNum]
                    if v.state['Settlement']:
                        if v.state["Player"] == catan.nowPlayer:
                            hexValues[hexIndex] -= resourceExpect
                        else:
                            hexValues[hexIndex] += resourceExpect
                    elif v.state["City"]:
                        if v.state["Player"] == catan.nowPlayer:
                            hexValues[hexIndex] -= resourceExpect*2
                        else:
                            hexValues[hexIndex] += resourceExpect*2
        #もう盗賊あるところには置けない
        for hexIndex in range(19):
            if board.hexTileDict[hexIndex].robber:
                hexValues[hexIndex] = -10**10
        #if catan.debugLog:
        #    print(f"ヒュ：hexの盗賊置評価,{hexValues}")
        return hexValues

        
    def choiceSettlement(self,catan,possibleVertices):
        board = catan.board
        maxValue = -1
        maxValue_vCoords = []

        #各頂点タイルについて、資源期待値の合計を求める
        for vCoord in possibleVertices.keys():
            vertexValue = self.getVertexValue(catan,vCoord)
            #if catan.debugLog:
            #    print(board.boardGraph[vCoord].vertexIndex,":",vertexValue)
            if vertexValue>maxValue:
                maxValue = vertexValue
                maxValue_vCoords = [vCoord]
            elif vertexValue==maxValue:
                maxValue_vCoords.append(vCoord)

        if self.random:
            #最大評価の頂点をランダムに一つ持ってくる
            selectVCoord = random.choice(maxValue_vCoords)
            selectVIndex = board.boardGraph[selectVCoord].vertexIndex
        else:
            selectVCoord = maxValue_vCoords[0]
            selectVIndex = board.boardGraph[selectVCoord].vertexIndex

        #持ってる資源タイル種類を更新
        for adjacentHexIndex in board.boardGraph[selectVCoord].adjacentHexList:
            resourceType = board.hexTileDict[adjacentHexIndex].resource.type
            if resourceType != 'DESERT':
                self.yetHaveResources.add(resourceType)

        return str({"name":"buildSettlement","v":selectVIndex})
    
    def choiceCity(self,catan,possibleVertices):
        board = catan.board
        maxValue = -1
        maxValue_vCoords = []

        #各頂点タイルについて、資源期待値の合計を求める
        for vCoord in possibleVertices.keys():
            vertexValue = self.getVertexValue(catan,vCoord)
            if vertexValue>maxValue:
                maxValue = vertexValue
                maxValue_vCoords = [vCoord]
            elif vertexValue==maxValue:
                maxValue_vCoords.append(vCoord)

        if self.random:
            #最大評価の頂点をランダムに一つ持ってくる
            selectVCoord = random.choice(maxValue_vCoords)
            selectVIndex = board.boardGraph[selectVCoord].vertexIndex
        else:
            selectVCoord = maxValue_vCoords[0]
            selectVIndex = board.boardGraph[selectVCoord].vertexIndex

        return str({"name":"buildCity","v":selectVIndex})
    
    def choiceRoad(self,catan,possibleRoads):
        board = catan.board
        
        if self.random:
            #適当に選ぶ
            selectRoad = random.choice(list(possibleRoads.keys()))
        else:
            selectRoad = list(possibleRoads.keys())[0]

        selectRoad_v1 = board.boardGraph[selectRoad[0]].vertexIndex
        selectRoad_v2 = board.boardGraph[selectRoad[1]].vertexIndex
        selectRoad_v1,selectRoad_v2 = min(selectRoad_v1,selectRoad_v2),max(selectRoad_v1,selectRoad_v2)
        return str({"name":"buildRoad","v1":selectRoad_v1,"v2":selectRoad_v2})
    
    def choiceDiscard(self,catan):
        resources = catan.nowPlayer.resources
        kouho_actionInfo = []
        for action in range(2,72):
            #保持したいリソースを四つ指定
            temp_actionInfo =  actionController(action)
            saveResources = temp_actionInfo["saveResources"]
            ok = True
            for r in self.resourceName:
                if saveResources[r] > resources[r]:
                    ok = False
            if ok:
                kouho_actionInfo.append(str(temp_actionInfo))

        if self.random:
            return str(random.choice(kouho_actionInfo))
        else:
            return str(kouho_actionInfo[0])
    
    def choiceMoveThief(self,catan):
        hexValues = self.getHexValues(catan)
        max_hexValue = -10**10
        hexIndex_kouho = []
        for i in range(19):
            if hexValues[i]>max_hexValue:
                max_hexValue = hexValues[i]
                hexIndex_kouho = [i]
            elif hexValues[i]==max_hexValue:
                hexIndex_kouho.append(i)
        if self.random:
            return str({"name":"moveThief","hexIndex":random.choice(hexIndex_kouho)})
        else:
            return str({"name":"moveThief","hexIndex":hexIndex_kouho[0]})
    

    def choiceNormal(self,catan):
        board,player = catan.board,catan.nowPlayer
        devCards,resources = player.devCards,player.resources
        #合法点の判定は前作ったプログラムを大いに利用
        legalMask = getLegalMask(catan)
        
        #　独占使えるなら使う 
        if sum(legalMask[110:115])>0:
            if self.random:
                # ランダム
                return str(actionController(random.randrange(110,115)))
            else:
                # 一番少ないやつ
                minResource = min(player.resources.values())
                for r in self.resourceName:
                    if resources[r] == minResource:
                        return str({"name":"useMonopoly","resource":r})

        #　収穫使えるなら使う (適当)
        if sum(legalMask[95:110])>0:
            if self.random:
                return str(actionController(random.randrange(95,110)))
            else:
                #最も少ないやつを二つ
                minResource = min(player.resources.values())
                for r in self.resourceName:
                    if resources[r] == minResource:
                        getResources = {'ORE':0, 'BRICK':0, 'WHEAT':0, 'WOOD':0, 'SHEEP':0}
                        getResources[r] += 2
                        return str({"name":"useYear","getResources":getResources})

        #　街道建設使えるなら使う
        if legalMask[94] == 1:
            return str(actionController(94))
        #　騎士使える&使ったら嬉しい場合は使う
        if legalMask[93]:
            hexValues = self.getHexValues(catan)
            if max(hexValues)>0:
                return str(actionController(93))
            
        # 使える発展カードがない→サイコロ振る
        if not catan.hasRoled:
            return str({'name': 'rollDice'})

        #　都市化できるならする
        if resources['WHEAT']>=2 and resources['ORE']>=3 and player.citiesLeft>0:
            possibleCities = board.get_potential_cities(player)
            if len(possibleCities)>0:
                return self.choiceCity(catan,possibleCities)
        
        # 開拓地建てれるなら建てる
        if resources['BRICK']>0 and resources['WOOD']>0 and resources['SHEEP']>0 and resources['WHEAT']>0 and player.settlementsLeft > 0:
            possibleSettlements = board.get_potential_settlements(player)
            if len(possibleSettlements)>0:
                return self.choiceSettlement(catan,possibleSettlements)
                
        # 発展カード引けるなら引く ランダムモーどは1/2
        if sum(board.devCardStack.values())>0 and resources['WHEAT'] > 0 and resources['ORE'] > 0 and resources['SHEEP'] > 0:
            if self.random:
                if random.randrange(2) == 0:
                    return str({'name': 'buyDevCard'})
            else:
                return str({'name': 'buyDevCard'})
            
        # 道建てれるならたてる　ランダムモードなら1/3
        if resources["BRICK"]>0 and resources["WOOD"]>0 and player.roadsLeft>0:
            if self.random:
                if random.randrange(3) == 0:
                   possibleRoads = board.get_potential_roads(player)
                   if len(possibleRoads)>0:
                      return self.choiceRoad(catan,possibleRoads)
            else:
                possibleRoads = board.get_potential_roads(player)
                if len(possibleRoads)>0:
                    return self.choiceRoad(catan,possibleRoads)
            
        #　めっちゃ多い資源(7個以上)あったら適当に交換
        for sellResource in ['ORE','BRICK','WHEAT','WOOD','SHEEP']:
            if resources[sellResource] >= 7:
                buyResource_kouho = ['ORE','BRICK','WHEAT','WOOD','SHEEP']
                buyResource_kouho.remove(sellResource)
                if self.random:
                    buyResource = random.choice(buyResource_kouho)
                else:
                    buyResource = buyResource_kouho[0]
                return str({"name":"bankTrade","buyResource":buyResource,"sellResource":sellResource})
            
        #　何も引っ掛からなかったらエンドターン
        return str({"name":"endTurn"})


    def choiceAction(self,catan):
        phase = catan.phase
        board,player = catan.board,catan.nowPlayer
        selectActionInfo = "random"

        if phase==Phase.firstInitialSettlement or phase==Phase.secondInitialSettlement:
            possibleSettlements =  board.get_setup_settlements(player)
            selectActionInfo = self.choiceSettlement(catan,possibleSettlements)

        elif phase==Phase.firstInitialRoad or phase==Phase.secondInitialRoad:
            possibleRoads = board.get_setup_roads(player)
            selectActionInfo = self.choiceRoad(catan,possibleRoads)

        elif phase==Phase.discard:
            selectActionInfo = self.choiceDiscard(catan)

        elif phase==Phase.moveThief:
            selectActionInfo = self.choiceMoveThief(catan)

        elif phase==Phase.roadBuilderFirst or phase==Phase.roadBuilderSecond:
            possibleRoads = board.get_potential_roads(player)
            selectActionInfo = self.choiceRoad(catan,possibleRoads)

        elif phase == Phase.normal:
            selectActionInfo = self.choiceNormal(catan)
 

        if self.cnn_or_graph == "cnn":
            #アクションインフォじゃなくてアクション番号で返したい
            return reverse_actionController[selectActionInfo]
        elif self.cnn_or_graph == "graph":
            return reverse_actionControllerGraph[selectActionInfo]
        else:
            print("cnn_or_graphエラー")
            exit()

if __name__ == "__main__":
    catan = Catan(viewMode=False)
    catan.nowPlayer.resources = {'ORE':1,'BRICK':4,'WHEAT':1,'WOOD':0,'SHEEP':0}
    agent = HeuristicBot(cnn_or_graph="graph")
    for h in catan.board.hexTileDict.values():
        print(h.resource)