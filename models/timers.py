# Savital https://github.com/Savital

from threading import Timer, Thread, Event

# Runs function hFunction on clock, when state is not zero
class RefreshEventGenerator():
    def __init__(self, t, hFunction):
        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)
        self.state = False

    def __del__(self):
        pass

    def handle_function(self):
        if self.state:
            self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

    def runF(self):
        self.state = True

    def stopF(self):
        self.state = False