
# _________________________________________________________________________________________________

import pickle
import time
import sched
import json
from socketIO_client import SocketIO

# _________________________________________________________________________________________________

SOCKETIO_IP = 'http://97.107.129.81'
SOCKETIO_PORT = 8888

INITIAL_DELAY_SECONDS = 3
BLOB_AGE_TO_EVENT_TYPE = {
    'OLD': 'update',
    'NEW': 'new',
    'LOST': 'remove'
}

# _________________________________________________________________________________________________

def schedule_send(filename = None, ids = None, blob_list = None):

    def send_next_blob(blob):
        if blob['age'] in BLOB_AGE_TO_EVENT_TYPE:
            eventType = BLOB_AGE_TO_EVENT_TYPE[blob['age']]
            socket.emit(eventType, blob)
            print blob

    try:
        with open(filename, 'rb') as handle:
            ids, blob_list = pickle.load(handle)
    except TypeError:
        print '[Error] schedule_send: no blob pickled file to read.'
        return
    except IOError:
        print '[Error] schedule_send: failed to read blob pickled file.'
        return

    if len(blob_list) == 0:
        return

    socket = SocketIO(SOCKETIO_IP, port=SOCKETIO_PORT)
    socket.emit('start', json.loads('{"connectionType": "DATASOURCE"}'))

    scheduler = sched.scheduler(time.time, time.sleep)
    size = len(blob_list)
    for tp in blob_list[:size]:
        delay = INITIAL_DELAY_SECONDS + (tp[0] - blob_list[0][0]).total_seconds()
        scheduler.enter(delay, 1, send_next_blob, (tp[1],))
    scheduler.run()

# _________________________________________________________________________________________________

if __name__ == '__main__':
    schedule_send(filename = './blob_pickled/single_1_human_blobs.pickle')

# _________________________________________________________________________________________________
