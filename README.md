**UniGym Project
-Author: Hongtao Liu 24010936
This section provides step by step instructions to deploy and run the UniGym system on your local machine.

Step 1. Install Python
1.	Go to the official Python website: https://www.python.org/downloads/ 
2.	Download and install the latest Python 3.13 or above.
3.	During the installation, tick the option “Add Python to PATH”
4.	After installation, open a terminal (PowerShell or CMD) and check your Python installation by running:
python --version 
or
py --version
You should be able to see your Python version 3.13.0 

Step 2. Clone the source code and set up Virtual Environment
1.	Open a terminal and clone the project repository:
git clone https://github.com/aaaTaooo/UniGym
cd UniGym
2.	Set up the Virtual Environment:
python -m venv .venv
or
py -m venv .venv
3.	Enable script execution and activate the environment
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\.venv\Scripts\activate
You should now see (.venv) before your terminal prompt.

Step 3. Install requirements dependency:
With the virtual environment activated, install the necessary Python packages
pip install Django
pip install Pillow

Step 4. Set up the database 
1.	Create database migration files based on the Django models:
python manage.py makemigrations
2.	Apply the migrations to generate the database schema:
python manage.py migrate

Step 5. Create your own superuser account:
	python manage.py createsuperuser
Follow the instructions and enter your own username, email, and password. This account will have all administrative privileges.

Step 6. Run the development server:
1.	Start the Django server:
python manage.py runserver
2.	Open your browser and enter 
http://127.0.0.1:8000/admin 
3.	Login with your superuser account.
In the Superuser dashboard, click ‘+Add’ Users under the ‘USERS’ section to create a new admin account.
4.	Enter your username and email address, select Role as admin, enter your password, tick staff status and click ‘SAVE’. 
5.	Now you are in the admin profile, tick “Is approved” and click “SAVE” on the bottom.
6.	New return to 
http://127.0.0.1:8000/ 

Step 7. Deployment completed
The UniGym system is now successfully running on your local server. You can begin testing different user roles (member, trainer, admin) and explore all available functionalities.
