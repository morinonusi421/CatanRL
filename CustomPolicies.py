import torch as th
import torch.nn as nn
from typing import Callable, Dict, List, Optional, Tuple, Type, Union
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
import gymnasium as gym
import numpy as np

from torch_geometric.data import HeteroData, Batch
from torch_geometric.nn import GATConv, Linear, HeteroConv

use_cuda = th.cuda.is_available()
device = th.device("cuda" if use_cuda else "cpu")

H,W = 11,21
VEC_FEATURE_SIZE = 53
CNN_FEATURE_SHAPE = (24,11,21) #5504
VEC_ACTION_SIZE = 115
CNN_ACTION_SHAPE = (4,11,21) #=924

HEXTILE_FEATURE_SHAPE = (19,6)
VERTEXTILE_FEATURE_SHAPE = (54,15)
ROADTILE_FEATURE_SHAPE = (72,2)
HEXTILE_NUM , VERTEXTILE_NUM , ROADTILE_NUM = 19,54,72

#エッジの接続関係 Controllerのところでコード書いて生成した
hextile_to_vertextile = [[0, 2, 3, 0, 1, 2, 0, 1, 6, 0, 5, 6, 0, 4, 5, 0, 3, 4, 1, 2, 8, 1, 7, 8, 1, 7, 18, 1, 6, 18, 2, 9, 10, 2, 8, 9, 2, 3, 10, 3, 10, 11, 3, 4, 12, 3, 11, 12, 4, 5, 14, 4, 13, 14, 4, 12, 13, 5, 6, 16, 5, 15, 16, 5, 14, 15, 6, 17, 18, 6, 16, 17, 7, 8, 7, 7, 7, 18, 8, 9, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 11, 12, 13, 12, 13, 14, 13, 13, 14, 15, 14, 15, 16, 15, 15, 16, 17, 16, 17, 18, 17, 17, 18], [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 25, 26, 27, 27, 28, 28, 29, 30, 31, 32, 32, 33, 34, 34, 35, 36, 36, 37, 38, 38, 39, 40, 40, 41, 42, 43, 43, 44, 45, 45, 46, 47, 48, 48, 49, 50, 50, 51, 52, 53]]
vertextile_to_hextile = [[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 25, 26, 27, 27, 28, 28, 29, 30, 31, 32, 32, 33, 34, 34, 35, 36, 36, 37, 38, 38, 39, 40, 40, 41, 42, 43, 43, 44, 45, 45, 46, 47, 48, 48, 49, 50, 50, 51, 52, 53], [0, 2, 3, 0, 1, 2, 0, 1, 6, 0, 5, 6, 0, 4, 5, 0, 3, 4, 1, 2, 8, 1, 7, 8, 1, 7, 18, 1, 6, 18, 2, 9, 10, 2, 8, 9, 2, 3, 10, 3, 10, 11, 3, 4, 12, 3, 11, 12, 4, 5, 14, 4, 13, 14, 4, 12, 13, 5, 6, 16, 5, 15, 16, 5, 14, 15, 6, 17, 18, 6, 16, 17, 7, 8, 7, 7, 7, 18, 8, 9, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 11, 12, 13, 12, 13, 14, 13, 13, 14, 15, 14, 15, 16, 15, 15, 16, 17, 16, 17, 18, 17, 17, 18]]
roadtile_to_vertextile = [[0, 1, 2, 0, 3, 4, 3, 5, 6, 5, 7, 8, 7, 9, 10, 1, 9, 11, 4, 12, 13, 12, 14, 15, 14, 16, 17, 6, 16, 18, 19, 20, 21, 13, 19, 22, 2, 20, 23, 23, 24, 25, 11, 26, 27, 24, 26, 28, 10, 29, 30, 29, 31, 32, 27, 31, 33, 8, 34, 35, 34, 36, 37, 30, 36, 38, 18, 39, 40, 35, 39, 41, 15, 42, 43, 42, 44, 44, 45, 17, 45, 46, 22, 47, 48, 43, 47, 49, 50, 48, 49, 21, 50, 51, 51, 52, 25, 52, 53, 53, 54, 28, 55, 56, 54, 55, 33, 57, 58, 56, 57, 32, 59, 60, 59, 61, 58, 61, 38, 62, 63, 60, 62, 37, 64, 65, 64, 66, 63, 66, 41, 67, 68, 65, 67, 40, 69, 70, 69, 71, 68, 71, 46, 70], [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 26, 26, 27, 27, 27, 28, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 32, 33, 33, 34, 34, 34, 35, 35, 36, 36, 36, 37, 37, 38, 38, 38, 39, 39, 40, 40, 40, 41, 41, 42, 42, 43, 43, 43, 44, 44, 45, 45, 45, 46, 46, 47, 47, 48, 48, 48, 49, 49, 50, 50, 50, 51, 51, 52, 52, 53, 53]]
vertextile_to_roadtile = [[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 26, 26, 27, 27, 27, 28, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 32, 33, 33, 34, 34, 34, 35, 35, 36, 36, 36, 37, 37, 38, 38, 38, 39, 39, 40, 40, 40, 41, 41, 42, 42, 43, 43, 43, 44, 44, 45, 45, 45, 46, 46, 47, 47, 48, 48, 48, 49, 49, 50, 50, 50, 51, 51, 52, 52, 53, 53], [0, 1, 2, 0, 3, 4, 3, 5, 6, 5, 7, 8, 7, 9, 10, 1, 9, 11, 4, 12, 13, 12, 14, 15, 14, 16, 17, 6, 16, 18, 19, 20, 21, 13, 19, 22, 2, 20, 23, 23, 24, 25, 11, 26, 27, 24, 26, 28, 10, 29, 30, 29, 31, 32, 27, 31, 33, 8, 34, 35, 34, 36, 37, 30, 36, 38, 18, 39, 40, 35, 39, 41, 15, 42, 43, 42, 44, 44, 45, 17, 45, 46, 22, 47, 48, 43, 47, 49, 50, 48, 49, 21, 50, 51, 51, 52, 25, 52, 53, 53, 54, 28, 55, 56, 54, 55, 33, 57, 58, 56, 57, 32, 59, 60, 59, 61, 58, 61, 38, 62, 63, 60, 62, 37, 64, 65, 64, 66, 63, 66, 41, 67, 68, 65, 67, 40, 69, 70, 69, 71, 68, 71, 46, 70]]
vertextile_to_vertextile = [[0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 25, 25, 26, 26, 27, 27, 27, 28, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 32, 33, 33, 34, 34, 34, 35, 35, 36, 36, 36, 37, 37, 38, 38, 38, 39, 39, 40, 40, 40, 41, 41, 42, 42, 43, 43, 43, 44, 44, 45, 45, 45, 46, 46, 47, 47, 48, 48, 48, 49, 49, 50, 50, 50, 51, 51, 52, 52, 53, 53], [1, 5, 12, 0, 2, 6, 1, 3, 9, 2, 4, 19, 3, 5, 16, 0, 4, 14, 1, 7, 11, 6, 8, 24, 7, 9, 27, 2, 8, 22, 11, 12, 32, 6, 10, 28, 0, 10, 13, 12, 15, 34, 5, 15, 18, 13, 14, 36, 4, 17, 21, 16, 18, 40, 14, 17, 38, 3, 20, 23, 19, 21, 45, 16, 20, 43, 9, 23, 50, 19, 22, 48, 7, 25, 29, 24, 26, 25, 27, 8, 26, 53, 11, 29, 31, 24, 28, 31, 32, 28, 30, 10, 30, 33, 32, 34, 13, 33, 35, 34, 37, 15, 37, 39, 35, 36, 18, 39, 42, 36, 38, 17, 41, 44, 40, 42, 38, 41, 21, 44, 47, 40, 43, 20, 46, 49, 45, 47, 43, 46, 23, 49, 52, 45, 48, 22, 51, 53, 50, 52, 48, 51, 27, 50]]
roadtile_to_roadtile = [[0, 1, 0, 2, 1, 2, 0, 3, 0, 4, 3, 4, 3, 5, 3, 6, 5, 6, 5, 7, 5, 8, 7, 8, 7, 9, 7, 10, 9, 10, 1, 9, 1, 11, 9, 11, 4, 12, 4, 13, 12, 13, 12, 14, 12, 15, 14, 15, 14, 16, 14, 17, 16, 17, 6, 16, 6, 18, 16, 18, 19, 20, 19, 21, 20, 21, 13, 19, 13, 22, 19, 22, 2, 20, 2, 23, 20, 23, 23, 24, 23, 25, 24, 25, 11, 26, 11, 27, 26, 27, 24, 26, 24, 28, 26, 28, 10, 29, 10, 30, 29, 30, 29, 31, 29, 32, 31, 32, 27, 31, 27, 33, 31, 33, 8, 34, 8, 35, 34, 35, 34, 36, 34, 37, 36, 37, 30, 36, 30, 38, 36, 38, 18, 39, 18, 40, 39, 40, 35, 39, 35, 41, 39, 41, 15, 42, 15, 43, 42, 43, 42, 44, 44, 45, 17, 45, 17, 46, 45, 46, 22, 47, 22, 48, 47, 48, 43, 47, 49, 50, 48, 49, 21, 50, 21, 51, 50, 51, 51, 52, 25, 52, 25, 53, 52, 53, 53, 54, 28, 55, 28, 56, 55, 56, 54, 55, 33, 57, 33, 58, 57, 58, 56, 57, 32, 59, 32, 60, 59, 60, 59, 61, 58, 61, 38, 62, 38, 63, 62, 63, 60, 62, 37, 64, 37, 65, 64, 65, 64, 66, 63, 66, 41, 67, 41, 68, 67, 68, 65, 67, 40, 69, 40, 70, 69, 70, 69, 71, 68, 71, 46, 70], [1, 0, 2, 0, 2, 1, 3, 0, 4, 0, 4, 3, 5, 3, 6, 3, 6, 5, 7, 5, 8, 5, 8, 7, 9, 7, 10, 7, 10, 9, 9, 1, 11, 1, 11, 9, 12, 4, 13, 4, 13, 12, 14, 12, 15, 12, 15, 14, 16, 14, 17, 14, 17, 16, 16, 6, 18, 6, 18, 16, 20, 19, 21, 19, 21, 20, 19, 13, 22, 13, 22, 19, 20, 2, 23, 2, 23, 20, 24, 23, 25, 23, 25, 24, 26, 11, 27, 11, 27, 26, 26, 24, 28, 24, 28, 26, 29, 10, 30, 10, 30, 29, 31, 29, 32, 29, 32, 31, 31, 27, 33, 27, 33, 31, 34, 8, 35, 8, 35, 34, 36, 34, 37, 34, 37, 36, 36, 30, 38, 30, 38, 36, 39, 18, 40, 18, 40, 39, 39, 35, 41, 35, 41, 39, 42, 15, 43, 15, 43, 42, 44, 42, 45, 44, 45, 17, 46, 17, 46, 45, 47, 22, 48, 22, 48, 47, 47, 43, 50, 49, 49, 48, 50, 21, 51, 21, 51, 50, 52, 51, 52, 25, 53, 25, 53, 52, 54, 53, 55, 28, 56, 28, 56, 55, 55, 54, 57, 33, 58, 33, 58, 57, 57, 56, 59, 32, 60, 32, 60, 59, 61, 59, 61, 58, 62, 38, 63, 38, 63, 62, 62, 60, 64, 37, 65, 37, 65, 64, 66, 64, 66, 63, 67, 41, 68, 41, 68, 67, 67, 65, 69, 40, 70, 40, 70, 69, 71, 69, 71, 68, 70, 46]]



