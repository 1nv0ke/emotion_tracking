
# _________________________________________________________________________________________________

from datetime import datetime
import json
import pickle

# _________________________________________________________________________________________________

TIME_STAMP_JS_WIDTH = 13
TIME_STAMP_JS_CONVERT = 1000.0

# _________________________________________________________________________________________________

def parse_human_blob(filename = None,
                     start_timestamp = datetime.min,
                     end_timestamp = datetime.max,
                     human_count = 1,
                     pickled_file = None):

    def split_timestamp_and_json(line):
        ptr = 0
        timestamp_str = ''
        while ptr < len(line) and not line[ptr] in '0123456789{':
            ptr += 1
        while ptr < len(line) and line[ptr] in '0123456789':
            timestamp_str += line[ptr]
            ptr += 1
        while ptr < len(line) and line[ptr] != '{':
            ptr += 1
        blob_json = json.loads(line[ptr:])
        return (timestamp_str, blob_json)

    def timestamp_string_to_datetime(timestamp_str):
        return datetime.fromtimestamp(int(timestamp_str) / TIME_STAMP_JS_CONVERT)

    def update_dict_ids(id):
        if id in dict_ids:
            dict_ids[id] += 1
        else:
            dict_ids[id] = 1

    try:
        full_blob_list = []
        blob_json_old = None
        dict_ids = {}

        with open(filename, 'r') as f:
            next(f) # skip first line
            for line in f:
                timestamp_str, blob_json = split_timestamp_and_json(line)
                if blob_json['age'] == 'LOST':
                    continue
                timestamp = None
                if len(timestamp_str) == 0:
                    blob_json_old = blob_json
                else:
                    if len(timestamp_str) > TIME_STAMP_JS_WIDTH:
                        timestamp_old = timestamp_string_to_datetime(timestamp_str[:TIME_STAMP_JS_WIDTH])
                        if timestamp_old >= start_timestamp and timestamp_old <= end_timestamp and blob_json_old != None:
                            full_blob_list.append((timestamp_old, blob_json_old))
                            update_dict_ids(blob_json_old['id'])
                        timestamp = timestamp_string_to_datetime(timestamp_str[TIME_STAMP_JS_WIDTH:])
                    else:
                        timestamp = timestamp_string_to_datetime(timestamp_str)
                    if timestamp > end_timestamp:
                        break
                    if timestamp >= start_timestamp:
                        full_blob_list.append((timestamp, blob_json))
                        update_dict_ids(blob_json['id'])

        sorted_ids = sorted(dict_ids, key = lambda id:dict_ids[id], reverse = True)
        human_ids = sorted_ids[0:human_count]
        human_list = [tp for tp in full_blob_list if tp[1]['id'] in human_ids]
        parsed = (sorted_ids[0:human_count], human_list)
        # status output
        print 'file name: %s' % (filename)
        print 'total blob count: %d' % (len(full_blob_list))
        print 'ids: %s count: %s' % (str(human_ids), [dict_ids[id] for id in sorted_ids[0:human_count]])
        # serialize to pickle
        if pickled_file != None:
            with open(pickled_file + '.pickle', 'wb') as handle:
                pickle.dump(parsed, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return parsed
    except TypeError:
        print '[Error] parse_human_blob: no blob log file to read.'
        return None
    except IOError:
        print '[Error] parse_human_blob: failed to read blob log file.'
        return None

    # should never get here
    return None

# _________________________________________________________________________________________________

if __name__ == '__main__':


    delimiter = '-' * 40
    blob_logs_directory = './blob_logs/'
    blob_pickled_directory = './blob_pickled/'

    single1_ids, single1_list = parse_human_blob(filename = blob_logs_directory + 'single_1.log',
                                                 start_timestamp = datetime(2017, 4, 28, 16, 01, 52, 0),
                                                 end_timestamp = datetime(2017, 4, 28, 16, 07, 20, 0),
                                                 human_count = 1,
                                                 pickled_file = blob_pickled_directory + 'single_1_human_blobs')

    print "start time: {}".format(single1_list[0][0])
    print "end time:   {}".format(single1_list[-1][0])
    print delimiter

    single2_ids, single2_list = parse_human_blob(filename = blob_logs_directory + 'single_2.log',
                                                 start_timestamp = datetime(2017, 4, 28, 16, 12, 40, 0),
                                                 end_timestamp = datetime(2017, 4, 28, 16, 18, 12, 0),
                                                 human_count = 1,
                                                 pickled_file = blob_pickled_directory + 'single_2_human_blobs')

    print "start time: {}".format(single2_list[0][0])
    print "end time:   {}".format(single2_list[-1][0])
    print delimiter

    single3_ids, single3_list = parse_human_blob(filename = blob_logs_directory + 'single_3.log',
                                                 start_timestamp = datetime(2017, 4, 28, 16, 35, 27, 0),
                                                 end_timestamp = datetime(2017, 4, 28, 16, 41, 05, 0),
                                                 human_count = 1,
                                                 pickled_file = blob_pickled_directory + 'single_3_human_blobs')

    print "start time: {}".format(single3_list[0][0])
    print "end time:   {}".format(single3_list[-1][0])
    print delimiter

    single4_ids, single4_list = parse_human_blob(filename = blob_logs_directory + 'single_4.log',
                                                 start_timestamp = datetime(2017, 4, 28, 16, 44, 28, 0),
                                                 end_timestamp = datetime(2017, 4, 28, 16, 50, 05, 0),
                                                 human_count = 1,
                                                 pickled_file = blob_pickled_directory + 'single_4_human_blobs')

    print "start time: {}".format(single4_list[0][0])
    print "end time:   {}".format(single4_list[-1][0])
    print delimiter

    single5_ids, single5_list = parse_human_blob(filename = blob_logs_directory + 'single_5.log',
                                                 start_timestamp = datetime(2017, 4, 28, 17, 13, 13, 0),
                                                 end_timestamp = datetime(2017, 4, 28, 17, 18, 45, 0),
                                                 human_count = 1,
                                                 pickled_file = blob_pickled_directory + 'single_5_human_blobs')

    print "start time: {}".format(single5_list[0][0])
    print "end time:   {}".format(single5_list[-1][0])
    print delimiter

    single6_ids, single6_list = parse_human_blob(filename = blob_logs_directory + 'single_6.log',
                                                 start_timestamp = datetime(2017, 4, 28, 17, 21, 55, 0),
                                                 end_timestamp = datetime(2017, 4, 28, 17, 27, 26, 0),
                                                 human_count = 1,
                                                 pickled_file = blob_pickled_directory + 'single_6_human_blobs')

    print "start time: {}".format(single6_list[0][0])
    print "end time:   {}".format(single6_list[-1][0])
    print delimiter

    dual1_ids, dual1_list = parse_human_blob(filename = blob_logs_directory + 'dual_1.log',
                                             start_timestamp = datetime(2017, 4, 28, 16, 21, 19, 0),
                                             end_timestamp = datetime(2017, 4, 28, 16, 25, 34, 0),
                                             human_count = 2,
                                             pickled_file = blob_pickled_directory + 'dual_1_human_blobs')

    print "start time: {}".format(dual1_list[0][0])
    print "end time:   {}".format(dual1_list[-1][0])
    print delimiter

    dual2_ids, dual2_list = parse_human_blob(filename = blob_logs_directory + 'dual_2.log',
                                             start_timestamp = datetime(2017, 4, 28, 16, 52, 28, 0),
                                             end_timestamp = datetime(2017, 4, 28, 16, 57, 24, 0),
                                             human_count = 2,
                                             pickled_file = blob_pickled_directory + 'dual_2_human_blobs')

    print "start time: {}".format(dual2_list[0][0])
    print "end time:   {}".format(dual2_list[-1][0])
    print delimiter

    dual3_ids, dual3_list = parse_human_blob(filename = blob_logs_directory + 'dual_3.log',
                                             start_timestamp = datetime(2017, 4, 28, 17, 30, 36, 0),
                                             end_timestamp = datetime(2017, 4, 28, 17, 34, 57, 0),
                                             human_count = 2,
                                             pickled_file = blob_pickled_directory + 'dual_3_human_blobs')

    print "start time: {}".format(dual3_list[0][0])
    print "end time:   {}".format(dual3_list[-1][0])
    print delimiter

# _________________________________________________________________________________________________
