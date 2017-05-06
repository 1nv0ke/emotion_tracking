
# _________________________________________________________________________________________________

import pickle
import random
import sys

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

    blob_id_dict = dict(zip(ids, [[]] * len(ids)))
    for ts, blob in blob_list:
        blob_id_dict[blob[u'id']].append((ts, blob))

    thermal_id_dict = dict(zip(ids, [[]] * len(ids)))
    for ts, id, tmp in thermal_list:
        thermal_id_dict[id].append((ts, tmp))

    fusion_list = []

    for id in ids:
        # pre-assign
        curr = 0
        prev_ts, prev_tmp = thermal_id_dict[id][0]
        while curr < len(blob_id_dict[id]) and blob_id_dict[id][curr][0] <= prev_ts:
            blob_id_dict[id][curr][1][u'temperature'] = prev_tmp
            curr += 1

        # in-assign
        for curr_ts, curr_tmp in thermal_id_dict[id][1:]:
            if curr_ts == prev_ts:
                continue
            while curr < len(blob_id_dict[id]) and blob_id_dict[id][curr][0] <= curr_ts:
                weight = (blob_id_dict[id][curr][0] - prev_ts).total_seconds() / \
                         (curr_ts - prev_ts).total_seconds()
                blob_id_dict[id][curr][1][u'temperature'] = prev_tmp + (curr_tmp - prev_tmp) * weight
                curr += 1
            prev_ts, prev_tmp = curr_ts, curr_tmp

        # post-assign
        while curr < len(blob_id_dict[id]):
            blob_id_dict[id][curr][1][u'temperature'] = prev_tmp
            curr += 1

        fusion_list += blob_id_dict[id]

    return sorted(fusion_list, key=lambda x: x[0])

# _________________________________________________________________________________________________

if __name__ == '__main__':

    blob_list = thermal_fusion(
        blob_filename = sys.args[1],
        thermal_filename = sys.args[2]
    )

# _________________________________________________________________________________________________
