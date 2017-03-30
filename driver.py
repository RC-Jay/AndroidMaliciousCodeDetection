from imports import *
from util import *
from DL import *

################# Driver code #####################

data = PreProcess("/media/jaydeep/Just Tv/Dataset/")
if micBeforeAE:
    X, y = data.getFeaturesMutualInfoClassif()
else:
    X, y = data.getFeats()

# Autoencoder used to reduce dimensionality of data
ae = AutoEncoders(X,y)
ae.fit()

X = ae.encode(np.array(X)) # Encoding/Mapping the exisiting feature set to lower dimensional space.

if micAfterAE:
    micIdx = mic(X.values[:, :].astype(float), y)
    idx = np.nonzero(micIdx)
    return (np.array(X)[idx], y[idx])

print(X[0])

dbn = DBN(X,y)
print dbn.fit()
