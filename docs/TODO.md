# Features
1. Create an endpoint that returns all assignments that has been corrected by both Umbridge and a teacher.
1. Multiprocessing so can run multiple students at the same time?
1. Remove dependency on canvasapi module. Write code to send zip as comment.
1. Rewrite /browse so it returns a html file with code from all files. Lika a SPA, so we dont send requests back and forth to server.
1. Error handling if canvas is down.
1. Send log as html file instead, so we dont need to save it in DB.
1. When browsing zip content make the log look pretty, use what is used in other show log template.
1. Support for assignment names in canvas not matching dbwebb course names. Ex. "Assignment 1" --> "kmom01".

# Before students arrive

1. Remove the the route `eve/reset`. Comment out
1. Create new python course.




Skriv dokumentation över hela flödet. Och vilka som har tillgång till inloggningsuppgifter. Ta med att det finns länk på canvas till koden. 


dbwebb:42Webbprogrammering!
ZGJ3ZWJiOjQyV2ViYnByb2dyYW1tZXJpbmch

användare hittas inte i course. är inte att den bara hämtar från 1 kurs.

får felet   
File "/home/dbwebb/repo/.dbwebb/test/examiner/helper_functions.py", line 215, in get_testfiles 
    tests = [(dir_, file[:-3]) for file in os.listdir(dir_) if re.match(pattern, file)] 
FileNotFoundError: [Errno 2] No such file or directory: ''
vet inte när eller för vilka användare... kanske har de inte ordentlig inlämning