import sys
import time
import argparse
import traceback

from pyndn import Interest
from pyndn import Name
from pyndn import Face



class Consumer(object):
    '''Hello World consumer'''

    def __init__(self, prefix):
        self.prefix = Name(prefix)
        self.outstanding = dict()
        self.isDone = False
        self.face = Face("127.0.0.1")
        self.start_time = 0;
        start_time = time.time()


    def run(self):
        try:
            self._sendNextInterest(self.prefix)

            while not self.isDone:
                self.face.processEvents()
                time.sleep(0.01)

        except RuntimeError as e:
            print "ERROR: %s" %  e


    def _sendNextInterest(self, name):
        self.start_time = time.time()
        interest = Interest(name)
        uri = name.toUri()
        
        interest.setInterestLifetimeMilliseconds(9000)
        interest.setMustBeFresh(False)

        if uri not in self.outstanding:
            self.outstanding[uri] = 1

        self.face.expressInterest(interest, self._onData, self._onTimeout)
#        print "Sent Interest for %s" % uri


    def _onData(self, interest, data):
        payload = data.getContent()
        name = data.getName()

#        print "Received data: ", len(payload.toRawStr())
#        print "Processing data: "
        time.sleep(2)
        
        del self.outstanding[name.toUri()]

        self.isDone = True
        elapsed_time = time.time() - self.start_time
        print elapsed_time


    def _onTimeout(self, interest):
        name = interest.getName()
        uri = name.toUri()

        print "TIMEOUT #%d: %s" % (self.outstanding[uri], uri)
        self.outstanding[uri] += 1

        if self.outstanding[uri] <= 3:
            self._sendNextInterest(name)
        else:
            self.isDone = True