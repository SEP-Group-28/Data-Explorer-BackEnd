This the backend of Crypstoxplorer

##First install python version 3.9.12 to your pc

##Create the environment using python version 3.9.12 using below command
python -m venv env


##on Unix,mac Activate environment
source env/bin/activate

##On windows Activate environment
.\env\Scripts\activate.bat

##Install dependencies
pip install -r requirements.txt 

##Install last TA-Lib dependency using below command
pip install TA_Lib-0.4.24-cp39-cp39-win_amd64.whl

#Then run below code
flask run

##CAUTION
(Since we have already host the backend in AWS EC-2 instance and this backend already connected to the mongodb
, dont run this backend , because it will make conflicts in mongodb and might cause to duplicate data using two backends)
