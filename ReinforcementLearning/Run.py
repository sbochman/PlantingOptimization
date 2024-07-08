from Agent.Agent import Agent
from Environment.Grid import Grid
import numpy as np
import tensorflow
tensorflow.keras.utils.disable_interactive_logging()

env = Grid(2, 6)  # Example dimensions
n_games = 100
agent = Agent(gamma=0.99, epsilon=1, eps_dec=1e-2, eps_min=0.01, lr=1e-4, input_dims=env.state.shape, mem_size=1000000, batch_size=32, num_tree_types=22)
scores = []


for i in range(n_games):  # Number of episodes
    done = False
    observation = env.reset()
    score = 0
    while not done:
        for x in range(env.x):
            for y in range(env.y):
                action = agent.choose_action(observation, x, y, env.cost_remaining)
                observation_, reward, done = env.step(action, x, y)
                observation = observation_
                if env.cost_remaining < 0:
                    done = True
                    reward = -250
                score += reward
                agent.store_transition(observation, action, reward, observation_, done, (x, y), env.cost_remaining)
                if done: break
            if done: break

    agent.learn()
    scores.append(score)
    print(f'Episode {i}, Score: {score}, Last 100 Avg: {np.mean(scores[-100:])} Epsilon: {agent.epsilon}')

# Assuming env has a method to render the final state
env.render()

print("Q_eval: ", agent.eval)
print("Q_next: ", agent.next)
print("Q_target: ", agent.target)

# Iterate over the layers of the model

