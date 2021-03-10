tryurbit - Let's new users experience the Urbit Landscape interface with no technical knowledge

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

