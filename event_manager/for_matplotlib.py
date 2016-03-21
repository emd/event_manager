'''This module implements classes for matplotlib figure data extraction
and window management.

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
        self.extraction_procedure = (
            'position mouse over desired data point and '
            'press `%s` to extract (x, y)' % self.event_key)

    def append(self, key, prompt=None):
        'Add data point to `self.data`:dict with `key`:str'
        key = str.lower(key)

        # Callback function. Matplotlib event handling only works when
        # the callback function has the *sole* argument `event`
        def on_key_press(event):
            'Get (x, y) coordinates of mouse when `event_key` is pressed.'
            sys.stdout.flush()

            # Different matplotlib interactive backends return `event.key`
            # as either a unicode or string type
            if type(event.key) is unicode:
                event.key = str(event.key)
            elif type(event.key) is not str:
                raise TypeError('`event.key` must be string or unicode')

            # Extract data
            if str.lower(event.key) == self.event_key:
                self.data[key] = event.xdata, event.ydata
                print '\n(x, y) = ' + str(self.data[key])
                print ('\nTo accept above (x, y), pres `Return` in console;\n'
                       'otherwise, %s' % self.extraction_procedure)
            else:
                print ('(%s)' % self.extraction_procedure)

        # Ensure key is not already taken
        if key not in self.data.keys():
            self.data[key] = None

            # Connect to event handler
            cid = self.fig.canvas.mpl_connect('key_press_event', on_key_press)

            # Construct and print prompt
            if prompt is None:
                prompt = 'Select data: '
            # raw_input(prompt + ' (Press `Return` to continue):\n')
            raw_input('%s\n(%s)\n' % (prompt, self.extraction_procedure))

            self.fig.canvas.mpl_disconnect(cid)

        else:
            print 'Key `' + key + '` has already been used.'


class FigureList(object):
    'Class for maintaining a list of active figures.'
    def __init__(self):
        self.getFigNums()

    def getFigNums(self):
        self.in_use = plt.get_fignums()
        return self.in_use[:]

    def getNext(self):
        'Obtain next largest unused figure number.'
        # Ensure figure list is up to date
        self.getFigNums()

        if len(self.in_use) > 0:
            return np.max(self.in_use) + 1
        else:
            return 0


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
