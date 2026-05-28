from sqlalchemy.orm import Session

from app.models.task_model import Task


def create_task(

    db: Session,

    task_data,

    created_by: int
):

    task = Task(

        title=task_data.title,

        description=
        task_data.description,

        priority=
        task_data.priority,

        status="todo",

        due_date=
        task_data.due_date,

        assigned_to=
        task_data.assigned_to,

        created_by=created_by,

        updated_by=created_by
    )

    db.add(task)

    db.commit()

    db.refresh(task)

    return task


def get_all_tasks(
    db: Session
):

    return db.query(Task).all()


def get_task_by_id(

    db: Session,

    task_id: int
):

    return db.query(Task).filter(
        Task.id == task_id
    ).first()


def update_task(

    db: Session,

    task: Task,

    task_data,

    updated_by: int
):

    task.title = (
        task_data.title
    )

    task.description = (
        task_data.description
    )

    task.priority = (
        task_data.priority
    )

    task.due_date = (
        task_data.due_date
    )

    task.assigned_to = (
        task_data.assigned_to
    )

    task.updated_by = (
        updated_by
    )

    db.commit()

    db.refresh(task)

    return task


def delete_task(

    db: Session,

    task: Task
):

    db.delete(task)

    db.commit()
