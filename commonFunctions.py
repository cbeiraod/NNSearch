
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

