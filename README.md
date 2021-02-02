# Cloudnomics

"#Cloudnomics" is python and bash library to get RateCard and other cloud cost optimization related items from public cloud (Azure for the time-being). The vision of this code base is to be single place to provide VM/Storage level advise for cloud (Azure) optimizations. 

## Development Machine setup

The base development environment that one needs to install and configure locally for this repository to work:

0. Clone the Github repository https://github.com/ninadkan/Cloudnomics. 
    whilst setting up, I used PAT authentication to configure bi-directional sync.  
1. My dev machine is a Mac book pro and that is what I do active development on. Meaning tested on bash+python only. Sorry Windows folks
2. Installed Python3.
3. Wherever required python environment will be created and called - '.venv'. This is the only name for python environment that'll be used throughout the project. 
    python3 -m venv .venv
    $ source ./.venv/bin/activate
4. For unit testing of BASH scripts - downloaded the https://github.com/kward/shunit2. I cloned the git-hub repository and then copied the binary (shutil2) and *.sh files from the root folders on to my /tests folder. 
5. For code coverage, I Installed the 'bashcov' - using the command : sudo gem install bashcov
6. In order to ensure that spurious files are not added, I added following lines to the .gitignore to the


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
7. The IDE I use is Visual Code. 'shellcheck' extension has been installed to ensure all the bash shell script that I write is linted. 
8. For Python programs, I am using following linter, unit testing and code-coverage tools 
    [flake8](https://flake8.pycqa.org/en/latest/), [pytest](https://docs.pytest.org/en/latest/), pytest-cov
    $ pip install flake8 pytest pytest-cov

    Before commit checklist for python programs
    $ flake8 --statistics 
        output of above should be nothing. The above code should be executed in the folder where python
        main code resides
    $ pytest -v --cov 
        run from the tests folder. 




## Usage

```python
# coming soon ...
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)








