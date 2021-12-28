from functions import Functions
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


n_frame = 200
n = 15
env_temperature = 5
frames = np.zeros((n_frame, n, n))

func = Functions()
snake_coor = func.generate_snake_coor(n)
mouse_coor = func.generate_mouse_coor(n, snake_coor)
map = func.generate_map(n, snake_coor, mouse_coor)
frames[0] = map

snakes_property, mouses_property = func.generate_snake_mouse_property()
snake_heat_loss_rate = func.heat_loss_rate(16, env_temperature, snakes_property[0])
mouse_heat_loss_rate = func.heat_loss_rate(1, env_temperature, mouses_property[0])

for i in range(1, n_frame):
    map, snake_coor, mouse_coor = func.snake_and_mouse_movements(n, snake_coor, mouse_coor, map, snakes_property, mouses_property, snake_heat_loss_rate, mouse_heat_loss_rate)
    frames[i] = map

def init():
    plt.clf()
    return None

def animate(i):
    plt.clf()
    ax = sns.heatmap(frames[i],
                    center=1,
                    square=True,
                    xticklabels=False,
                    yticklabels=False)
    return None

fig = plt.figure()
anim = animation.FuncAnimation(fig,
                               animate,
                               frames=range(1, n_frame, 1),
                               blit=False,
                               interval=30,
                               init_func=init)
                            
plt.show()