#超最低限のカタン(cnn用入力)を処理するネットワーク
class CustomMaskableNetwork(nn.Module):

    def __init__(
        self,
        feature_dim: int,
        last_layer_dim_pi: int = 64,
        last_layer_dim_vf: int = 64,
    ):
        super(CustomMaskableNetwork, self).__init__()

        # Save output dimensions, used to create the distributions
        self.latent_dim_pi = last_layer_dim_pi
        self.latent_dim_vf = last_layer_dim_vf

        # Define layers for the policy network
        self.policy_layer1 = nn.Linear(feature_dim, 128)
        self.policy_layer2 = nn.Linear(128, last_layer_dim_pi)

        # Define layers for the value network
        self.value_layer1 = nn.Linear(feature_dim, 128)
        self.value_layer2 = nn.Linear(128, last_layer_dim_vf)

        # Define activation function
        self.activation = nn.ReLU()

    def forward(self, features: Dict[str, th.Tensor]) -> Tuple[th.Tensor, th.Tensor]:
        # Process 'matrix' input
        matrix_input = features['matrix'].view(features['matrix'].size(0), -1)  # Flatten the matrix
        scalar_input = features['vector']  # Scalar input remains the same

        # Concatenate inputs
        combined_input = th.cat((matrix_input, scalar_input), dim=1)

        # Policy network forward pass
        policy_out = self.activation(self.policy_layer1(combined_input))
        latent_policy = self.policy_layer2(policy_out)

        # Value network forward pass
        value_out = self.activation(self.value_layer1(combined_input))
        latent_value = self.value_layer2(value_out)

        return latent_policy, latent_value
    
    def forward_actor(self, features: th.Tensor) -> th.Tensor:
        return self.forward(features)[0]

    def forward_critic(self, features: th.Tensor) -> th.Tensor:
        return self.forward(features)[1]


