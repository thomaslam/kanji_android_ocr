import struct
import os, time, csv
from urllib import pathname2url
from PIL import Image, ImageEnhance
from scipy import signal, misc

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

filename_base = 'ETL9G/ETL9G_'
img_folder = 'Images/'
record_size = 8199
file_size = 12144
start_time = time.clock()

# conver jis target label to url-encoded string
def jis2url(code):
    b = b'\033$B' + bytes(bytearray.fromhex(code))
    c = b.decode('iso2022_jp')
    url_code = pathname2url(c.encode('utf-8'))
    return url_code

# return a struct for byte-level processing from raw record from raw file data
def getRecord(id_num, fileobj):
    fileobj.seek(id_num * record_size)
    s = fileobj.read(record_size)
    r = struct.unpack('>2H8sI4B4H2B34x8128s7x', s)
    return r

# save as png on disk given struct r
def saveImage(r, dataset_id, scale=1):
    iF = Image.frombytes('F', (int(128*scale), int(127*scale)), r[14], 'bit', 4)
    iP = iF.convert('P')
    fn = 'ETL9G_{:02d}_{:s}.png'.format(dataset_id, hex(r[1])[-4:]) # (r[0]-1)%20+1
    fn = img_folder + fn
    enhancer = ImageEnhance.Brightness(iP)
    iE = enhancer.enhance(16)
    iE.save(fn, 'PNG')

# save as png files for all records in range record_ids in data set range set_ids
def saveImages(set_ids, record_ids):
    sid_start, sid_end = set_ids
    rid_start, rid_end = record_ids

    for dataset_id in range(sid_start, sid_end):
        filename = filename_base + '{:02d}'.format(dataset_id)
        print "Dataset: ", filename
        with open(filename, 'r') as f:
            for id_record in range(rid_start,rid_end):
                r = getRecord(id_record, f)
                saveImage(r, dataset_id)

# given PIL image, return its resized (default 50%) pixel value list
def getImgData(iF, resize=50):
    iP = iF.convert('P')
    enhancer = ImageEnhance.Brightness(iP)
    iE = enhancer.enhance(16)
    resizedImg = misc.imresize(iE, resize, mode='F')
    return resizedImg

# save as csv file for all records in range record_ids in data set range set_ids
def storeCSV(set_ids, record_ids, savefname):
    sid_start, sid_end = set_ids
    rid_start, rid_end = record_ids

    savefile = open(savefname, "wb")
    wr = csv.writer(savefile, quoting=csv.QUOTE_ALL)
    header = True
    print "Storing data to", savefname
    print ""
    for dataset_id in range(sid_start, sid_end):
        filename = filename_base + '{:02d}'.format(dataset_id)
        print "Dataset: ", filename
        with open(filename, 'r') as f:
            for id_record in range(rid_start,rid_end):
                r = getRecord(id_record, f)
                iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
                data = getImgData(iF)
                data_med_filtered = signal.medfilt(data) # Median filter

                y_label = hex(r[1])[-4:]
                data_med_filtered = np.append(data_med_filtered, y_label)
                if header == True:
                    wr.writerow(["Header"]*len(data_med_filtered))
                    print "\tData dimension:", len(data_med_filtered)
                    header = False
                wr.writerow(data_med_filtered)
    savefile.close()

# save as npy file for all records in range record_ids in data set range set_ids
def storeNPY(set_ids, record_ids, savefname):
    sid_start, sid_end = set_ids
    rid_start, rid_end = record_ids
    print "Storing data to", savefname
    row_sz = (sid_end - sid_start) * (rid_end - rid_start)
    dataset = np.array([])
    counter = 0
    for dataset_id in range(sid_start, sid_end):
        filename = filename_base + '{:02d}'.format(dataset_id)
        print "Dataset: ", filename
        with open(filename, 'r') as f:
            for id_record in range(rid_start, rid_end):
                r = getRecord(id_record, f)
                iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
                data = getImgData(iF)
                data_med_filtered = signal.medfilt(data)

                y_label = jis2url(hex(r[1])[-4:])
                data_med_filtered = np.append(data_med_filtered, y_label)
                if dataset.size == 0:
                    dataset = np.empty((row_sz, len(data_med_filtered)), dtype=unicode)
                dataset[counter] = data_med_filtered
                counter += 1
    print "Dataset dimensions: ", dataset.shape
    np.save(savefname, dataset)

train_data = []
test_data = []
train_set_ids = (1, 46)
test_set_ids = (46, 51)
record_ids = (0, 100)

### Store as csv files
storeCSV(train_set_ids, record_ids, "Data/train_data.csv")
print "\nOutput Data/train_data.csv"
print "========================\n"
storeCSV(test_set_ids, record_ids, "Data/test_data.csv")
print "\nOutput Data/test_data.csv"
print "========================\n"

### Store as png files
# saveImages(train_set_ids, record_ids)
# saveImages(test_set_ids, record_ids)

### Store as npy files
# storeNPY(train_set_ids, record_ids, "Data/train_data.npy")
# print "\nOutput Data/train_data.npy"
# print "========================\n"
# storeNPY(test_set_ids, record_ids, "Data/test_data.npy")
# print "\nOutput Data/train_data.npy"
# print "========================\n"

print "\n\nPreprocessing time: ", time.clock() - start_time
print "========================\n"