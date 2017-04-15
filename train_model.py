import struct
from PIL import Image, ImageEnhance
from urllib import pathname2url

import numpy as np
import tensorflow as tf
from sklearn.neural_network import MLPClassifier
from sklearn.decomposition import PCA

def getRecord(id_num, filename):
    filename.seek(id_num * sz_record)
    s = filename.read(sz_record)
    r = struct.unpack('>2H8sI4B4H2B34x8128s7x', s)
    return r

def jis2url(code):
    b = b'\033$B' + bytes(bytearray.fromhex(code))
    c = b.decode('iso2022_jp')
    url_code = pathname2url(c.encode('utf-8'))
    return url_code

if __name__ == "__main__":
    # filename = 'ETL9G/ETL9G_01'
    # id_record = 0
    # sz_record = 8199
    # X = []
    # y = []
    # with open(filename, 'r') as f:
    #     for id_record in range(1):
    #         r = getRecord(id_record, f)
    #         # print len(r[14]) # 8128
    #         print type(r[14]) #<type 'str'>
    #         iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
    #         # print len(list(iF.getdata())) # 16256
    #         jis = hex(r[1])[-4:]
    #         print r[0:14], jis
    #         print "URL encoding:", jis2url(jis)
    #         X.append(list(iF.getdata()))
    #         y.append(hex(r[1])[-4:])
        # clf = MLPClassifier(alpha=1e-5, 
        #                     hidden_layer_sizes=(100),
        #                     random_state=1)
        # X = np.array(X)
        # y = np.array(y)
        # pca = PCA(n_components=200)
        # X_reduced = pca.fit(X).transform(X)
        # clf.fit(X_reduced, y)

        # # predict 1001th sample
        # f.seek(3037* sz_record)
        # s = f.read(sz_record)
        # r = struct.unpack('>2H8sI4B4H2B34x8128s7x', s)
        # iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
        # predict_X_reduced = pca.transform(np.array(list(iF.getdata())))
        # print "Predicted:", clf.predict(predict_X_reduced)
        # print "Target:", hex(r[1])[-4:]


        ####################
        # print r[0:14], r[1]
        # iF = Image.frombytes('F', (128, 127), r[14], 'bit', 4)
        # iP = iF.convert('P')
        # fn = 'ETL9G_{:d}_{:s}.png'.format((r[0]-1)%20+1, hex(r[1])[-4:])
        # iP.save(fn, 'PNG', bits=4)
        # enhancer = ImageEnhance.Brightness(iP)
        # iE = enhancer.enhance(16)
        # iE.save(fn, 'PNG')
        ####################