class CustomMaskableActorCriticPolicy(MaskableActorCriticPolicy):


    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        lr_schedule: Callable[[float], float],
        net_arch: Optional[List[Union[int, Dict[str, List[int]]]]] = None,
        activation_fn: Type[nn.Module] = nn.Tanh,
        *args,
        **kwargs,
    ):
        super(CustomMaskableActorCriticPolicy, self).__init__(
            observation_space,
            action_space,
            lr_schedule,
            net_arch,
            activation_fn,
            *args,
            **kwargs,
        )
        # Disable orthogonal initialization
        self.ortho_init = False

    def extract_features(self,obs):
        return obs

    def _build_mlp_extractor(self) -> None:
        # Use the custom network instead of the default one
        self.mlp_extractor = CustomMaskableNetwork(self.features_dim)

    def get_distribution(self, obs , action_masks: Optional[np.ndarray] = None):
        features = obs
        latent_pi = self.mlp_extractor.forward_actor(features)
        distribution = self._get_action_dist_from_latent(latent_pi)
        if action_masks is not None:
            distribution.apply_masking(action_masks)
        return distribution

    def predict_values(self, obs) -> th.Tensor:
        features = obs
        latent_vf = self.mlp_extractor.forward_critic(features)
        return self.value_net(latent_vf)
    


