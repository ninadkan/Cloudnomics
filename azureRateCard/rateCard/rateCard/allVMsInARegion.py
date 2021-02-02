import os
import json
import pandas as pd
import argparse


def processJsonAndCreateCSV(inputFileName, outputFileName):
    """
    Convert the JSON file to CSV FILE whilst re-arranging the column names
    inputFileName = full path name of the JSON file that should've been downloaded before
    outputFileName = full path name of the CSV file that is created as a result of execution of this code
    """
    counter = 0
    ColumnNames= ['maxDataDiskCount', 'memoryInMb', 'name', 'numberOfCores', 'osDiskSizeInMb', 'resourceDiskSizeInMb']
    DATA_LIST = []
    with open(inputFileName) as json_file:
        data = json.load(json_file)
        # data is an array of elements
        for elements in data:
            thisdict = {}
            for eachItem in ColumnNames:
                thisdict[eachItem] = elements[eachItem]
            counter += 1 
            DATA_LIST.append(thisdict)

    dfOut = pd.DataFrame(DATA_LIST)
    dfOut = dfOut[['name', 'numberOfCores', 'memoryInMb', 'maxDataDiskCount', 'osDiskSizeInMb', 'resourceDiskSizeInMb']]
    dfOut.to_csv(outputFileName, index=0)
    return




if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )


    parser.add_argument("-v", "--verbose", help="increase output verbosity",action="store_true")
    parser.add_argument("inputFileName", help="inputFileName")
    parser.add_argument("outputFileName", help="outputFileName")

    args = parser.parse_args()
    processJsonAndCreateCSV(    inputFileName = args.inputFileName, 
                                outputFileName=args.outputFileName )
