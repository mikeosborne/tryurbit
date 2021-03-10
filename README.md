tryurbit - Lets new users experience the Urbit Landscape interface with no technical knowledge

[![awesome urbit badge](https://img.shields.io/badge/~-awesome%20urbit-lightgrey)](https://github.com/urbit/awesome-urbit)
<<<<<<< HEAD
tryurbit consists of a web front end based on the Flask framework and a backend database and system script. 

The web front end:
 - collects minimal information: name, email, newsletter optin
 - redirects the landing page to a live Urbit Landscape instance with a comet ID
 - updates the backend database to tie the user to a comet
 
The script:
 - mines comets, creating a pool for use
 - extracts the code for the comet
 - boots the comet and records the pid and port it runs on
 - updates the database and logs for each of these processes
 - scans the database for comets that have expired and cleans them up
=======


tryurbit consists of a web front end based on the Flask framework and a series of server side scripts to:
 - mine comets
 - extract the code for the comet
 - start the process and record the port it runs on
 - update the database and logs for each of these processes
>>>>>>> b52064a97b7d6444c334942a13d53f824b585f5e

