import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Dense
from tensorflow.keras.models import Model
import numpy as np
from Agent.ReplayBuffer import ReplayBuffer

def build_dqn(grid_size, num_features, num_tree_types):
    input_layer = Input(shape=(grid_size[0], grid_size[1], num_features))
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    output_layer = Conv2D(num_tree_types, (1, 1), activation='softmax', padding='same')(x)

    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(optimizer='adam', loss='categorical_crossentropy')
    return model

class Agent():
    def __init__(self, lr, gamma, epsilon, batch_size, input_dims, epsilon_dec=1e-3, epsilon_end=0.01, mem_size=1000000, filename='dqn_model.h5'):
        self.gamma = gamma
        self.epsilon = epsilon
        self.eps_dec = epsilon_dec
        self.eps_min = epsilon_end
        self.batch_size = batch_size
        self.model_file = filename
        self.memory = ReplayBuffer(mem_size, input_dims)
        self.q_eval = build_dqn(input_dims[0:2], input_dims[2], num_tree_types=6)  # Specify the number of tree types

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            # Random action selection by randomly choosing a tree type for each cell
            action = np.random.randint(0, 5, size=(state.shape[0], state.shape[1]))
        else:
            state = np.expand_dims(state, axis=0)  # Add batch dimension
            action_probs = self.q_eval.predict(state)
            action = np.argmax(action_probs, axis=-1)  # Choose the most likely tree type for each cell
            action = action[0]
        return action

    def learn(self):
        if self.memory.mem_counter < self.batch_size:
            return

        states, actions, rewards, states_, dones = self.memory.sample_buffer(self.batch_size)

        q_eval = self.q_eval.predict(states)
        q_next = self.q_eval.predict(states_)

        q_target = np.copy(q_eval)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        # Update rule needs to consider that each cell has its own action and reward
        for idx, (reward, done, action) in enumerate(zip(rewards, dones, actions)):
            q_target[idx, :, :, action] = reward + self.gamma * np.max(q_next[idx], axis=-1) * (1 - done)

        self.q_eval.train_on_batch(states, q_target)

        self.epsilon = max(self.epsilon - self.eps_dec, self.eps_min)
