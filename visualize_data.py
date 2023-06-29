import matplotlib.pyplot as plt
import numpy as np
from save_data import load_dict_from_file

hyper_parameters = load_dict_from_file('data/hyper_parameters.json')

data = np.genfromtxt('data/scores.csv', delimiter=',')
data = data[:500]
generation = data[:, 0]
best_scores = data[:, 1]
average_scores = data[:, 2]


plt.rcParams['font.size'] = 15
plt.figure(figsize=(6, 6))

# plot
plt.plot(generation, best_scores, label='best score')
plt.plot(generation, average_scores, label='average score')

# titles
plt.title('Evolution of snake ai over generations')
plt.xlabel("generation")
plt.ylabel("score")
plt.legend()

# make
plt.tight_layout()
plt.savefig('figures/1.png')
# plt.show()
plt.close()





