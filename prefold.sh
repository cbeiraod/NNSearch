#!/bin/bash

#python prefold.py --type "k-fold" --folds 3 --splitting "random" --presplit 0 --inputDirectory test --outputDirectory testFolded
#python prefold.py --type "k-fold" --folds 3 --splitting "random" --presplit 1 --inputDirectory train --outputDirectory trainFolded


python prefold.py --type "n-fold" --folds 3 --splitting "random" --inputDirectory train --outputDirectory trainFolded/train
