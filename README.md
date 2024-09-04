
                                            Spam Caller Detection

This project is designed to help identify and manage spam calls by leveraging user-generated reports. The project can be run using either SQLite3 or MySQL as the database.


                                                Database Setup


Using SQLite3
    1) Navigate to the settings.py file in the spam_caller directory.
    2) Comment out the MySQL database credentials.
    3) Uncomment the SQLite3 configuration to enable SQLite3 as your database.
    
Using MySQL with Docker
    1) Ensure you have Docker installed and set up on your system.

    2) Open your terminal and navigate to the project directory.

    3) Run the following command to start the MySQL database with Docker:

        docker-compose -f mysql-docker-compose.yml up

                                            Initial Data Population
The api_test directory contains three scripts to populate your database with random data. Before running these scripts, make sure to apply migrations.

    1) Apply migrations:

        python manage.py makemigrations
        python manage.py migrate

    2) Run the scripts in the following order:

        generate_random_registration_data.py: This script generates random users.
        generate_random_contact_data.py: Generates random contacts for the users.
        set_spam_number.py: Marks specific numbers as spam.
        Note: After running the first script, random users will be created in the database. Before running the second and third scripts, copy a username from the User table and paste it into the user_name variable in the scripts to authenticate.

                                            Project Structure
The project consists of three main apps:

    1) API: This is the secondary gateway after the root URLs, redirecting to the contacts and users apps.
    2) Contacts: This app contains the core logic of the project, managing contacts and spam reports.
    3) Users: This app handles authentication and user management.
