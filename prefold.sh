#!/bin/bash

#python prefold.py --type "k-fold" --folds 3 --splitting "random" --presplit 0 --inputDirectory test --outputDirectory testFolded
#python prefold.py --type "k-fold" --folds 3 --splitting "random" --presplit 1 --inputDirectory train --outputDirectory trainFolded

export NTUPLE_DIR=/lstore/cms/cbeiraod/Stop4Body/nTuples_v2017-10-19
export FOLDS_DIR=/lstore/cms/dbastos/Stop4Body/nTuples_v2017-10-19_folds
export FOLDED_DIR=/lstore/cms/dbastos/Stop4Body/nTuples_v2017-10-19_folded

export FOLD_TYPE=n
export NUM_FOLDS=3

python prefold.py --type "${FOLD_TYPE}-fold" --folds $NUM_FOLDS --splitting "random" --inputDirectory ${NTUPLE_DIR} --outputDirectory ${FOLDS_DIR} --noRecurse
python prepSamples.py --nTupleDirectory ${NTUPLE_DIR} --foldsDirectory ${FOLDS_DIR} --outputDirectory ${FOLDED_DIR} --suffix ${FOLD_TYPE}${NUM_FOLDS} --noRecurse
