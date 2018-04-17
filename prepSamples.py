import sys
from ROOT import TFile, TH1F, TCanvas
import commonFunctions as funk

def recursiveSampleWithFold(nTupleDir,foldsDir,outDir,suffix, verbose = False, noRecurse=False):
    import os
    import ROOT
    funk.make_sure_path_exists(outDir)

    nubs = funk.listDir(nTupleDir)

    for nub in nubs:
        if verbose:
            print "Checking ", nTupleDir + "/" + nub
        if os.path.isdir(nTupleDir + "/" + nub):
            if not noRecurse:
                if verbose:
                    print "Recursing into directory"
                recursiveSampleWithFold(nTupleDir + "/" + nub, foldsDir + "/" + nub, outDir + "/" + nub, suffix, verbose, noRecurse)
        elif os.path.isfile(nTupleDir + "/" + nub):
            if nub[-4:] == "root":
                if verbose:
                    print "It is a root file, trying to get trees"
                file = ROOT.TFile(nTupleDir + "/" + nub, "READ")
                tree = file.Get("bdttree")
                if tree:
                    if verbose:
                        print "Found the tree in the input file"
                    foldFile = ROOT.TFile(foldsDir + "/" + nub[:-5] + "_" + suffix + ".root", "READ")
                    foldTree = foldFile.Get("bdttree_folds")
                    if foldTree:
                        if verbose:
                            print "Found the tree in the folds file"
                            print "Creating the output file and tree"
                        outFile = ROOT.TFile(outDir + "/" + nub[:-5] + "_" + suffix + ".root", "RECREATE")
                        outTree = combineFoldsTree(tree, foldTree)
                        outTree.Write("", ROOT.TObject.kOverwrite)
                        outFile.Close()
            else:
                print "Skipping " + nub
        else:
            print "Weird stuff is happening, will ignore it."

    return

def combineFoldsTree(nTupleRootFile, foldsRootFile):
    import ROOT

    if nTupleRootFile.GetEntries() == foldsRootFile.GetEntries():
        #from array import array
        #tmpvarID = array( 'l', [ 0 ] )
        #tmpvar_a = array( 'l', [ 0 ] )
        #tmpvar_b = array( 'l', [ 0 ] )
        #nTupleRootFile.Branch('foldID',tmpvarID,'foldID/L')
        #nTupleRootFile.Branch('fold_a',tmpvar_a,'fold_a/L')
        #foldsBranches = [x.GetName() for x in foldsRootFile.GetListOfBranches()]
        #if 'fold_b' in foldsBranches:
        #    nTupleRootFile.Branch('fold_b',tmpvar_b,'fold_b/L')

        #nTupleRootFile.AddFriend(foldsRootFile)

        nTupleRootFile.SetBranchStatus("*",0)
        for branch in nTupleRootFile.GetListOfBranches():
            if branch.GetName()[-4:] != "Down" and branch.GetName()[-2:] != "Up":
                nTupleRootFile.SetBranchStatus(branch.GetName(),1)

        outTree = nTupleRootFile.CopyTree("")

        import ctypes
        foldsBranches = [x.GetName() for x in foldsRootFile.GetListOfBranches()]
        tmpFoldID = ctypes.c_int64(0)
        tmpFold_a = ctypes.c_int64(0)
        tmpFold_b = ctypes.c_int64(0)
        branchFoldID = outTree.Branch("foldID", tmpFoldID, "foldID/L")
        foldsRootFile.SetBranchAddress("foldID", tmpFoldID)
        branchFold_a = outTree.Branch("fold_a", tmpFold_a, "fold_a/L")
        foldsRootFile.SetBranchAddress("fold_a", tmpFold_a)
        if 'fold_b' in foldsBranches:
            branchFold_b = outTree.Branch("fold_b", tmpFold_b, "fold_b/L")
            foldsRootFile.SetBranchAddress("fold_b", tmpFold_b)

        for i in range(nTupleRootFile.GetEntries()):
            foldsRootFile.GetEntry(i)
            branchFoldID.Fill()
            branchFold_a.Fill()
            if 'fold_b' in foldsBranches:
                branchFold_b.Fill()
    else:
        print "Number of entries from nTuples is different from the number of entries on the folds sample."
    return outTree

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Process the command line options')
    parser.add_argument('-v', '--verbose', action='store_true', help='Whether to print verbose output')
    parser.add_argument(      '--nTupleDirectory', required=True, help='')
    parser.add_argument(      '--foldsDirectory', required=True, help='')
    parser.add_argument(      '--outputDirectory', required=True, help='')
    parser.add_argument(      '--suffix', default=None, help='')
    parser.add_argument(      '--noRecurse', action='store_true', help='Whether to recurse into the subdirectories')

    args = parser.parse_args()

    recursiveSampleWithFold(args.nTupleDirectory,args.foldsDirectory,args.outputDirectory,args.suffix,args.verbose,args.noRecurse)
