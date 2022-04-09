# Real-Time-Plotting-PyGame
This program allows you to **live plot** data in PyGame engine using ```Matplollib```. In order to work, the program must be provided with an list updating it-self in the Pygame ```main``` function.
## Preview of the final result
Here is an example of how this algorithm can be used:
<p align ="center"><img src="https://user-images.githubusercontent.com/72025267/162576290-8c8fc99a-7345-4265-8a51-91d5e332fdd3.gif" width="531" height="313"></p>

## The Algorithm

### Library
To make it work, here are the following library use to compile the program properly:

```python
import pygame
import random
import matplotlib.backends.backend_agg as agg
from pygame.locals import *
import matplotlib.pyplot as plt
```

### Main function
The main function used to create the new pygame window has to include two updating ```list```. The first one corresponds to the **x** axis and is updated with the ```XValue()``` function. This function is appending a list by incrementing it one by one until it reachs a given limit. When the limit is reached the function is poping out the first element of the list but is still doing the same thing:

#### XValue function

```python
# Updating x list:
def XValue(lst, i, limit):
    if len(lst) < limit:
        lst.append(len(lst))
    else:
        lst.pop(0)
        lst.append(i)
    return lst
```
This list is what will be later the **x** axis.

The second list corresponds to the **y** axis that we will plot later. In this example we will add random data to this list however we will still use the same principle as the **x** function:

#### YValue function

```python
def YValue(lst,limit):
    if len(lst) < limit:
        lst.append(random.randint(-10, 10))
    else:
        lst.pop(0)
        lst.append(random.randint(-10, 10))
    return lst
```

To call the ```LivePlot``` function so that we can plot the data, **x**'s list must be the same size as the **y**'s one. Here is how it is working:

```python
# Constant:
SWidth, SHeight = 1080, 720
position = (0, SHeight / 4)
# Test if the live Plotting is possible:
def possible(XLst, YLst):
    return len(XLst) == len(YLst)
```
```python
def main():
    FPS, LIMIT = 24, 50
    run = True
    i = 0
    YLst, XLst = [], []
    screen.fill((67, 82, 105))
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        YLst = YValue(YLst, LIMIT)
        XLst = XValue(XLst, i, LIMIT)
        if possible(XLst,YLst):
            LivePlot(XLst, YLst, position, (SWidth/100, 4))
        i += 1
        pygame.display.update()
    pygame.quit()
```

### The live Plotting function
This function needs to be provided with the following parameter:
* Xval which reffers to the **x** list
* Yval which reffers to the **y** list
* position reffers to **position** on the PyGame window
* size reffers to the **size** of your figure 
We are not using the built-in animation proposed by matplotlib, instead we are creating a new image that we draw inside the Pygame window every loop turn which creates the animation. The speed of the animation depend of the value that you enter on your ```FPS``` constant. Here is the following function:
```python
# Color:
CBLUE = (67 / 255, 82 / 255, 105 / 255)
CWHITE = (204 / 255, 220 / 255, 245 / 255)
CORANGE = (237 / 255, 152 / 255, 16 / 255)
```
```python
# Graph design:
def GraphDesign(ax,fig):
    # Couleur du graphe, des axes:
    ax.set_facecolor(CBLUE)
    fig.patch.set_facecolor(CBLUE)
    ax.tick_params(axis='x', colors = CWHITE)
    ax.tick_params(axis='y', colors = CWHITE)
    plt.setp(ax.spines.values(), color = CWHITE)
    # Couleur des bordures du tableau:
    for axis in ['top', 'bottom', 'left', 'right']:
        ax.spines[axis].set_linewidth(2)

# Plot in real time:
def LivePlot(Xval, Yval, position, size):
    # New figure
    fig = plt.figure(figsize = size, dpi = 100)
    # Parameters:
    ax = fig.gca()
    GraphDesign(ax,fig)
    ax.plot(Xval, Yval, 'ro-',color = CORANGE)
    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.tostring_rgb()
    size = canvas.get_width_height()
    surf = pygame.image.fromstring(raw_data, size, "RGB")
    screen.blit(surf, position)
    plt.close(fig)
```
