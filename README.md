# LE2M-v2.1

LE2M is a software dedicated to experimental economics. It is developed with the 
Python language. The graphical user interface (GUI) is developed with Qt4. 
The network exchanges are ensured by the twisted library and the data are 
stored in a sqlite database, with the SQLAlchemy library.  

## Prerequisites
__Windows__  
Install [Python 2.7](https://www.python.org/downloads/) and 
[PyQt4] (https://riverbankcomputing.com/software/pyqt/download). For PyQt4 
be careful to select the version for Python 2.7. Then install a [Microsoft 
C++ compiler for Python 2.7](https://www.microsoft.com/en-us/download/details.aspx?id=44266)
(this is for twisted, the network library). After that, open a DOS console and 
write the following lines (one by one):  
* pip install twisted
* pip install sqlalchemy
* pip install numpy
* pip install matplotlib
* pip install pandas  

__Ubuntu/Debian__  
Python 2.7 is already installed, but if not, install it. Then in a console, 
just write sudo apt-get install python-qt4 python-twisted python-sqlalchemy 
python-numpy python-pandas python-matplotlib

## Install  
Put LE2M in a shared directory on the server. Then configure the server by 
editing the file le2m/configuration/configparam.py, in particular the IP of 
the server. Create a shortcut of clientrun.py and put this shortcut on the 
clients' computers (take care to change C:\\... to \\\\server\...  (windows) 
or /home/... to smb://server/... (linux)) in order the shortcut to point to 
the clientrun.py file through the network.


Additional informations: 
http://www.duboishome.info/dimitri/index.php?page=le2m&lang=eng
