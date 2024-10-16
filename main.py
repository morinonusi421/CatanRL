import numpy as np
import os
import warnings
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import gymnasium as gym
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecEnv, VecMonitor, is_vecenv_wrapped
from sb3_contrib.common.maskable.utils import get_action_masks, is_masking_supported
from sb3_contrib.ppo_mask import MaskablePPO
from stable_baselines3.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines3.common.utils import set_random_seed
from stable_baselines3.common.monitor import Monitor

from sb3_contrib.ppo_mask import MaskablePPO
#from sb3_contrib.common.maskable.callbacks import MaskableEvalCallback
from stable_baselines3.common.callbacks import EvalCallback
from sb3_contrib.common.maskable.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import sync_envs_normalization
from stable_baselines3.common import results_plotter

from CatanImplements.Environment import EnvironmentWithCNNFeature,EnvironmentWithGraphFeature
from CatanImplements.Bots import HeuristicBot
from CustomPolicies import CustomMaskableActorCriticPolicy , CrossCNNPolicy, CrossGraphPolicy


NUM_AGENTS = 16 #環境の並列数
TOTAL_TIMESTEPS = 1000000000
EVAL_FREQ = 5000
N_EVAL_EPISODES = 20 #テスト時の対戦回数
EVAL_LOG_PATH = "./cnn_eval/"
EVAL_LOG_PATH_GRAPH = "./graph_eval/"