class CrossDimensionalNet(nn.Module):

    def __init__(self,n_in,n_out,c_in,c_out,add_res):
        super(CrossDimensionalNet, self).__init__()
        self.vec_to_vec = nn.Linear(n_in, n_out)
        self.cnn_to_cnn = nn.Conv2d(c_in, c_out, kernel_size=(3, 5), padding=(1, 2))
        self.cnn_to_vec = nn.Linear(c_in*2 , n_out) #deflatenしたcnnの特徴量を、ベクトル出力に変換する
        self.vec_to_cnn = nn.Linear(n_in,c_out)
        self.add_res = add_res #残渣接続を入れるかどうか,bool
      
    def forward(self, x_vec, x_cnn, x_cnn_res=0):
        x_vec_out_form_vec = self.vec_to_vec(x_vec)
        x_cnn_out_from_cnn = self.cnn_to_cnn(x_cnn)

        #チャンネルごとの平均と分散を取り、それを並べたものをdeflattenとする。
        x_cnn_mean = th.mean(x_cnn, dim=(2,3))
        x_cnn_var = th.var(x_cnn, dim=(2,3))
        x_cnn_deflatten = th.cat((x_cnn_mean,x_cnn_var),dim=1)
        x_vec_out_from_cnn = self.cnn_to_vec(x_cnn_deflatten)

        x_cnn_out_from_vec_notinflatten = self.vec_to_cnn(x_vec)
        x_cnn_out_from_vec_notinflatten = x_cnn_out_from_vec_notinflatten.unsqueeze(-1).unsqueeze(-1)
        x_cnn_out_from_vec = x_cnn_out_from_vec_notinflatten.expand(-1, -1, * CNN_FEATURE_SHAPE[1:])
        
        x_vec_out = x_vec_out_form_vec + x_vec_out_from_cnn
        
        x_cnn_out = x_cnn_out_from_vec + x_cnn_out_from_cnn

        if self.add_res:
            x_cnn_out += x_cnn_res

        return x_vec_out,x_cnn_out
    

