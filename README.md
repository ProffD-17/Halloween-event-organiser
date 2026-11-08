# Halloween Event Organiser

## Link
[Halloween Event Organiser](https://halloween-event-organiser.onrender.com/)

I used a service called Render's free tier to host it so some delay for it to load when you click the link is normal.

## Description
A web based system for organising and scheduling events for halloween. I find it hard to organise a big event on a groupchat and someone always ends up turning up 2hrs early so this is to make the experience smoother and keep all the information in one place so it is convenient and easy to access. It also encourages community because you might attend an event you wouldn't usually and make new friends. All you need to do is to make an account and host or sign up for events. All information is stored in a database so will be there for everyone. Only times are included in the event information because the date is 31st October for all of them.

If you are actually  going to use this keep in mind everyone can see where and when you are meeting so be careful and have a trusted adult.

## Github repository explanation
- README_screenshots - a folder containing all the screenshots in the readme file.
- flask_session - a folder that contains the flask session trackers. Not sure if I need this in the repo so left it in just in case
- static - contains the CSS and images for the web pages
- templates - all the templates for the different pages
- .gitignore - just ignore it 
- README.md - the readme for the project
- app.py - the logic for the backend and contains all the flask that links it to the frontend
- mydata.db - stores the data for the users and events ect. (wish I'd chose a better name)
- requirements.txt - the things you or Render need to download to run this(only if your running it locally)

## Features
You can:
- Make an account
- Login
- Create events
- Sign up for events
- View who is going to events
- Edit event information
- Delete events

## Inspiration
I just watched the week 9 lecture of CS50 about flask and wanted to put it into practice. It is a great experience to see everything I have learned like python, SQL and HTML all come together in one project to make something actually  useful.

## Technologies
I used:
- HTML and jinja - displaying content on the frontend
- CSS(mainly bootstrap) - making things look spooky and responsive
- Flask - connecting the frontend to the backend
- SQLite - store the users, events and more
- Python - making the logic for everything

Flask and Jinja were new so I had to learn them as I went.

### SQLite database
Here is the schema of the database:

```sql
CREATE TABLE events (
    id INTEGER UNIQUE PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    time TEXT NOT NULL,
    location TEXT NOT NULL,
    host_id INTEGER NOT NULL,
    FOREIGN KEY (host_id) REFERENCES users(id)
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user'
);

CREATE TABLE guests (
    id INTEGER PRIMARY KEY,
    event_id INTEGER,
    guest_id INTEGER,
    FOREIGN KEY (guest_id) REFERENCES users(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);
```

## How to use
You can use it through the web because I hosted it on Render's free tier. If you want to run it locally all the things you need to download are in requirements.txt(don't think you need to download Gunicorn, that is for Render)

### Steps:
1. Make an account or sign in if you already have one
2. Create an event or skip this step if you dont want to host something
    - If you make a mistake or want to change the info of the event you can do so by going to view events -> edit
    - If you want to delete the event it is at the bottom of the edit menu
3. View events that are on and maybe sign up for one
4. Try and break things and let me know what happens so I can fix it
5. Logout

## Next steps
The next steps for this project are:
- Make the front end look actually nice and halloweeny
- Let users see events they are hosting and attending
- Add more event categories

## Notes for reviewers
The password for getting the admin role is in the message you send to reviewers when submitting you project on Terra.

## License
Use whatever you want.

## Screenshots
### Home
![Home page](README_screenshots\home.png)

### Create event
![Create event form](README_screenshots\create_event.png)

### Event info
![Event info page](README_screenshots\event_info.png)