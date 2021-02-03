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
python3 ../rateCard/allVMsInARegion.py "../output/AllVmsIn-westeurope.json" "../output/AllVmsIn-westeurope.csv"

echo "Finished"
