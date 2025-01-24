# Project Status
This app was developed as part of a school project. Due to time constraints and the scope of the assignment, the app remains incomplete.\
While I do not intend to continue development, a substantial portion of the final planned product has been developed, hence why I have uploaded it to GitHub.

# The vision
Ever found yourself mindlessly killing your free time when you could be having fun playing sports? You're not alone.

I wanted to create an app that allows like-minded people to share their sports events with locals. Anyone can register to participate in your event.

The best part about ProActive is about it's recommendation algorithm. It considers weighted factors based on your event participation history, and calculates the most suitable events for you, allowing you to engage with the sports you love.

# Project Structure
(The project set up walkthrough assumes you have downloaded this project fully, frontend and backend!)

## Tech Stack
Front-end (app): **CustomTKinter** (built on top of TKinter)  
Back-end (API): **Flask**  
Database: **PostgreSQL**  
Language: Python
## Client
### About
The client side is built using [CustomTKinter](https://customtkinter.tomschimansky.com/)
### Running the app
To run the app,
1. Go into the client folder, `cd client`
2. Install the required libraries, `pip install -r requirements.py`
3. Exit the client folder, `cd ..`
4. Activate the client's virtual environment, `.\client\env\Scripts\activate`
5. Launch the app, `python -m client.main`
### Notes/Requirements
- The app has a default resolution of 1600x900, make sure your screen is large enough to run!
- The app does not have a responsive layout, it is not suited for mobile use

## Server
## About
The API is built using [Flask](https://flask.palletsprojects.com/)  The database uses a local database from my local installation of [PostgreSQL](https://www.postgresql.org/docs/)

The server and client were developed independently, but concurrently. This effectively means that the API has more features than the client uses.
### Starting a local server to run the API
To start the local server,
1. Go into the server folder, `cd server`
2. Install the required libraries, `pip install -r requirements.py`
4. Activate the server's virtual environment, `.\env\Scripts\activate`
5. Start the server & API, `flask run`

