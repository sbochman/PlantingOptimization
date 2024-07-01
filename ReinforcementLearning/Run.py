import seaborn as sns

from Environment.Grid import Grid
import numpy as np
import tensorflow as tf
from Agent.Agent import Agent
import matplotlib.pyplot as plt



tf.compat.v1.disable_eager_execution()
env = Grid(5, 6)
n_games = 500
action_space = env.x * env.y * len(env.tree_types_dict)
lr = 1e-5
agent = Agent(gamma=0.99, epsilon=0.995, lr=lr, input_dims=env.numericalGrid.shape, n_actions=action_space, mem_size=1000000,
              batch_size=64)
scores, eps_history, q_values_map = [], [], []

for i in range(n_games):
    done = False
    score = 0
    env.reset()
    observation = env.get_state()
    episode_q_values = []
    num_invalid = 0
    num_valid = 0
    while not done:
        action = agent.choose_action(observation)
        observation_, reward, done = env.step(action)
        if reward == -10: num_invalid += 1
        else: num_valid += 1
        score += reward
        q_values = agent.get_q_values(observation)
        episode_q_values.append(q_values)
        agent.store_transition(observation, action, reward, observation_, done)
        observation = observation_
        agent.learn()

    q_values_map.append(episode_q_values)
    scores.append(score)
    eps_history.append(agent.epsilon)
    avg_score = np.mean(scores[-100:])
    print(f'episode: {i}, score: {score}, last 100 average score: {avg_score}, invalid actions: {num_invalid}, valid actions: {num_valid} epsilon: {agent.epsilon}')

env.render()

# Average Q-values across episodes
average_q_values = np.mean(q_values_map, axis=0)

# Assuming the environment has a grid-like structure # You need to define this based on your environment
#num_actions = env.num_actions  # This should match your environment's action space

#print("Shape of average_q_values:", average_q_values.shape)

'''
grid_x, grid_y = 5, 6  # grid size
num_tree_types = 22   # number of tree types

# Initialize an array to hold the average Q-values for visualization
q_values_grid = np.zeros((grid_x, grid_y))

# Map each action to a grid cell and average across 'episodes'
for action in range(660):
    x = action // (grid_y * num_tree_types)
    y = (action // num_tree_types) % grid_y
    # Average Q-values across whatever the dimension of average_q_values signifies (e.g., episodes or states)
    q_values_grid[x, y] = np.mean(average_q_values[:, action])

    # Plot the heatmap for this configuration if needed for every tree type or just once per (x, y)
    if action % num_tree_types == 0:  # This could be adjusted based on how you want to trigger plotting
        plt.figure(figsize=(10, 8))
        plt.title(f"Heatmap for Grid Position ({x}, {y}) Over All Tree Types")
        sns.heatmap(q_values_grid, annot=True, fmt=".2f", cmap="coolwarm")
        plt.show()
'''





"""

env = Grid(5, 6)
agent = DQNAgent(gamma=0.99, epsilon=1.0, lr=1e-5, input_dims=(env.x, env.y, len(env.tree_types_dict)), batch_size=32, n_actions=env.x * env.y * len(env.tree_types_dict))
scores, eps_history = [], []
n_games = 500

for i in range(n_games):
    score = 0
    done = False
    env.reset()
    observation = env.get_state()
    while not done:
        action = agent.choose_action(observation)
        observation_, reward, done = env.step(decode_action(action, env.y, len(env.tree_types_dict)))
        score += reward
        agent.store_transition(observation, action, reward, observation_, done)
        agent.learn()
        observation = observation_
    scores.append(score)
    eps_history.append(agent.epsilon)

    avg_score = np.mean(scores[-100:])
    print(f'episode: {i}, score: {score}, last 100 average score: {avg_score}, epsilon: {agent.epsilon}')


env.render()

"""










#def select_action(state_tensor, model, epsilon, y_size, num_tree_types):
# print("Shape entering select_action:", state_tensor.shape)  # Verify shape at function entry
#  if random.random() < epsilon:
#      action = random.choice([(x, y, tree_type)
#                               for x in range(env.x)
#                               for y in range(env.y)
#                               for tree_type in range(num_tree_types)])
# print("Random action selected:", action)
#        return action
#    else:
#        try:
#        q_values = model(state_tensor)
# print("Q-values shape from model:", q_values.shape)  # Check output shape
#          best_action = q_values.argmax().item()
#          decoded_action = decode_action(best_action, y_size, num_tree_types)
#print("Decoded action from Q-values:", decoded_action)
#            return decoded_action
#       except Exception as e:
#print("Error in model prediction within select_action:", str(e))
# Fallback to a random action if there's an error
#           print('here')
#           return random.choice([(x, y, tree_type)
#                                 for x in range(env.x)
#                                  for y in range(env.y)
#                                  for tree_type in range(num_tree_types)])

# Parameters
"""
num_episodes = 500
gamma = 0.99
epsilon_start = 1.0
epsilon_min = 0.01
epsilon_decay = 0.9995
learning_rate = 1e-5

env = Grid(5, 6)
input_dim = (3, env.x, env.y)  # 3 channels: Plantable grid, tree grid, reward grid
num_tree_types = len(env.tree_types_dict)
n_actions = env.x * env.y * num_tree_types

model = DQN(3, env.x, env.y, n_actions)
optimizer = optim.Adam(model.parameters(), lr=learning_rate)
criterion = nn.MSELoss()

epsilon = epsilon_start
for episode in range(num_episodes):
    env.reset()
    state = env.get_state()  # This must return a numpy array or a list of lists with shape (5, 6, 3)
    total_reward = 0
    done = False

    while not done:
        # Prepare state_tensor for CNN input
        state_tensor = torch.tensor(state, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)

        # Call select_action and pass the state_tensor
        action = select_action(state_tensor, model, epsilon, env.y, num_tree_types)
        reward, done = env.step(action)
        next_state = env.get_state()

        next_state_tensor = torch.tensor(next_state, dtype=torch.float32).permute(2, 0, 1).unsqueeze(0)

        target = reward + gamma * torch.max(model(next_state_tensor)).item()
        target_f = model(state_tensor).detach()
        action_index = encode_action(*action, env.y, num_tree_types)
        target_f[0, action_index] = target

        optimizer.zero_grad()
        outputs = model(state_tensor)
        loss = criterion(outputs, target_f)
        loss.backward()
        optimizer.step()

        state = next_state
        total_reward += reward

        epsilon = max(epsilon_min, epsilon * epsilon_decay)
    print(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {epsilon}")


    if episode % 20 == 0: env.render()

"""