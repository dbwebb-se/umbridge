# Features
1. Create an endpoint that returns all assignments that has been corrected by both Umbridge and a teacher.
1. Multiprocessing so can run multiple students at the same time?
1. Remove dependency on canvasapi module. Write code to send zip as comment.
1. Rewrite /browse so it returns a html file with code from all files. Lika a SPA, so we dont send requests back and forth to server.
1. Error handling if canvas is down.
1. Send log as html file instead, so we dont need to save it in DB.
1. When browsing zip content make the log look pretty, use what is used in other show log template.
1. Support for assignment names in canvas not matching dbwebb course names. Ex. "Assignment 1" --> "kmom01" in settings.
1. Extract known error exit codes from being hardcoded.
