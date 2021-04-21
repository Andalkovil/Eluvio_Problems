import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from multiprocessing import Pool
 
import base64
import random
import string
import enum
from time import time
 
requests.packages.urllib3.disable_warnings(InsecureRequestWarning) # this is to suppress insecure warnings
 
class Status(enum.Enum):
   SUCCESS = 1
   FAILURE = 2
 
INPUT_SIZE = 100  #this is to specify input size
INPUT_ID_LENGTH = 27 #length of the input key
INPUT_ID_REGEX = string.ascii_letters + string.digits #generates input id with [0-9, a-z, A-Z]
ELUVIO_URL = 'https://eluv.io/items/' #URL to get item ids
MAX_RETRIES = 3 #retry attempts if api gives error code or exception
WORKER_POOL = 100 #number of parellel workers which is max number of simultaneous requests that can be processed which is 5
 
def generate_input_list():
    # generates random keys of given input size and length
    lst = [''.join(random.choice(INPUT_ID_REGEX) for i in range(INPUT_ID_LENGTH)) for _ in range(INPUT_SIZE)]
    lst = list(dict.fromkeys(lst))  # removes duplicates just in case
    return lst
 
def make_request(id):
    try:
        b64Val = base64.b64encode(id.encode('ascii'))
        url = ''.join((ELUVIO_URL, id))
        r = requests.get(url, verify=False, headers={'Authorization': b64Val})
        if r.status_code == 200: # if it is too many requests error, it is failure
            return id, Status.FAILURE
        else:
            return id, Status.SUCCESS
    except:
        return id, Status.FAILURE
 
def trigger_requests():
    input = generate_input_list()
    pool = Pool(WORKER_POOL) # initiate worker pool to max number of simultaneous requests
    ts = time()
    num_tries = MAX_RETRIES
 
    while num_tries > 0 and len(input) > 0:
        data = pool.map_async(make_request, input)
        failure_tuple = filter(lambda x: x[1] == Status.FAILURE, data.get()) # filter failed request ids for next retry
        failure_list = [x[0] for x in list(failure_tuple)]
        print(failure_list)
        input = failure_list
        num_tries -= 1
 
    pool.close()
    pool.join()
    print('Took %s seconds', time() - ts)
 

trigger_requests()
 
