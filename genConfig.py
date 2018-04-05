import json
from pprint import pprint

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

def consolidateListType(myList):

    return


if __name__ == "__main__":
    import os
    import subprocess
    import argparse
    import sys
    #from commonFunctions import make_sure_path_exists
    import datetime

    parser = argparse.ArgumentParser(description='Process the command line options')
    parser.add_argument('--layers', nargs='+', type=int, default=[], help='Layers: min max entries (entries can be ommited). Ex:1 4 1 -> 1 2 3 4')
    parser.add_argument('--neurons', nargs='+', type=int, default=[], help='Neurons: min max entries')
    parser.add_argument('--epochs', nargs='+', type=int, default=[], help='Epochs: min max entries')
    parser.add_argument('--batch-size', nargs='+', type=int, default=[], help='Batch size: min max entries')
    parser.add_argument('--learning-rate', nargs='+', type=float, default=[], help='Learning rate: min max entries')
    parser.add_argument('--learning-rate-decay', nargs='+', type=float, default=[], help='Learning rate decay: min max entries')
    parser.add_argument('--dropout-rate', nargs='+', type=int, default=[], help='Dropout rate: min max entries')
    parser.add_argument('--L2-regularizer', nargs='+', type=int, default=[], help='L2 regularizer: min max entries')

    parser.add_argument('-c', '--inputFile', required=True, help='Inpunt configuration file dirctory')
    parser.add_argument('-d', '--directory', required=True, help='Output directory to save configuration file')

    args = parser.parse_args()
    input_file = args.inputFile
    dir = args.directory

    scanParams = {}

    for arg,value in args.__dict__.iteritems():
        if arg =='inputFile' or arg == 'directory':
            continue
        if len(value)>3 or len(value)==1:
            parser.error('For ' + arg + ' you should define a minimun, maximun and optionally entries.')
        if len(value) is not 0:
            scanParams[arg]=value

    scanCombinations(scanParams)
    exit()



    '''
    n_layers = args.layers
    n_neurons = args.neurons
    n_epochs = args.epochs
    batch_size = args.batchSize #len(XDev)/100
    learning_rate = args.learningRate
    my_decay = args.decay
    dropout_rate = args.dropoutRate
    regularizer = args.regularizer
    '''
    #name = "L"+str(n_layers)+"_N"+str(n_neurons)+"_E"+str(n_epochs)+"_Bs"+str(batch_size)+"_Lr"+str(learning_rate)+"_Dr"+str(dropout_rate)+"_De"+str(args.decay)+"_L2Reg"+str(regularizer)+"_Tr"+train_DM+"_Te"+test_point+"_DT"+suffix

    #make_sure_path_exists(filepath+"/accuracy/"+"dummy.txt")

    json_data=open(input_file).read()

    data = json.loads(json_data)
    #pprint(data)
