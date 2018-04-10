#!/bin/bash

#$ -cwd
#$ -pe mcore 3

#$ -l container=True
#$ -v CONTAINER=CENTOS7
#...$ -v CONTAINER=UBUNTU16

#...$ -v SGEIN=script.py
#...$ -v SGEIN=pima-indians-diabetes.data

#...$ -v SGEOUT=accuracy.pickle
#...$ -v SGEOUT=loss.pickle

#$ -l gpu

cd /exper-sw/cmst3/cmssw/users/dbastos/NNSearch

module load root-6.10.02

python runNN.py -c cfg.json -o outputDir -b

