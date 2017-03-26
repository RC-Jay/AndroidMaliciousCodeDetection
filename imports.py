import gzip
import pandas as pd
from collections import Counter
import scipy as sp
from keras.layers import Input, Dense
from keras.models import Model
from numpy.random import seed
from sklearn.model_selection import train_test_split
import numpy as np
import pickle
from sklearn.svm import SVC, LinearSVC, NuSVR
from sklearn.metrics import classification_report
from dbn.models import UnsupervisedDBN
from sklearn.pipeline import Pipeline

LOAD_DATA = True
LOAD_AE = False