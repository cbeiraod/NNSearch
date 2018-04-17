import root_numpy
import pandas
import numpy as np
from sklearn.preprocessing import StandardScaler

class BranchInformation(object):
  """
  A class to help handle the branches from the cfg files
  """
  def __init__(self, cfgJson, verbose = False, batch = False, tmpdir = None):
    self._tmpdir = tmpdir
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
  def __init__(self, cfgJson, verbose = False, batch = False, tmpdir = None):
    self._tmpdir = tmpdir
    self._rawSource = cfgJson
    self._verbose = verbose
    self._batch = batch

    self.type = self._rawSource["type"]

    if self.type == "simple":
      self.nLayers = self._rawSource["nLayers"]
      self.neurons = self._rawSource["neurons"]

      self.activation = "relu"
      if "activation" in self._rawSource:
        self.activation = self._rawSource["activation"]

      self.dropout = 0
      if "dropout" in self._rawSource:
        self.dropout = self._rawSource["dropout"]

      self.l1 = 0
      if "l1" in self._rawSource:
        self.l1 = self._rawSource["l1"]

      self.l2 = 0
      if "l2" in self._rawSource:
        self.l2 = self._rawSource["l2"]

  @property
  def type(self):
    """This is 'type' property"""
    if self._verbose:
      print "Getter of 'type' is called"
    return self._type
  @type.setter
  def type(self, value):
    """Setter of 'type' property"""
    if not isinstance(value, basestring):
      raise TypeError("type must be a string")
    allTypes = ['simple']
    if value not in allTypes:
      raise ValueError("type is not a recognized type")
    self._type = value

  @property
  def activation(self):
    """This is 'activation' property"""
    if self._verbose:
      print "Getter of 'activation' is called"
    return self._activation
  @activation.setter
  def activation(self, value):
    """Setter of 'activation' property"""
    if not isinstance(value, basestring):
      raise TypeError("activation must be a string")
    allActivations = ['relu', 'selu']
    if value not in allActivations:
      raise ValueError("activation is not a recognized activation")
    self._activation = value

  @property
  def nLayers(self):
    """The 'nLayers' property"""
    if self._verbose:
      print "Getter of 'nLayers' called"
    return self._nLayers
  @nLayers.setter
  def nLayers(self, value):
    """Setter of the 'nLayers' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0:
        raise ValueError("The number of nLayers must be greater than 0")
      else:
        self._nLayers = int(value)
    else:
      raise TypeError("nLayers must be an integer")

  @property
  def neurons(self):
    """The 'neurons' property"""
    if self._verbose:
      print "Getter of 'neurons' called"
    return self._neurons
  @neurons.setter
  def neurons(self, value):
    """Setter of the 'neurons' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0:
        raise ValueError("The number of neurons must be greater than 0")
      else:
        self._neurons = int(value)
    else:
      raise TypeError("neurons must be an integer")

  @property
  def dropout(self):
    """The 'dropout' property"""
    if self._verbose:
      print "Getter of 'dropout' called"
    return self._dropout
  @dropout.setter
  def dropout(self, value):
    """Setter of the 'dropout' property"""
    if isinstance(value, (int, long, float)):
      if value < 0 or value >= 1:
        raise ValueError("Fraction must be between 0 and 1")
      else:
        self._dropout = float(value)
    else:
      raise TypeError("dropout must be a double")

  @property
  def l1(self):
    """The 'l1' property"""
    if self._verbose:
      print "Getter of 'l1' called"
    return self._l1
  @l1.setter
  def l1(self, value):
    """Setter of the 'l1' property"""
    if isinstance(value, (int, long, float)):
      if value < 0:
        raise ValueError("L1 must be positive")
      else:
        self._l1 = float(value)
    else:
      raise TypeError("L1 must be a double")

  @property
  def l2(self):
    """The 'l2' property"""
    if self._verbose:
      print "Getter of 'l2' called"
    return self._l2
  @l2.setter
  def l2(self, value):
    """Setter of the 'l2' property"""
    if isinstance(value, (int, long, float)):
      if value < 0:
        raise ValueError("L2 must be positive")
      else:
        self._l2 = float(value)
    else:
      raise TypeError("L2 must be a double")

  def buildModel(self, nIn, nOut, compileArgs):
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, AlphaDropout
    from keras.regularizers import l1_l2

    if self.type == "simple":
      model = Sequential()
      model.add(Dense(self.neurons, input_dim=nIn, kernel_initializer='he_normal', activation=self.activation, kernel_regularizer=l1_l2(l1=self.l1, l2=self.l2)))
      if self.dropout > 0:
        if self.activation == "selu":
          model.add(AlphaDropout(self.dropout))
        else:
          model.add(Dropout(self.dropout))
      for i in range(self.nLayers - 1):
        model.add(Dense(self.neurons, kernel_initializer='he_normal', activation=self.activation, kernel_regularizer=l1_l2(l1=self.l1, l2=self.l2)))
        if self.dropout > 0:
          if self.activation == "selu":
            model.add(AlphaDropout(self.dropout))
          else:
            model.add(Dropout(self.dropout))
      model.add(Dense(nOut, activation="sigmoid", kernel_initializer='glorot_normal',kernel_regularizer=l1_l2(l1=self.l1, l2=self.l2)))
      model.compile(**compileArgs)
      return model
    return None