class MaskableEvalCallback(EvalCallback):


    def __init__(self, *args, use_masking: bool = True, hande, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_masking = use_masking
        self.hande = hande
        self.stopped_early = False  # コールバックで停止したかどうかのフラグ

    def _on_step(self) -> bool:
        continue_training = True

        if self.eval_freq > 0 and self.n_calls % self.eval_freq == 0:
            self.logger.record("eval/hande", self.hande)

            # Sync training and eval env if there is VecNormalize
            if self.model.get_vec_normalize_env() is not None:
                try:
                    sync_envs_normalization(self.training_env, self.eval_env)
                except AttributeError as e:
                    raise AssertionError(
                        "Training and eval env are not wrapped the same way, "
                        "see https://stable-baselines3.readthedocs.io/en/master/guide/callbacks.html#evalcallback "
                        "and warning above."
                    ) from e

            # Reset success rate buffer
            self._is_success_buffer = []

            # Note that evaluate_policy() has been patched to support masking
            episode_rewards, episode_lengths = evaluate_policy(
                self.model,  # type: ignore[arg-type]
                self.eval_env,
                n_eval_episodes=self.n_eval_episodes,
                render=self.render,
                deterministic=self.deterministic,
                return_episode_rewards=True,
                warn=self.warn,
                callback=self._log_success_callback,
                use_masking=self.use_masking,
            )

            if self.log_path is not None:
                assert isinstance(episode_rewards, list)
                assert isinstance(episode_lengths, list)
                self.evaluations_timesteps.append(self.num_timesteps)
                self.evaluations_results.append(episode_rewards)
                self.evaluations_length.append(episode_lengths)

                kwargs = {}
                # Save success log if present
                if len(self._is_success_buffer) > 0:
                    self.evaluations_successes.append(self._is_success_buffer)
                    kwargs = dict(successes=self.evaluations_successes)

                np.savez(
                    self.log_path,
                    timesteps=self.evaluations_timesteps,
                    results=self.evaluations_results,
                    ep_lengths=self.evaluations_length,
                    **kwargs,
                )

            mean_reward, std_reward = np.mean(episode_rewards), np.std(episode_rewards)
            mean_ep_length, std_ep_length = np.mean(episode_lengths), np.std(episode_lengths)
            self.last_mean_reward = float(mean_reward)

            if self.verbose > 0:
                print(f"Eval num_timesteps={self.num_timesteps}, " f"episode_reward={mean_reward:.2f} +/- {std_reward:.2f}")
                print(f"Episode length: {mean_ep_length:.2f} +/- {std_ep_length:.2f}")
            # Add to current Logger
            self.logger.record("eval/mean_reward", float(mean_reward))
            self.logger.record("eval/mean_ep_length", mean_ep_length)

            if len(self._is_success_buffer) > 0:
                success_rate = np.mean(self._is_success_buffer)
                if self.verbose > 0:
                    print(f"Success rate: {100 * success_rate:.2f}%")
                self.logger.record("eval/success_rate", success_rate)

            # Dump log so the evaluation results are printed with the correct timestep
            self.logger.record("time/total_timesteps", self.num_timesteps, exclude="tensorboard")
            self.logger.dump(self.num_timesteps)

            if mean_reward > self.best_mean_reward:
                if self.verbose > 0:
                    print("New best mean reward!")
                if self.best_model_save_path is not None:
                    self.model.save(os.path.join(self.best_model_save_path, f"best_model_{self.hande}"))
                self.best_mean_reward = float(mean_reward)
                # Trigger callback on new best model, if needed
                if self.callback_on_new_best is not None:
                    continue_training = self.callback_on_new_best.on_step()

            # Trigger callback after every evaluation, if needed
            if self.callback is not None:
                continue_training = continue_training and self._on_event()

            #episode_wins = sum([x>0 for x in episode_rewards])
            #winrate = episode_wins / self.n_eval_episodes
            #print("勝率:",winrate)
            #if success_rate >= 0.8:
            #    self.stopped_early = True
            #    print(f"ハンデ{self.hande}の学習をアーリーストップ")
            #    continue_training = False
                

        return continue_training





def custom_evaluate_policy(
    model: MaskablePPO,
    env: Union[gym.Env, VecEnv],
    n_eval_episodes: int = 10,
    deterministic: bool = True,
    render: bool = False,
    callback: Optional[Callable[[Dict[str, Any], Dict[str, Any]], None]] = None,
    reward_threshold: Optional[float] = None,
    return_episode_rewards: bool = False,
    warn: bool = True,
    use_masking: bool = True,
) -> Union[Tuple[float, float], Tuple[List[float], List[int]]]:
   

    if use_masking and not is_masking_supported(env):
        raise ValueError("Environment does not support action masking. Consider using ActionMasker wrapper")

    is_monitor_wrapped = False

    if not isinstance(env, VecEnv):
        env = DummyVecEnv([lambda: env])  # type: ignore[list-item, return-value]

    is_monitor_wrapped = is_vecenv_wrapped(env, VecMonitor) or env.env_is_wrapped(Monitor)[0]

    if not is_monitor_wrapped and warn:
        warnings.warn(
            "Evaluation environment is not wrapped with a ``Monitor`` wrapper. "
            "This may result in reporting modified episode lengths and rewards, if other wrappers happen to modify these. "
            "Consider wrapping environment first with ``Monitor`` wrapper.",
            UserWarning,
        )

    n_envs = env.num_envs
    episode_rewards = []
    episode_lengths = []
    success_count = 0

    episode_counts = np.zeros(n_envs, dtype="int")
    # Divides episodes among different sub environments in the vector as evenly as possible
    episode_count_targets = np.array([(n_eval_episodes + i) // n_envs for i in range(n_envs)], dtype="int")

    current_rewards = np.zeros(n_envs)
    current_lengths = np.zeros(n_envs, dtype="int")
    observations = env.reset()
    states = None
    episode_starts = np.ones((env.num_envs,), dtype=bool)
    while (episode_counts < episode_count_targets).any():
        if use_masking:
            action_masks = get_action_masks(env)
            actions, state = model.predict(
                observations,  # type: ignore[arg-type]
                state=states,
                episode_start=episode_starts,
                deterministic=deterministic,
                action_masks=action_masks,
            )
        else:
            actions, states = model.predict(
                observations,  # type: ignore[arg-type]
                state=states,
                episode_start=episode_starts,
                deterministic=deterministic,
            )
        observations, rewards, dones, infos = env.step(actions)
        current_rewards += rewards
        current_lengths += 1
        for i in range(n_envs):
            if episode_counts[i] < episode_count_targets[i]:
                # unpack values so that the callback can access the local variables
                reward = rewards[i]
                done = dones[i]
                info = infos[i]
                episode_starts[i] = done
                if "is_success" in info:
                    if info["is_success"]:
                        success_count += 1

                if callback is not None:
                    callback(locals(), globals())

                if dones[i]:
                    if is_monitor_wrapped:
                        # Atari wrapper can send a "done" signal when
                        # the agent loses a life, but it does not correspond
                        # to the true end of episode
                        if "episode" in info.keys():
                            # Do not trust "done" with episode endings.
                            # Monitor wrapper includes "episode" key in info if environment
                            # has been wrapped with it. Use those rewards instead.
                            episode_rewards.append(info["episode"]["r"])
                            episode_lengths.append(info["episode"]["l"])
                            # Only increment at the real end of an episode
                            episode_counts[i] += 1
                    else:
                        episode_rewards.append(current_rewards[i])
                        episode_lengths.append(current_lengths[i])
                        episode_counts[i] += 1
                    current_rewards[i] = 0
                    current_lengths[i] = 0

        if render:
            env.render()

    mean_reward = np.mean(episode_rewards)
    std_reward = np.std(episode_rewards)
    if reward_threshold is not None:
        assert mean_reward > reward_threshold, "Mean reward below threshold: " f"{mean_reward:.2f} < {reward_threshold:.2f}"
    if return_episode_rewards:
        return episode_rewards, episode_lengths
    return mean_reward, std_reward, success_count





def make_env(rank: int, hande, seed: int = 0):
    def _init():
        env = EnvironmentWithCNNFeature(opponetAgent=HeuristicBot(cnn_or_graph="cnn"),hande=hande)
        env = Monitor(env)
        env.reset(seed=seed + rank)
        return env
    set_random_seed(seed)
    return _init

def make_env_graph(rank: int, hande, seed: int = 0):
    def _init():
        env = EnvironmentWithGraphFeature(opponetAgent=HeuristicBot(cnn_or_graph="graph"),hande=hande)
        env = Monitor(env)
        env.reset(seed=seed + rank)
        return env
    set_random_seed(seed)
    return _init

def eval_cnn(N):

    env = EnvironmentWithCNNFeature(opponetAgent=HeuristicBot(cnn_or_graph="cnn"),hande=0)
    model = MaskablePPO(CrossCNNPolicy, env, verbose=1,)
    model.set_parameters(os.path.join(EVAL_LOG_PATH, f"best_model_0.zip"))

    mean_reward, std_reward, success_count = custom_evaluate_policy(model,env,N,use_masking=True)
    print(f"CNN{N}戦,報酬，分散，勝ち回数")
    print(mean_reward, std_reward, success_count)

def eval_graph(N):

    env = EnvironmentWithGraphFeature(opponetAgent=HeuristicBot(cnn_or_graph="graph"),hande=0)
    model = MaskablePPO(CrossGraphPolicy, env, verbose=1,)
    model.set_parameters(os.path.join(EVAL_LOG_PATH_GRAPH, f"best_model_0.zip"))

    mean_reward, std_reward, success_count = custom_evaluate_policy(model,env,N,use_masking=True)
    print(f"GCN{N}戦,報酬，分散，勝ち回数")
    print(mean_reward, std_reward, success_count)






def main_cnn():

    os.makedirs(EVAL_LOG_PATH, exist_ok=True)

    hande = 8
    # 並列環境を作成
    env = DummyVecEnv([make_env(i,hande) for i in range(NUM_AGENTS)])
    #モデルを作成
    model = MaskablePPO(CrossCNNPolicy, env, verbose=1,tensorboard_log=f"./hande{hande}_tensorboard/")
    #model = MaskablePPO(CustomMaskableActorCriticPolicy, env, verbose=1)

    eval_env = DummyVecEnv([make_env(0,hande)])

    eval_callback = MaskableEvalCallback(
        eval_env,
        best_model_save_path=EVAL_LOG_PATH,
        log_path=EVAL_LOG_PATH,
        eval_freq=EVAL_FREQ,  
        deterministic=True,
        render=False,
        n_eval_episodes=N_EVAL_EPISODES,
        verbose = 0,
        hande = hande
    )

    while(True):
            
        model.learn(total_timesteps=TOTAL_TIMESTEPS, callback=eval_callback)

        #通常終了ではなく，勝率が一定を超えて終了した場合
        if eval_callback.stopped_early:

            #　ハンデを下げる
            hande -= 1

            eval_env = DummyVecEnv([make_env(0,hande)])

            eval_callback = MaskableEvalCallback(
                eval_env,
                best_model_save_path=EVAL_LOG_PATH,
                log_path=EVAL_LOG_PATH,
                eval_freq=EVAL_FREQ,  
                deterministic=True,
                render=False,
                n_eval_episodes=N_EVAL_EPISODES,
                verbose = 0,
                hande = hande
            )

            # 新しいハンデで並列環境を作成
            env = DummyVecEnv([make_env(i,hande) for i in range(NUM_AGENTS)])
            #　新しいハンデようのモデルを作成
            model = MaskablePPO(CrossCNNPolicy, env, verbose=1)
            #model = MaskablePPO(CustomMaskableActorCriticPolicy, env, verbose=1)
            # 前のハンデでの重みを読み込む
            model.set_parameters(os.path.join(EVAL_LOG_PATH, f"best_model_{hande+1}.zip"))



def main_graph():
            
    os.makedirs(EVAL_LOG_PATH_GRAPH, exist_ok=True)

    hande = 0
    # 並列環境を作成
    env = DummyVecEnv([make_env_graph(i,0) for i in range(NUM_AGENTS)])
    #モデルを作成
    model = MaskablePPO(CrossGraphPolicy, env, verbose=1,tensorboard_log="./tensorboard/")

    #前回の続きから始める
    model = MaskablePPO.load(f"{EVAL_LOG_PATH_GRAPH}/best_model_0", env=env)

    eval_env = DummyVecEnv([make_env_graph(0,hande)])

    eval_callback = MaskableEvalCallback(
        eval_env,
        best_model_save_path=EVAL_LOG_PATH_GRAPH,
        log_path=EVAL_LOG_PATH_GRAPH,
        eval_freq=EVAL_FREQ, 
        deterministic=True,
        render=False,
        n_eval_episodes=N_EVAL_EPISODES,
        verbose = 0,
        hande = hande
    )

    model.learn(total_timesteps=TOTAL_TIMESTEPS, callback=eval_callback,tb_log_name="PPO_2", reset_num_timesteps=False)
    


if __name__ == "__main__":
    print("cn")
    eval_cnn(300)
    #main_graph()