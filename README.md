# Dental Management Platform

## Setup

- You will need Python version `3.12.6` to run this project. Please refer to the [Python's documentation](https://www.python.org/downloads/) to install it on your system.
- Make sure you have `poetry` installed on your system. If not, use `pip install poetry` command.
- Configure `poetry` to create virtual environments inside project directory by executing `poetry config virtualenvs.in-project true` command.
- Install dependencies by executing `poetry install` command.
- To enter the virtual environment, use `poetry shell` command.
- Create a super user for development using `python manage.py createsuperuser` command. Make sure you remember the credentials.

## Running the server
- Enter the virtual environment (Refer to the steps mentioned in the Setup section).
- Execute `python manage.py runserver <PORT>` command. Note that providing the port is optional.
