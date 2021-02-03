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