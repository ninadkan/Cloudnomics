# unit test for allVMsInARegion.py
# given the relative import, this file has to be executed from 
# the parent folder with following syntax:
# python -m tests.test_allVMsInARegion
# or the other option is to execute it from the same tests folder using either 
# pytest ./test_allVMsInARegion.py
# or using following for complete code coverage
# pytest --cov=rateCard . 
from rateCard import allVMsInARegion as av
import os
import pandas as pd
import logging

outputPath = "../output/"
inputFileName="AllVmsIn-westeurope"
inputFileNameComplete = outputPath+inputFileName+".json"
outputfileNameComplete = outputPath+inputFileName+".csv"

def removeExistingFile():
    if (os.path.exists(outputfileNameComplete)):
        os.remove(outputfileNameComplete)
    return

def test_success_creation_of_csvfile():
    # PREPARE
    # clear the output folder
    removeExistingFile()
    # ACT
    av.processJsonAndCreateCSV( inputFileName=inputFileNameComplete,
                                outputFileName=outputfileNameComplete)
    # ASSERT
    assert os.path.isfile(outputfileNameComplete)
    return

def test_unsuccessful_creation_of_csvfile():
    # PREPARE
    # clear the output folder
    removeExistingFile()
    # ACT
    # av.processJsonAndCreateCSV( inputFileName=inputFileNameComplete+"spuriousData",
    #                             outputFileName=outputfileNameComplete)
    # ASSERT
    assert (os.path.isfile(outputfileNameComplete) == False)
    return

def getDataFrameFromCSV(fullFileName):
    # from io import StringIO

    logging.info(fullFileName)
    dfDynamic = None
    try:
        dfDynamic = pd.read_csv(fullFileName)
    except Exception as e:
        logging.error("Error reading data file. Error = {}".format(str(e)))
        pass
    return dfDynamic



def test_functional_csv_file():
    '''
    Test that the file that exists is a csv file and that it can be opened
    and read with non-zero records.
    '''
    test_success_creation_of_csvfile()
    # now open the csv file and check that the length is greater than one
    dfDynamic = getDataFrameFromCSV(fullFileName=outputfileNameComplete)
    assert (isinstance(dfDynamic, pd.DataFrame) and (len(dfDynamic) > 1))

