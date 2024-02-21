import matplotlib.pyplot as plt
import numpy as np


plt.ion()


class DynamicGraph():
    # suppose we know the x range
    max_x = 15
    min_x = 0


    def __init__(self, title=""):
        self.title = title
        self.xdata = []
        self.ydata = []
        self.on_launch()


    def on_launch(self):
        # set up plot
        self.figure, self.ax = plt.subplots()
        self.ax.set_title(self.title)
        self.lines, = self.ax.plot([],[], 'o')
        # autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(self.min_x, self.max_x)

        self.ax.grid()

    def on_running(self, new_x, new_y):
        # update data with new points
        self.xdata.append(new_x)
        self.ydata.append(new_y)

        if len(self.xdata) > self.max_x:
            self.shift_ax(1)

        # update lines with new data
        self.lines.set_xdata(self.xdata)
        self.lines.set_ydata(self.ydata)
        # need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        # we need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


    def shift_ax(self, nb_shift):
        self.min_x += nb_shift
        self.max_x += nb_shift
        # set xlim w/ updated values
        self.ax.set_xlim(self.min_x, self.max_x)


    ##Example
    #def __call__(self):
    #    self.on_launch()
    #    xdata = []
    #    ydata = []
    #    for x in np.arange(0,10,0.5):
    #        xdata.append(x)
    #        ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
    #        self.on_running(xdata, ydata)
    #        time.sleep(1)
    #    return xdata, ydata
