#!/bin/bash
# container for testing all 

baseDownloadFunctionImpl(){
    # for the function to execute properly, following needs to be done one-time per terminal?
    # tenantID="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX"
    # az login --tenant $tenantID
    # extract the correct SubscriptionID and set that as environment variable 
    # the key for the environment variable is SUBSCRPTION_ID

    # default region name
    regionName="westeurope"

    # parameter passed is signal as to test for non-existing region and see what it results
    if [ "$1" ];
    then
        regionName="nonexistingregion"
    fi
    # export REGION_NAME="$regionName"

    outputlocation="../output/"
    # export OUTPUT_LOCATION="$outputlocation"

    # setup the TEST - ARRANGE
    # notice that I do not pass the arguments to this command!!!
    rm $outputlocation*.json

    # execute the test - ACT
    ./getVMSizesForARegion.sh $regionName

    # if the original code changes, this will trigger an error in the test script. 
    outputFileName="AllVmsIn-$regionName.json"
    # check if the output happened ok
    # ASSERT

    if [ "$1" ];
    then
        # want to trigger the false selection. the file should not exist this time around. 
        if [[ ! ( -f "$outputlocation$outputFileName" && -s "$outputlocation$outputFileName" ) ]];
        then
            assertEquals 1 1
        fi
    else
        if [[ -f "$outputlocation$outputFileName" && -s "$outputlocation$outputFileName" ]];
        then
            assertEquals 1 1
        fi
    fi
}


testIncorrectDownloadOfVMList(){
    baseDownloadFunctionImpl "passdummyVariable"
}

PREVIOUS_SUBSCRIPTION_ID=""

testUnsetSubscriptionIDFromEnv(){
    # remove the SUBSCRIPTION_ID from the environment variable and then again execute the test
    # expectatio is that the test should fail
    PREVIOUS_SUBSCRIPTION_ID=$SUBSCRIPTION_ID
    unset SUBSCRIPTION_ID
    testIncorrectDownloadOfVMList
}

# Added this last such that after successful tests, the file is moved to output folder
testCorrectDownLoadOfVMList(){
    export SUBSCRIPTION_ID="$PREVIOUS_SUBSCRIPTION_ID"
    baseDownloadFunctionImpl
}

. ./shunit2

# rm *.csv
# rm *.json
# ./getVMSizesForARegion.sh
# python3 allVMsInARegion.py
# python3 getAzureVMListWithACUs.py
# python3 getAzureRateCard.py
# python3 combineACUandRateCardData.py
# # optional
# python3 testRateCard.py