class NetworkOptimizer(object):
  """
  A class to help handle the network optimizer
  """
  def __init__(self, cfgJson, verbose = False, batch = False, tmpdir = None):
    self._tmpdir = tmpdir
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
        raise KeyError("the key '" + key + "' is not recognised for optimizer '" + self.optimizer + "'")
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

class SampleComponents(object):
  """
  A class to help handle reading the sample components
  """
  def __init__(self, cfgJson, sampleType, basePath, foldsPath, foldedPath, foldSuffix, suffix = "", verbose = False, batch = False, tmpdir = None):
    self._tmpdir = tmpdir
    self._rawSource = cfgJson
    self._verbose = verbose
    self._batch = batch
    self._sampleType = sampleType
    self._basePath = basePath
    self._foldedPath = foldedPath
    self._foldsPath = foldsPath
    self._foldSuffix = foldSuffix
    self._suffix = suffix

    if "name" not in self._rawSource:
      raise KeyError("A component with no name is defined")
    self.name = self._rawSource["name"]

    self.tag = self.name
    if "tag" in self._rawSource:
      self.tag = self._rawSource["tag"]

    self.label = self.name
    if "label" in self._rawSource:
      self.label = self._rawSource["label"]

    if "color" not in self._rawSource:
      raise KeyError("A component with no color is defined")
    self.color = self._rawSource["color"]

    self.lcolor = 1
    if "lcolor" in self._rawSource:
      self.lcolor = self._rawSource["lcolor"]

    self.lwidth = 1
    if "lwidth" in self._rawSource:
      self.lwidth = self._rawSource["lwidth"]

    self.lstyle = 1
    if "lstyle" in self._rawSource:
      self.lstyle = self._rawSource["lstyle"]

    import os.path
    if self._sampleType == "unified":
      self.files = []
      if "files" not in self._rawSource:
        raise KeyError("A component with no files is defined")
      for file in self._rawSource["files"]:
        filename = file
        if suffix != "":
          filename = filename + "_" + suffix
        if not os.path.isfile(self._basePath + "/" + filename + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (component: " + self.name + ")")
        if not os.path.isfile(self._foldsPath + "/" + filename + "_" + foldSuffix + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (folds of component: " + self.name + ")")
        if not os.path.isfile(self._foldedPath + "/" + filename + "_" + foldSuffix + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (fold file of component: " + self.name + ")")
        self.files.append(filename)
    elif self._sampleType == "legacy":
      self.testFiles = []
      self.trainFiles = []
      if "testFiles" not in self._rawSource:
        raise KeyError("A component with no testFiles is defined")
      if "trainFiles" not in self._rawSource:
        raise KeyError("A component with no trainFiles is defined")
      for file in self._rawSource["testFiles"]:
        filename = file
        if suffix != "":
          filename = filename + "_" + suffix
        if not os.path.isfile(self._basePath + "/" + filename + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (component: " + self.name + ")")
        if not os.path.isfile(self._foldsPath + "/" + filename + "_" + foldSuffix + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (folds of component: " + self.name + ")")
        if not os.path.isfile(self._foldedPath + "/" + filename + "_" + foldSuffix + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (fold file of component: " + self.name + ")")
        self.testFiles.append(filename)
      for file in self._rawSource["trainFiles"]:
        filename = file
        if suffix != "":
          filename = filename + "_" + suffix
        if not os.path.isfile(self._basePath + "/" + filename + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (component: " + self.name + ")")
        if not os.path.isfile(self._foldsPath + "/" + filename + "_" + foldSuffix + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (folds of component: " + self.name + ")")
        if not os.path.isfile(self._foldedPath + "/" + filename + "_" + foldSuffix + ".root"):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (fold file of component: " + self.name + ")")
        self.trainFiles.append(filename)

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
  def color(self):
    """The 'color' property"""
    if self._verbose:
      print "Getter of 'color' called"
    return self._color
  @color.setter
  def color(self, value):
    """Setter of the 'color' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      self._color = int(value)
    else:
      raise TypeError("color must be an integer")

  @property
  def lcolor(self):
    """The 'lcolor' property"""
    if self._verbose:
      print "Getter of 'lcolor' called"
    return self._lcolor
  @lcolor.setter
  def lcolor(self, value):
    """Setter of the 'lcolor' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      self._lcolor = int(value)
    else:
      raise TypeError("lcolor must be an integer")

  @property
  def lwidth(self):
    """The 'lwidth' property"""
    if self._verbose:
      print "Getter of 'lwidth' called"
    return self._lwidth
  @lwidth.setter
  def lwidth(self, value):
    """Setter of the 'lwidth' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0:
        raise ValueError("The lwidth must be greater than 0")
      else:
        self._lwidth = int(value)
    else:
      raise TypeError("lwidth must be an integer")

  @property
  def lstyle(self):
    """The 'lstyle' property"""
    if self._verbose:
      print "Getter of 'lstyle' called"
    return self.lstyler
  @lstyle.setter
  def lstyle(self, value):
    """Setter of the 'lstyle' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0 or value > 10:
        raise ValueError("The lstyle must be greater than 0 and smaller or equal to 10")
      else:
        self._lstyle = int(value)
    else:
      raise TypeError("lstyle must be an integer")

  @property
  def files(self):
    """The 'files' property"""
    if self._verbose:
      print "Getter of 'files' called"
    return self._files
  @files.setter
  def files(self, value):
    """Setter of the 'files' property """
    if not isinstance(value, list):
      raise TypeError("files must be a list")
    self._files = value

  @property
  def testFiles(self):
    """The 'testFiles' property"""
    if self._verbose:
      print "Getter of 'testFiles' called"
    return self._testFiles
  @testFiles.setter
  def testFiles(self, value):
    """Setter of the 'testFiles' property """
    if not isinstance(value, list):
      raise TypeError("testFiles must be a list")
    self._testFiles = value

  @property
  def trainFiles(self):
    """The 'trainFiles' property"""
    if self._verbose:
      print "Getter of 'trainFiles' called"
    return self._trainFiles
  @trainFiles.setter
  def trainFiles(self, value):
    """Setter of the 'trainFiles' property """
    if not isinstance(value, list):
      raise TypeError("trainFiles must be a list")
    self._trainFiles = value

  def getData(self, selection, branches, fraction, skipSystematics=False):
    Data = None

    tmpFile = None
    if self._tmpdir is not None:
      import ROOT
      tmpFile = ROOT.TFile(self._tmpdir + "/tmpFile.root", "RECREATE")

    if "weight" not in branches:
      branches.append("weight")
    if "Event" not in branches:
      branches.append("Event")

    foldBranches = ["foldID", "fold_a"]
    if self._foldSuffix[0] == "k":
      foldBranches = foldBranches + ["fold_b"]

    if self._sampleType == "unified":
      for file in self.files:
        npData = root_numpy.root2array(
                                        self._foldedPath + "/" + file + "_" + self._foldSuffix + ".root",
                                        treename="bdttree",
                                        selection=selection,
                                        branches=branches + foldBranches
                                      )

        if fraction < 1.0:
          npData = npData[:int(len(npData)*fraction)]

        if Data is None:
          Data = pandas.DataFrame(npData)
        else:
          Data = Data.append(pandas.DataFrame(npData), ignore_index=True)

        npData = None

      if fraction < 1.0:
        Data.weight = Data.weight/fraction

    elif self._sampleType == "legacy":
      for file in self.trainFiles:
        npData = root_numpy.root2array(
                                        self._foldedPath + "/" + file + "_" + self._foldSuffix + ".root",
                                        treename="bdttree",
                                        selection=selection,
                                        branches=branches + foldBranches
                                      )

        if fraction < 1.0:
          npData = npData[:int(len(npData)*fraction)]

        if Data is None:
          Data = pandas.DataFrame(npData)
        else:
          Data = Data.append(pandas.DataFrame(npData), ignore_index=True)

        npData = None

      for file in self.testFiles:
        npData = root_numpy.root2array(
                                        self._foldedPath + "/" + file + "_" + self._foldSuffix + ".root",
                                        treename="bdttree",
                                        selection=selection,
                                        branches=branches + foldBranches
                                      )

        if fraction < 1.0:
          npData = npData[:int(len(npData)*fraction)]

        if Data is None:
          Data = pandas.DataFrame(npData)
        else:
          Data = Data.append(pandas.DataFrame(npData), ignore_index=True)

        npData = None

      if fraction < 1.0:
        Data.weight = Data.weight/fraction

    else:
      raise ValueError("Unknown type '" + self._sampleType + "'")

    if tmpFile is not None:
      tmpFile.Close()

    return Data

class NetworkSample(object):
  """
  A class to help handle reading the sample files
  """
  def __init__(self, cfgJson, preselection, fraction, branches, foldSuffix, verbose = False, batch = False, tmpdir = None):
    self._tmpdir = tmpdir
    self._rawSource = cfgJson
    self._verbose = verbose
    self._batch = batch
    self._preselection = preselection
    self._fraction = fraction
    self._branches = branches
    self._foldSuffix = foldSuffix

    if "name" not in self._rawSource:
      raise KeyError("A sample with no name is defined")
    self.name = self._rawSource["name"]

    if "cfgFile" not in self._rawSource:
      raise KeyError("A sample with no cfgFile is defined")
    self.cfgFile = self._rawSource["cfgFile"]

    self.excludeWeight = []
    if "excludeWeight" in self._rawSource:
      self.excludeWeight = self._rawSource["excludeWeight"]

    import json
    self._rawCfg = json.load(open(self.cfgFile, "rb"))

    if "basePath" not in self._rawCfg["sample"]:
      raise KeyError("sample '" + self.name + "' does not have a basePath")
    self.basePath = self._rawCfg["sample"]["basePath"]

    if "foldsPath" not in self._rawCfg["sample"]:
      raise KeyError("sample '" + self.name + "' does not have a foldsPath")
    self.foldsPath = self._rawCfg["sample"]["foldsPath"]

    if "foldedPath" not in self._rawCfg["sample"]:
      raise KeyError("sample '" + self.name + "' does not have a foldedPath")
    self.foldedPath = self._rawCfg["sample"]["foldedPath"]

    self.type = "unified"
    if "type" in self._rawCfg["sample"]:
      self.type = self._rawCfg["sample"]["type"]

    self.suffix = ""
    if "suffix" in self._rawCfg["sample"]:
      self.suffix = self._rawCfg["sample"]["suffix"]

    self.components = {}
    if "components" not in self._rawCfg["sample"]:
      raise KeyError("sample '" + self.name + "' does not have any components")
    for component in self._rawCfg["sample"]["components"]:
      tmp = SampleComponents(component, self.type, self.basePath, self.foldsPath, self.foldedPath, self._foldSuffix, suffix = self.suffix, verbose = self._verbose, batch = self._batch, tmpdir=self._tmpdir)
      self.components[tmp.name] = tmp

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
  def cfgFile(self):
    """The 'cfgFile' property"""
    if self._verbose:
      print "Getter of 'cfgFile' called"
    return self._cfgFile
  @cfgFile.setter
  def cfgFile(self, value):
    """Setter of the 'cfgFile' property """
    if not isinstance(value, basestring):
      raise TypeError("cfgFile must be a string")
    self._cfgFile = value

  @property
  def excludeWeight(self):
    """The 'excludeWeight' property"""
    if self._verbose:
      print "Getter of 'excludeWeight' called"
    return self._excludeWeight
  @excludeWeight.setter
  def excludeWeight(self, value):
    """Setter of the 'excludeWeight' property """
    if not isinstance(value, list):
      raise TypeError("excludeWeight must be a list")
    self._excludeWeight = value

  @property
  def type(self):
    """The 'type' property"""
    if self._verbose:
      print "Getter of 'type' called"
    return self._type
  @type.setter
  def type(self, value):
    """Setter of the 'type' property """
    if not isinstance(value, basestring):
      raise TypeError("type must be a string")
    validTypes = ["unified", "legacy"]
    if value not in validTypes:
      raise ValueError("Unknown type '" + value + "'")
    self._type = value

  @property
  def basePath(self):
    """The 'basePath' property"""
    if self._verbose:
      print "Getter of 'basePath' called"
    return self._basePath
  @basePath.setter
  def basePath(self, value):
    """Setter of the 'basePath' property """
    if not isinstance(value, basestring):
      raise TypeError("basePath must be a string")
    import os
    if not os.path.isdir(value):
      import errno
      #raise OSError("'" + value + "' is not a valid path")
      raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), value + " (from file '" + self.cfgFile + "')")
    self._basePath = value

  @property
  def foldsPath(self):
    """The 'foldsPath' property"""
    if self._verbose:
      print "Getter of 'foldsPath' called"
    return self._foldsPath
  @foldsPath.setter
  def foldsPath(self, value):
    """Setter of the 'foldsPath' property """
    if not isinstance(value, basestring):
      raise TypeError("foldsPath must be a string")
    import os
    if not os.path.isdir(value):
      import errno
      #raise OSError("'" + value + "' is not a valid path")
      raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), value + " (from file '" + self.cfgFile + "')")
    self._foldsPath = value

  @property
  def foldedPath(self):
    """The 'foldedPath' property"""
    if self._verbose:
      print "Getter of 'foldedPath' called"
    return self._foldedPath
  @foldedPath.setter
  def foldedPath(self, value):
    """Setter of the 'foldedPath' property """
    if not isinstance(value, basestring):
      raise TypeError("foldedPath must be a string")
    import os
    if not os.path.isdir(value):
      import errno
      #raise OSError("'" + value + "' is not a valid path")
      raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), value + " (from file '" + self.cfgFile + "')")
    self._foldedPath = value

  @property
  def suffix(self):
    """The 'suffix' property"""
    if self._verbose:
      print "Getter of 'suffix' called"
    return self._suffix
  @suffix.setter
  def suffix(self, value):
    """Setter of the 'suffix' property """
    if not isinstance(value, basestring):
      raise TypeError("suffix must be a string")
    self._suffix = value

  @property
  def components(self):
    """The 'components' property"""
    if self._verbose:
      print "Getter of 'components' called"
    return self._components
  @components.setter
  def components(self, value):
    """Setter of the 'components' property"""
    if isinstance(value, dict):
      self._components = value
    else:
      raise TypeError("Components must be a dictionary")

  def getData(self, skipSystematics=False):
    Data = None

    componentID = 0
    for componentName in self.components:
      component = self.components[componentName]
      componentData = component.getData(self._preselection, self._branches.keys(), self._fraction, skipSystematics=skipSystematics)
      componentData["NNSearch_componentID"] = componentID
      componentID += 1

      if Data is None:
        Data = componentData
      else:
        Data = Data.append(componentData, ignore_index=True)

    Data["sampleWeight"] = Data.weight

    for weight in self.excludeWeight:
      Data.sampleWeight = Data.sampleWeight/Data[weight]

    return Data

class NetworkBuilder(object):
  """
  A class to help handle reading the cfg file and then building/training the NN
  """
  def __init__(self, cfgJson, verbose = False, batch = False, tmpdir = None):
    import json
    self._tmpdir = tmpdir
    self._rawSource = json.load(open(cfgJson, "rb"))
    self._verbose = verbose
    self._batch = batch
    self.transformations = {}
    self._foldInfo = {}

    self.name            = self._rawSource["network"]["name"]
    self.epochs          = self._rawSource["network"]["epochs"]
    self.batchSize       = self._rawSource["network"]["batchSize"]
    self.splitting       = "n-fold"
    self.splittingType   = "random"
    self.numberFolds     = 3
    self.splittingSeed   = -1
    self.doCombinatorics = False
    self.fraction        = 1.0
    self.seed            = -1
    self.multiple        = 1
    self.preselection    = ""
    if "splittingType" in self._rawSource["network"]:
      self.splittingType   = self._rawSource["network"]["splittingType"]
    if "splitting" in self._rawSource["network"]:
      self.splitting   = self._rawSource["network"]["splitting"]
    if "numberFolds" in self._rawSource["network"]:
      self.numberFolds   = self._rawSource["network"]["numberFolds"]
    if "splittingSeed" in self._rawSource["network"]:
      self.splittingSeed     = self._rawSource["network"]["splittingSeed"]
    if "doCombinatorics" in self._rawSource["network"]:
      self.doCombinatorics   = self._rawSource["network"]["doCombinatorics"]
    if "fraction" in self._rawSource["network"]:
      self.fraction = self._rawSource["network"]["fraction"]
    if "seed" in self._rawSource["network"]:
      self.seed     = self._rawSource["network"]["seed"]
    if "preselection" in self._rawSource["network"]:
      self.preselection = self._rawSource["network"]["preselection"]
    if "multiple" in self._rawSource["network"]:
      self.multiple     = self._rawSource["network"]["multiple"]

    self.branches = {}
    for branch in self._rawSource["network"]["branches"]:
      tmp = BranchInformation(branch, verbose=self._verbose, batch=self._batch)
      self.branches[tmp.name] = tmp

    self.topology  = NetworkTopology (self._rawSource["network"]["topology"],  verbose=self._verbose, batch=self._batch)
    self.optimizer = NetworkOptimizer(self._rawSource["network"]["optimizer"], verbose=self._verbose, batch=self._batch)

    foldSuffix = ""
    if self.splitting == "n-fold":
      foldSuffix = "n" + str(self.numberFolds)
    elif self.splitting == "k-fold":
      foldSuffix = "k" + str(self.numberFolds)
    self.samples = []
    for sample in self._rawSource["network"]["samples"]:
      tmp = NetworkSample(sample, self.preselection, self.fraction, self.branches, foldSuffix, verbose=self._verbose, batch=self._batch, tmpdir=self._tmpdir)
      self.samples.append(tmp)

    consistentType = True
    firstType = None
    for sample in self.samples:
      if firstType is None:
        firstType = sample.type
      if firstType != sample.type:
        consistentType = False
        break
    if not consistentType:
      raise ValueError("The samples must have consistent types")

    if len(self.getFeatures()) < 1:
      raise ValueError("You must define at least 1 feature")

    if len(self.samples) < 2:
      raise ValueError("You must define at least 2 sample types")

    if self.samples[0].type == "legacy" and self.splitting == "n-fold":
      raise ValueError("Can not do n-folding with legacy samples")

    if self.splitting == "n-fold" and self.numberFolds <= 2:
      raise ValueError("The number of splitting folds must be greater than 2 for n-folding")

    #if self.samples[0].type == "legacy" and self.numberFolds < 2:
    #  self.numberFolds = 2

    np.random.seed(self.seed)

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
  def splitting(self):
    """The 'splitting' property"""
    if self._verbose:
      print "Getter of 'splitting' called"
    return self._splitting
  @splitting.setter
  def splitting(self, value):
    """Setter of the 'splitting' property """
    if not isinstance(value, basestring):
      raise TypeError("splitting must be a string")
    validSplits = ["k-fold", "n-fold"]
    if value not in validSplits:
      raise ValueError("Unknown type '" + value + "'")
    self._splitting = value

  @property
  def splittingType(self):
    """The 'splittingType' property"""
    if self._verbose:
      print "Getter of 'splittingType' called"
    return self._splittingType
  @splittingType.setter
  def splittingType(self, value):
    """Setter of the 'splittingType' property """
    if not isinstance(value, basestring):
      raise TypeError("splittingType must be a string")
    validSplits = ["random", "modulus"]
    if value not in validSplits:
      raise ValueError("Unknown type '" + value + "'")
    self._splittingType = value

  @property
  def numberFolds(self):
    """The 'numberFolds' property"""
    if self._verbose:
      print "Getter of 'numberFolds' called"
    return self._numberFolds
  @numberFolds.setter
  def numberFolds(self, value):
    """Setter of the 'numberFolds' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0:
        raise ValueError("The number of splitting folds must be greater than 0")
      else:
        self._numberFolds = int(value)
    else:
      raise TypeError("number_folds must be an integer")

  @property
  def splittingSeed(self):
    """The 'splittingSeed' property"""
    if self._verbose:
      print "Getter of 'splittingSeed' called"
    return self._splittingSeed
  @splittingSeed.setter
  def splittingSeed(self, value):
    """Setter of the 'splittingSeed' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      self._splittingSeed = int(value)
    else:
      raise TypeError("Splitting seed must be an integer")

  @property
  def doCombinatorics(self):
    """The 'doCombinatorics' property"""
    if self._verbose:
      print "Getter of 'doCombinatorics' called"
    return self._doCombinatorics
  @doCombinatorics.setter
  def doCombinatorics(self, value):
    """Setter of the 'doCombinatorics' property """
    if not isinstance(value, bool):
      raise TypeError("doCombinatorics must be a boolean")
    self._doCombinatorics = value

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

  @property
  def preselection(self):
    """The 'preselection' property"""
    if self._verbose:
      print "Getter of 'preselection' called"
    return self._preselection
  @preselection.setter
  def preselection(self, value):
    """Setter of the 'preselection' property """
    if not isinstance(value, basestring):
      raise TypeError("preselection must be a string")
    self._preselection = value

  @property
  def samples(self):
    """The 'samples' property"""
    if self._verbose:
      print "Getter of 'samples' called"
    return self._samples
  @samples.setter
  def samples(self, value):
    """Setter of the 'samples' property """
    if not isinstance(value, list):
      raise TypeError("samples must be a list")
    self._samples = value

  @property
  def multiple(self):
    """The 'multiple' property"""
    if self._verbose:
      print "Getter of 'multiple' called"
    return self._multiple
  @multiple.setter
  def multiple(self, value):
    """Setter of the 'multiple' property"""
    if isinstance(value, (int, long)) or (isinstance(value, float) and value.is_integer()):
      if value <= 0:
        raise ValueError("The multiplicity of networks to train must be greater than 0")
      else:
        self._multiple = int(value)
    else:
      raise TypeError("multiple must be an integer")

  @property
  def model(self):
    """The 'model' property"""
    if self._verbose:
      print "Getter of 'model' called"
    return self._model
  @model.setter
  def model(self, value):
    """Setter of the 'model' property"""
    self._model = value

  @property
  def transformations(self):
    """The 'transformations' property"""
    if self._verbose:
      print "Getter of 'transformations' called"
    return self._transformations
  @transformations.setter
  def transformations(self, value):
    """Setter of the 'transformations' property"""
    self._transformations = value

  @property
  def history(self):
    """The 'history' property"""
    if self._verbose:
      print "Getter of 'history' called"
    return self._history
  @history.setter
  def history(self, value):
    """Setter of the 'history' property"""
    self._history = value

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

  def getData(self, skipSystematics=False):
    Data = None
    dataArray = []

    i = 0
    for sample in self.samples:
      sampleData = sample.getData(skipSystematics=skipSystematics)
      sampleData["category"] = i
      sampleData.sampleWeight = sampleData.sampleWeight/sampleData.sampleWeight.sum()

      if Data is None:
        Data = sampleData
      else:
        Data = Data.append(sampleData, ignore_index = True)

      i += 1

    return Data

  def getFeatures(self):
    features = []
    for branch in self.branches:
      branchInfo = self.branches[branch]
      if branchInfo.isFeature:
        features = features + [branch]
    return features

  def train(self, skipSystematics=False):
    import keras
    features = self.getFeatures()

    allData = self.getData(skipSystematics=skipSystematics)

    if self.splitting == "n-fold" and len(allData.foldID.unique()) != self.numberFolds:
      raise ValueError("Something went seriously wrong because the folds do not match the requested parameters")
    if self.splitting == "k-fold" and len(allData.foldID.unique()) != 2*self.numberFolds:
      raise ValueError("Something went seriously wrong because the folds do not match the requested parameters")

    XFeatures = allData.ix[:,self.getFeatures()]
    YValues = np.ravel(allData.category)
    if len(self.samples) > 2:
      YValues = keras.utils.to_categorical(YValues, num_classes=len(self.samples))
    weights = np.ravel(allData.sampleWeight)

    # TODO: what about regression? Should use loss MSE and the output of the last layer should not be sigmoid
    compileArgs = {
      "loss": "binary_crossentropy",
      "optimizer": self.optimizer.build(),
      "metrics": ["accuracy"]
    }
    if len(self.samples) > 2:
      compileArgs["loss"] = "categorical_crossentropy"
    #if len(self.samples) == 2: # TODO: Add ROC
    #  compileArgs["metrics"] = compileArgs["metrics"] + ["roc_auc"] # TODO: Add FOM

    outputNeurons = len(self.samples)
    if outputNeurons == 2:
      outputNeurons = 1

    trainParams = {
      "epochs": self.epochs,
      "batch_size": self.batchSize,
      "verbose": 1
    }

    foldCombinatorics = {}
    if self.splitting == "n-fold":
      for test in range(self.numberFolds):
        for val in range(self.numberFolds):
          if test == val:
            continue
          tmp = {}
          tmp["testFoldID"] = test
          tmp["valFoldID"] = val

          tmp["testFold"]  = (allData.foldID == test)
          tmp["valFold"]   = (allData.foldID == val)
          tmp["trainFold"] = np.logical_not(np.logical_or(tmp["testFold"], tmp["valFold"]))

          tmp["testScale"] = self.numberFolds
          tmp["valScale"] = self.numberFolds
          tmp["trainScale"] = self.numberFolds/(self.numberFolds - 2)

          name = "t" + str(test) + "_v" + str(val)
          foldCombinatorics[name] = tmp
    elif self.splitting == "k-fold":
      for test in [0,1]:
        for val in range(self.numberFolds):
          tmp = {}
          tmp["testFoldID"] = test
          tmp["valFoldID"] = val

          tmp["testFold"]  = (allData.fold_a == test)
          tmp["valFold"]   = (allData.foldID == (((test+1)%2)*self.numberFolds + val))
          tmp["trainFold"] = np.logical_not(np.logical_or(tmp["testFold"], tmp["valFold"]))

          tmp["testScale"] = 2
          tmp["valScale"] = self.numberFolds * 2
          tmp["trainScale"] = 2 * self.numberFolds/(self.numberFolds - 1)

          name = "t" + str(test) + "_v" + str(val)
          foldCombinatorics[name] = tmp

          #print "test",  np.unique(tmp["testFold"], return_counts=True)
          #print "val",   np.unique(tmp["valFold"], return_counts=True)
          #print "train", np.unique(tmp["trainFold"], return_counts=True)

    #print np.unique(testFold, return_counts=True)
    #print XFeatures[trainFold].describe()
    #print len(YValues[trainFold])

    self.transformations = []
    self.model = []
    self.history = []
    index = 0
    for name, combinatoricPoint in foldCombinatorics.iteritems():
      transformations, model, history = self.internalTrain(
                                                            name,
                                                            XFeatures[combinatoricPoint["trainFold"]],
                                                            XFeatures[combinatoricPoint["valFold"]],
                                                            YValues[combinatoricPoint["trainFold"]],
                                                            YValues[combinatoricPoint["valFold"]],
                                                            weights[combinatoricPoint["trainFold"]] * combinatoricPoint["trainScale"],
                                                            weights[combinatoricPoint["valFold"]] * combinatoricPoint["valScale"],
                                                            compileArgs,
                                                            trainParams
                                                          )

      self.transformations.append(transformations)
      self.model.append(model)
      self.history.append(history)
      tmp = {'name': name, 'index': index, 'testID': combinatoricPoint["testFoldID"], 'valID': combinatoricPoint["valFoldID"]}
      self._foldInfo[index] = tmp

      index = index + 1
      if not self.doCombinatorics:
        break

    return

  def internalTrain(self, name, XTrain, XValidation, YTrain, YValidation, weightTrain, weightValidation, compileArgs, trainParams):
    outputNeurons = len(self.samples)
    if outputNeurons == 2:
      outputNeurons = 1

    transformations = {}

    transformations["scaler"] = StandardScaler().fit(XTrain)
    XTrain = transformations["scaler"].transform(XTrain)
    XValidation = transformations["scaler"].transform(XValidation)

    from keras.callbacks import Callback

    class roc_callback(Callback):
      def __init__(self, XTrain, XValidation, YTrain, YValidation, weightTrain, weightValidation):
        self.x = XTrain
        self.y = YTrain
        self.w = weightTrain
        self.x_val = XValidation
        self.y_val = YValidation
        self.w_val = weightValidation

      def on_epoch_end(self, epoch, logs={}):
        from sklearn.metrics import roc_auc_score

        y_pred = self.model.predict(self.x)
        roc = roc_auc_score(self.y, y_pred, sample_weight=self.w)
        y_pred_val = self.model.predict(self.x_val)
        roc_val = roc_auc_score(self.y_val, y_pred_val, sample_weight=self.w_val)
        logs["roc"] = roc
        logs["val_roc"] = roc_val

    callbacks = []
    callbacks.append(roc_callback(XTrain, XValidation, YTrain, YValidation, weightTrain, weightValidation))

    model = self.topology.buildModel(len(self.getFeatures()), outputNeurons, compileArgs)
    import time
    start = time.time()
    history = model.fit(XTrain, YTrain, sample_weight=weightTrain, validation_data=(XValidation, YValidation, weightValidation), callbacks=callbacks, **trainParams)
    print("Training ", name, " took ", time.time()-start, " seconds")

    return transformations, model, history

  def saveAllFolds(self, directory):
    for index, info in self._foldInfo.iteritems():
      self.save_h5(directory, saveModel=index, foldString=info["name"])
      self.save_history(directory, saveModel=index, foldString=info["name"])

  def save_h5(self, directory, saveModel=None, epoch = None, foldString = None):
    from sklearn.externals import joblib

    fileName = self.name
    if foldString is not None:
      fileName = fileName + "_" + str(foldString)

    make_sure_path_exists(directory + "/" + fileName)

    model = self.model
    if isinstance(model, list):
      model = self.model[0]
    if saveModel is not None:
      model = self.model[saveModel]

    transformations = self.transformations
    if isinstance(transformations, list):
      transformations = self.transformations[0]
    if saveModel is not None:
      transformations = self.transformations[saveModel]

    for key, val in transformations.iteritems():
      joblib.dump(val, directory + "/" + fileName + "/" + key + ".sav")

    if epoch is None:
      model.save(directory + "/" + fileName + "/model.h5")
    else:
      model.save(directory + "/" + fileName + "/E" + str(epoch) + ".h5")
    return

  def save_history(self, directory, saveModel = None, foldString = None):
    fileName = self.name
    if foldString is not None:
      fileName = fileName + "_" + str(foldString)

    make_sure_path_exists(directory + "/" + fileName)

    history = self.history
    if isinstance(history, list):
      history = self.history[0]
    if saveModel is not None:
      history = self.history[saveModel]

    #print history
    import pickle
    pickle.dump(history.history, open(directory + "/" + fileName + "/hist.pkl", "wb"))
    return

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

def listDir(path):
  import subprocess
  cmd = "ls " + path
  p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  out, err = p.communicate()
  return out.split()

def remove_field_name(a, name):
  names = list(a.dtype.names)
  if name in names:
    names.remove(name)
  b = a[names]
  return b
