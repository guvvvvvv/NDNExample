#!/usr/bin/env python2
#encoding: UTF-8

from ndn_example.producer import *
from ndn_example.consumer import *
import multiprocessing 

def init_certs():
    keyChain = KeyChain()
    try:
        keyChain.getDefaultIdentity()
    except SecurityException:
        keyChain._setDefaultCertificate()  
        
def worker_with_consumer(num):
    """thread worker function"""
#    Consumer("/"+str (num)).run()
    Consumer("/1").run()
    return

def worker(num):
    """thread worker function"""
    print "Downloading : %s" % str(num)

    min_char = 8800 - 400
    max_char = 8800 - 400
    allchar = string.ascii_letters + string.punctuation + string.digits
    rint = randint(min_char, max_char)
    cont = "".join(choice(allchar) for x in range(rint))
    time.sleep(2)
    print "Received data: ", len(cont)
    print "Processing data: "
    time.sleep(2)    
    return

if __name__ == '__main__':
#    Start the nfd docker: sudo docker run -i -t -p 127.0.0.1:6363:6363 nfd

    parser = argparse.ArgumentParser(description='Parse command line args for ndn consumer or producer')
    parser.add_argument("-c", "--consumer", action='store_true')
    parser.add_argument("-p", "--producer", action='store_true')
    parser.add_argument("-ndn", "--ndn_experiment", action='store_true')
    parser.add_argument("-tcp", "--tcp_experiment", action='store_true')
    parser.add_argument("-n", "--namespace", required=False, help='namespace to listen under')
    parser.add_argument("-u", "--uri", required=False, help='ndn name to retrieve')
    args = parser.parse_args()
    try:
        init_certs()
        if args.consumer:
            uri = args.uri
            Consumer(uri).run()
        elif args.producer:
            namespace = args.namespace
            Producer().run(namespace)
        elif args.ndn_experiment:
            jobs = []
            for i in range(5):
                p = multiprocessing.Process(target=worker_with_consumer, args=(i,))
                jobs.append(p)
                p.start()
                time.sleep(0.5)
        elif args.tcp_experiment:
            jobs = []
            for i in range(5):
                p = multiprocessing.Process(target=worker, args=(i,))
                jobs.append(p)
                p.start()     
                time.sleep(0.5)
            
    except:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)