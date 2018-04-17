import sys
from ROOT import TFile, TH1F, TCanvas
import commonFunctions as funk

def recursiveSampleWithFold(nTupleDir,foldingDir,outDir,suffix, verbose = False, noRecurse=False):
    import os
    import ROOT
    funk.make_sure_path_exists(outDir)

    nubs = funk.listDir(nTupleDir)

    for nub in nubs:
        if verbose:
             print "Checking ", nTupleDir + "/" + nub
        if os.path.isdir(nTupleDir + "/" + nub):
          if not noRecurse:
            recursiveSampleWithFold(nTupleDir + "/" + nub, foldingDir + "/" + nub, outDir + "/" + nub, suffix, verbose, noRecurse)
        elif os.path.isfile(nTupleDir + "/" + nub):
          if nub[-4:] == "root":
            file = ROOT.TFile(nTupleDir + "/" + nub, "READ")
            tree = file.Get("bdttree")
            if tree:
                foldFile = ROOT.TFile(foldingDir + "/" + nub[:-5] + "_" + suffix + ".root", "READ")
                foldTree = foldFile.Get("bdttree_folds")
                if foldTree:
                    outFile = ROOT.TFile(outDir + "/" + nub[:-5] + "_" + suffix + ".root", "RECREATE")
                    outTree = combineFoldedTree(tree, foldTree)

              #fold(nTupleDir + "/" + nub, outDir + "/" + nub[:-5], foldingType, folds, splitting, presplit, verbose)
              #  root_numpy.array2root(npData, outFile, 'bdttree_folds', mode='recreate')
            else:
              print "Skipping " + nub
        else:
          print "Weird stuff is happening, will ignore it."

    return

def combineFoldedTree(nTupleRootFile, foldedRootFile):
    import ROOT

    if nTupleRootFile.GetEntries() == foldedRootFile.GetEntries():
        nTupleRootFile.AddFriend(foldedRootFile)
        nTupleRootFile.SetBranchStatus("*",0)
        for branch in nTupleRootFile.GetListOfBranches():
            if branch.GetName()[-4:] != "Down" and branch.GetName()[-2:] != "Up":
                nTupleRootFile.SetBranchStatus(branch.GetName(),1)
        outTree = nTupleRootFile.CopyTree("")
    else:
        print "Number of entries from nTuples is different from the number of entries on the folded sample."
    return outTree

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process the command line options')
    parser.add_argument('-v', '--verbose', action='store_true', help='Whether to print verbose output')
    parser.add_argument(      '--nTupleDirectory', required=True, help='')
    parser.add_argument(      '--foldedDirectory', required=True, help='')
    parser.add_argument(      '--outputDirectory', required=True, help='')
    parser.add_argument(      '--suffix', default=None, help='')
    parser.add_argument(      '--noRecurse', action='store_true', help='Whether to recurse into the subdirectories')

    args = parser.parse_args()

    recursiveSampleWithFold(args.nTupleDir,args.foldingDir,args.outputDirectory,args.suffix,True,True):
