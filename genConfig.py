import json
from pprint import pprint
import math
from copy import deepcopy
from commonFunctions import make_sure_path_exists

def scanCombinations(scanParams):
    myParam = scanParams.keys()[0]

    r = dict(scanParams)
    del r[myParam]

    list=[]
    myList=[]

    if len(r) is not 0:
        list=scanCombinations(r)

    min = scanParams[myParam][0]
    max = scanParams[myParam][1]
    if max < min:
        tmpVal = max
        max = min
        min = tmpVal
    entries = 2
    if len(scanParams[myParam]) == 3:
        entries = scanParams[myParam][2]

    from numpy import linspace
    if len(list) is 0:
        for value in linspace(min,max,entries):
            tmp = {}
            tmp[myParam]=value
            myList.append(tmp)
    else:
        for point in list:
            for value in linspace(min,max,entries):
                tmp = dict(point)
                tmp[myParam]=value
                myList.append(tmp)
    return myList

def consolidateListType(myList,intTypeList):
    for i in range (0, len(myList)):
        for j in range(0,len(intTypeList)):
            if intTypeList[j] in myList[i]:
                myList[i][intTypeList[j]] = int(math.floor(myList[i][intTypeList[j]]))
    return myList

def createJson(pointParam,cfgJson):

    newJson = deepcopy(cfgJson)

    if "layers" in pointParam:
        newJson["network"]["topology"]["layers"] = pointParam["layers"]
    if "neurons" in pointParam:
        newJson["network"]["topology"]["neurons"] = pointParam["neurons"]
    if "dropout_rate" in pointParam:
        newJson["network"]["topology"]["dropout"] = pointParam["dropout_rate"]
    if "epochs" in pointParam:
        newJson["network"]["epochs"] = pointParam["epochs"]
    if "batch_size" in pointParam:
        newJson["network"]["batchSize"] = pointParam["batch_size"]
    if "learning_rate" in pointParam:
        newJson["network"]["optimizer"]["lr"] = pointParam["learning_rate"]
    if "learning_rate_decay" in pointParam:
        newJson["network"]["optimizer"]["decay"] = pointParam["learning_rate_decay"]
    if "L2_regularizer" in pointParam:
        newJson["network"]["topology"]["l2"] = pointParam["L2_regularizer"]

    return newJson

def saveJson(myList,cfgJson,dir):
    for i in range(0,len(myList)):
        pointParam = myList[i]
        name = getNameFromPoint(pointParam)
        path = dir+"/"+name+"/"
        make_sure_path_exists(path)
        newJson = createJson(pointParam,cfgJson)
        with open(path+'cfg.json', 'w') as outfile:
            json.dump(newJson, outfile, sort_keys = True, indent = 4, ensure_ascii = False)

def getNameFromPoint(pointParam):
    name = ""
    for k,v in pointParam.iteritems():
        name = name + str(k) + str(v)+"_"
    name = name[:-1]
    name = name.replace("layers","L")
    name = name.replace("neurons","N")
    name = name.replace("dropout_rate","Dr")
    name = name.replace("epochs","E")
    name = name.replace("batch_size","Bs")
    name = name.replace("learning_rate","Lr")
    name = name.replace("learning_rate_decay","De")
    name = name.replace("L2_regularizer","L2Reg")

    return name

if __name__ == "__main__":
    import os
    import subprocess
    import argparse
    import sys
    import datetime

    parser = argparse.ArgumentParser(description='Process the command line options')
    parser.add_argument('--layers', nargs='+', type=int, default=[], help='Layers: min max entries (entries can be ommited). Ex:1 4 1 -> 1 2 3 4')
    parser.add_argument('--neurons', nargs='+', type=int, default=[], help='Neurons: min max entries')
    parser.add_argument('--epochs', nargs='+', type=int, default=[], help='Epochs: min max entries')
    parser.add_argument('--batch-size', nargs='+', type=int, default=[], help='Batch size: min max entries')
    parser.add_argument('--learning-rate', nargs='+', type=float, default=[], help='Learning rate: min max entries')
    parser.add_argument('--learning-rate-decay', nargs='+', type=float, default=[], help='Learning rate decay: min max entries')
    parser.add_argument('--dropout-rate', nargs='+', type=float, default=[], help='Dropout rate: min max entries')
    parser.add_argument('--L2-regularizer', nargs='+', type=float, default=[], help='L2 regularizer: min max entries')

    parser.add_argument('-c', '--inputFile', required=True, help='Inpunt configuration file dirctory')
    parser.add_argument('-d', '--directory', required=True, help='Output directory to save configuration file')

    args = parser.parse_args()
    input_file = args.inputFile
    dir = args.directory
    make_sure_path_exists(dir)

    scanParams = {}

    for arg,value in args.__dict__.iteritems():
        if arg =='inputFile' or arg == 'directory':
            continue
        if len(value)>3 or len(value)==1:
            parser.error('For ' + arg + ' you should define a minimun, maximun and optionally entries.')
        if len(value) is not 0:
            scanParams[arg]=value

    if scanParams == {}:
        raise KeyError("You must parse at least one grid search parameter")

    intTypeList=["layers","neurons","epochs","batch_size"]
    floatTypeList=["learning_rate","learning_rate_decay","dropout_rate","L2_regularizer"]
    allTypesList = intTypeList + floatTypeList

    myParamsList=consolidateListType(scanCombinations(scanParams),intTypeList)

    json_data=open(input_file).read()
    cfgJson = json.loads(json_data)

    saveJson(myParamsList,cfgJson,dir)
