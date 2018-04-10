#!/bin/bash

#python prefold.py --type "k-fold" --folds 3 --splitting "random" --presplit 0 --inputDirectory test --outputDirectory testFolded
#python prefold.py --type "k-fold" --folds 3 --splitting "random" --presplit 1 --inputDirectory train --outputDirectory trainFolded

export NTUPLE_DIR=/lstore/cms/cbeiraod/Stop4Body/nTuples_v2017-10-19
export FOLDED_DIR=/lstore/cms/dbastos/Stop4Body/nTuples_v2017-10-19_folded

python prefold.py --type "n-fold" --folds 3 --splitting "random" --inputDirectory ${NTUPLE_DIR} --outputDirectory ${FOLDED_DIR}
python prefold.py --type "n-fold" --folds 6 --splitting "random" --inputDirectory ${NTUPLE_DIR} --outputDirectory ${FOLDED_DIR}
