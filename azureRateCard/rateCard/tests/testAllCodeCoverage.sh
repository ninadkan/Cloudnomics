#!/bin/bash
# Remove previous code coverage output
rm -rf ./htmlcov
rm -rf ./coverage

# test all scripts
bashcov ./testAll.sh
# test all python code
pytest --cov=rateCard .
# create the html from the lastest run
coverage html

# the problem with the previous run is that it come back with 
# code covverage missing %, as the __main__ is not invoked 
# when calling through pytest. Hmmm. and test this manually here
# First one should give error
python3 ../rateCard/allVMsInARegion.py
# second one should work perfectly
python3 ../rateCard/allVMsInARegion.py "$CLOUDNOMICS_OUTPUT_PATH""AllVmsIn-""$CLOUDNOMICS_REGION"".json" "$CLOUDNOMICS_OUTPUT_PATH""AllVmsIn-westeurope.csv"

# Lets create the combined file
python3 ../rateCard/getAzureVMListWithACUs.py   "$CLOUDNOMICS_REGION" \
                                                "$CLOUDNOMICS_OUTPUT_PATH""AllVMsIn-""$CLOUDNOMICS_REGION"".csv" \
                                                "$CLOUDNOMICS_OUTPUT_PATH""AllResourceData.json" \
                                                "$CLOUDNOMICS_OUTPUT_PATH""AzureVMWithACUs.csv" \
                                                "$CLOUDNOMICS_OUTPUT_PATH""CombinedVmsIn""$CLOUDNOMICS_REGION""WithACU.csv"

echo "Finished"