# Flask User API

This is an application that creates,deletes and updates user data. There us two types of users, Parent and Child. The child doesn't have an address and belongs to a parent.

Each type of user has an auto-generated id associated with it which acts as the primary key. The id of the parent type user acts as a foreign key for the child type user.

No new child user can be created if the parent id for it does not exist already.


## Installation
 
Requirements- Flask 1.1.2, SQLite, Python 3.7.0 

Download the project from Git and open it in a python IDE(I used Pycharm). Run the app.py file. After the process starts successfully, open the app on localhost. 
