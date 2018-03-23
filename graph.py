import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

style.use("ggplot")


fig = plt.figure()
axis = fig.add_subplot(1,1,1)


def animate(i):

    data = open("twitter-out.txt", "r").read()
    lines = data.split('\n')

    xar = []
    yar = []

    x = 0
    y = 0

    for l in lines:
        x += 1
        if "pos" in l:
            y += 1
        elif "neg" in l:
            y -= 2

        xar.append(x)
        yar.append(y)

    axis.clear()
    axis.plot(xar,yar)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

