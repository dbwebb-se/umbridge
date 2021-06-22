"""
Contains routes for main purpose of app
"""

from ansi2html import Ansi2HTMLConverter
from flask import render_template
from app.results import bp
from app.models import Submission



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
