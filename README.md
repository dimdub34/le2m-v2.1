# LE2M-v2.1

LE2M is a software dedicated to experimental economics. It is developed with the Python language. The graphical user interface (GUI) is developed with Qt4. The network exchanges are ensured by the twisted library and the data are stored in a sqlite database, with the SQLAlchemy library.  

## Prerequisites
__Windows__  
Install Python 2.7 and PyQt4. Then in a console, just write: pip install twisted sqlalchemy numpy pandas matplotlib  

__Ubuntu/Debian__  
Python 2.7 is already installed, but if not, install it. Then in a console, just write sudo apt-get install python-qt4 python-twisted python-sqlalchemy python-numpy python-pandas python-matplotlib

## Install  
Put LE2M in a shared directory on the server. Then configure the server by editing the file le2m/configuration/configparam.py, in particular the IP of the server. Create a shortcut of clientrun.py and put this shortcut on the clients' computers (take care to change C:/... to //server/...  (windows) or /home/... to smb://server/... (linux)) in order the shortcut to point to the clientrun.py file through the network.


Additional informations: http://www.duboishome.info/dimitri/index.php?page=le2m&lang=eng
