import math, pygame, sys, time
from pygame.locals import *

DEFAULT_POINTS = 480000
WIDTH = 800
HEIGHT = 600
FIX_SKEW = True

def printText(text, window, backColor=(255,255,255), textColor=(0,0,0), x=0, y=0, size=14):
    font = pygame.font.Font('freesansbold.ttf', size)
    textobject = font.render(str(text), False, textColor, backColor)
    textRect = textobject.get_rect()
    textRect.center = (x, y)
    window.blit(textobject, textRect)
        
def ends(z):
    '''
    Let f(x) = x^2+z, where z is a complex constant.
    This says how long it takes for f(f(...f(z)))) to get above 5(model of divergence)
    '''
    a = z
    #We first let a = z, then f(z), then f(f(z)), etc.
    for n in range(100):
        #If the absolute value of a is greater than 5, then we assume it diverges.
        #We then return how long it took for it to diverge.
        if abs(a) > 5:
            return n
        #a = f(a)
        a = a*a+z
    #If it still hasn't diverged after 100 applications of the function, we return 100.
    return 100

def data_generator(start=-3-2j, end=1+2j, points=DEFAULT_POINTS):
    '''This function computes ends(z) for "points" z-values evenly distributed inside
    the box with lower left corner "start" and upper right corner "end". It then returns
    the data generated.'''
    a = start
    b = end
    start = min(a.real, b.real) + 1j*min(a.imag, b.imag)
    end = max(a.real, b.real) + 1j*max(a.imag, b.imag)
    #Compute the area of the box
    area = (end.real-start.real)*(end.imag-start.imag)
    #Get the amount to change by for each z to evenly distribute the points
    epsilon = math.sqrt(float(area)/float(points))
    z = start
    a = []
    b = []
    c = []
    epsiloni = epsilon*1j
    #iterate through the z-values that we are going to test
    while z.real <= end.real:
        while z.imag <= end.imag:
            #compute ends(z) and log the data
            a.append(z.real)
            b.append(z.imag)
            c.append(ends(z))
            #increment z's imaginary coordinate
            z += epsiloni
        #make z's imaginary coordinate original and increment z's real coordinate.
        z = z.real + start.imag*1j
        z += epsilon
    #return a = [real coordinates], b = [imaginary coordinates], c = [times to diverge]
    return a, b, c

def get_colour(time):
    if time == 100:
        return (0, 0, 0)
    if time > 70:
        return (255, int(255*(time-70)/100.0), int(255*(time-70)/100.0))
    if time > 40:
        return (255, 255, int(255*(time-40)/100.0))
    if time > 10:
        return (int(255*time/100.0), int(255*time/100.0), 255)
    return (0, 0, 0)

def pygame_plot(start=-3-2j, end=1+2j, pix=DEFAULT_POINTS, axes_on=True):
    print('Plotting the Mandelbrot set from %s+%si to %s+%si...' % (round(start.real, 3), round(start.imag, 3), round(end.real, 3), round(end.imag, 3)))
    print('Resolution: %s megapixels.' % (round(pix/1000000, 2)))
    t = time.clock()
    reals, imags, times = data_generator(start, end, pix)
    print('This plot took %s seconds to compute.' % (round(time.clock()-t, 2)))
    t = time.clock()
    if axes_on:
        screen = pygame.display.set_mode((WIDTH+65, HEIGHT+65))
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0,0,0))
    r = (start.real-end.real)/(start.imag-end.imag)
    h = int(math.sqrt(pix/r))
    w = int(h*r)
    hep = (end.real-start.real)/w
    vep = (start.imag-end.imag)/h
    colour_table = []
    for x in range(101):
        colour_table.append(get_colour(x))
    panel = pygame.Surface((w, h))
    pixarray = pygame.PixelArray(panel)
    umap = {}
    vmap = {}
    for x in range(pix):
        y = colour_table[times[x]]
        if reals[x] in umap:
            u = umap[reals[x]]
        else:
            u = umap[reals[x]] = int((reals[x]-start.real)/hep)
        if imags[x] in vmap:
            v = vmap[imags[x]]
        else:
            v = vmap[imags[x]] = int((imags[x]-start.imag)/vep)
        pixarray[u][v]=y
    del pixarray
    pygame.display.set_caption('Mandelbrot Set from %s+%si to %s+%si' % (round(start.real, 3), round(start.imag, 3), round(end.real, 3), round(end.imag, 3)))

    if axes_on:
        screen.blit(pygame.transform.scale(panel, (WIDTH, HEIGHT)), (50, 15))
        pygame.draw.line(screen, (0, 255, 0), (50, 15), (50, HEIGHT+15), 1)
        pygame.draw.line(screen, (0, 255, 0), (50, HEIGHT+15), (50+WIDTH, HEIGHT+15), 1)
        for x in range(7):
            printText('%s' % (round(start.real+(end.real-start.real)*x/6.0, 3)), \
             screen, x=int(WIDTH*x/6)+50, y=HEIGHT+25, backColor=(0, 0, 0), textColor=(0, 255, 0))
            printText('%si' % (round(end.imag+(start.imag-end.imag)*x/6.0, 3)),
             screen, x=25, y=int(HEIGHT*x/6)+15, backColor=(0, 0, 0), textColor=(0, 255, 0))
    else:
        screen.blit(pygame.transform.scale(panel, (WIDTH, HEIGHT)), (0, 0))
        
    pygame.display.update()
    print('This plot took %s seconds to draw.' % (round(time.clock()-t, 2)))
    return panel