class MultiCrossNetwork(nn.Module):

    def __init__(self):
        super(MultiCrossNetwork, self).__init__()

        # Save output dimensions, used to create the distributions
        self.latent_dim_pi = 1039
        self.latent_dim_vf = 1024

        self.cross1 = CrossDimensionalNet(VEC_FEATURE_SIZE,40,CNN_FEATURE_SHAPE[0],15,False) 
        self.cross2 = CrossDimensionalNet(40,40,15,15,False)
        self.cross3 = CrossDimensionalNet(40,40,15,15,True)
        self.cross4 = CrossDimensionalNet(40,40,15,15,False)
        self.cross5 = CrossDimensionalNet(40,40,15,15,True)
        self.cross6 = CrossDimensionalNet(40,40,15,15,False)

        self.cross7a = CrossDimensionalNet(40,40,15,15,True)
        self.cross8a = CrossDimensionalNet(40,VEC_ACTION_SIZE,15,CNN_ACTION_SHAPE[0],False)

        self.cross7c = CrossDimensionalNet(40,40,15,15,True)
        self.dense_critic = nn.Linear(15*H*W+40,1024)

        self.leakyrelu = nn.LeakyReLU()
        self.tanh = nn.Tanh()
        self.flatten = nn.Flatten() 

    def forward(self, features: Dict[str, th.Tensor]) -> Tuple[th.Tensor, th.Tensor]:
        # Process 'matrix' input
        x_cnn0 = features['matrix']
        x_vec0 = features['vector'] 

        x_vec1,x_cnn1 = map(self.tanh,(self.cross1(x_vec0,x_cnn0)))
        x_vec2,x_cnn2 = map(self.leakyrelu,(self.cross2(x_vec1,x_cnn1)))
        x_vec3,x_cnn3 = map(self.tanh,(self.cross3(x_vec2,x_cnn2,x_cnn1))) #res
        x_vec4,x_cnn4 = map(self.leakyrelu,(self.cross4(x_vec3,x_cnn3)))
        x_vec5,x_cnn5 = map(self.tanh,(self.cross5(x_vec4,x_cnn4,x_cnn3))) #res
        x_vec6,x_cnn6 = map(self.leakyrelu,(self.cross6(x_vec5,x_cnn5)))

        x_vec7a,x_cnn7a = map(self.tanh,(self.cross7a(x_vec6,x_cnn6,x_cnn5))) #res
        x_vec8a,x_cnn8a = map(self.leakyrelu,(self.cross8a(x_vec7a,x_cnn7a)))
        x_cnn8a_flatten = self.flatten(x_cnn8a)
        x_actor =  th.cat((x_vec8a,x_cnn8a_flatten),dim=1)

        x_vec7c,x_cnn7c = map(self.tanh,(self.cross7c(x_vec6,x_cnn6,x_cnn5))) #res
        x_cnn7c_flatten = self.flatten(x_cnn7c)
        x_critic = th.cat((x_vec7c,x_cnn7c_flatten),dim=1)
        x_critic = self.dense_critic(x_critic)

        return x_actor,x_critic
    
    def forward_actor(self, features: th.Tensor) -> th.Tensor:
        return self.forward(features)[0]

    def forward_critic(self, features: th.Tensor) -> th.Tensor:
        return self.forward(features)[1]


class CrossCNNPolicy(MaskableActorCriticPolicy):


    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        lr_schedule: Callable[[float], float],
        net_arch: Optional[List[Union[int, Dict[str, List[int]]]]] = None,
        activation_fn: Type[nn.Module] = nn.Tanh,
        *args,
        **kwargs,
    ):
        super(CrossCNNPolicy, self).__init__(
            observation_space,
            action_space,
            lr_schedule,
            net_arch,
            activation_fn,
            *args,
            **kwargs,
        )
        # Disable orthogonal initialization
        self.ortho_init = False

    def extract_features(self,obs):
        return obs

    def _build_mlp_extractor(self) -> None:
        # Use the custom network instead of the default one
        self.mlp_extractor = MultiCrossNetwork()

    def get_distribution(self, obs , action_masks: Optional[np.ndarray] = None):
        features = obs
        latent_pi = self.mlp_extractor.forward_actor(features)
        distribution = self._get_action_dist_from_latent(latent_pi)
        if action_masks is not None:
            distribution.apply_masking(action_masks)
        return distribution

    def predict_values(self, obs) -> th.Tensor:
        features = obs
        latent_vf = self.mlp_extractor.forward_critic(features)
        return self.value_net(latent_vf)











class HeteroGAT(th.nn.Module):
    def __init__(self , out_hex, out_vertex, out_road):
        super(HeteroGAT, self).__init__()
        # 異種グラフの畳み込み層1
        self.conv1 = HeteroConv({
            ("hexTile","to","vertexTile"): GATConv((-1,-1), out_vertex,add_self_loops=False).to(device),
            ("vertexTile","to","hexTile"): GATConv((-1,-1), out_hex,add_self_loops=False).to(device),
            ("roadTile","to","vertexTile"): GATConv((-1,-1), out_vertex,add_self_loops=False).to(device),
            ("vertexTile","to","roadTile"): GATConv((-1,-1), out_road,add_self_loops=False).to(device),
            ("vertexTile","to","vertexTile"): GATConv((-1,-1), out_vertex,add_self_loops=False).to(device),
            ("roadTile","to","roadTile"): GATConv((-1,-1), out_road,add_self_loops=False).to(device)
        }, aggr='mean')
        #自分自身の情報を見るための部分
        self.lin = th.nn.ModuleDict({
                'hexTile': Linear(-1, out_hex).to(device),
                'vertexTile': Linear(-1, out_vertex).to(device),
                'roadTile': Linear(-1, out_road).to(device),
            })    

    def forward(self, x_graph):
        x_dict, edge_index_dict = x_graph.x_dict, x_graph.edge_index_dict
        x_dict_conved = self.conv1(x_dict, edge_index_dict)
        x_dict_lined = {key: self.lin[key](x) for key,x in x_dict.items()}
        x_dict_ret = {key: x_dict_conved[key]+x_dict_lined[key] for key in x_dict.keys()}
        batch_size = x_graph.num_graphs
        num_nodes_dict = {"hexTile":HEXTILE_NUM,"vertexTile":VERTEXTILE_NUM,"roadTile":ROADTILE_NUM}
        # [batchsize*タイル数,特徴数]なのを、[batchsize,タイル数,特徴数]に変形する
        x_dict_ret_reshape = {key: x.view(batch_size, num_nodes_dict[key], -1) for key, x in x_dict_ret.items()}

        return x_dict_ret_reshape["hexTile"],x_dict_ret_reshape["vertexTile"],x_dict_ret_reshape["roadTile"]

