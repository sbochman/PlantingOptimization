import seaborn as sns

from Environment.Grid import Grid
import numpy as np
import tensorflow as tf
from Agent.Agent import Agent
import matplotlib.pyplot as plt

tf.compat.v1.disable_eager_execution()
env = Grid(3, 6)
n_games = 1000
action_space = 6     # env.x * env.y #* len(env.tree_types_dict)
lr = 1e-5



agent = Agent(gamma=0.95, epsilon=1, lr=lr, input_dims=env.state.shape, mem_size=1000000,
              batch_size=32)
scores, eps_history = [], []

for i in range(n_games):
    done = False
    score = 0
    observation = env.reset()
    num_invalid = 0
    num_valid = 0
    num_actions = 0

   # for x in range(env.x):
   #     for y in range(env.y):
    observation = env.get_state()
    action = agent.choose_action(observation)

    observation_, reward, done = env.step(action) #change back to action
    score += reward

    agent.store_transition(observation, action, reward, observation_, done)
    observation = observation_
    #agent.learn()
    num_actions += 1

    agent.learn()
    scores.append(score)
    eps_history.append(agent.epsilon)
    avg_score = np.mean(scores[-100:])
    print(f'episode: {i}, score: {score}, last 100 average score: {avg_score}, invalid actions: {num_invalid}, valid actions: {num_valid} epsilon: {agent.epsilon}')

env.render()