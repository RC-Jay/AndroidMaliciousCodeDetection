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

class AutoEncoders(object):

    def __init__(self, X, y):

        self.X = np.array(X, dtype=float)
        self.y = y
        self.encoding_dim = 3

    def fit(self):

        ncol = self.X.shape[1]
        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.y, train_size=0.7, random_state=seed(2017))

        input_dim = Input(shape=(ncol,))
        # DEFINE THE DIMENSION OF ENCODER ASSUMED 10

        # DEFINE THE ENCODER LAYER
        encoded = Dense(self.encoding_dim, activation='relu')(input_dim)
        # DEFINE THE DECODER LAYER
        decoded = Dense(ncol, activation='sigmoid')(encoded)
        # COMBINE ENCODER AND DECODER INTO AN AUTOENCODER MODEL
        autoencoder = Model(input=input_dim, output=decoded)
        # CONFIGURE AND TRAIN THE AUTOENCODER
        autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
        autoencoder.fit(X_train, X_train, nb_epoch=5, batch_size=100, shuffle=True, validation_data=(X_test, X_test))
        # THE ENCODER TO EXTRACT THE REDUCED DIMENSION FROM THE ABOVE AUTOENCODER
        self.encoder = Model(input=input_dim, output=encoded)

        # encoded_input = Input(shape=(encoding_dim,))
        # encoded_out = encoder.predict(X_test)
        # print encoded_out[0:2]

    def encode(self, dp):

        dp = np.array(dp, dtype=float)
        encoded_input = Input(shape=(self.encoding_dim,))
        return self.encoder.predict(dp)

class DBN(object):

    def __init__(self, X, y):

        self.X = np.array(X, dtype=float)
        self.y = y

        svm = SVC()
        dbn = UnsupervisedDBN(hidden_layers_structure=[256, 512],
                              batch_size=10,
                              learning_rate_rbm=0.06,
                              n_epochs_rbm=2,
                              activation_function='sigmoid')

        self.classifier = Pipeline(steps=[('dbn', dbn),
                                     ('svm', svm)])

    def fit(self):

        X_train, X_test, Y_train, Y_test = train_test_split(self.X, self.y, train_size=0.7, random_state=seed(2017))
        self.classifier.fit(X_train, Y_train)

        return classification_report(Y_test, self.predict(X_test))

    def predict(self, X):

        return self.classifier.predict(X)



PreProcess("data/kddcup.data_10_percent.gz")
