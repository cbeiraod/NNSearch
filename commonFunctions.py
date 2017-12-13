
class BranchInformation(object):
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

class NetworkTopology(object):
  """
  A class to help handle the network topology
  """
  def __init__(self, cfgJson, verbose = False, batch = False):
    self._rawSource = cfgJson
    self._verbose = verbose
    self._batch = batch

class NetworkOptimizer(object):
  """
  A class to help handle the network optimizer
  """
  def __init__(self, cfgJson, verbose = False, batch = False):
    self._rawSource = cfgJson
    self._verbose = verbose
    self._batch = batch
    self._recognizedOptimizers = ["SGD", "sgd", "Adam", "adam", "Nadam", "nadam"]
    self._availableKeys = []

    if "optimizer" not in self._rawSource:
      raise KeyError("No optimizer is defined")
    self.optimizer = self._rawSource["optimizer"]

    self.parameters = {}
    for key, value in self._rawSource.items():
      if key == "optimizer":
        continue
      if self.optimizer in self._recognizedOptimizers and key not in self._availableKeys:
        raise ValueError("the key '" + key + "' is not recognised for optimizer '" + self.optimizer + "'")
      #self.parameters[key.encode('ascii','ignore')] = value
      self.parameters[key] = value

  @property
  def optimizer(self):
    """The 'optimizer' property"""
    if self._verbose:
      print "Getter of 'optimizer' called"
    return self._optimizer
  @optimizer.setter
  def optimizer(self, value):
    """Setter of the 'optimizer' property """
    if not isinstance(value, basestring):
      raise TypeError("optimizer must be a string")
    if value not in self._recognizedOptimizers:
      print "A not recognised optimizer was chosen,",
      if self._batch:
        print " trusting that the parameters in the cfg are correctly set up"
      else:
        if not query_yes_no(" do you want to trust the parameters as in the cfg file?", "n"):
          raise ValueError("not recognised optimizer")

    import inspect
    from keras import optimizers
    existingOptimizers = []
    for name in dir(optimizers):
      element = getattr(optimizers, name)
      if inspect.isclass(element):
        existingOptimizers.append(name)
    if value not in existingOptimizers:
      raise ValueError("chosen optimizer does not exist")

    self._optimizer = value

    switchStatement = {
      "SGD": lambda: ["clipnorm", "clipvalue", "lr", "momentum", "decay", "nesterov"],
      "sgd": lambda: switchStatement["SGD"](),
      "Adam": lambda: ["clipnorm", "clipvalue", "lr", "beta_1", "beta_2", "epsilon", "decay"],
      "adam": lambda: switchStatement["Adam"](),
      "Nadam": lambda: ["clipnorm", "clipvalue", "lr", "beta_1", "beta_2", "epsilon", "schedule_decay"],
      "nadam": lambda: switchStatement["Nadam"]()
    }

    try:
      self._availableKeys = switchStatement[self._optimizer]()
    except KeyError:
      self._availableKeys = []

  @property
  def parameters(self):
    """The 'parameters' property"""
    if self._verbose:
      print "Getter of 'parameters' called"
    return self._parameters
  @parameters.setter
  def parameters(self, value):
    """Setter of the 'parameters' property """
    if isinstance(value, dict):
      self._parameters = value
    else:
      raise TypeError("Parameters must be a dictionary")

  def build(self):
    from keras import optimizers
    element = getattr(optimizers, self.optimizer)
    return element(**self.parameters)


class NetworkBuilder(object):
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

    self.branches = {}
    for branch in self._rawSource["network"]["branches"]:
      tmp = BranchInformation(branch, verbose=self._verbose, batch=self._batch)
      self.branches[tmp.name] = tmp

    self.topology  = NetworkTopology (self._rawSource["network"]["topology"],  verbose=self._verbose, batch=self._batch)
    self.optimizer = NetworkOptimizer(self._rawSource["network"]["optimizer"], verbose=self._verbose, batch=self._batch)

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

  @property
  def branches(self):
    """The 'branches' property"""
    if self._verbose:
      print "Getter of 'branches' called"
    return self._branches
  @branches.setter
  def branches(self, value):
    """Setter of the 'branches' property"""
    if isinstance(value, dict):
      self._branches = value
    else:
      raise TypeError("Branches must be a dictionary")

  @property
  def topology(self):
    """The 'topology' property"""
    if self._verbose:
      print "Getter of 'topology' called"
    return self._topology
  @topology.setter
  def topology(self, value):
    """Setter of the 'topology' property"""
    if isinstance(value, NetworkTopology):
      self._topology = value
    else:
      raise TypeError("Topology must be a NetworkTopology")

  @property
  def optimizer(self):
    """The 'optimizer' property"""
    if self._verbose:
      print "Getter of 'optimizer' called"
    return self._optimizer
  @optimizer.setter
  def optimizer(self, value):
    """Setter of the 'optimizer' property"""
    if isinstance(value, NetworkOptimizer):
      self._optimizer = value
    else:
      raise TypeError("Topology must be a NetworkOptimizer")

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

    #return model.fit(...)

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

