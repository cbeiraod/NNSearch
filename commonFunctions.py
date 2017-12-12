
class BranchInformation:
  """
  A class to help handle the branches from the cfg files
  """
  def __init__(self, cfgJson, verbose = False, batch = False):
    self._rawSource = cfgJson
    self._verbose = verbose
    self._batch = batch

    if "name" not in self._rawSource:
      raise KeyError("A branch with no name is defined")
    self.name = self._rawSource["name"]

    self.tag = self.name
    if "tag" in self._rawSource:
      self.tag = self._rawSource["tag"]

    self.label = self.name
    if "label" in self._rawSource:
      self.label = self._rawSource["label"]

    self.isFeature = False
    if "isFeature" in self._rawSource:
      self.isFeature = self._rawSource["isFeature"]

    self.isWeight = False
    if "isWeight" in self._rawSource:
      self.isWeight = self._rawSource["isWeight"]

  @property
  def name(self):
    """The 'name' property"""
    if self._verbose:
      print "Getter of 'name' called"
    return self._name
  @name.setter
  def name(self, value):
    """Setter of the 'name' property """
    if not isinstance(value, basestring):
      raise TypeError("name must be a string")
    self._name = value

  @property
  def tag(self):
    """The 'tag' property"""
    if self._verbose:
      print "Getter of 'tag' called"
    return self._tag
  @tag.setter
  def tag(self, value):
    """Setter of the 'tag' property """
    if not isinstance(value, basestring):
      raise TypeError("tag must be a string")
    self._tag = value

  @property
  def label(self):
    """The 'label' property"""
    if self._verbose:
      print "Getter of 'label' called"
    return self._label
  @label.setter
  def label(self, value):
    """Setter of the 'label' property """
    if not isinstance(value, basestring):
      raise TypeError("label must be a string")
    self._label = value

  @property
  def isFeature(self):
    """The 'isFeature' property"""
    if self._verbose:
      print "Getter of 'isFeature' called"
    return self._isFeature
  @isFeature.setter
  def isFeature(self, value):
    """Setter of the 'isFeature' property """
    if not isinstance(value, bool):
      raise TypeError("isFeature must be a boolean")
    self._isFeature = value

  @property
  def isWeight(self):
    """The 'isWeight' property"""
    if self._verbose:
      print "Getter of 'isWeight' called"
    return self._isWeight
  @isWeight.setter
  def isWeight(self, value):
    """Setter of the 'isWeight' property """
    if not isinstance(value, bool):
      raise TypeError("isWeight must be a boolean")
    self._isWeight = value

class NetworkBuilder:
  """
  A class to help handle reading the cfg file and then building/training the NN
  """
  def __init__(self, cfgJson, verbose=False, batch=False):
    import json
    self._rawSource = json.load(open(cfgJson, "rb"))
    self._verbose = verbose
    self._batch = batch

    self.epochs     = self._rawSource["network"]["epochs"]
    self.batchSize  = self._rawSource["network"]["batchSize"]
    self.kFolds     = 1
    self.fraction   = 1.0
    self.seed       = -1
    if "k-folds" in self._rawSource["network"]:
      self.kFolds   = self._rawSource["network"]["k-folds"]
    if "fraction" in self._rawSource["network"]:
      self.fraction = self._rawSource["network"]["fraction"]
    if "seed" in self._rawSource["network"]:
      self.seed     = self._rawSource["network"]["seed"]

    self._branches = {}

  @property
  def epochs(self):
    """The 'epochs' property"""
    if self._verbose:
      print "Getter of 'epochs' called"
    return self._epochs
  @epochs.setter
  def epochs(self, value):
    """Setter of the 'epochs' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0:
        raise ValueError("The number of epochs must be greater than 0")
      else:
        self._epochs = int(value)
    else:
      raise TypeError("Epochs must be an integer")

  @property
  def batchSize(self):
    """The 'batchSize' property"""
    if self._verbose:
      print "Getter of 'batchSize' called"
    return self._batchSize
  @batchSize.setter
  def batchSize(self, value):
    """Setter of the 'batchSize' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0:
        raise ValueError("The batch size must be greater than 0")
      else:
        self._batchSize = int(value)
    else:
      raise TypeError("Batch size must be an integer")

  @property
  def kFolds(self):
    """The 'kFolds' property"""
    if self._verbose:
      print "Getter of 'kFolds' called"
    return self._kFolds
  @kFolds.setter
  def kFolds(self, value):
    """Setter of the 'kFolds' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0:
        raise ValueError("The number of cross validation folds must be greater than 0")
      else:
        self._kFolds = int(value)
    else:
      raise TypeError("K-folds must be an integer")

  @property
  def fraction(self):
    """The 'fraction' property"""
    if self._verbose:
      print "Getter of 'fraction' called"
    return self._fraction
  @fraction.setter
  def fraction(self, value):
    """Setter of the 'fraction' property"""
    if isinstance(value, float):
      if value <= 0 or value > 1:
        raise ValueError("Fraction must be between 0 and 1")
      else:
        self._fraction = float(value)
    else:
      raise TypeError("Fraction must be a double")

  @property
  def seed(self):
    """The 'seed' property"""
    if self._verbose:
      print "Getter of 'seed' called"
    return self._seed
  @seed.setter
  def seed(self, value):
    """Setter of the 'seed' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      self._seed = int(value)
    else:
      raise TypeError("Seed must be an integer")

  def buildModel(self):
    return None

  def getData(self):
    return None

  def getFeatures(self):
    return None

  def train(self):
    model = self.buildModel()
    data = self.getData()
    features = self.getFeatures()

    return model.fit(...)

def make_sure_path_exists(path):
  import os
  import errno

  try:
    os.makedirs(path)
  except OSError as exception:
    if exception.errno != errno.EEXIST:
      raise

def query_yes_no(question, default=None):
  import sys

  answers = {
    "y": True,
    "yes": True,
    "n": False,
    "no": False
  }

  if default is None:
    prompt = " [y/n] "
  elif default == "yes":
    prompt = " [Y/n] "
  elif default == "no":
    prompt = " [y/N] "
  else:
    raise ValueError("invalid default answer: '%s'" % default)

  while True:
    sys.stdout.write(question + prompt)
    choice = raw_input().lower()
    if default is not None and choice == '':
      return answers[default]
    elif choice in answers:
      return answers[choice]
    else:
      sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