class CrossDimensionalGraphNet(nn.Module):

    def makeGraphDataObject(self,hexTileFeature, vertexTileFeature, roadTileFeature):

        batch_size = hexTileFeature.size(0)  # バッチサイズを取得
        data_list = []

        for i in range(batch_size):
            data = HeteroData()
            # 各タイルの特徴を設定
            data["hexTile"].x = hexTileFeature[i]  # i番目のバッチの特徴量
            data["vertexTile"].x = vertexTileFeature[i]
            data["roadTile"].x = roadTileFeature[i]
            
            data["hexTile", "to", "vertexTile"].edge_index = th.tensor(hextile_to_vertextile, dtype=th.long, device=device)
            data["vertexTile", "to", "hexTile"].edge_index = th.tensor(vertextile_to_hextile, dtype=th.long, device=device)
            data["roadTile", "to", "vertexTile"].edge_index = th.tensor(roadtile_to_vertextile, dtype=th.long, device=device)
            data["vertexTile", "to", "roadTile"].edge_index = th.tensor(vertextile_to_roadtile, dtype=th.long, device=device)
            data["vertexTile", "to", "vertexTile"].edge_index = th.tensor(vertextile_to_vertextile, dtype=th.long, device=device)
            data["roadTile", "to", "roadTile"].edge_index = th.tensor(roadtile_to_roadtile, dtype=th.long, device=device)
            
            data_list.append(data)

        return Batch.from_data_list(data_list)

    def compute_mean_and_max(self, x_hexTile, x_vertexTile, x_roadTile):
        batch_size = x_hexTile.size(0)
        hex_means, hex_maxs = [], []
        vertex_means, vertex_maxs = [], []
        road_means, road_maxs = [], []

        for i in range(batch_size):
            # x_hexTileの平均と分散を求める
            hex_mean = th.mean(x_hexTile[i], dim=0)  # 各特徴次元の平均
            hex_max,_ = th.max(x_hexTile[i], dim=0)    # 各特徴次元の分散
            hex_means.append(hex_mean)
            hex_maxs.append(hex_max)

            # x_vertexTileの平均とmaxを求める
            vertex_mean = th.mean(x_vertexTile[i], dim=0)  # 各特徴次元の平均
            vertex_max,_ = th.max(x_vertexTile[i], dim=0)    # 各特徴次元の分散
            vertex_means.append(vertex_mean)
            vertex_maxs.append(vertex_max)

            # x_roadTileの平均と分散を求める
            road_mean = th.mean(x_roadTile[i], dim=0)  # 各特徴次元の平均
            road_max,_ = th.max(x_roadTile[i], dim=0)    # 各特徴次元の分散
            road_means.append(road_mean)
            road_maxs.append(road_max)

        # 各バッチの結果を結合してバッチ次元を持つテンソルにする
        hex_mean_tensor = th.stack(hex_means, dim=0)
        hex_max_tensor = th.stack(hex_maxs, dim=0)
        vertex_mean_tensor = th.stack(vertex_means, dim=0)
        vertex_max_tensor = th.stack(vertex_maxs, dim=0)
        road_mean_tensor = th.stack(road_means, dim=0)
        road_max_tensor = th.stack(road_maxs, dim=0)

        # 各タイルの平均とmaxを結合
        mean_tensor = th.cat([hex_mean_tensor, vertex_mean_tensor, road_mean_tensor], dim=1)
        max_tensor = th.cat([hex_max_tensor, vertex_max_tensor, road_max_tensor], dim=1)

        result = th.cat([mean_tensor, max_tensor], dim=1)
        return result
    
    #g_in_sum = hex,vertex,roadのチャンネルの合計
    #g_out = 3つそれぞれの出力チャンネル数
    def __init__(self,n_in,n_out,g_in_sum,hex_out,vertex_out,road_out,add_res):
        super(CrossDimensionalGraphNet, self).__init__()
        self.vec_to_vec = nn.Linear(n_in,n_out).to(device)
        self.graph_to_graph = HeteroGAT(hex_out,vertex_out,road_out).to(device)
        self.graph_to_vec = nn.Linear(g_in_sum*2,n_out).to(device)
        self.vec_to_graph = nn.Linear(n_in,hex_out+vertex_out+road_out).to(device)
        self.hex_out = hex_out
        self.vertex_out = vertex_out
        self.road_out = road_out
        self.add_res = add_res
   
    def forward(self,x_vec, x_hexTile, x_vertexTile, x_roadTile, x_hexTile_res=0, x_vertexTile_res=0, x_roadTile_res=0):
        batchsize = x_vec.size(0)
        #ベクトルからベクトルへの変換
        x_vec_out_from_vec = self.vec_to_vec(x_vec)
        #グラフobject作成
        x_graph = self.makeGraphDataObject(x_hexTile,x_vertexTile,x_roadTile)
        #グラフからグラフへ変換
        x_hexTile_from_graph,x_vertexTile_from_graph,x_roadTile_from_graph = self.graph_to_graph(x_graph)
        #グラフからベクトルへの変換 プーリングした後dense
        x_graph_deflatten = self.compute_mean_and_max(x_hexTile,x_vertexTile,x_roadTile)
        x_vec_out_from_graph = self.graph_to_vec(x_graph_deflatten)
        #ベクトルからグラフへの変換 denseした後に逆プーリング
        x_graph_out_from_vec = self.vec_to_graph(x_vec)
        x_hexTile_out_from_vec = th.empty(batchsize, HEXTILE_NUM, self.hex_out).to(device)
        x_vertexTile_out_from_vec = th.empty(batchsize, VERTEXTILE_NUM, self.vertex_out).to(device)
        x_roadTile_out_from_vec = th.empty(batchsize, ROADTILE_NUM, self.road_out).to(device)
        for i in range(batchsize):
            x_hexTile_out_from_vec[i] = x_graph_out_from_vec[i][0:self.hex_out].expand(HEXTILE_NUM, -1)
            x_vertexTile_out_from_vec[i] = x_graph_out_from_vec[i][self.hex_out:self.hex_out+self.vertex_out].expand(VERTEXTILE_NUM,-1)
            x_roadTile_out_from_vec[i] = x_graph_out_from_vec[i][self.hex_out+self.vertex_out:].expand(ROADTILE_NUM,-1)        
        x_vec_out =  x_vec_out_from_vec + x_vec_out_from_graph


        x_hexTile_out = x_hexTile_out_from_vec + x_hexTile_from_graph
        x_vertexTile_out = x_vertexTile_out_from_vec + x_vertexTile_from_graph
        x_roadTile_out = x_roadTile_out_from_vec + x_roadTile_from_graph

        if self.add_res:
            x_hexTile_out += x_hexTile_res
            x_vertexTile_out += x_vertexTile_res
            x_roadTile_out += x_roadTile_res

        return x_vec_out,x_hexTile_out,x_vertexTile_out,x_roadTile_out  
    



