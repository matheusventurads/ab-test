import numpy as np

class GreedyAgent(object):
    def __init__(self, prob_list):
        self.prob_list = prob_list

    def pull(self, bandit_machine):
        if np.random.random() < self.prob_list[bandit_machine]:
            reward = 1
        else:
            reward = 0

        return reward


# probabilidade de ter um resultado positivo da página
prob_list = [0.25, 0.33]

# parametros do experimento
trials = 1000
episodes = 200

# agent
bandit = GreedyAgent(prob_list)

prob_reward_array = np.zeros(len(prob_list))
accumulated_reward_array = list()
avg_accumulated_reward_array = list()
eps_init = 0

for episode in range(episodes):
    reward_array = np.zeros(len(prob_list))
    bandit_array = np.full(len(prob_list), 1.0e-5)
    accumulated_reward = 0

    for trial in range(trials):
        # agent - escolha
        if eps_init == 0: # exploracao - escolhendo a primeira pagina
            bandit_machine = 0 # pagina A
        elif eps_init == 1:
            bandit_machine = 1 # pagina B
        elif eps_init == 2:
            prob_reward = reward_array/bandit_array
            max_prob_reward = np.where(prob_reward == np.max(prob_reward))[0]
            bandit_machine = max_prob_reward[0]
        else:
            eps_init += 1

        eps_init += 1

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