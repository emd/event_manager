'''This module implements a class for extracting data from
matplotlib figures.

'''

import sys
import numpy as np
import matplotlib.pyplot as plt


class KeyHandler(object):
    '''Class for handling matplotlib key events. Using a class allows
    easy transfer of parameters to callback function.
    '''
    def __init__(self, fig, event_key='e'):
        'Key handler for `fig`:matplotlib.figure.Figure with `event_key`:str'
        self.fig = fig
        self.data = {}
        self.event_key = str.lower(event_key)

    def append(self, key, prompt=None):
        'Add data point to `self.data`:dict with `key`:str'
        key = str.lower(key)

        # Callback function. Matplotlib event handling only works when
        # the callback function has the *sole* argument `event`
        def on_key_press(event):
            'Get (x, y) coordinates of mouse when `event_key` is pressed.'
            sys.stdout.flush()
            if str.lower(event.key) == self.event_key:
                self.data[key] = event.xdata, event.ydata
                print '(x, y) = ' + str(self.data[key])
            else:
                print ('Position mouse over desired data point and '
                       'press `' + self.event_key + '` to extract.')

        # Ensure key is not already taken
        if key not in self.data.keys():
            self.data[key] = None

            # Connect to event handler
            cid = self.fig.canvas.mpl_connect('key_press_event', on_key_press)

            # Construct and print prompt
            if prompt is None:
                prompt = 'Select data: '
            raw_input(prompt + ' (Press `Return` to continue):\n')

            self.fig.canvas.mpl_disconnect(cid)

        else:
            print 'Key `' + key + '` has already been used.'


def example():
    'Example use of KeyHandler class. NOTE: Must be in %pylab mode to use.'
    # Initialize figure and key handler
    fig = plt.figure()
    h = KeyHandler(fig)

    x = np.linspace(0, 10, 1000)
    plt.plot(x, 2 * np.sin(x))
    plt.show()

    h.append('1', prompt='Select data 1:')
    h.append('2', prompt='Select data 2:')
    h.append('3', prompt='Select data 3:')

    print h.data