class MultiCrossGraphNetwork(nn.Module):

    def __init__(self):
        super(MultiCrossGraphNetwork, self).__init__()

        # Save output dimensions, used to create the distributions
        self.latent_dim_pi = 314
        self.latent_dim_vf = 1024

        self.cross1 = CrossDimensionalGraphNet(VEC_FEATURE_SIZE,40,(6+15+2),20,20,20,False).to(device)
        self.cross2 = CrossDimensionalGraphNet(40,40,60,20,20,20,False).to(device)
        self.cross3 = CrossDimensionalGraphNet(40,40,60,20,20,20,True).to(device) 
        self.cross4 = CrossDimensionalGraphNet(40,40,60,20,20,20,False).to(device)
        self.cross5 = CrossDimensionalGraphNet(40,40,60,20,20,20,True).to(device)
        self.cross6 = CrossDimensionalGraphNet(40,40,60,20,20,20,False).to(device)
        self.cross7a = CrossDimensionalGraphNet(40,40,60,20,20,20,True).to(device)
        self.cross8a = CrossDimensionalGraphNet(40,VEC_ACTION_SIZE,60,1,2,1,False).to(device)
        self.cross7c = CrossDimensionalGraphNet(40,40,60,20,20,20,True).to(device)

        self.dense_critic = nn.Linear(20*(HEXTILE_NUM+VERTEXTILE_NUM+ROADTILE_NUM)+40,self.latent_dim_vf).to(device)

        self.leakyrelu = nn.LeakyReLU()
        self.tanh = nn.Tanh()
        self.flatten = nn.Flatten() 

    def forward(self, features: Dict[str, th.Tensor]) -> Tuple[th.Tensor, th.Tensor]:
        # Process 'matrix' input
        x_hex0 = features['hex']
        x_vertex0 = features["vertex"]
        x_road0 = features["road"]
        x_vec0 = features['vector'] 

        x_vec1,x_hex1,x_vertex1,x_road1 = map(self.tanh,(self.cross1(x_vec0,x_hex0,x_vertex0,x_road0)))
        x_vec2,x_hex2,x_vertex2,x_road2 = map(self.leakyrelu,(self.cross2(x_vec1,x_hex1,x_vertex1,x_road1)))
        x_vec3,x_hex3,x_vertex3,x_road3 = map(self.tanh,(self.cross3(x_vec2,x_hex2,x_vertex2,x_road2,x_hex1,x_vertex1,x_road1)))
        x_vec4,x_hex4,x_vertex4,x_road4 = map(self.leakyrelu,(self.cross4(x_vec3,x_hex3,x_vertex3,x_road3)))
        x_vec5,x_hex5,x_vertex5,x_road5 = map(self.tanh,(self.cross5(x_vec4,x_hex4,x_vertex4,x_road4,x_hex3,x_vertex3,x_road3)))
        x_vec6,x_hex6,x_vertex6,x_road6 = map(self.leakyrelu,(self.cross6(x_vec5,x_hex5,x_vertex5,x_road5)))
     
        x_vec7a,x_hex7a,x_vertex7a,x_road7a = map(self.tanh,(self.cross7a(x_vec6,x_hex6,x_vertex6,x_road6,x_hex5,x_vertex5,x_road5)))
        x_vec8a,x_hex8a,x_vertex8a,x_road8a = map(self.leakyrelu,(self.cross8a(x_vec7a,x_hex7a,x_vertex7a,x_road7a)))
        
        x_actor = th.cat((x_vec8a,self.flatten(x_hex8a),self.flatten(x_vertex8a),self.flatten(x_road8a)),dim=1)
        
        x_vec7c,x_hex7c,x_vertex7c,x_road7c = map(self.tanh,(self.cross7c(x_vec6,x_hex6,x_vertex6,x_road6,x_hex5,x_vertex5,x_road5)))
        x_critic = th.cat((x_vec7c,self.flatten(x_hex7c),self.flatten(x_vertex7c),self.flatten(x_road7c)),dim=1)
        x_critic = self.leakyrelu(self.dense_critic(x_critic))

        return x_actor,x_critic
    
    def forward_actor(self, features: th.Tensor) -> th.Tensor:
        return self.forward(features)[0]

    def forward_critic(self, features: th.Tensor) -> th.Tensor:
        return self.forward(features)[1]
    





