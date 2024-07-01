import tensorflow
from tensorflow import keras
import numpy as np
from Agent.ReplayBuffer import ReplayBuffer

def build_dqn(lr, input_dims, n_actions, fc1_dims, fc2_dims, dropout=0.2):
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=input_dims),  # Flatten if input_dims is a matrix
        keras.layers.Dense(fc1_dims, activation='relu'),
        keras.layers.Dropout(dropout),
        keras.layers.Dense(fc2_dims, activation='relu'),
        keras.layers.Dropout(dropout),
        keras.layers.Dense(n_actions, activation='linear')  # Adjust n_actions based on your action space
    ])

    # Model compilation
    model.compile(optimizer=keras.optimizers.Adam(learning_rate=lr), loss='mse')

    return model

class Agent():
    def __init__(self, lr, gamma, n_actions, epsilon, batch_size, input_dims,
                 epsilon_dec=1e-4, epsilon_end=0.01, mem_size=1000000,
                 filename='dqn_model.h5'):
        self.action_space = [i for i in range(n_actions)]
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = filename
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(lr, input_dims, n_actions, 256, 256)

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, state):
        if np.random.random() > self.epsilon:
            state = np.array([state])
            actions = self.q_eval.predict(state)
            action = np.argmax(actions)
        else:
            action = np.random.choice(self.action_space)

        return self.decode_action(action, 6, 22)

    def learn(self):
        if self.memory.mem_counter < self.batch_size:
            return

        states, actions, rewards, states_, dones = self.memory.sample_buffer(self.batch_size)

        q_eval = self.q_eval.predict(states)
        q_next = self.q_eval.predict(states_)

        action_indices = np.array([self.action_index(action[0], action[1], action[2], max_y=6, max_tree_type=22) for action in actions])

        q_target = np.copy(q_eval)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        q_target[batch_index, action_indices] = rewards + self.gamma * np.max(q_next, axis=1) * dones

        self.q_eval.train_on_batch(states, q_target)


        if self.epsilon > self.eps_min:
            self.epsilon *= self.eps_dec


        #self.epsilon = self.epsilon - self.eps_dec if self.epsilon > self.eps_min else self.eps_min

    def decode_action(self, action, y_size, num_tree_types):
        x = action // (y_size * num_tree_types)
        action -= x * y_size * num_tree_types
        y = action // num_tree_types
        tree_type = action % num_tree_types
        return x, y, tree_type

    def action_index(self, x, y, tree_type, max_y, max_tree_type):
        return x * max_y * max_tree_type + y * max_tree_type + tree_type

    def get_q_values(self, state):
        state = np.array([state])  # Reshape appropriately if needed
        return self.q_eval.predict(state)[0]  # Assuming using Keras/TensorFlow
