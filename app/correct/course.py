
from app.exceptions.exceptions import MissingGroupError
from app.settings.settings import Config
from app.correct.course_manager import CourseManager
from app.correct import grader
from flask import current_app

def course(canvas, course_id, course_name,):
    current_app.logger.debug(f"Course {course_id}, name {course_name}")

    course = canvas.get_course(course_id)
    groups = course.get_groups(include=["users"])
    submissions = course.get_multiple_submissions(
        student_ids="all",
        workflow_state="submitted",
        include=["assignment", "user"]
    )
    current_app.logger.debug(f"submissions {submissions}")

    config = Config(course_name)

    users_to_skip = {}
    for sub in submissions[:10]:
        assignment = sub.assignment
        if should_grade(sub, sub.assignment, users_to_skip, config):
            # test
            CM = CourseManager(course_name, assignment, sub, config)
            result = CM.test()

            # grade
            grader.grade_submission(sub, result)
            
            # handle group submissions
            if assignment["group_category_id"] is not None and not assignment["grade_group_students_individually"]:
                add_users_to_skip_from_group(sub.user_id, groups, assignment, users_to_skip)
        else:
            current_app.logger.debug(f"Skipped correcting {sub.user['login_id']} {assignment['name']}")



def should_grade(sub, assignment, users_to_skip, config):
    """
    should skip if its ignored in config or if group partner has already been graded.
    """
    skip = (
        assignment["group_category_id"] is not None
        and not assignment["grade_group_students_individually"]
        and sub.user_id in users_to_skip.get(assignment["id"], [])
    ) or assignment["name"] in config["ignore_assignments"]

    return not skip




def add_users_to_skip_from_group(user_id, groups, assignment, users_to_skip):
    group = get_group_using_category_and_user(
        groups,
        assignment["group_category_id"],
        user_id
    )
    partners = get_users_group_partners(group, user_id)
    if assignment["id"] in users_to_skip:
        users_to_skip[assignment["id"]].extend(partners)
    else:
        users_to_skip[assignment["id"]] = partners



def get_users_group_partners(group, user_id):
    """
    Return a list with a groups users without a user
    """
    current_app.logger.debug(f"get group partners in group {group} for user: {user_id}")

    return [user["id"] for user in group.users if user["id"] != user_id]



def get_group_using_category_and_user(groups, group_category_id, user_id):
    for group in groups:
        if group.group_category_id == group_category_id:
            if user_id in [user["id"] for user in group.users]:
                return group
    raise MissingGroupError("No group for group_category_id {group_category_id} and user_id {user_id} found")


