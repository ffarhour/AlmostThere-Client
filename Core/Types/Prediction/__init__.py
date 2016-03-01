
from .Predictor import Native

if Native == True:
	from ._Predictor import Predictor
else:
	from .Predictor import Predictor
