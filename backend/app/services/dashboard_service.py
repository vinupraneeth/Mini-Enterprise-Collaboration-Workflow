from datetime import (
    datetime,
    timedelta
)

from sqlalchemy import func, or_, select

from app.models.task_model import Task

from app.models.user_model import User

from app.models.approval_model import (
    Approval
)

from app.models.task_comment_model import (
    TaskComment
)

from app.core.cache import (
    cache_get,
    cache_set
)


def count_records(
    db,
    model,
    *conditions
):

    statement = select(
        func.count(model.id)
    )

    if conditions:

        statement = statement.where(
            *conditions
        )

    return db.execute(statement).scalar_one()


def get_task_conditions(current_user):

    role = current_user.role.lower()

    organization_condition = []

    if current_user.organization_id:

        organization_user_ids = select(User.id).where(
            User.organization_id ==
            current_user.organization_id
        )

        organization_condition.append(
            or_(
                Task.created_by.in_(
                    organization_user_ids
                ),
                Task.assigned_to.in_(
                    organization_user_ids
                )
            )
        )

    if role == "manager":

        return [
            *organization_condition,
            or_(
                Task.created_by == current_user.id,
                Task.assigned_to == current_user.id
            )
        ]

    if role == "employee":

        return [
            *organization_condition,
            Task.assigned_to == current_user.id
        ]

    return organization_condition


def get_visible_task_ids(
    db,
    current_user,
    *task_conditions
):

    statement = select(Task.id)

    if task_conditions:

        statement = statement.where(
            *task_conditions
        )

    return db.execute(
        statement
    ).scalars().all()


def count_visible_comments(
    db,
    current_user,
    *task_conditions
):

    if current_user.role.lower() == "admin":

        return count_records(
            db,
            TaskComment
        )

    task_ids = get_visible_task_ids(
        db,
        current_user,
        *task_conditions
    )

    if not task_ids:

        return 0

    comment_conditions = [
        TaskComment.task_id.in_(task_ids)
    ]

    if current_user.role.lower() == "employee":

        comment_conditions.append(
            TaskComment.is_internal.is_(False)
        )

    return count_records(
        db,
        TaskComment,
        *comment_conditions
    )


def count_pending_approvals(
    db,
    current_user
):

    role = current_user.role.lower()

    active_statuses = [
        "pending",
        "manager_approved",
        "hold"
    ]

    statement = select(
        func.count(Approval.id)
    )

    if role == "admin":

        statement = statement.where(
            Approval.current_level == "admin",
            Approval.status.in_(
                active_statuses
            )
        )

    elif role == "manager":

        statement = statement.outerjoin(
            Task,
            Approval.task_id == Task.id
        ).where(
            Approval.current_level == "manager",
            Approval.requested_by != current_user.id,
            Approval.status.in_(
                [
                    "pending",
                    "hold"
                ]
            ),
            or_(
                Task.created_by == current_user.id,
                Task.assigned_to == current_user.id
            )
        )

    elif role == "employee":

        statement = statement.where(
            Approval.requested_by == current_user.id,
            Approval.current_level != "completed",
            Approval.status.in_(
                active_statuses
            )
        )

    else:

        return 0

    return db.execute(
        statement
    ).scalar_one()


def get_dashboard_analytics(
    db,
    current_user
):

    cache_key = (
        f"dashboard:analytics:user:{current_user.id}:role:{current_user.role}"
    )

    cached = cache_get(
        cache_key
    )

    if cached:

        return cached

    role = current_user.role.lower()

    task_conditions = []

    approval_conditions = []

    # ADMIN

    if role == "admin":

        pass

    # MANAGER

    elif role == "manager":

        task_conditions.extend(
            get_task_conditions(
                current_user
            )
        )

        approval_conditions.append(
            Approval.reviewed_by ==
            current_user.id
        )

    # EMPLOYEE

    elif role == "employee":

        task_conditions.extend(
            get_task_conditions(
                current_user
            )
        )

        approval_conditions.append(
            Approval.requested_by ==
            current_user.id
        )

    total_tasks = count_records(
        db,
        Task,
        *task_conditions
    )

    todo_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status == "todo"
    )

    in_progress_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status == "in_progress"
    )

    review_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status == "review"
    )

    done_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status == "done"
    )

    pending_approvals = count_pending_approvals(
        db,
        current_user
    )

    approved_approvals = count_records(
        db,
        Approval,
        *approval_conditions,
        Approval.status.in_(
            [
                "approved",
                "manager_approved",
                "admin_approved"
            ]
        )
    )

    rejected_approvals = count_records(
        db,
        Approval,
        *approval_conditions,
        Approval.status == "rejected"
    )

    total_comments = count_visible_comments(
        db,
        current_user,
        *task_conditions
    )

    result = {

        "role": role,

        "tasks": {

            "total": total_tasks,

            "todo": todo_tasks,

            "in_progress":
            in_progress_tasks,

            "review":
            review_tasks,

            "done": done_tasks
        },

        "approvals": {

            "pending":
            pending_approvals,

            "approved":
            approved_approvals,

            "rejected":
            rejected_approvals
        },

        "comments": {

            "total": total_comments
        }
    }

    cache_set(
        cache_key,
        result
    )

    return result


