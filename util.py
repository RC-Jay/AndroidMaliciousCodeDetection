from imports import *

class PreProcess():

    def __init__(self, path):
        '''
        A class to preprocess the dataset and obtain a dataframe that could be easily passed to a classifer.
        :param path: The path on the disk where dataset(APKs) is stored.
        '''

        self.path = path
        self.dataBenign = {"permissions":[], "isValidAPK":[], "services":[], "receivers":[] }
        self.dataMalign = {"permissions":[], "isValidAPK":[], "services":[], "receivers":[] }
        self.vocabPerm = list()
        self.vocabServ = list()
        self.vocabRecv = list()

        if LOAD_DATA:

            print("Loading data..")
            f = open("pickled/dataDictBenign.pkl", "rb")
            self.dataBenign = pickle.load(f)
            f.close()

            f = open("pickled/dataDictMalign.pkl", "rb")
            self.dataMalign = pickle.load(f)
            f.close()

            f = open("pickled/vocabLen.pkl", "rb")
            self.vocabLengths = pickle.load(f)
            f.close()

        elif MAKE_DICT:

            # Extract info from APKS and store them in dict with attr as keys
            print("Extracting data from APKs..")
            self.makeDataDicts()

            print "Pickling the data dicts and vocabs..."

            f = open("pickled/dataDictBenign.pkl", "wb")
            pickle.dump(self.dataBenign, f)
            f.close()

            f = open("pickled/dataDictMalign.pkl", "wb")
            pickle.dump(self.dataMalign, f)
            f.close()

            f = open("pickled/vocabPerm.pkl", "wb")
            pickle.dump(self.vocabPerm, f)
            f.close()

            f = open("pickled/vocabRecv.pkl", "wb")
            pickle.dump(self.vocabRecv, f)
            f.close()

            f = open("pickled/vocabServ.pkl", "wb")
            pickle.dump(self.vocabServ, f)
            f.close()

            # A dict that stores lengths os all vocabularies used.
            self.vocabLengths = {"perm":len(self.vocabPerm), "serv":len(self.vocabServ), \
                            "recv":len(self.vocabRecv)}

            f = open("pickled/vocabLen.pkl", 'wb')
            pickle.dump(self.vocabLengths, f)
            f.close()


        if LOAD_FEATS:

            print("Loading Features.")
            f = open("pickled/feats.pkl", "rb")
            self.feats = pickle.load(f)
            f.close()

            f = open("pickled/labels.pkl", "rb")
            self.labels = pickle.load(f)
            f.close()

        else:

            # Convert the data stored in dict to a appropriate integer dataframe in pandas
            print("Creating Data Frames..")
            self.makeDataFrames()

            f = open("pickled/feats.pkl", "wb")
            pickle.dump(self.feats, f)
            f.close()

            f = open("pickled/labels.pkl", "wb")
            pickle.dump(self.labels, f)
            f.close()

        print self.feats
        #print(len(mic(self.feats.values[:, :].astype(float), self.labels)))

    def getFeats(self):

        return (self.feats, self.labels)

    def getFeaturesMutualInfoClassif(self):

        micIdx = mic(self.feats.values[:, :].astype(float), self.labels)
        idx = np.nonzero(micIdx)
        return (np.array(self.feats)[idx], self.labels[idx])


    def makeDataDicts(self):
        '''
        This method extracts info from APKs using Androguard and stores the data in form of dicts as described for
        self.dataBenign and self.dataMalign.

        :return: Changes take in place.
        '''

        try:
            bt = dt.now()
            # Creating the benign data dict first.
            print "Processing Benign Folder"
            count = 1
            for filename in glob.glob(self.path + "benign/*"):

                try:
                    # The main class that statically analyzes the APK and returns the report
                    t = dt.now()
                    a, d, dx = AnalyzeAPK(filename)
                    print count, "--", os.path.basename(filename), "--", str(dt.now() - t)
                    temp = list()
                    temp.append(int(a.valid_apk))
                    temp.append(a.get_permissions())
                    temp.append(a.get_services())
                    temp.append(a.get_receivers())
                except Exception as  e:
                    print("Error during analysis of above APK - IGNORED")
                    print e.message
                    continue

                # Checking whether the APK is valid according to Androguard
                self.dataBenign["isValidAPK"].append(temp[0])

                # Adding app permissions as a multi valued attribute
                if temp[1]:

                    perm = list()
                    for p in temp[1]:
                        if p not in self.vocabPerm:
                            self.vocabPerm.append(p)
                            perm.append(self.vocabPerm.index(p))
                        else:
                            perm.append(self.vocabPerm.index(p))

                    self.dataBenign["permissions"].append(perm)
                else:
                    self.dataBenign["permissions"].append(list())

                # Adding app services as a multi valued attribute
                if temp[2]:

                    serv = list()
                    for p in temp[2]:
                        if p not in self.vocabServ:
                            self.vocabServ.append(p)
                            serv.append(self.vocabServ.index(p))
                        else:
                            serv.append(self.vocabServ.index(p))

                    self.dataBenign["services"].append(serv)
                else:
                    self.dataBenign["services"].append(list())

                # Adding app receivers as a multi valued attribute
                if temp[3]:

                    recv = list()
                    for p in temp[3]:
                        if p not in self.vocabRecv:
                            self.vocabRecv.append(p)
                            recv.append(self.vocabRecv.index(p))
                        else:
                            recv.append(self.vocabRecv.index(p))

                    self.dataBenign["receivers"].append(recv)
                else:
                    self.dataBenign["receivers"].append(list())

                count += 1
                if count == MAX_DATA / 2:
                    break
            print("Total time taken to process benign folder -- ", str(dt.now() - bt))
        except Exception as e:
            print e.message
            exit(0)

        try:
            mt = dt.now()
            print "Processing Malign Folder"
            count = 1
            for filename in glob.glob(self.path + "malign/*"):

                try:
                    t = dt.now()
                    a, d, dx = AnalyzeAPK(filename)
                    print count, "--", os.path.basename(filename), "--", str(dt.now() - t)
                    temp = list()
                    temp.append(int(a.valid_apk))
                    temp.append(a.get_permissions())
                    temp.append(a.get_services())
                    temp.append(a.get_receivers())
                except Exception as  e:
                    print("Error during analysis of above APK - IGNORED")
                    print e.message
                    continue

                self.dataMalign["isValidAPK"].append(temp[0])

                # Adding app permissions as a multi valued attribute
                if temp[1]:

                    perm = list()
                    for p in temp[1]:
                        if p not in self.vocabPerm:
                            self.vocabPerm.append(p)
                            perm.append(self.vocabPerm.index(p))
                        else:
                            perm.append(self.vocabPerm.index(p))

                    self.dataMalign["permissions"].append(perm)
                else:
                    self.dataMalign["permissions"].append(list())

                # Adding app services as a multi valued attribute
                if temp[2]:

                    serv = list()
                    for p in temp[2]:
                        if p not in self.vocabServ:
                            self.vocabServ.append(p)
                            serv.append(self.vocabServ.index(p))
                        else:
                            serv.append(self.vocabServ.index(p))

                    self.dataMalign["services"].append(serv)
                else:
                    self.dataMalign["services"].append(list())

                # Adding app receivers as a multi valued attribute
                if temp:

                    recv = list()
                    for p in temp[3]:
                        if p not in self.vocabRecv:
                            self.vocabRecv.append(p)
                            recv.append(self.vocabRecv.index(p))
                        else:
                            recv.append(self.vocabRecv.index(p))

                    self.dataMalign["receivers"].append(recv)
                else:
                    self.dataMalign["receivers"].append(list())

                count += 1
                if count == MAX_DATA / 2:
                    break
            print("Total time taken to process malign folder -- ", str(dt.now() - mt))
        except Exception as e:
            print e.message
            exit(0)

    def makeDataFrames(self):
        '''
        This method converts the data dicts into dataframes suitable for training with further DL algorithms.
        :return: Changes take in place.
        '''

        try:

            data_len = len(self.dataBenign["isValidAPK"])+1
            index = np.array(range(1, data_len ))
            self.dfBenign = pd.DataFrame(index = index)

            isValid = pd.Series(self.dataBenign['isValidAPK'], name="isValidAPK", index = index)
            self.dfBenign[isValid.name] = isValid

            perm = self.makeHotMatrix(self.dataBenign["permissions"], self.vocabLengths["perm"])
            columns = self.makeContCol("perm", self.vocabLengths["perm"])
            temp = pd.DataFrame(perm, columns=columns, index=index)
            self.dfBenign = self.dfBenign.join(temp)

            serv = self.makeHotMatrix(self.dataBenign["services"], self.vocabLengths["serv"])
            columns = self.makeContCol("serv", self.vocabLengths["serv"])
            temp = pd.DataFrame(serv, columns=columns, index=index)
            self.dfBenign = self.dfBenign.join(temp)

            recv = self.makeHotMatrix(self.dataBenign["receivers"], self.vocabLengths["recv"])
            columns = self.makeContCol("recv", self.vocabLengths["recv"])
            temp = pd.DataFrame(recv, columns=columns, index=index)
            self.dfBenign = self.dfBenign.join(temp)

        except Exception as e:
            print "Error while creating benign dataframe"
            print e.args, e.message
            exit(0)

        try:

            index = np.array(range(data_len, 2*data_len-1))
            self.dfMalign = pd.DataFrame(index=index)

            isValid = pd.Series(self.dataMalign['isValidAPK'], name="isValidAPK", index=index)
            self.dfMalign[isValid.name] = isValid

            perm = self.makeHotMatrix(self.dataMalign["permissions"], self.vocabLengths["perm"])
            columns = self.makeContCol("perm", self.vocabLengths["perm"])
            temp = pd.DataFrame(perm, columns=columns, index=index)
            self.dfMalign = self.dfMalign.join(temp)

            serv = self.makeHotMatrix(self.dataMalign["services"], self.vocabLengths["serv"])
            columns = self.makeContCol("serv", self.vocabLengths["serv"])
            temp = pd.DataFrame(serv, columns=columns, index=index)
            self.dfMalign = self.dfMalign.join(temp)

            recv = self.makeHotMatrix(self.dataMalign["receivers"], self.vocabLengths["recv"])
            columns = self.makeContCol("recv", self.vocabLengths["recv"])
            temp = pd.DataFrame(recv, columns=columns, index=index)
            self.dfMalign = self.dfMalign.join(temp)

        except Exception as e:
            print "Error while creating malign dataframe"
            print e.args, e.message
            exit(0)

        self.dfBenign.to_csv("csv/benign.csv", index=False)

        self.dfMalign.to_csv("csv/malign.csv", index=False)

        self.labels =  np.array([0]*self.dfBenign.shape[0] + [1]*self.dfMalign.shape[0])
        self.feats = pd.concat([self.dfBenign, self.dfMalign])

        # print(self.df)
        # print(self.labels)


    def makeHotMatrix(self, vec2D, len):
        '''
        Helper method to create a Hot Matrix of occurences
        :param vec2D: All the indices of data points
        :param len: dimnsion of each hot vector
        :return: A Hot matrix of shape(length(vec2D), len)
        '''

        hotMat = list()
        for vec in vec2D:
            if vec:
                hotMat.append(self.makeHotVector(vec, len))
            else:
                hotMat.append(np.zeros(len, dtype='int'))
        return hotMat

    def makeHotVector(self, vec, len):
        '''
        Helper method to create a Hot vector of occurences
        :param vec: the indices of the vector that are active
        :param len: the total length/dimension of the hot vector
        :return: Hot Vector of shape(1,len)
        '''

        hotVec = np.zeros(len, dtype='int')
        hotVec[vec] = 1

        return hotVec

    def makeContCol(self, base, len):

        col = list()
        for i in range(len):
            col.append(base + "_" + str(i+1))

        return col




