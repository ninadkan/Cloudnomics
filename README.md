# Foobar

"#Cloudnomics" is python and bash library to get RateCard and related items from cloud (Azure for the time-being)

## Development Machine setup

The base development environment that one needs to install and configure locally for this repository to work
0. Github repository https://github.com/ninadkan/Cloudnomics was created and whilst setting up, PAT authentication was used locally to configure bi-directional sync.  
1. My dev environment now is Mac book pro and that is what I've tested on. Meaning tested on bash+python only. Sorry Windows folks
2. Installed Python3. 
3. created a python environment - and called it - '.venv'. This is the default name that'll be used throughout the project. 
4. For unit testing of BASH scripts - downloaded the https://github.com/kward/shunit2. I cloned the git-hub repositoru and the copied the binary and .sh files from the root folders to my /tests folder. 
5. For code coverage installed the 'bashcov' - using the command : sudo gem install bashcov
6. In order to ensure that spurious files are not added, I added following lines to the .gitignore to the
7. The IDE I use is Visual Code. 'shellcheck' extension has been installed to ensure all the bash shell script that I write is linted. 

```python
# Adding following line to ensure that all the environment files are missed.
**/.venv

# ignore anything that is in the output folder
**/output
# for MAC files, ignore the DS_Store
**/.DS_Store

# don't include everything that is part of shunit2 anything that yout don't need to include
**/shunit2-1

# bashcov generates all the code coverage metrics locally under the /coverage folder. Ignore.
**/coverage
```




## Usage

```python
# coming soon ...
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)








