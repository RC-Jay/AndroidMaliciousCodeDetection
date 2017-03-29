from imports import *


class PreProcess(object):

    def __init__(self, path):

        self.path = path

        if LOAD_DATA:

            print "Loading features..........."
            f = open("pickled/XFeats.pkl", 'rb')
            self.X = pickle.load(f)
            f.close()

            f = open("pickled/yFeats.pkl", 'rb')
            self.y = pickle.load(f)
            f.close()

            self.yNames = Counter(self.y).keys()


        else:

            data = gzip.GzipFile(self.path).readlines()

            self.X = []
            self.y = []


            for dp in data:
                clean = str(dp).strip("\n").strip(".").split(",")
                self.X.append(clean[:-1])
                self.y.append(clean[-1])

            self.yNames = Counter(self.y).keys()
            self.cleanData()

            f = open("pickled/XFeats.pkl", 'wb')
            pickle.dump(self.X, f)
            f.close()

            f = open("pickled/yFeats.pkl", 'wb')
            pickle.dump(self.y, f)
            f.close()

        if LOAD_AE:

            f = open("pickled/autoencode.pkl", "rb")
            auto = pickle.load(f)
            f.close()
        else:

            auto = AutoEncoders(self.X, self.y)
            auto.fit()

            # f = open("pickled/autoencode.pkl", "wb")
            # pickle.dump(auto, f)
            # f.close()

        self.X = auto.encode(self.X)

        dbn = DBN(self.X, self.y)
        dbn.fit()

    def getFeats(self):

        return self.X, self.y, self.yNames


    def cleanData(self):

        print "Cleaning the raw data.........."
        try:
            names = {'x1': [], 'x2': [], 'x3': []}

            for i in range(len(self.X)):
                for j in range(len(self.X[i])):
                    if j == 1:
                        if self.X[i][j] in names['x1']:
                            self.X[i][j] = names['x1'].index(self.X[i][j])
                        else:
                            print self.X[i][j]
                            names['x1'].append(self.X[i][j])
                            self.X[i][j] = names['x1'].index(self.X[i][j])
                    elif j == 2:
                        if self.X[i][j] in names['x2']:
                            self.X[i][j] = names['x2'].index(self.X[i][j])
                        else:
                            print self.X[i][j]
                            names['x2'].append(self.X[i][j])
                            self.X[i][j] = names['x2'].index(self.X[i][j])
                    elif j == 3:
                        if self.X[i][j] in names['x3']:
                            self.X[i][j] = names['x3'].index(self.X[i][j])
                        else:
                            print self.X[i][j]
                            names['x3'].append(self.X[i][j])
                            self.X[i][j] = names['x3'].index(self.X[i][j])
                    else:
                        self.X[i][j] = float(self.X[i][j])

            for i in range(len(self.y)):

                if self.y[i] in self.yNames:
                    self.y[i] = self.yNames.index(self.y[i])

                else:
                    raise Exception

        except Exception as e:
            print "Error in cleaning data."
            print str(e.args), str(e.message)
            exit(0)





PreProcess("data/kddcup.data_10_percent.gz")
