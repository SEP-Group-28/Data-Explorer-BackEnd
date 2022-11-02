This is for conda environment users

Create conda virtual environment:
    'conda create --name <env_name>'

To see environment list:
    'conda env list'

import packages to your environment and create conda environment  using conda environment(change environment name by editing environment.yml)
    'conda env create -f environment.yml'

import packages to your environment and create conda environment  using pip environment
    'conda create --name <env_name> --file requirements.txt '

Update packages of existing environment 
    'conda env update -n <env_name> --file enviornment.yml'

see imported packages:
    'conda list'

Activate the environment:
    'conda activate <env_name>' or 'activate <env_name>'

Deactivate your conda environment:
    'conda deactivate'

Export your active environment to a new file:
    'conda env export > enviornment.yml'


-------------------------------------------------------

This is for pip environment users

Create virtual environment:
    'python -m venv (<env_name> or path)'

Can use python inside virtual environment by: (but this is annoying and therefore normally we activate the environment and then use its python using following Activate virtual environment code)
    'path\to\venv\Scripts\python.exe <file_name_path>'

Activate virtual environment (for cmd)
    'path\to\venv\Scripts\activate.bat'

Activate virtual environment (for powershell)
    'path\to\venv\Scripts\Activate.ps1'

Deactivate your pip environment:
    'deactivate.bat'

import packages in new virtual env
    'pip install -r requirements.txt'

Export your active environment to a new text file  
    'pip freeze > requirements.txt'
################################################################

Create environment
python -m venv env

activate environment
.\env\Scripts\activate.bat

install dependencies
pip install -r requirements.txt 


then run
