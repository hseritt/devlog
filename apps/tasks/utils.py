def get_task_title(task):
    try:
        title = (
            f"{task.project.prefix}-{task.id} / Subj: {task.subject} / {task.status}"
        )
    except AttributeError as err:
        # Added since prefix is null and can be left blank
        if (
            repr(err)
            == "AttributeError(\"'NoneType' object has no attribute 'prefix'\")"  # noqa: W503
        ):
            title = f"{task.id} / Subj: {task.subject} / {task.status}"

    title += f" / {task.type} / Effort: {task.effort}"

    return title
