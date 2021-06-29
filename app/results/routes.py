"""
Contains routes for main purpose of app
"""

import os
from ansi2html import Ansi2HTMLConverter
from flask import render_template, abort, request
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

    submission_id, submission_uuid = log_id[-1], log_id[:-1]

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





@bp.route('/results/browse/', defaults={'req_path': ''})
@bp.route('/results/browse/<path:req_path>')
def browse_files(req_path):
    """
    Displays a file tree
    """
    ROOT_DIR = APP_BASE_PATH # Where the base dir is. Change this value.
    file_content = None

    # Finds the previus folder
    previus_directory = "/".join(req_path.split('/')[:-1])
    abs_path = os.path.join(ROOT_DIR, req_path)

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
            'browse.html', previus_directory=previus_directory,
            file_type=file_extention, file_content=file_content,
            link_content=link_content)


    # Show directory contents
    files = os.listdir(abs_path)
    return render_template(
        'browse.html', files=files, previus_directory=previus_directory, link_content=link_content)