def get_ai_summary(
    db,
    current_user
):

    cache_key = (
        f"dashboard:ai-summary:v2:user:{current_user.id}:role:{current_user.role}"
    )

    cached = cache_get(
        cache_key
    )

    if cached:

        return cached

    role = current_user.role.lower()

    task_conditions = get_task_conditions(
        current_user
    )

    pending_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.status != "done"
    )

    high_priority_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.priority == "high",
        Task.status != "done"
    )

    delayed_tasks = count_records(
        db,
        Task,
        *task_conditions,
        Task.due_date < func.now(),
        Task.status != "done"
    )

    insights = [
        f"{pending_tasks} pending tasks need attention.",
        f"{high_priority_tasks} high priority tasks are pending.",
        f"{delayed_tasks} delayed tasks are past their due date."
    ]

    delay_risks = get_delay_risk_tasks(
        db,
        current_user,
        limit=5
    )

    if delay_risks:

        insights.append(
            f"{len(delay_risks)} visible tasks have delay risk signals."
        )

    if pending_tasks == 0:

        insights.append(
            "All visible tasks are completed."
        )

    result = {

        "pending_tasks": pending_tasks,

        "high_priority_tasks": high_priority_tasks,

        "delayed_tasks": delayed_tasks,

        "insights": insights,

        "delay_risks": delay_risks
    }

    cache_set(
        cache_key,
        result
    )

    return result


def normalize_datetime(
    value
):

    if not value:

        return None

    if value.tzinfo:

        return value.replace(
            tzinfo=None
        )

    return value


def calculate_delay_risk(
    task,
    now
):

    score = 0

    reasons = []

    if task.priority == "high":

        score += 35

        reasons.append(
            "High priority"
        )

    elif task.priority == "medium":

        score += 20

    else:

        score += 10

    due_date = normalize_datetime(
        task.due_date
    )

    if due_date:

        if due_date < now:

            score += 40

            reasons.append(
                "Past due date"
            )

        elif due_date <= now + timedelta(days=2):

            score += 25

            reasons.append(
                "Due within 48 hours"
            )

    if task.status in [
        "todo",
        "in_progress"
    ]:

        score += 10

    updated_at = normalize_datetime(
        task.updated_at or task.created_at
    )

    if updated_at and updated_at < now - timedelta(days=5):

        score += 15

        reasons.append(
            "No recent update"
        )

    if not reasons:

        reasons.append(
            "Normal monitoring"
        )

    return min(
        score,
        100
    ), reasons


def get_delay_risk_tasks(
    db,
    current_user,
    limit=5
):

    task_conditions = get_task_conditions(
        current_user
    )

    statement = select(
        Task,
        User.name
    ).outerjoin(
        User,
        Task.assigned_to == User.id
    ).where(
        Task.status != "done",
        *task_conditions
    )

    tasks = db.execute(
        statement
    ).all()

    now = datetime.utcnow()

    risk_items = []

    for task, assignee_name in tasks:

        score, reasons = calculate_delay_risk(
            task,
            now
        )

        if score < 45:

            continue

        risk_items.append(
            {
                "task_id": task.id,
                "title": task.title,
                "priority": task.priority,
                "status": task.status,
                "due_date": task.due_date.isoformat()
                if task.due_date else None,
                "assigned_to": task.assigned_to,
                "assigned_to_name": assignee_name,
                "risk_score": score,
                "reasons": reasons
            }
        )

    return sorted(
        risk_items,
        key=lambda item: item["risk_score"],
        reverse=True
    )[:limit]


