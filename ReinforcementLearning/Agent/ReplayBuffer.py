import numpy as np

class ReplayBuffer():
    def __init__(self, max_size, input_dims):
        self.mem_size = max_size
        self.mem_counter = 0

        self.state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.new_state_memory = np.zeros((self.mem_size, *input_dims), dtype=np.float32)
        self.action_memory = np.zeros((self.mem_size, 30), dtype=np.int32) #was 3
        self.coords_memory = np.zeros((self.mem_size, 2), dtype=np.int32)
        self.cost_remaining_memory = np.zeros(self.mem_size, dtype=np.float32)
        #self.tree_stats_memory = np.zeros((self.mem_size, 44), dtype=np.float32)

        self.reward_memory = np.zeros(self.mem_size, dtype=np.float32)
        self.terminal_memory = np.zeros(self.mem_size, dtype=np.int32) #maybe dtype=bool_

    def store_transition(self, state, action, reward, new_state, done, coords, cost_remaining):
        index = self.mem_counter % self.mem_size
        # Flatten the action array before storing if necessary
        #flattened_action = action.flatten()
        self.action_memory[index] = action
        self.state_memory[index] = state
        self.reward_memory[index] = reward
        self.new_state_memory[index] = new_state
        self.terminal_memory[index] = done
        self.coords_memory[index] = coords
        self.cost_remaining_memory[index] = cost_remaining
        #self.tree_stats_memory[index] = tree_stats.reshape(-1)
        self.mem_counter += 1


    def sample_buffer(self, batch_size):
        max_mem = min(self.mem_counter, self.mem_size)
        batch = np.random.choice(max_mem, batch_size, replace=False)

        states = self.state_memory[batch]
        actions = self.action_memory[batch]
        rewards = self.reward_memory[batch]
        states_ = self.new_state_memory[batch]
        terminal = self.terminal_memory[batch]
        coords = self.coords_memory[batch]
        cost_remaining = self.cost_remaining_memory[batch]
        #tree_stats = self.tree_stats_memory[batch]

        return states, actions, rewards, states_, terminal, coords, cost_remaining
