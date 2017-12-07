
class NetworkBuilder:
  """
  A class to help handle reading the cfg file and then building/training the NN
  """
  def __init__(self, cfgJson, verbose=False, batch=False):

    import json
    self._rawSource = json.load(open(cfgJson, "rb"))

    self._epochs    = self._rawSource["network"]["epochs"]
    self._batchSize = self._rawSource["network"]["batchSize"]
    self._seed      = self._rawSource["network"]["seed"]
    self._kFolds    = self._rawSource["network"]["k-folds"]

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

