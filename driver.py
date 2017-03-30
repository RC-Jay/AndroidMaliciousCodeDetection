from imports import *
from util import *
from DL import *

data = PreProcess("/media/jaydeep/Just Tv/Dataset/")
X, y = data.getFeats()
ae = AutoEncoders(X,y)
ae.fit()
