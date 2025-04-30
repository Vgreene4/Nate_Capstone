import matplotlib.pyplot as plt
import numpy as np
import sampleData

points = sampleData.sampleCirc((0,0), 1, 0, 20)

x = [p[0] for p in points]
y = [p[1] for p in points]


print(x)

plt.scatter(x,y)
plt.axis('square')

plt.show()