from timeit import repeat
from matplotlib import projections
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt

class VisualizeFourierTransform:
    def __init__(self, f, tp=3):
        self.time = np.linspace(0, tp, 1000)
        self.freq = f
        self.phi = np.zeros_like(self.freq)
        self.fig = plt.figure(figsize=(12,5))
        # self.ax.set_rticks([])
        self.winding_frequency = []
        self.com_r = []

    def getWaveform(self):
        waveforms = []
        for f, p in zip(self.freq, self.phi):
            y = np.sin((2*np.pi*f*self.time) + p) + 1
            # print(y.shape)
            waveforms.append(y)

        waveforms = np.array(waveforms)
        # print(waveforms.shape)
        self.y_ = np.sum(waveforms, axis=0)

    def rotateWaveform(self, frame):
        winding_freq = frame * 0.025
        self.winding_frequency.append(winding_freq)
        if winding_freq>10:
            self.anim.event_source.stop()
        self.rotated_y_ = np.exp(-2*np.pi*1j*winding_freq*self.time)*self.y_
        self.r_ = np.abs(self.rotated_y_)
        self.theta_ = np.angle(self.rotated_y_)
        
        # get center of mass
        cx, cy = np.sum(np.real(self.rotated_y_))/len(self.rotated_y_), np.sum(np.imag(self.rotated_y_))/len(self.rotated_y_)
        # print(cx, cy)
        self.cr_ = np.sqrt(cx**2 + cy**2)
        self.ctheta_ = np.arctan2(cy, cx)
        self.com_r.append(self.cr_)

        self.l1.set_data(self.theta_, self.r_)
        self.l2.set_offsets(np.c_[self.ctheta_, self.cr_])
        self.title.set_text(f'Frequency: {winding_freq}')

        self.com.set_data(self.winding_frequency, self.com_r)

        return self.l1, self.l2, self.com, self.title

    def plotWaveform(self):
        self.getWaveform()
        winding_freq = 0.01
        self.winding_frequency.append(winding_freq)
        self.rotated_y_ = np.exp(-2*np.pi*1j*winding_freq*self.time)*self.y_
        self.r_ = np.abs(self.rotated_y_)
        self.theta_ = np.angle(self.rotated_y_)

        # get center of mass
        cx, cy = np.sum(np.real(self.rotated_y_))/len(self.rotated_y_), np.sum(np.imag(self.rotated_y_))/len(self.rotated_y_)
        # print(cx, cy)
        self.cr_ = np.sqrt(cx**2 + cy**2)
        self.ctheta_ = np.arctan2(cy, cx)
        self.com_r.append(self.cr_)

        self.ax1 = self.fig.add_subplot(1,4,1,projection='polar')
        self.ax1.set_rticks([])
        self.l1, = self.ax1.plot(self.theta_, self.r_)
        self.l2 = self.ax1.scatter(self.ctheta_, self.cr_, color='red')
        # self.ax.set_title(f'Frequency: {winding_freq}')

        # track center of mass
        self.ax2 = self.fig.add_subplot(1,4,(3,4))
        self.title = self.ax2.set_title(f'Frequency: {winding_freq}')
        self.ax2.set_xlim([0,10])
        self.ax2.set_ylim([-0.1,2.1])
        self.ax2.set_xticks(range(0,11))
        self.com, = self.ax2.plot(self.winding_frequency, self.com_r, color='red')

        return self.l1, self.l2, self.com, self.title

    def visualize(self):
        self.anim = FuncAnimation(self.fig, self.rotateWaveform, init_func=self.plotWaveform, frames=1000, interval=30, repeat=False, blit=True)
        plt.show()