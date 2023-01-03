import os
from flask import current_app



def grade_submission(submission, test_result):
    """
    Grade submission
    """
    passed_comment = "Testerna har passerat. En rättare kommer läsa din redovisningstext, kolla på koden och sätta betyg."
    failed_comment = "Tyvärr gick något fel i testerna. Läs igenom loggfilen för att se vad som gick fel. Lös felet och gör en ny inlämning."
    error_comment = "Något gick fel i umbridge, kontakta kursansvarig."

    respons = send_zip_archive(submission, test_result)

    if respons is not None:
        if test_result["grade"].lower() == "pg":
            feedback = passed_comment
        elif test_result["grade"].lower() == "ux":
            feedback = failed_comment
        else:
            feedback = error_comment

        id_ = respons["id"]
        uuid = respons["uuid"]

        feedback_text = (
            "Automatiska rättningssystemet 'Umbridge' har gått igenom din inlämning.\n\n"
            f"{feedback}\n\n"
            f"Loggfilen för alla tester kan du se via följande länk: {current_app.config['HOST']}/results/feedback/UPPDATERA\n\n"
            f"Du kan inspektera filerna som användes vid rättning via följande länk: {current_app.config['HOST']}/results/inspect/{id_}/{uuid}\n\n"
            "Kontakta en av de kursansvariga om resultatet är felaktigt."
        )
    else:
        feedback_text = (
            "Automatiska rättningssystemet 'Umbridge' har gått igenom din inlämning.\n\n"
            f"Umbridge kunde inte hitta filerna efter rättningen, försök göra en ny inlämning. Om det inte hjälper, kontakta kursansvarig.\n\n"
            f"Loggfilen för alla tester kan du se via följande länk: {current_app.config['HOST']}/results/feedback/UPPDATERA\n\n"
        )

    payload = {
        "comment": {
            "text_comment": feedback_text,
            "group_comment": not submission.assignment["grade_group_students_individually"]
        },
        "submission": {
            "posted_grade": test_result['grade']
        }
    }

    current_app.logger.debug(f"Set grade {test_result['grade']} for {submission.user['login_id']} in assignment {submission.assignment['name']}")

    submission.edit(**payload)



def send_zip_archive(submission, result):
    """
    Sends archive as a comment
    """
    file_name = result["zip_path"]

    current_app.logger.debug(f"Sending zip as comment to {submission.user['login_id']} in assignment {submission.assignment['name']}")
    try:
        respons = submission.upload_comment(file_name)
    except IOError:
        current_app.logger.error(f"File {file_name} is missing, can't upload file for {submission.user['login_id']} in {submission.assignment['name']}.")
        result["grade"] = "U"
        return None
    current_app.logger.debug(f"zip respons: {respons}")
    os.remove(file_name)
    return respons[1]
