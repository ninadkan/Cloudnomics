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