def get_employee_assignment_metrics(
    db,
    employee
):

    active_tasks = count_records(
        db,
        Task,
        Task.assigned_to == employee.id,
        Task.status != "done"
    )

    high_priority_tasks = count_records(
        db,
        Task,
        Task.assigned_to == employee.id,
        Task.priority == "high",
        Task.status != "done"
    )

    overdue_tasks = count_records(
        db,
        Task,
        Task.assigned_to == employee.id,
        Task.due_date < func.now(),
        Task.status != "done"
    )

    completed_tasks = count_records(
        db,
        Task,
        Task.assigned_to == employee.id,
        Task.status == "done"
    )

    score = (
        active_tasks * 10
        + high_priority_tasks * 5
        + overdue_tasks * 20
        - min(completed_tasks, 20)
    )

    return {
        "user_id": employee.id,
        "name": employee.name,
        "email": employee.email,
        "active_tasks": active_tasks,
        "high_priority_tasks": high_priority_tasks,
        "overdue_tasks": overdue_tasks,
        "completed_tasks": completed_tasks,
        "score": max(score, 0)
    }


def get_smart_assignment(
    db,
    current_user
):

    if current_user.role.lower() not in [
        "admin",
        "manager"
    ]:

        return {
            "recommendation": None,
            "candidates": []
        }

    employees = db.execute(
        select(User).where(
            User.role == "employee",
            User.is_active.is_(True),
            User.organization_id ==
            current_user.organization_id
        )
    ).scalars().all()

    candidates = [
        get_employee_assignment_metrics(
            db,
            employee
        )
        for employee in employees
    ]

    candidates = sorted(
        candidates,
        key=lambda item: (
            item["score"],
            item["active_tasks"],
            item["name"]
        )
    )

    recommendation = None

    if candidates:

        best_candidate = candidates[0]

        recommendation = {
            **best_candidate,
            "reason": (
                "Lowest current workload score based on active, high priority, overdue, and completed tasks."
            )
        }

    return {
        "recommendation": recommendation,
        "candidates": candidates[:5]
    }


def get_role_dashboard(
    db,
    current_user
):

    analytics = get_dashboard_analytics(
        db,
        current_user
    )

    role = current_user.role.lower()

    if role == "employee":

        return {
            "role": role,
            "title": "Employee Workspace",
            "summary": [
                {
                    "label": "Assigned Tasks",
                    "value": analytics["tasks"]["total"]
                },
                {
                    "label": "My Pending Requests",
                    "value": analytics["approvals"]["pending"]
                }
            ],
            "actions": [
                {
                    "label": "Track Assigned Tasks",
                    "description": "Use the Kanban board to move assigned work through allowed workflow stages.",
                    "target": "kanban"
                },
                {
                    "label": "Raise Approval Request",
                    "description": "Submit leave, laptop, purchase, or task-related requests for review.",
                    "target": "/approvals"
                },
                {
                    "label": "Review Notifications",
                    "description": "Check task assignments, approval updates, and document activity.",
                    "target": "notifications"
                }
            ]
        }

    if role == "manager":

        return {
            "role": role,
            "title": "Manager Control View",
            "summary": [
                {
                    "label": "Team Tasks",
                    "value": analytics["tasks"]["total"]
                },
                {
                    "label": "Pending Approvals",
                    "value": analytics["approvals"]["pending"]
                }
            ],
            "actions": [
                {
                    "label": "Track Team Kanban",
                    "description": "Monitor related tasks and review workflow movement.",
                    "target": "kanban"
                },
                {
                    "label": "Review Approvals",
                    "description": "Approve, reject, or hold requests waiting at manager level.",
                    "target": "/approvals"
                },
                {
                    "label": "Check Activity Feed",
                    "description": "Review recent task, comment, approval, and document activity.",
                    "target": "activity"
                }
            ]
        }

    return {
        "role": role,
        "title": "Admin Monitoring View",
        "summary": [
            {
                "label": "System Tasks",
                "value": analytics["tasks"]["total"]
            },
            {
                "label": "Pending Approvals",
                "value": analytics["approvals"]["pending"]
            }
        ],
        "actions": [
            {
                "label": "Monitor Analytics",
                "description": "Review system workload, completion rate, and approval status.",
                "target": "analytics"
            },
            {
                "label": "Review Admin Approvals",
                "description": "Handle final approval requests and escalated workflow decisions.",
                "target": "/approvals"
            },
            {
                "label": "Open Audit Logs",
                "description": "Inspect immutable system activity for traceability.",
                "target": "/audit-logs"
            }
        ]
    }
