# from app.exceptions.exceptions import MissingGroupError
# from flask import current_app

def grade_course(canvas, course_id, course_name):
    course = canvas.get_course(course_id)
    groups = course.get_groups(include=["users"])
    users = course.get_users()
    assignments = course.get_assignments()
    submissions = course.get_multiple_submissions(
        student_ids="all",
        workflow_state="submitted",
    )

    for sub in submissions:
        assignment = get_assignment(assignments, sub.assignment_id)

        if assignment.grade_group_students_individually:
            grade_submission()
        else:
            user_id = sub.user_id
            group = get_group_with_category_and_user(groups, assignment.group_category_id, sub.user_id)

            partners = get_users_group_partners(group, user_id)
            remove_group_partners_submissions(partners, submissions)
            grade_submissions_group()



def grade_submission(submission, users):
    pass



def remove_group_partners_submissions(partners, submissions):
    for sub in submissions:
        for user in partners:
            if sub.user_id == user["id"]:
                print(user)
                # remove sub - i efterhand? ändra inte en lista som loopas igenom




def grade_submissions_group():
    pass



def get_users_group_partners(group, user_id):
    """
    Return a list with a groups users without a user
    """
    return [user for user in group.users if user["id"] != user_id]



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



if __name__ == "__main__":
    from canvasapi import Canvas

    grade_course(canvas, CID, CN)