class CrossGraphPolicy(MaskableActorCriticPolicy):

    def __init__(
        self,
        observation_space: gym.spaces.Space,
        action_space: gym.spaces.Space,
        lr_schedule: Callable[[float], float],
        net_arch: Optional[List[Union[int, Dict[str, List[int]]]]] = None,
        activation_fn: Type[nn.Module] = nn.Tanh,
        *args,
        **kwargs,
    ):
        super(CrossGraphPolicy, self).__init__(
            observation_space,
            action_space,
            lr_schedule,
            net_arch,
            activation_fn,
            *args,
            **kwargs,
        )
        # Disable orthogonal initialization
        self.ortho_init = False

    def extract_features(self,obs):
        return obs

    def _build_mlp_extractor(self) -> None:
        # Use the custom network instead of the default one
        self.mlp_extractor = MultiCrossGraphNetwork()

    def get_distribution(self, obs , action_masks: Optional[np.ndarray] = None):
        features = obs
        latent_pi = self.mlp_extractor.forward_actor(features)
        distribution = self._get_action_dist_from_latent(latent_pi)
        if action_masks is not None:
            distribution.apply_masking(action_masks)
        return distribution

    def predict_values(self, obs) -> th.Tensor:
        features = obs
        latent_vf = self.mlp_extractor.forward_critic(features)
        return self.value_net(latent_vf)