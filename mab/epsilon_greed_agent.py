import numpy as np

class EpsGreedyAgent(object):
    def __init__(self, prob_list):
        self.prob_list = prob_list

    def pull(self, bandit_machine):
        if np.random.random() < self.prob_list[bandit_machine]:
            reward = 1
        else:
            reward = 0

        return reward


# probabilidade de ter um resultado positivo da página
prob_list = [0.25, 0.30]

# parametros do experimento
trials = 1000
episodes = 200

# agent
bandit = EpsGreedyAgent(prob_list)

prob_reward_array = np.zeros(len(prob_list))
accumulated_reward_array = list()
avg_accumulated_reward_array = list()
eps_init = 1
decay = 0.055

# valores de decaimento de epsilon
eps_array = [(eps_init*(1-decay))**i for i in range(trials)]
#eps = (1-decay) + (decay/2)

for episode in range(episodes):
    reward_array = np.zeros(len(prob_list))
    bandit_array = np.full(len(prob_list), 1.0e-5)
    accumulated_reward = 0

    for trial in range(trials):
        # agent - escolha

        if eps_array[trial] >= np.random.random(): # balanco entre exploration / exploitation
            bandit_machine = np.random.randint(low=0, high=2, size=1)[0]
        else:
            # fase de exploitation
            prob_reward = reward_array/bandit_array
            max_prob_reward = np.where(prob_reward == np.max(prob_reward))[0]
            bandit_machine = max_prob_reward[0]

        # agent - recompensa
        reward = bandit.pull(bandit_machine)

        # agent - guarda recompensa
        reward_array[bandit_machine] += reward
        bandit_array[bandit_machine] += 1
        accumulated_reward += reward
    
    prob_reward_array += reward_array/bandit_array
    accumulated_reward_array.append(accumulated_reward)
    avg_accumulated_reward_array.append(np.mean(accumulated_reward_array))

prob01 = np.round(prob_reward_array[0]/episodes, 2)
prob02 = np.round(prob_reward_array[1]/episodes, 2)


print(f'\nProb Bandit 01: {prob01}% - Prob Bandit 02 {prob02}%')
print(f'\nAvg accumulated reward: {np.mean(avg_accumulated_reward_array)}')