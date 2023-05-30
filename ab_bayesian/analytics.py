import pandas as pd
import numpy as np

from scipy import stats
from matplotlib.animation import FuncAnimation
from matplotlib import pyplot as plt


def bayesian_inference(data):
    N_mc = 10000

    proba_b_better_a = []
    expected_loss_a = []
    expected_loss_b = []

    for day in range(len(data)):
        u_a, var_a = stats.beta.stats(a = 1 + data.loc[day, 'acc_click_control'],
                                      b = (1 + data.loc[day, 'acc_visit_control'] - data.loc[day, 'acc_click_control']),
                                      moments='mv')
        
        u_b, var_b = stats.beta.stats(a = 1 + data.loc[day, 'acc_click_treatment'],
                                      b = 1 + (data.loc[day, 'acc_visit_treatment'] - data.loc[day, 'acc_click_treatment']),
                                      moments='mv')
        
        # Amostras da distribuicao normal A
        x_a = np.random.normal(loc = u_a,
                               scale = 1.25 * np.sqrt(var_a),
                               size=N_mc)
        
        x_b = np.random.normal(loc = u_b,
                               scale = 1.25 * np.sqrt(var_b),
                               size=N_mc)
        
        # Beta distribution
        fa = stats.beta.pdf(x_a,
                            a = 1 + data.loc[day, 'acc_click_control'],
                            b = 1 + (data.loc[day, 'acc_visit_control'] - data.loc[day, 'acc_click_control']))
    
        fb = stats.beta.pdf(x_b,
                            a = 1 + data.loc[day, 'acc_click_treatment'],
                            b = 1 + (data.loc[day, 'acc_visit_treatment'] - data.loc[day, 'acc_click_treatment']))
        
        ga = stats.norm.pdf(x_a,
                            loc = u_a,
                            scale = 1.25 * np.sqrt(var_a))
        
        gb = stats.norm.pdf(x_b,
                            loc = u_b,
                            scale = 1.25 * np.sqrt(var_b))
        
        # Beta / Normal
        y = (fa*fb)/(ga*gb)

        # Somente para valores de B maior que A
        yb = y[x_b >= x_a]

        # Probabilidade de B ser melhor do que A
        p = (1/N_mc)*np.sum(yb)

        # Erro ao assumir B melhor do que A
        expected_loss_A = (1/N_mc) * np.sum(((x_b - x_a) * y)[x_b >= x_a])
        expected_loss_B = (1/N_mc) * np.sum(((x_a - x_b) * y)[x_a >= x_b])

        proba_b_better_a.append(p)
        expected_loss_a.append(expected_loss_A)
        expected_loss_b.append(expected_loss_B)

    return proba_b_better_a, expected_loss_a, expected_loss_b


def animate(i):
    data = pd.read_csv('data_experiment.csv')

    data = data.dropna()

    #dtypes
    data['click'] = data['click'].astype(int)
    data['visit'] = data['visit'].astype(int)

    # pitvot table
    data = data.reset_index().rename(columns={'index': 'day'})
    data = data.pivot(index='day', columns='group', values=['click', 'visit'])
    data.columns = ['click_control', 'click_treatment', 'visit_control', 'visit_treatment']
    data = data.reset_index(drop=True)
    data = data[['visit_control', 'click_control', 'visit_treatment', 'click_treatment']].fillna(0)

    data['acc_visit_control'] = data['visit_control'].cumsum()
    data['acc_click_control'] = data['click_control'].cumsum()

    data['acc_visit_treatment'] = data['visit_treatment'].cumsum()
    data['acc_click_treatment'] = data['click_treatment'].cumsum()

    # bayesian inference
    p, expected_loss_a, expected_loss_b = bayesian_inference(data)

    x1 = np.arange(len(p))    

    plt.cla()
    plt.plot(x1, p, label='Probability B better A')
    plt.plot(x1, expected_loss_a, label='Risk Choosing A')
    plt.plot(x1, expected_loss_b, label='Risk Choosing B')

    plt.legend(loc='upper right')
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()