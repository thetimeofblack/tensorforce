# Copyright 2016 reinforce.io. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""
Implements normalized advantage functions as described here:
https://arxiv.org/abs/1603.00748
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import tensorflow as tf

from tensorforce.neural_networks.layers import dense
from tensorforce.neural_networks.neural_network import get_network
from tensorforce.value_functions.value_function import ValueFunction


class NormalizedAdvantageFunctions(ValueFunction):
    default_config = {
        'tau': 0,
        'epsilon': 0.1,
        'gamma': 0,
        'alpha': 0.5,
        'clip_gradients': False
    }

    def __init__(self, config):
        """
        Training logic for NAFs.

        :param config: Configuration parameters
        """
        super(NormalizedAdvantageFunctions, self).__init__(config)
        self.config = config
        self.state = tf.placeholder(tf.float32, [None] + list(self.config.state_shape), name="state")
        self.next_states = tf.placeholder(tf.float32, [None] + list(self.config.state_shape), name="next_states")
        self.actions = tf.placeholder(tf.int64, [None], name='actions')
        self.terminals = tf.placeholder(tf.float32, [None], name='terminals')
        self.rewards = tf.placeholder(tf.float32, [None], name='rewards')
        self.target_network_update = []
        self.step = 0

        # get hidden layers from network generator, then add NAF outputs, same for target network
        self.create_outputs(get_network(self.config.network_layers, self.state, 'training'))

    def get_noise(self, step):
        return 0

    def get_action(self, state):
        action = self.mu, {self.state: [state]}[0]

        return action + self.get_noise(self.step)

    def update(self, batch):
        pass

    def create_outputs(self, hidden_layers):
        """
        Creates NAF specific outputs.
        :param hidden_layers: Points to last hidden layer
        """

        # State-value function
        self.v = dense(hidden_layers, {'neurons': 1, 'regularization': self.config['regularizer'],
                                       'regularization_param': self.config['regularization_param']}, 'v')

        # Action outputs
        self.mu = dense(hidden_layers, {'neurons': self.config['actions'], 'regularization': self.config['regularizer'],
                                        'regularization_param': self.config['regularization_param']}, 'v')

        # Advantage computation
        # Network outputs entries of lower triangular matrix L
        lower_triangular_size = self.config['actions'] * (self.config['actions'] + 1) / 2
        self.l_entries = dense(hidden_layers, {'neurons': lower_triangular_size,
                                               'regularization': self.config['regularizer'],
                                               'regularization_param': self.config['regularization_param']}, 'v')

        # Construct matrix P
        batch_size = self.config['batch_size']

        # TODO figure out tensor shapes

        #action_difference =
        self.advantage = -tf.batch_matmul()
        self.q_value = self.v + self.advantage


        def create_training_operations(self):
            """
            NAF training logic.
            """

            pass
