import gymnasium as gym
import numpy as np
from gymnasium import spaces

# Custom Environment class (Your code)
class CustomEnv(gym.Env):
    def __init__(self):
        super().__init__()
        
        # Observation space definition
        self.observation_space = spaces.Dict({
            "matrix": spaces.Box(low=0, high=1, shape=(4, 2), dtype=np.float32),  # 4x2 matrix
            "scalar": spaces.Box(low=0, high=10, shape=(1,), dtype=np.float32)    # Scalar value (0 to 10)
        })

        # Action space definition
        self.action_space = spaces.Discrete(3)  # 3 discrete actions
        self.turn = 0

    def reset(self, seed=0):
        observation = {
            "matrix": np.zeros((4, 2), dtype=np.float32),
            "scalar": np.array([0.0], dtype=np.float32)
        }
        info = {}
        self.turn = 0
        return observation, info

    def step(self, action):

        if action == 1:
           print("1エラー")
           exit()
           
        if action == 0:
            reward = 1
        else:
            reward = -1

        self.turn += 1
        next_observation = {
            "matrix": np.random.rand(4, 2).astype(np.float32),
            "scalar": np.random.rand(1).astype(np.float32) * 10
        }

        terminated = False
        truncated = False
        info = {}

        if self.turn == 100:
            terminated = True

        return next_observation, reward, terminated, truncated, info

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def action_masks(self):
        return [True,False,True]

if __name__ == "__main__":
    env = CustomEnv()
    from stable_baselines3.common.env_checker import check_env
    check_env(env)