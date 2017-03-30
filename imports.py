import gzip
import pandas as pd
from collections import Counter
import scipy as sp
from keras.layers import Input, Dense
from keras.models import Model
from numpy.random import seed
from sklearn.cross_validation import train_test_split
import numpy as np
import pickle
from sklearn.svm import SVC, LinearSVC, NuSVR
from sklearn.metrics import classification_report
from dbn.models import UnsupervisedDBN
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import mutual_info_classif as mic
import glob
from  DL import *
from androguard.misc import *

LOAD_DATA = False
LOAD_AE = False
LOAD_FEATS = False

MAX_DATA = 200
