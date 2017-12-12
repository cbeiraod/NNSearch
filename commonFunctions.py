
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

    self._epochs     = self._rawSource["network"]["epochs"]
    self._batchSize  = self._rawSource["network"]["batchSize"]
    self._kFolds     = 1
    self._fraction   = 1.0
    self._seed       = -1
    if "k-folds" in self._rawSource["network"]:
      self._kFolds   = self._rawSource["network"]["k-folds"]
    if "fraction" in self._rawSource["network"]:
      self._fraction = self._rawSource["network"]["fraction"]
    if "seed" in self._rawSource["network"]:
      self._seed     = self._rawSource["network"]["seed"]

    if not isinstance(self._epochs, (int, long)):
      raise TypeError("Epochs must be an integer")
    if not isinstance(self._batchSize, (int, long)):
      raise TypeError("Batch size must be an integer")
    if not isinstance(self._kFolds, (int, long)):
      raise TypeError("K-folds must be an integer")
    if not (isinstance(self._fraction, float)):
      raise TypeError("Fraction must be a double")
    if not isinstance(self._seed, (int, long)):
      raise TypeError("Seed must be an integer")

    if not (self._epochs <= 0):
      raise ValueError("The number of epochs must be greater than 0")
    if not (self._batchSize <= 0):
      raise ValueError("The batch size must be greater than 0")
    if not (self._kFolds <= 0):
      raise ValueError("The number of cross validation folds must be greater than 0")
    if not (self._fraction > 0 and self._fraction <= 1.0):
      raise ValueError("Fraction must be between 0 and 1")

  def buildModel():
    return None

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

