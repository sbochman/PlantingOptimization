import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, Dense
from tensorflow.keras.layers import Concatenate, Embedding, Flatten
from tensorflow.keras.models import Model
import tensorflow.keras as keras
import numpy as np
from Agent.ReplayBuffer import ReplayBuffer
tf.random.set_seed(100)
np.random.seed(100)


class Agent():
    def __init__(self, gamma, epsilon, eps_min, eps_dec, lr, input_dims, mem_size, batch_size, num_tree_types=22):
        self.gamma = gamma
        self.epsilon = epsilon
        self.lr = lr
        self.batch_size = batch_size
        self.eps_min = eps_min
        self.eps_dec = eps_dec
        #self.x = input_dims[0]
        #self.y = input_dims[1]
        self.q_eval = self.build_dqn(input_dims, num_tree_types)
        self.memory = ReplayBuffer(mem_size, input_dims)

        self.eval = []
        self.next = []
        self.target = []



    def build_dqn(self, input_dims, num_tree_types):
        # Inputs
        input_layer = Input(shape=input_dims)  # State of the entire grid
        coord_input = Input(shape=(2,))  # Current cell coordinates
        cost_remaining_input = Input(shape=(1,))  # Remaining budget

        # Convolutional layers to process the grid
        x = Conv2D(32, (3, 3), activation='relu', padding='same')(input_layer)
        x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
        x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
        x = Flatten()(x)

        # Flatten the additional inputs
        coord_flat = Flatten()(coord_input)
        cost_remaining_flat = Flatten()(cost_remaining_input)

        # Combine all inputs
        combined = Concatenate()([x, coord_flat, cost_remaining_flat])

        # Dense layers for final decision making
        x = Dense(256, activation='relu')(combined)
        x = Dense(128, activation='relu')(x)
        x = keras.layers.Dropout(0.3)(x)
        x = Dense(64, activation='tanh')(x)
        output_layer = Dense(num_tree_types, activation='softmax')(x)  # Output the tree type for the current cell

        # Model compilation
        model = Model(inputs=[input_layer, coord_input, cost_remaining_input], outputs=output_layer)
        model.compile(optimizer='adam', loss='categorical_crossentropy')
        return model


    def store_transition(self, state, action, reward, new_state, done, coords, cost_remaining):
        self.memory.store_transition(state, action, reward, new_state, done, coords, cost_remaining)

    def choose_action(self, state, x, y, cost_remaining):
        if np.random.random() < self.epsilon:
            action = np.random.randint(0, 22)  # Choose from number of tree types
        else:
            state = np.expand_dims(state, axis=0)
            coords = np.array([[x, y]])
            cost_remaining = np.array([[cost_remaining]])
            #tree_stats = np.array([tree_stats])
            action_probs = self.q_eval.predict([state, coords, cost_remaining])
            action = np.argmax(action_probs)
        return action

    def learn(self):
        if self.memory.mem_counter < self.batch_size:
            return

        states, actions, rewards, states_, dones, coords, cost_remaining = self.memory.sample_buffer(self.batch_size)

        cost_remaining = cost_remaining.reshape(-1, 1)
        #tree_stats = tree_stats.reshape(-1, 22, 2)

        q_eval = self.q_eval.predict([states, coords, cost_remaining])
        q_next = self.q_eval.predict([states_, coords, cost_remaining])

        q_target = np.copy(q_eval)
        batch_index = np.arange(self.batch_size, dtype=np.int32)

        # Update rule needs to consider that each cell has its own action and reward

        for idx, (reward, done, action) in enumerate(zip(rewards, dones, actions)):
            q_target[idx][action] = reward + self.gamma * np.max(q_next[idx]) * (1 - done)

        #for idx, (reward, done, action, coord, cost_remaining) in enumerate(zip(rewards, dones, actions, coords, cost_remaining)):
            #selected_action_q_value = q_next[idx].reshape(-1)[action]  # Flatten and select the action's Q-value
           # selected_action_q_value = np.max(q_next[idx])
            #q_target[idx].reshape(-1)[action] = reward + self.gamma * selected_action_q_value * (1 - done)
           # q_target[idx][action] = reward + self.gamma * selected_action_q_value * (1 - done)

        #print(f"Q_eval: {q_eval}")
        #print(f"Q_next: {q_next}")
        #print(f"Q_target: {q_target}")

        self.q_eval.train_on_batch([states,coords, cost_remaining], q_target)

        self.epsilon = max(self.epsilon - self.eps_dec, self.eps_min)

        self.eval = q_eval
        self.next = q_next
        self.target = q_target
