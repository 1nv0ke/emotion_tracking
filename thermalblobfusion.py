
# _________________________________________________________________________________________________

import pickle
import random

# _________________________________________________________________________________________________


# _________________________________________________________________________________________________

def thermal_fusion(blob_filename=None,
                   thermal_filename=None):

    try:
        with open(blob_filename, 'rb') as handle:
            ids, blob_list = pickle.load(handle)
    except TypeError:
        print '[Error] thermal_fusion: no blob pickled file to read.'
        return []
    except IOError:
        print '[Error] thermal_fusion: failed to read blob pickled file.'
        return []

    if len(blob_list) == 0:
        print '[Error] thermal_fusion: no blob to process.'
        return []

    try:
        with open(thermal_filename, 'rb') as handle:
            thermal_list = pickle.load(handle)
    except TypeError:
        print '[Error] thermal_fusion: no thermal pickled file to read.'
        return []
    except IOError:
        print '[Error] thermal_fusion: failed to read thermal pickled file.'
        return []

    if len(thermal_list) == 0:
        print '[Error] thermal_fusion: no thermal to process.'
        return []

    """
    thermal_size = 5 # len(thermal_list)
    thermal_list = []
    for i in range(thermal_size):
        t1 = blob_list[2*i][0]
        t2 = blob_list[2*i+1][0]
        ts = t1 + (t2 - t1) / 2
        thermal_list.append((ts, 12052, random.randint(28, 35)))
    print thermal_list
    """

    blob_id_dict = dict(zip(ids, [[]] * len(ids)))
    for ts, blob in blob_list[:10]:
        blob_id_dict[blob['id']].append((ts, blob))

    thermal_id_dict = dict(zip(ids, [[]] * len(ids)))
    for ts, id, tmp in thermal_list:
        thermal_id_dict[id].append((ts, tmp))

    fusion_list = []

    for id in ids:
        # pre-assign
        curr = 0
        prev_ts, prev_tmp = thermal_id_dict[id][0]
        while curr < len(blob_id_dict[id]) and blob_id_dict[id][curr][0] <= prev_ts:
            blob_id_dict[id][curr][1]['temperature'] = prev_tmp
            curr += 1
        curr -= 1

        # in-assign
        for curr_ts, curr_tmp in thermal_id_dict[id][1:]:
            while curr < len(blob_id_dict[id]) and blob_id_dict[id][curr][0] <= curr_ts:
                weight = (blob_id_dict[id][curr][0] - prev_ts).total_seconds() / \
                         (curr_ts - prev_ts).total_seconds()
                blob_id_dict[id][curr][1]['temperature'] = prev_tmp + (curr_tmp - prev_tmp) * weight
                curr += 1
            curr -= 1
            prev_ts, prev_tmp = curr_ts, curr_tmp

        # post-assign
        while curr < len(blob_id_dict[id]):
            blob_id_dict[id][curr][1]['temperature'] = prev_tmp
            curr += 1

        fusion_list += blob_id_dict[id]

    return sorted(fusion_list, key=lambda x: x[0])

# _________________________________________________________________________________________________

if __name__ == '__main__':

    blob_list = thermal_fusion(
        blob_filename='./blob_pickled/single_1_human_blobs.pickle',
        thermal_filename=None
    )

    #for ts, blob in blob_list:
    #    print '{} \t {}'.format(ts, blob['temperature'])

# _________________________________________________________________________________________________
