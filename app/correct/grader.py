import os
from flask import current_app



def create_comment_text(grade, file_link="", first_attempt=False, error_send_zip=False):
    """
    Create comment text
    """
    passed_comment = "Testerna har passerat. En rättare kommer läsa din redovisningstext, kolla på koden och sätta betyg."
    error_comment = "Något gick fel i umbridge, kontakta kursansvarig."
    error_send_zip_comment = f"Umbridge kunde inte hitta filerna efter rättningen, försök göra en ny inlämning. Om det inte hjälper, kontakta kursansvarig."

    if first_attempt:
        texts = {
            "intro": "Automatiska rättningssystemet 'Umbridge' har gått igenom din inlämning.",
            "link_text": f"Du kan inspektera loggfilen och koden som användes vid rättning via följande länk: {file_link}",
            "ending": "Kontakta en av de kursansvariga om resultatet är felaktigt.",
            "failed_comment": "Tyvärr gick något fel i testerna. Läs igenom loggfilen för att se vad som gick fel. Lös felet och gör en ny inlämning.",
        }
    else:
        texts = {
            "intro": "Umbridge har gått igenom din inlämning.",
            "link_text": f"Länk till filerna {file_link}",
            "ending": "",
            "failed_comment": "Något gick fel i testerna.",
        }

    if error_send_zip:
        result = error_send_zip_comment
    elif grade == "pg":
        result = passed_comment
    elif grade == "ux":
        result = texts["failed_comment"]
    else:
        result = error_comment

    comment = (
        f"{texts['intro']}\n\n"
        f"{result}\n\n"
        f"{texts['link_text']}\n\n"
        f"{texts['ending']}"
    )

    return comment


def grade_submission(submission, test_result):
    """
    Grade submission
    """
    respons = send_zip_archive(submission, test_result)
    first_attempt = True if submission.attempt == 1 else False

    if respons is not None:
        id_ = respons["id"]
        uuid = respons["uuid"]

        comment = create_comment_text(
            test_result["grade"].lower(),
            f"{current_app.config['HOST']}/results/inspect/{id_}/{uuid}",
            first_attempt,
        )
    else:
        comment = create_comment_text(
            test_result["grade"].lower(),
            first_attempt,
            True,
        )

    payload = {
        "comment": {
            "text_comment": comment,
            "group_comment": not submission.assignment["grade_group_students_individually"],
            "attempt": submission.attempt,
        },
        "submission": {
            "posted_grade": test_result['grade']
        }
    }

    current_app.logger.info(f"Set grade {test_result['grade']} for {submission.user['login_id']} in assignment {submission.assignment['name']}")
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
