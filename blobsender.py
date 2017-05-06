
# _________________________________________________________________________________________________

import pickle
import time
import sched
import json
import sys
from socketIO_client import SocketIO
from thermalblobfusion import thermal_fusion

# _________________________________________________________________________________________________

# Test locally
SOCKETIO_IP = 'http://127.0.0.1'
SOCKETIO_PORT = 8888

INITIAL_DELAY_SECONDS = 1
BLOB_AGE_TO_EVENT_TYPE = {
    'OLD': 'update',
    'NEW': 'new',
    'LOST': 'remove'
}

# _________________________________________________________________________________________________

def schedule_send(filename=None, blob_list=None):

    def send_next_blob(blob):
        if blob['age'] in BLOB_AGE_TO_EVENT_TYPE:
            eventType = BLOB_AGE_TO_EVENT_TYPE[blob['age']]
            socket.emit(eventType, blob)
            print blob

    if filename != None:
        try:
            with open(filename, 'rb') as handle:
                ids, blob_list = pickle.load(handle)
        except IOError:
            print '[Error] schedule_send: failed to read blob pickled file.'
            return
    elif blob_list == None:
        print '[Error] schedule_send: neither file or blob list specified.'

    if len(blob_list) == 0:
        print '[Error] schedule_send: no blob to send.'
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
    schedule_send(
        blob_list = thermal_fusion(
            blob_filename = sys.args[1],
            thermal_filename = sys.args[2]
        )
    )

# _________________________________________________________________________________________________
