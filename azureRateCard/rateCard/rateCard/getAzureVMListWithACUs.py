import adal
import requests
import os
import json
import pandas as pd
import argparse

# What you need to do is execute the following from command line.
# clear
# replace the rbac name with your own choice
# az ad sp create-for-rbac --name NI20125743-sp-rbac-billing
# capture the output and create the azure.sh file and
# on the command line execute source azure.sh.
# example taken from
# https://docs.microsoft.com/en-us/rest/api/compute/resourceskus/list
'''
azure.sh content
export AZURE_SUBSCRIPTION_ID="c4cf8e0a...e5692a10526"
export AZURE_TENANT_ID="a85f58...c30cba5b6da"
export AZURE_CLIENT_ID="9e...5e0e280"
export AZURE_CLIENT_SECRET="BXpb...NOn"

'''


def saveToFile(data, fileName):
    '''
    Saves the json passed in a txt file with file name formatted as
    '1_AABBCCDD.json'
    '''
    with open(fileName, 'w') as f:
        json.dump(data, f)
    return


def getAllResourceData(regionName, outputFileName):
    '''
    Captures all the Azure price list from particular Azure Subscription
    + Tenant  and saves them in a collection of json files.
    '''
    tenant = os.environ['AZURE_TENANT_ID']
    authority_url = 'https://login.microsoftonline.com/' + tenant
    client_id = os.environ['AZURE_CLIENT_ID']
    client_secret = os.environ['AZURE_CLIENT_SECRET']

    resource = 'https://management.azure.com/'
    context = adal.AuthenticationContext(authority_url)
    token = context.acquire_token_with_client_credentials(resource,
                                                          client_id,
                                                          client_secret)

    headers = {'Authorization': 'Bearer ' + token['accessToken'],
               'Content-Type': 'application/json'}

    url = 'https://management.azure.com/subscriptions/' +\
          os.environ['AZURE_SUBSCRIPTION_ID'] +\
          '/providers/Microsoft.Compute/skus?' +\
          'api-version=2019-04-01&$filter=location eq ' +\
          regionName
    # print(url)
    r = requests.get(url, headers=headers)
    if (r.status_code == 200):
        data = r.json()
        saveToFile(data, outputFileName)
    return


'''
{
    "value": [
        {
            "resourceType": "availabilitySets",
            "name": "Classic",
            "locations": [
                "eastus"
            ],
            "locationInfo": [
                {
                    "location": "eastus",
                    "zones": [],
                    "zoneDetails": []
                }
            ],
            "capabilities": [
                {
                    "name": "MaximumPlatformFaultDomainCount",
                    "value": "3"
                }
            ],
            "restrictions": []
        },

........
........
........

        {
            "resourceType": "virtualMachines",
            "name": "Standard_E16ds_v4",
            "tier": "Standard",
            "size": "E16ds_v4",
            "family": "standardEDSv4Family",
            "locations": [
                "southeastasia"
            ],
            "locationInfo": [
                {
                    "location": "southeastasia",
                    "zones": [
                        "2",
                        "1",
                        "3"
                    ],
                    "zoneDetails": [
                        {
                            "Name": [
                                "1",
                                "2",
                                "3"
                            ],
                            "capabilities": [
                                {
                                    "name": "UltraSSDAvailable",
                                    "value": "True"
                                }
                            ]
                        }
                    ]
                }
            ],
            "capabilities": [
                {
                    "name": "MaxResourceVolumeMB",
                    "value": "614400"
                },
                {
                    "name": "OSVhdSizeMB",
                    "value": "1047552"
                },
                {
                    "name": "vCPUs",
                    "value": "16"
                },
                {
                    "name": "HyperVGenerations",
                    "value": "V1,V2"
                },
                {
                    "name": "MemoryGB",
                    "value": "128"
                },
                {
                    "name": "MaxDataDiskCount",
                    "value": "32"
                },
                {
                    "name": "LowPriorityCapable",
                    "value": "True"
                },
                {
                    "name": "PremiumIO",
                    "value": "True"
                },
                {
                    "name": "VMDeploymentTypes",
                    "value": "IaaS"
                },
                {
                    "name": "vCPUsAvailable",
                    "value": "16"
                },
                {
                    "name": "ACUs",
                    "value": "195"
                },
                {
                    "name": "vCPUsPerCore",
                    "value": "2"
                },
                {
                    "name": "CombinedTempDiskAndCachedIOPS",
                    "value": "154000"
                },
                {
                    "name": "CombinedTempDiskAndCachedReadBytesPerSecond",
                    "value": "967835648"
                },
                {
                    "name": "CombinedTempDiskAndCachedWriteBytesPerSecond",
                    "value": "484442112"
                },
                {
                    "name": "CachedDiskBytes",
                    "value": "429496729600"
                },
                {
                    "name": "UncachedDiskIOPS",
                    "value": "25600"
                },
                {
                    "name": "UncachedDiskBytesPerSecond",
                    "value": "402653184"
                },
                {
                    "name": "EphemeralOSDiskSupported",
                    "value": "True"
                },
                {
                    "name": "EncryptionAtHostSupported",
                    "value": "True"
                },
                {
                    "name": "AcceleratedNetworkingEnabled",
                    "value": "True"
                },
                {
                    "name": "RdmaEnabled",
                    "value": "False"
                },
                {
                    "name": "MaxNetworkInterfaces",
                    "value": "8"
                }
            ],
            "restrictions": []
        },


'''


