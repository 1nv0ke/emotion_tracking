
import pickle
import time
from datetime import datetime
import sched

# _________________________________________________________________________________________________

INITIAL_DELAY_SECONDS = 3

# _________________________________________________________________________________________________

def send_next_blob(blob):
    pass

def schedule_send():
    blob_pickled = './blob_pickled/single_1_human_blobs.pickle'
    with open(blob_pickled, 'rb') as handle:
        ids, blob_list = pickle.load(handle)
    if len(blob_list) == 0:
        return
    scheduler = sched.scheduler(time.time, time.sleep)
    size = len(blob_list)
    for tp in blob_list[:size]:
        delay = INITIAL_DELAY_SECONDS + (tp[0] - blob_list[0][0]).total_seconds()
        scheduler.enter(delay, 1, send_next_blob, (tp[1],))
    scheduler.run()

# _________________________________________________________________________________________________

def main():
    schedule_send()

# _________________________________________________________________________________________________

if __name__ == '__main__':
    main()

# _________________________________________________________________________________________________
