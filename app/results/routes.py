"""
Contains routes for main purpose of app
"""

import os
import shutil
import requests
from ansi2html import Ansi2HTMLConverter
from flask import render_template, abort, request, current_app, redirect
from app.results import bp
from app.models import Submission
from app.settings.settings import APP_BASE_PATH

@bp.route('/results/feedback/<log_id>', methods=['GET', 'POST'])
def get_log(log_id):
    """
    Route for fetching gradable submissions
    """
    if not log_id:
        return { "message": "No Log-id provided" }, 400

    seperator_index = log_id.rfind("-")
    submission_uuid = log_id[:seperator_index]
    submission_id = log_id[seperator_index+1:]

    sub = Submission.query.filter_by(id=submission_id, uuid=submission_uuid).first()

    if not sub:
        return { "message": f"{log_id} not found" }, 400

    conv = Ansi2HTMLConverter()
    ansi = sub.feedback
    html = conv.convert(ansi)


    return render_template(
        "feedback.html",
        sub=sub,
        colored_feedback=html
    )



@bp.route('/results/inspect/<id_>/<uuid_>')
def download_zip(id_, uuid_):
    """
    Displays a file tree
    """
    DL_URL = f"https://bth.instructure.com/files/{id_}/download?download_frd=1&verifier={uuid_}"
    current_app.logger.debug(f"Downloading {DL_URL}")
    TEMP_DIR = APP_BASE_PATH + "/wall_e/temp"

    r = requests.get(DL_URL)
    current_app.logger.debug(f"Response headers {r.headers}")
    if r.headers["Content-Type"] != 'application/zip':
        current_app.logger.info(f"Response code {r.status_code}, url {r.url}")
        current_app.logger.info(f"couldn't download {DL_URL}. Got headers {r.headers}.")
        return abort(404)

    filenamezip = r.headers['Content-Disposition'].split("=")[-1].strip('"')
    filepathzip = f"{TEMP_DIR}/{filenamezip}"
    dirname = filenamezip[:-4]

    with open(filepathzip,'wb') as output_file:
        output_file.write(r.content)
    current_app.logger.debug(f"Done downloading to {filepathzip}")

    shutil.unpack_archive(filepathzip, f"{TEMP_DIR}/{dirname}", format="zip")
    current_app.logger.debug(f"Unpacked zip to {TEMP_DIR}/{dirname}")
    os.remove(filepathzip)

    return redirect(f"/results/browse/{dirname}")



@bp.route('/results/browse/<path:req_path>')
def browse_files(req_path):
    """
    Displays a file tree
    """
    TEMP_DIR = APP_BASE_PATH + "/wall_e/temp"
    file_content = None

    # Finds the previous folder
    previous_directory = "/".join(req_path.split('/')[:-1])
    abs_path = os.path.join(TEMP_DIR, req_path)

    link_content = "/".join(request.path.split('/')[3:])

    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)


    # When a file is requested
    if os.path.isfile(abs_path):
        with open(abs_path, 'r') as file:
            file_content = file.read()
        file_extention = abs_path.split('.')[-1]

        return render_template(
            'browse.html', previous_directory=previous_directory,
            file_type=file_extention, file_content=file_content,
            link_content=link_content)


    # Show directory contents
    files = os.listdir(abs_path)
    return render_template(
        'browse.html', files=files, previous_directory=previous_directory, link_content=link_content)
