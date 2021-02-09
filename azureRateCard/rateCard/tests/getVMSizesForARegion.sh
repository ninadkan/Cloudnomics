#!/bin/bash
# SET the REGION_NAME variable in the environment and don't pass it in the parameter. 
# Huh. That might not be best option when we move all this to an Azure DevOPS pipeline. 
# for the script to execute properly, following needs to be done one-time per terminal?
# tenantID="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXX"
# az login --tenant $tenantID

# set default values
regionName="$CLOUDNOMICS_REGION"
outputlocation="$CLOUDNOMICS_OUTPUT_PATH"

processDownloadingVMList(){
    # At the time of writing this script, the accepted regions were
    
    # 'eastus, eastus2, westus, centralus, northcentralus, southcentralus, 
    # northeurope, westeurope, 
    # eastasia, southeastasia, 
    # japaneast, japanwest, 
    # australiaeast, australiasoutheast, australiacentral, 
    # brazilsouth, 
    # southindia, centralindia, westindia, 
    # canadacentral, canadaeast, 
    # westus2, westcentralus, 
    # uksouth, ukwest, 
    # koreacentral, koreasouth, 
    # francecentral, 
    # southafricanorth, uaenorth, 
    # switzerlandnorth, 
    # germanywestcentral, 
    # norwayeast'

    if [ "$1" ];
    then
        regionName="$1"
    fi

    outputFileName="./AllVmsIn-$regionName.json"
    echo "Region name set to $regionName. Getting the VM list..."

    # Invoke the az function to get the actual list in json
    az vm list-sizes --location "$regionName" --output json >> "$outputFileName"
    echo "...done"

    # check if the output happened ok
    # read $outputFileName
    if [[ -f "$outputFileName" && -s "$outputFileName" ]];
    then
        echo "SUCCESS: $outputFileName file created. Copying it to the $outputlocation folder"
        # move the file to output folder
        mv "$outputFileName" "$outputlocation"
    else
        echo "Error: $outputFileName Not found!"
    fi
}

# SUBSCRIPTION_ID Needs to be set in the environment variable.  
# Azure tenant. 
if [ "$SUBSCRIPTION_ID" ];
    then
        az account set --subscription "$SUBSCRIPTION_ID"
        processDownloadingVMList "$1"
    else
        echo "Need to pass Subscription ID as environment variable"
fi

