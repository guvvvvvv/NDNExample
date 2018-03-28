from pyndn import Name
from pyndn import Face
from pyndn import Data
from pyndn.security import KeyChain

from pyndn.util.blob import Blob


from contextlib import closing


import time
import urllib2
import shutil
import os
from random import choice
from string import ascii_uppercase

import string
from random import *



class Producer(object):
    def __init__(self):
        self.keyChain = KeyChain()
        self.isDone = False
        self.maxNdnPacketSize = 0


    def run(self, namespace):
        # Create a connection to the local forwarder over a Unix socket
#        face = Face()
        face = Face("127.0.0.1")
        prefix = Name(namespace)
        
        # Use the system default key chain and certificate name to sign commands.
        cert_name = self.keyChain.getDefaultCertificateName()
        face.setCommandSigningInfo(self.keyChain, cert_name)

        # Also use the default certificate name to sign Data packets.
        face.registerPrefix(prefix, self.onInterest, self.onRegisterFailed)

        print "Registering prefix", prefix.toUri()
        
        self.maxNdnPacketSize = face.getMaxNdnPacketSize()

        # Run the event loop forever. Use a short sleep to
        # prevent the Producer from using 100% of the CPU.
        while not self.isDone:
            face.processEvents()
            time.sleep(0.01)



    def onInterest(self, prefix, interest, transport, registeredPrefixId):
        interestName = interest.getName()
        
        data = Data(interestName)
        
        print "Downloading : %s" % interestName.toUri()

        min_char = self.maxNdnPacketSize - 400
        max_char = self.maxNdnPacketSize - 400
        allchar = string.ascii_letters + string.punctuation + string.digits
        rint = randint(min_char, max_char)
        cont = "".join(choice(allchar) for x in range(rint))
        data.setContent(cont)
        time.sleep(2)
        
        hourMilliseconds = 3600 * 1000
        data.getMetaInfo().setFreshnessPeriod(hourMilliseconds)

        self.keyChain.sign(data, self.keyChain.getDefaultCertificateName())

        transport.send(data.wireEncode().toBuffer())

        print "Replied to: %s" % interestName.toUri()


    def onRegisterFailed(self, prefix):
        print "Register failed for prefix", prefix.toUri()
        self.isDone = True

    def getKeyID(self,key):
        pub_der = key.publickey().exportKey(format="DER")
        return bytearray(hashlib.sha256(pub_der).digest())
