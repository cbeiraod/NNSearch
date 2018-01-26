import root_numpy
import pandas

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

    self.type = self._rawSource["type"]
    self.activation = self._rawSource["activation"]
    self.nLayers = self._rawSource["nLayers"]
    self.neurons = self._rawSource["neurons"]
    self.dropout = self._rawSource["dropout"]

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

  def buildModel(self, nIn, nOut, compileArgs):
    if self.type == "simple":
      model = Sequential()
      model.add(Dense(self.neurons, input_dim=nIn, kernel_initializer='he_normal', activation=self.activation))
      if self.dropout > 0:
        model.add(Dropout(self.dropout))
      for i in range(self.nLayers - 1):
        model.add(Dense(self.neurons, kernel_initializer='he_normal', activation=self.activation))
        if self.dropout > 0:
          model.add(Dropout(self.dropout))
      model.add(Dense(nOut, activation="sigmoid", kernel_initializer='glorot_normal'))
      model.compile(**compileArgs)
      return model
    return None

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

class SampleComponents(objects):
  """
  A class to help handle reading the sample components
  """
  def __init__(self, cfgJson, sampleType, basePath, suffix = "", verbose = False, batch = False):
    self._rawSource = cfgJson
    self._verbose = verbose
    self._batch = batch
    self._sampleType = sampleType
    self._basePath = basePath
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
        filename = self.basePath + "/" + file
        if suffix not "":
          filename = filename + "_" + suffix
        filename = filename + ".root"
        if not os.path.isfile(filename):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (component: " + self.name + ")")
        self.files.append(file)
    elif self._sampleType == "legacy":
      self.testFiles = []
      self.trainFiles = []
      if "testFiles" not in self._rawSource:
        raise KeyError("A component with no testFiles is defined")
      if "trainFiles" not in self._rawSource:
        raise KeyError("A component with no trainFiles is defined")
      for file in self._rawSource["testFiles"]:
        filename = self.basePath + "/" + file
        if suffix not "":
          filename = filename + "_" + suffix
        filename = filename + ".root"
        if not os.path.isfile(filename):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (component: " + self.name + ")")
        self.testFiles.append(file)
      for file in self._rawSource["trainFiles"]:
        filename = self.basePath + "/" + file
        if suffix not "":
          filename = filename + "_" + suffix
        filename = filename + ".root"
        if not os.path.isfile(filename):
          import errno
          raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), file + " (component: " + self.name + ")")
        self.trainFiles.append(file)

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

  def getData(self, selection, branches, fraction):
    trainData = None
    testData = None

    if "weight" not in branches:
      branches.append("weight")

    if self._sampleType == "unified":
      if "Event" not in branches:
        branches.append("Event")
      Data = None
      for file in self.files:
        data = root_numpy.root2array(
                                     file,
                                     treename="bdttree",
                                     selection=selection,
                                     branches=branches
                                     )

        if fraction < 1.0:
          data = data[:int(len(data)*fraction)]

        if Data is None:
          Data = pandas.DataFrame(data)
        else:
          Data = testData.append(pandas.DataFrame(data), ignore_index=True)
      Data["NNSearch_Class"] = Data["Event"] % 2
      trainData = Data[Data["NNSearch_Class"] == 1]
      testData = Data[Data["NNSearch_Class"] == 0]
    elif self._sampleType == "legacy":
      for file in self.trainFiles:
        data = root_numpy.root2array(
                                     file,
                                     treename="bdttree",
                                     selection=selection,
                                     branches=branches
                                     )

        if fraction < 1.0:
          data = data[:int(len(data)*fraction)]

        if trainData is None:
          trainData = pandas.DataFrame(data)
        else:
          trainData = testData.append(pandas.DataFrame(data), ignore_index=True)

      for file in self.testFiles:
        data = root_numpy.root2array(
                                     file,
                                     treename="bdttree",
                                     selection=selection,
                                     branches=branches
                                     )

        if fraction < 1.0:
          data = data[:int(len(data)*fraction)]

        if testData is None:
          testData = pandas.DataFrame(data)
        else:
          testData = testData.append(pandas.DataFrame(data), ignore_index=True)
    else:
      raise ValueError("Unknown type '" + self._sampleType + "'")

    if fraction < 1.0:
      trainData.weight = trainData.weight/fraction
      testData.weight  = testData.weight/fraction

    return trainData, testData

