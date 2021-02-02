"#Cloudnomics" 

Some of the base framework that one needs to install locally for this repository to work
1. My dev environment now is Mac book pro and that is what I've tested on. Meaning Linux only. Sorry Windows folks
2. Install Python3
3. For unit testing of BASH scripts - downloaded the https://github.com/kward/shunit2. I copied the binary and .sh files to my ./tests folder
4. For code coverage installed the 'bashcov' - using the command : sudo gem install bashcov
5. In order to ensure that spurious files are not added, I added following lines to the .gitignore to the 

## Adding following line to ensure that all the environment files are missed. 
**/.venv
## ignore anything that is in the output files
**/output

## for MAC files, ignore the DS_Store
**/.DS_Store

## don't include everything that is part of shunit2 anything that yout don't need to include
**/shunit2-1
## bashcov generates all the code coverage metrics locally under the /coverage folder. Ignore. 
**/coverage