jsonKeyValue = 'value'
jsonKeycapabilities = 'capabilities'
jsonKeyresourceType = 'resourceType'


def ifKeyExistsValue(json, key):
    boolRV = False
    strRV = ""
    if (key in json):
        strRV = json[key]
        boolRV = True
    return strRV, boolRV


def processJsonAndCreateCSV(regionName, inputFileName, outputFileName):
    # ColumnNames= ['maxDataDiskCount', 'memoryInMb', 'name', 'numberOfCores',
    # 'osDiskSizeInMb', 'resourceDiskSizeInMb']
    DATA_LIST = []
    jsonKeyValue = 'value'
    with open(inputFileName) as json_file:
        data = json.load(json_file)
        if jsonKeyValue in data:     # contains 'value'
            value = data[jsonKeyValue]
            for eachItem in value:
                resourceType, b = ifKeyExistsValue(eachItem,
                                                   jsonKeyresourceType)
                if (resourceType == 'virtualMachines'):
                    # initalise our variables
                    name = ""
                    tier = ""
                    size = ""
                    family = ""
                    locationsValue = ""
                    OSVhdSizeMB = 0
                    vCPUs = 0
                    HyperVGenerations = ""
                    MemoryGB = 0
                    MaxDataDiskCount = 0
                    PremiumIO = False
                    vCPUsAvailable = 0
                    ACUs = 0
                    vCPUsPerCore = 0
                    UncachedDiskIOPS = 0

                    # start iterating through the data

                    '''
                    "name": "Standard_E16ds_v4",
                    "tier": "Standard",
                    "size": "E16ds_v4",
                    "family": "standardEDSv4Family",
                    "locations": [
                                "southeastasia"
                                ],
                    ...
                    '''

                    name, b = ifKeyExistsValue(eachItem, "name")
                    tier, b = ifKeyExistsValue(eachItem, "tier")
                    size, b = ifKeyExistsValue(eachItem, "size")
                    family, b = ifKeyExistsValue(eachItem, "family")
                    locations, b = ifKeyExistsValue(eachItem, "locations")
                    if (b):
                        locationsValue = ' '.join([str(item)
                                                   for item in locations])

                    capabilities, b = ifKeyExistsValue(eachItem,
                                                       jsonKeycapabilities)
                    if (b):
                        '''
                        ...
                        ...
                        ...
                            {
                                "name": "OSVhdSizeMB",
                                "value": "1047552"
                            },
                            {
                                "name": "vCPUs",
                                "value": "16"
                            },
                        ...
                        ...
                        ...
                        '''
                        for eachCapabilityItem in capabilities:
                            if (eachCapabilityItem["name"] == "OSVhdSizeMB"):
                                OSVhdSizeMB = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] == "vCPUs"):
                                vCPUs = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] ==
                                    "HyperVGenerations"):
                                HyperVGenerations = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] == "MemoryGB"):
                                MemoryGB = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] ==
                                    "MaxDataDiskCount"):
                                MaxDataDiskCount = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] == "PremiumIO"):
                                PremiumIO = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] == "vCPUsAvailable"):
                                vCPUsAvailable = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] == "ACUs"):
                                ACUs = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] == "vCPUsPerCore"):
                                vCPUsPerCore = eachCapabilityItem["value"]
                            if (eachCapabilityItem["name"] ==
                                    "UncachedDiskIOPS"):
                                UncachedDiskIOPS = eachCapabilityItem["value"]
                    dictObj = {
                        'name1': name,
                        'tier': tier,
                        'size': size,
                        'family': family,
                        'locationsValue': locationsValue,
                        'OSVhdSizeMB': OSVhdSizeMB,
                        'vCPUs': vCPUs,
                        'HyperVGenerations': HyperVGenerations,
                        'MemoryGB': MemoryGB,
                        'MaxDataDiskCount': MaxDataDiskCount,
                        'PremiumIO': PremiumIO,
                        'vCPUsAvailable': vCPUsAvailable,
                        'ACUs': ACUs,
                        'vCPUsPerCore': vCPUsPerCore,
                        'UncachedDiskIOPS':  UncachedDiskIOPS
                    }
                    # cnt += 1
                    # print("----- current count = {} ------".format(str(cnt)))
                    # print("=== name = {}, size = {}, vCPU = {} ,
                    #       Memory = {}, ACUs = {}, vCPUperCore = {}".
                    #       format(name, str(size), str(vCPUs), str(MemoryGB),
                    #       str(ACUs), str(vCPUsPerCore)))
                    DATA_LIST.append(dictObj)

    dfOut = pd.DataFrame(DATA_LIST)
    # reference of calculating the VCPU calculations
    # https://www.wintellect.com/sizing-azure-virtual-machines/
    dfOut['TotalACU'] =\
        dfOut['vCPUsAvailable'].apply(pd.to_numeric)*dfOut['ACUs'].apply(pd.to_numeric)

    dfOut = dfOut[(dfOut['locationsValue'] == regionName)]
    dfOut.to_csv(outputFileName, index=0)
    return


