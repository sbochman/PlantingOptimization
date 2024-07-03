from Agent.Agent import Agent
from Environment.Grid import Grid
import numpy as np

env = Grid(5, 6)  # Example dimensions
n_games = 1000
agent = Agent(gamma=0.95, epsilon=1, eps_dec = 1e-3, eps_min=0.01, lr=1e-5, input_dims=env.state.shape, mem_size=1000000, batch_size=32, num_tree_types=22)
scores = []

for i in range(n_games):
    done = False
    score = 0
    observation = env.reset()
    for x in range(env.x):  # Assuming env.x and env.y define grid dimensions
        for y in range(env.y):
            action = agent.choose_action(observation, x, y)
            observation_, reward, done = env.step(action, x, y)
            agent.store_transition(observation, action, reward, observation_, done)
            score += reward

    agent.learn()
    scores.append(score)
    avg_score = np.mean(scores[-100:])
    print(f'episode: {i}, score: {score}, last 100 average score: {avg_score}, epsilon: {agent.epsilon}')

# Assuming env has a method to render the final state
env.render()