class NetworkSample(object):
  """
  A class to help handle reading the sample files
  """
  def __init__(self, cfgJson, preselection, fraction, branches, verbose = False, batch = False):
    self._rawSource = cfgJson
    self._verbose = verbose
    self._batch = batch
    self._preselection = preselection
    self._fraction = fraction
    self._branches = branches

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
      tmp = SampleComponents(component, self.type, self.basePath, suffix = self.suffix, verbose = self._verbose, batch = self._batch)
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

  def getData(self):
    trainData = None
    testData = None

    for component in self.components:
      componentTrain, componentTest = component.getData(self._preselection, self.branches.keys(), self._fraction)
      if trainData is None:
        trainData = componentTrain
      else:
        trainData = trainData.append(componentTrain, ignore_index=True)
      if testData is None:
        testData = componentTest
      else:
        testData = testData.append(componentTest, ignore_index=True)

    trainData["sampleWeight"] = sample.weight
    testData["sampleWeight"] = sample.weight

    for weight in self.excludeWeight:
      trainData.sampleWeight = trainData.sampleWeight/trainData[weight]
      testData.sampleWeight  = testData.sampleWeight/testData[weight]

    return trainData, testData

class NetworkBuilder(object):
  """
  A class to help handle reading the cfg file and then building/training the NN
  """
  def __init__(self, cfgJson, verbose=False, batch=False):
    import json
    self._rawSource = json.load(open(cfgJson, "rb"))
    self._verbose = verbose
    self._batch = batch

    self.name         = self._rawSource["network"]["name"]
    self.epochs       = self._rawSource["network"]["epochs"]
    self.batchSize    = self._rawSource["network"]["batchSize"]
    self.kFolds       = 1
    self.fraction     = 1.0
    self.seed         = -1
    self.multiple     = 1
    self.preselection = ""
    if "k-folds" in self._rawSource["network"]:
      self.kFolds   = self._rawSource["network"]["k-folds"]
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

    self.samples = []
    for sample in self._rawSource["network"]["samples"]:
      tmp = NetworkSample(sample, self.preselection, self.fraction, self.branches, verbose=self._verbose, batch=self._batch)
      self.samples.append(tmp)

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

  def buildModel(self):
    return self.topology.buildModel()

  def getData(self):
    trainData = None
    testData = None

    trainDataArray = []
    testDataArray = []

    for sample in self.samples:
      train, test = sample.getData()
      trainDataArray.append(train)
      testDataArray.append(test)

    for i in range(len(trainDataArray)):
      trainDataArray[i]["category"]  = i
      testDataArray[i]["category"]   = i
      trainDataArray[i].sampleWeight = trainDataArray[i].sampleWeight/trainDataArray[i].sampleWeight.sum()
      testDataArray[i].sampleWeight  = testDataArray[i].sampleWeight/testDataArray[i].sampleWeight.sum()

    for train in trainDataArray:
      if trainData is None:
        trainData = train
      else:
        trainData = trainData.append(train, ignore_index=True)

    for test in testDataArray:
      if testData is None:
        testData = test
      else:
        testData = testData.append(test, ignore_index=True)

    return trainData, testData

  def getFeatures(self):
    features = []
    for branch, branchInfo in self.branches:
      if branchInfo.isFeature:
        features = features + [branch]
    return features

  def train(self):
    import numpy as np
    import keras
    features = self.getFeatures()

    trainData, testData = self.getData()

    # TODO: implement k-folding
    XDev = trainData.ix[:,self.getFeatures()]
    XVal = testData.ix[:,self.getFeatures()]
    YDev = None
    YVal = None
    if len(self.samples) > 2:
      YDev = keras.utils.to_categorical(np.ravel(trainData.category), num_classes=len(self.samples))
      YVal = keras.utils.to_categorical(np.ravel(testData.category), num_classes=len(self.samples))
    else:
      YDev = np.ravel(trainData.category)
      YVal = np.ravel(testData.category)
    weightDev = np.ravel(trainData.sampleWeight)
    weightVal = np.ravel(testData.sampleWeight)

    # TODO: what about regression? Should use loss MSE and the output of the last layer should not be sigmoid
    compileArgs = {
      "loss": "binary_crossentropy",
      "optimizer": self.optimizer.build(),
      "metrics": ["accuracy"] # TODO: Add ROC AUC
    }
    if len(self.samples) > 2:
      compileArgs["loss"] = "categorical_crossentropy"

    self.model = self.buildModel(len(self.getFeatures()), len(self.samples), compileArgs)

    trainParams = {
      "epochs": self.epochs,
      "batch_size": self.batchSize,
      "verbose": 1
    }

    start = time.time()
    self.history = self.model.fit(XDev, YDev, validation_data=(XVal,YVal,weightVal), sample_weight=weightDev, **trainParams)
    print("Training took ", time.time()-start, " seconds")

    return

  def save_h5(self, directory, epoch = None):
    if epoch is None:
      self.model.save(directory + "/" + self.name + ".h5")
    else:
      self.model.save(directory + "/" + self.name + "_E" + str(epoch) + ".h5")
    return

  def save_history(self, directory):
    import pickle
    pickle.dump(self.history, open(directory + "/" + self.name + ".hist", "wb"))
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
