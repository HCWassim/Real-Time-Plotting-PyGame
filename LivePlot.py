# Library:
import pygame
import random
import matplotlib.backends.backend_agg as agg
from pygame.locals import *
import matplotlib.pyplot as plt

# Constant:
SWidth, SHeight = 1080, 720
position = (0, SHeight / 4)

# Color:
CBLUE = (67 / 255, 82 / 255, 105 / 255)
CWHITE = (204 / 255, 220 / 255, 245 / 255)
CORANGE = (237 / 255, 152 / 255, 16 / 255)

# Initialisation:
pygame.init()
window = pygame.display.set_mode((1080, 720))
screen = pygame.display.get_surface()

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
    # Nouvelle figure
    fig = plt.figure(figsize = size, dpi = 100)
    # Paramétrage:
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

# Updating y list:
def YValue(lst,limit):
    if len(lst) < limit:
        lst.append(random.randint(-10, 10))
    else:
        lst.pop(0)
        lst.append(random.randint(-10, 10))
    return lst

# Updating x list:
def XValue(lst, i, limit):
    if len(lst) < limit:
        lst.append(len(lst))
    else:
        lst.pop(0)
        lst.append(i)
    return lst

# Test if the live Plotting is possible:
def possible(XLst, YLst):
    return len(XLst) == len(YLst)

# Main function:
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

# Demarrage:
if __name__ == "__main__":
    main()