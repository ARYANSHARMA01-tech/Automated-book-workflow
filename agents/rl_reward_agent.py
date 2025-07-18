import random
import numpy as np
import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def grammar_score(text):
    matches = tool.check(text)
    return max(0, 1 - len(matches) / max(len(text.split()), 1))

def lexical_diversity(text):
    words = text.split()
    return len(set(words)) / len(words) if words else 0

def reward_function(text):
    g_score = grammar_score(text)
    l_score = lexical_diversity(text)
    return round(0.6 * g_score + 0.4 * l_score, 3)

class QLearningAgent:
    def __init__(self, actions, alpha=0.5, gamma=0.9, epsilon=0.2):
        self.q_table = {}
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            qs = [self.get_q(state, a) for a in self.actions]
            max_q = max(qs)
            return self.actions[qs.index(max_q)]

    def update(self, state, action, reward, next_state):
        old_q = self.get_q(state, action)
        max_future_q = max([self.get_q(next_state, a) for a in self.actions], default=0)
        new_q = old_q + self.alpha * (reward + self.gamma * max_future_q - old_q)
        self.q_table[(state, action)] = new_q
