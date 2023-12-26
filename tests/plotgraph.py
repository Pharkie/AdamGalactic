import matplotlib.pyplot as plt

i = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
reduced_delay = [0.4, 0.356, 0.312, 0.268, 0.224, 0.18, 0.136, 0.092, 0.048, 0.004, 0]

plt.plot(i, reduced_delay, marker='o', linestyle='-', color='b')
plt.xlabel('i')
plt.ylabel('Reduced Delay')
plt.title('Graph of Reduced Delay vs. i')
plt.grid(True)
plt.show()
