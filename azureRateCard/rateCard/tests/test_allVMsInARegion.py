# unit test for allVMsInARegion.py
# given the relative import, this file has to be executed from
# the parent folder with following syntax:
# python -m tests.test_allVMsInARegion
# or the other option is to execute it from the same tests folder using either
# pytest ./test_allVMsInARegion.py
# or using following for complete code coverage
# pytest --cov=rateCard .
from rateCard import allVMsInARegion as av
from rateCard import getAzureVMListWithACUs as gaz
import os
import pandas as pd
import logging
import pytest

outputPath = os.environ['CLOUDNOMICS_OUTPUT_PATH']
inputFileName = "AllVmsIn-" + os.environ['CLOUDNOMICS_REGION']
inputFileNameComplete = outputPath+inputFileName+".json"
outputfileNameComplete = outputPath+inputFileName+".csv"


def removeExistingFile(fileName):
    if (os.path.exists(fileName)):
        os.remove(fileName)
    return

@pytest.mark.run(order=1)
def test_success_creation_of_csvfile():
    # PREPARE
    # clear the output folder
    removeExistingFile(outputfileNameComplete)
    # ACT
    av.processJsonAndCreateCSV(inputFileName=inputFileNameComplete,
                               outputFileName=outputfileNameComplete)
    # ASSERT
    assert os.path.isfile(outputfileNameComplete)
    return

@pytest.mark.run(order=2)
def test_unsuccessful_creation_of_csvfile():
    # PREPARE
    # clear the output folder
    removeExistingFile(outputfileNameComplete)
    # ACT
    # av.processJsonAndCreateCSV( inputFileName=inputFileNameComplete+"e",
    #                             outputFileName=outputfileNameComplete)
    # ASSERT
    assert (not os.path.isfile(outputfileNameComplete))
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

@pytest.mark.run(order=3)
def test_functional_csv_file():
    '''
    Test that the file that exists is a csv file and that it can be opened
    and read with non-zero records.
    '''
    test_success_creation_of_csvfile()
    # now open the csv file and check that the length is greater than one
    dfDynamic = getDataFrameFromCSV(fullFileName=outputfileNameComplete)
    assert (isinstance(dfDynamic, pd.DataFrame) and (len(dfDynamic) > 1))

@pytest.mark.run(order=4)
def test_coverage_get_azureVMListWithACUs():
    '''
    Test complete end-2-end happy path of the getAzureVMListWithACUs.py
    '''
    outputFolder = os.environ['CLOUDNOMICS_OUTPUT_PATH']
    originalCSVfile = outputFolder + 'AllVMsIn-' +\
        os.environ['CLOUDNOMICS_REGION'] +\
        '.csv'
    jsonOutputFileName = outputFolder + 'AllResourceData.json'
    outputFileName = outputFolder + 'AzureVMWithACUs.csv'
    finalCombinedCSVFile = outputFolder + 'CombinedVmsIn' +\
        os.environ['CLOUDNOMICS_REGION'] +\
        'WithACU.csv'

    # PREPARE
    assert (os.path.isfile(originalCSVfile))
    removeExistingFile(jsonOutputFileName)
    removeExistingFile(outputFileName)
    removeExistingFile(finalCombinedCSVFile)

    assert (not os.path.exists(jsonOutputFileName))
    assert (not os.path.exists(outputFileName))
    assert (not os.path.exists(finalCombinedCSVFile))

    # ACT
    gaz.invokeAll(regionName=os.environ['CLOUDNOMICS_REGION'],
                  originalCSVfile=originalCSVfile,
                  jsonOutputFileName=jsonOutputFileName,
                  outputFileName=outputFileName,
                  finalCombinedCSVFile=finalCombinedCSVFile)

    # ASSERT
    assert (os.path.exists(jsonOutputFileName))
    assert (os.path.exists(outputFileName))
    assert (os.path.exists(finalCombinedCSVFile))