# from app.exceptions.exceptions import MissingGroupError
# from flask import current_app

from flask import current_app
from app.settings.settings import Config

def course(canvas, course_id, course_name,):
    current_app.logger.debug(f"Course {course_id}, name {course_name}")

    course = canvas.get_course(course_id)
    groups = course.get_groups(include=["users"])
    users = course.get_users()
    assignments = course.get_assignments()
    submissions = course.get_multiple_submissions(
        student_ids="all",
        workflow_state="submitted",
        include=["assignment"]
    )
    current_app.logger.debug(f"submissions {submissions}")

    config = Config(course_name)


    users_to_skip = {}
    for sub in submissions:
        assignment = get_assignment(assignments, sub.assignment_id)
        if should_grade(sub, users_to_skip, assignment, config):
            # grade
            if assignment.group_category_id is not None and not assignment.grade_group_students_individually:
                add_users_to_skip_from_group(sub.user_id, groups, assignment, users_to_skip)
            print("graded", sub)
        else:
            print("Skipped", sub)



def should_grade(sub, users_to_skip, assignment, config):
    """
    should skip if graded group partner if group assignment
    and if setting says it should skip assignment
    """
    skip = (
        assignment.group_category_id is not None
        and not assignment.grade_group_students_individually
        and sub.user_id in users_to_skip.get(assignment.id, [])
    ) or assignment.name in config["ignore_assignments"]

    return not skip




def add_users_to_skip_from_group(user_id, groups, assignment, users_to_skip):
    group = get_group_with_category_and_user(
        groups,
        assignment.group_category_id,
        user_id
    )
    partners = get_users_group_partners(group, user_id)
    if assignment.id in users_to_skip:
        users_to_skip[assignment.id].extend(partners)
    else:
        users_to_skip[assignment.id] = partners



def grade_submission(submission, users):
    pass



def get_group_partners_submissions(partners, submissions, submissions_to_skip):
    for sub in submissions:
        for user in partners:
            if sub.user_id == user["id"]:
                submissions_to_skip.append(sub)
    return submissions_to_skip


def grade_submissions_group():
    pass



def get_users_group_partners(group, user_id):
    """
    Return a list with a groups users without a user
    """
    current_app.logger.debug(f"group {group} for user: {user_id}")

    return [user["id"] for user in group.users if user["id"] != user_id]



def get_assignment(assignments, assignment_id):
    for assignment in assignments:
        if assignment.id == assignment_id:
            return assignment



def get_group_with_category_and_user(groups, group_category_id, user_id):
    for group in groups:
        if group.group_category_id == group_category_id:
            if user_id in [user["id"] for user in group.users]:
                return group
    # raise MissingGroupError("No group for group_category_id {group_category_id} and user_id {user_id} found")

# hitta användares grupp
# sparas deras id
# vid ny rättning
# jämför mot id

if __name__ == "__main__":
    from canvasapi import Canvas

    canvas = Canvas(
        URL,
        TOKEN
    )

    course(canvas, CID, CN)
