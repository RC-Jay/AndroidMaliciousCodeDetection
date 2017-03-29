
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