def reload(start, end, panel, axes_on=True, selection_rect=None):
    if axes_on:
        screen = pygame.display.set_mode((WIDTH+65, HEIGHT+65))
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((0,0,0))
    if axes_on:
        screen.blit(pygame.transform.scale(panel, (WIDTH, HEIGHT)), (50, 15))
        pygame.draw.line(screen, (0, 255, 0), (50, 15), (50, HEIGHT+15), 1)
        pygame.draw.line(screen, (0, 255, 0), (50, HEIGHT+15), (50+WIDTH, HEIGHT+15), 1)
        for x in range(7):
            printText('%s' % (round(start.real+(end.real-start.real)*x/6.0, 3)), \
             screen, x=int(WIDTH*x/6)+50, y=HEIGHT+25, backColor=(0, 0, 0), textColor=(0, 255, 0))
            printText('%si' % (round(end.imag+(start.imag-end.imag)*x/6.0, 3)),
             screen, x=25, y=int(HEIGHT*x/6)+15, backColor=(0, 0, 0), textColor=(0, 255, 0))
    else:
        screen.blit(pygame.transform.scale(panel, (WIDTH, HEIGHT)), (0, 0))
    if selection_rect is not None:
        pygame.draw.rect(screen, (0, 255, 0), selection_rect)
    pygame.display.update()
    
def pygame_plotter():
    print('Mandelbrot Set Plotter - Pygame Version')
    print('Controls:')
    print('Drag mouse to highlight an area to zoom in on.')
    print('Type \'p\' to zoom in by 50%.')
    print('Type \'m\' to zoom out by 50%.')
    print('Type \'x\' to change whether axes are shown.')
    print('Type \'s\' to save the current image.')
    print('Default resolution: %s megapixels.' % (round(DEFAULT_POINTS/1000000, 2)))
    print('Type \'r\' to change the resolution.')
    pygame.init()
    clock = pygame.time.Clock()
    start = (-2.6-1.2j)
    end = (0.6+1.2j)
    currentPanel = pygame_plot(start, end)
    mouseStart = None
    mouseEnd = None
    axes_on = True
    res = DEFAULT_POINTS
    mouseRect = None
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mouseStart = event.pos
                reload(start, end, currentPanel, axes_on=axes_on, selection_rect=mouseRect)
            if event.type == MOUSEMOTION and mouseStart is not None:
                mouseEnd = event.pos
            if event.type == MOUSEBUTTONUP:
                mouseEnd = event.pos
                if mouseStart != None and mouseStart != mouseEnd:
                    if FIX_SKEW:
                        mouseEnd = mouseEnd[0],int(mouseStart[1]+(mouseEnd[0]-mouseStart[0])*HEIGHT/WIDTH)
                    if axes_on:
                        mouseStart = (mouseStart[0]-50, mouseStart[1]-15)
                        mouseEnd = (mouseEnd[0]-50, mouseEnd[1]-15)
                    firstPoint = (start.real + mouseStart[0]*((end.real-start.real)/WIDTH)) + 1j*(end.imag + mouseStart[1]*((start.imag-end.imag)/HEIGHT))
                    secondPoint = (start.real + mouseEnd[0]*((end.real-start.real)/WIDTH)) + 1j*(end.imag + mouseEnd[1]*((start.imag-end.imag)/HEIGHT))
                    start = min(firstPoint.real, secondPoint.real)+1j*min(firstPoint.imag, secondPoint.imag)
                    end = max(firstPoint.real, secondPoint.real)+1j*max(firstPoint.imag, secondPoint.imag)
                    currentPanel = pygame_plot(start, end, pix=res, axes_on=axes_on)
                    mouseStart = None
                    mouseEnd = None
                    break
            if event.type == KEYDOWN:
                if event.key == ord('p'):
                    currentPanel = pygame_plot(start+(end-start)/6.0, end-(end-start)/6.0, pix=res, axes_on=axes_on)
                    start = start+(end-start)/6.0
                    end = end-(end-start)/6.0
                    mouseStart = None
                    mouseEnd = None
                    break
                if event.key == ord('m'):
                    currentPanel = pygame_plot(start-(end-start)*0.25, end+(end-start)*0.25, pix=res, axes_on=axes_on)
                    start = start-(end-start)*0.25
                    end = end+(end-start)*0.25
                    mouseStart = None
                    mouseEnd = None
                    break
                if event.key == ord('x'):
                    axes_on = not axes_on
                    reload(start, end, currentPanel, axes_on=axes_on, selection_rect=mouseRect)
                    mouseStart = None
                    mouseEnd = None
                    break
                if event.key == ord('r'):
                    res = int(input('Type the desired resolution in pixels.'))
                if event.key == ord('s'):
                    filename = 'mandelbrot_set_%s+%si_to_%s+%si_%s.jpg' % \
(start.real, start.imag, end.real, end.imag, res)
                    pygame.image.save(currentPanel, filename)
        if mouseStart != None and mouseEnd != None:
            if axes_on:
                screen = pygame.display.set_mode((WIDTH+65, HEIGHT+65))
            else:
                screen = pygame.display.set_mode((WIDTH, HEIGHT))
            reload(start, end, currentPanel, axes_on=axes_on, selection_rect=mouseRect)
            pygame.draw.rect(screen, (0,255,0), (min(mouseStart[0],mouseEnd[0]), min(mouseStart[1],mouseEnd[1]),
                                abs(mouseEnd[0]-mouseStart[0]), int(abs(mouseEnd[0]-mouseStart[0])*HEIGHT/WIDTH)), 1)
            pygame.display.update()
        clock.tick(25)
pygame_plotter()
