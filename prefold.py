import commonFunctions as funk

def fold(inFile, outFile, foldingType, folds, splitting, presplit = None, verbose = False):
  import root_numpy
  import pandas
  import numpy as np

  folds =  int(folds)
  if presplit is not None:
    presplit = int(presplit)

  if foldingType == "n-fold":
    outFile = outFile + "_n"
  elif foldingType == "k-fold":
    outFile = outFile + "_k"
  else:
    print "What is happening here?"

  outFile = outFile + str(folds) + ".root"
  branches = ["Run", "LumiSec", "Event"]

  npData = root_numpy.root2array(
                                  inFile,
                                  treename="bdttree",
                                  #selection=selection,
                                  branches=branches
                                )
  pdData = pandas.DataFrame(npData)

  if foldingType == "n-fold":
    if splitting == "modulus":
      if verbose:
        print "Doing n-fold with modulus"
      pdData["fold_a"] = (pdData.Event%int(folds)).astype(int)

    elif splitting == "random":
      if verbose:
        print "Doing n-fold with random"
      samplesPerFold = len(pdData.index)/folds
      tmpData = pdData

      pdData["fold_a"] = folds - 1
      for i in range(1, folds):
        fold = tmpData.sample(n=samplesPerFold)
        tmpData = tmpData.drop(fold.index)
        pdData.loc[fold.index, "fold_a"] = i-1

    pdData["foldID"] = pdData.fold_a.astype(int)

  elif foldingType == "k-fold":
    if splitting == "modulus":
      if verbose:
        print "Doing k-fold with modulus"
      if presplit is not None:
        pdData["fold_a"] = presplit
      else:
        pdData["fold_a"] = (pdData.Event%2).astype(int)
      pdData["fold_b"] = (((pdData.Event/2).astype(int))%folds).astype(int)

    elif splitting == "random":
      if verbose:
        print "Doing k-fold with random"
      tmpData = pdData

      pdData["fold_a"] = 1
      pdData["fold_b"] = folds - 1
      if presplit is not None:
        samplesPerFold = len(pdData.index)/(folds)
        pdData["fold_a"] = presplit
        for i in range(1, folds):
          fold = tmpData.sample(n=samplesPerFold)
          tmpData = tmpData.drop(fold.index)
          pdData.loc[fold.index, "fold_b"] = i-1
      else:
        samplesPerFold = len(pdData.index)/(2*folds)
        prefold = tmpData.sample(n=len(pdData.index)/2)
        tmpData = tmpData.drop(prefold.index)
        pdData.loc[prefold.index, "fold_a"] = 0
        pdData.loc[tmpData.index, "fold_a"] = 1
        for i in range(1, folds):
          fold = tmpData.sample(n=samplesPerFold)
          tmpData = tmpData.drop(fold.index)
          pdData.loc[fold.index, "fold_b"] = i-1
          fold = prefold.sample(n=samplesPerFold)
          prefold = prefold.drop(fold.index)
          pdData.loc[fold.index, "fold_b"] = i-1

    pdData["foldID"] = (pdData.fold_a*folds + pdData.fold_b).astype(int)

  npData = pdData.to_records()
  npData = funk.remove_field_name(npData, "index") # To remove the index, but keeping it might make things better???
  root_numpy.array2root(npData, outFile, 'bdttree_folds', mode='recreate')

  return

def recursiveFolding(baseDir, outDir, foldingType, folds, splitting, presplit = None, verbose = False, noRecurse=False):
  import os
  import ROOT
  funk.make_sure_path_exists(outDir)

  folds =  int(folds)
  if presplit is not None:
    presplit = int(presplit)

  nubs = funk.listDir(baseDir)

  for nub in nubs:
    if verbose:
      print "Checking ", baseDir + "/" + nub

    if os.path.isdir(baseDir + "/" + nub):
      if not noRecurse:
        recursiveFolding(baseDir + "/" + nub, outDir + "/" + nub, foldingType, folds, splitting, presplit, verbose)
    elif os.path.isfile(baseDir + "/" + nub):
      if nub[-4:] == "root":
        file = ROOT.TFile(baseDir + "/" + nub, "READ")
        tree = file.Get("bdttree")
        if tree:
          fold(baseDir + "/" + nub, outDir + "/" + nub[:-5], foldingType, folds, splitting, presplit, verbose)
        else:
          print "Skipping " + nub
    else:
      print "Weird stuff is happening, will ignore it."

  return

if __name__ == "__main__":
  import argparse
  import os
  import sys

  parser = argparse.ArgumentParser(description='Process the command line options')
  parser.add_argument('-d', '--dryRun', action='store_true', help='Do a dry run (i.e. do not actually run the potentially dangerous commands but print them to the screen)')
  parser.add_argument('-v', '--verbose', action='store_true', help='Whether to print verbose output')
  parser.add_argument('-i', '--inputDirectory', required=True, help='Name of the directory where the root files are located')
  parser.add_argument('-o', '--outputDirectory', required=True, help='Name of the directory where the splitted root files will be saved')
  parser.add_argument('-p', '--presplit', type=int, help='Whether the samples have previously been split, set it to the number of the fold (for bookeeping)')
  parser.add_argument('-s', '--splitting', default="random", choices=["random", "modulus"], help='How to determine the splitting')
  parser.add_argument('-f', '--folds', type=int, default=3, help='Into how many folds should the sample be split')
  parser.add_argument('-t', '--type', default="n-fold", choices=["n-fold", "k-fold"], help='The folding technique to use')
  parser.add_argument(      '--seed', type=int, default=42, help='Seed for the random number generator (only used for random splitting)')
  parser.add_argument(      '--noRecurse', action='store_true', help='Whether to recurse into the subdirectories')

  args = parser.parse_args()

  import numpy as np
  np.random.seed(args.seed)

  if args.presplit is not None and args.type == "n-fold":
    parser.error("It is not possible to do n-fold splitting when using a previously split sample")

  if args.type == "n-fold" and args.folds < 3:
    parser.error("You really should not use fewer than 3 folds with n-folding")

  if args.type == "k-fold" and args.folds < 2:
    parser.error("You really should not use fewer than 2 folds with k-folding")

  if not args.dryRun:
    print "You did not enable dry run. You are on your own!"

  if args.verbose:
    print "Will split all the root files from directory:", args.inputDirectory, "into " + str(args.folds) + " folds for", args.type, "."
    print "The fold annotation will be saved in the directory:", args.outputDirectory, "with the same structure."

  if not args.noRecurse:
    recursiveFolding(args.inputDirectory, args.outputDirectory, args.type, int(args.folds), args.splitting, args.presplit, args.verbose)
  else:
    recursiveFolding(args.inputDirectory, args.outputDirectory, args.type, int(args.folds), args.splitting, args.presplit, args.verbose, args.noRecurse)
