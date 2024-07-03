import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Dense
from tensorflow.keras.models import Model
import numpy as np
from Agent.ReplayBuffer import ReplayBuffer


class Agent():
    def __init__(self, gamma, epsilon, eps_min, eps_dec, lr, input_dims, mem_size, batch_size, num_tree_types=22):
        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.batch_size = batch_size
        self.eps_min = eps_min
        self.eps_dec = eps_dec
        self.q_eval = self.build_dqn(input_dims, num_tree_types)
        self.memory = ReplayBuffer(mem_size, input_dims)


    def build_dqn(self, input_dims, num_tree_types):
        input_layer = Input(shape=input_dims)
        x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
        x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        output_layer = Conv2D(num_tree_types, (1, 1), activation='softmax', padding='same')(x)
        model = Model(inputs=input_layer, outputs=output_layer)
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return model

    def store_transition(self, state, action, reward, new_state, done):
        self.memory.store_transition(state, action, reward, new_state, done)

    def choose_action(self, state, x, y):
        if np.random.random() < self.epsilon:
            action = np.random.randint(0, 22)  # Choose from number of tree types
        else:
            state = np.expand_dims(state, axis=0)
            action_probs = self.q_eval.predict(state)
            action = np.argmax(action_probs[0, x, y])
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