def formatVMName(row):
    strRV = row['name']
    strRV = strRV.replace('Standard_', '')
    # strRV = strRV.replace('Basic_', '')
    strRV = strRV.replace('_', ' ')
    return strRV


def joinTwoExcelFilesIntoOne(firstFileName,
                             secondFileName,
                             firstFileColumnIndex,
                             secondFileColumnIndex,
                             outputFileName):
    dfFirst = pd.read_csv(firstFileName)
    dfFirst.set_index(firstFileColumnIndex)
    dfSecond = pd.read_csv(secondFileName)
    dfSecond.set_index(secondFileColumnIndex)
    # result = pd.concat([dfFirst, dfSecond], axis=1, sort=False)

    result = pd.merge(dfFirst, dfSecond, how="outer",
                      left_on=firstFileColumnIndex,
                      right_on=secondFileColumnIndex)
    result['secondaryName'] = result.apply(lambda row: formatVMName(row),
                                           axis=1)
    result['secondaryName'] = result['secondaryName'].str.strip().str.upper()
    result.to_csv(outputFileName, index=0)
    return


def invokeAll(regionName,
              originalCSVfile,
              jsonOutputFileName,
              outputFileName,
              finalCombinedCSVFile):
    getAllResourceData(regionName=regionName,
                       outputFileName=jsonOutputFileName)
    processJsonAndCreateCSV(regionName=regionName,
                            inputFileName=jsonOutputFileName,
                            outputFileName=outputFileName)
    joinTwoExcelFilesIntoOne(originalCSVfile,
                             outputFileName,
                             'name',
                             'name1',
                             finalCombinedCSVFile)
    return


if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    parser.add_argument("regionName", help="regionName")
    parser.add_argument("originalCSVfile", help="originalCSVfile")
    parser.add_argument("jsonOutputFileName", help="jsonOutputFileName")
    parser.add_argument("outputFileName", help="outputFileName")
    parser.add_argument("finalCombinedCSVFile", help="finalCombinedCSVFile")

    args = parser.parse_args()
    invokeAll(regionName=args.regionName,
              originalCSVfile=args.originalCSVfile,
              jsonOutputFileName=args.jsonOutputFileName,
              outputFileName=args.outputFileName,
              finalCombinedCSVFile=args.finalCombinedCSVFile)
