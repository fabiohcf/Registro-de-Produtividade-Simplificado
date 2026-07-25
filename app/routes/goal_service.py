#app/routes/goal_service.py

from flask import jsonify, request

from app.models.goal import Goal


# ==========================================================
# Goal V2 constants
# ==========================================================

GOAL_FIELDS = (
    "target_hours",
    "target_questions",
)


# ==========================================================
# Generic validations
# ==========================================================

def get_request_data():
    """
    Obtém o JSON da requisição.
    """

    data = request.get_json()

    if not data:
        return None, (
            jsonify(
                {"error": "Dados JSON são obrigatórios"}
            ),
            400,
        )

    return data, None


def validate_positive_int(value, field_name):
    """
    Valida inteiro positivo.
    """

    if not isinstance(value, int) or value <= 0:

        return (
            jsonify(
                {
                    "error":
                    f"{field_name} deve ser um número inteiro positivo"
                }
            ),
            400,
        )

    return None


def validate_goal_targets(target_hours, target_questions):
    """
    Pelo menos uma meta deve ser informada.
    """

    if target_hours is None and target_questions is None:

        return (
            jsonify(
                {
                    "error":
                    "Informe uma meta de horas e/ou questões."
                }
            ),
            400,
        )

    if (
        target_hours is not None
        and target_hours <= 0
    ):

        return (
            jsonify(
                {
                    "error":
                    "A meta de horas deve ser maior que zero."
                }
            ),
            400,
        )

    if (
        target_questions is not None
        and target_questions <= 0
    ):

        return (
            jsonify(
                {
                    "error":
                    "A meta de questões deve ser maior que zero."
                }
            ),
            400,
        )

    return None


# ==========================================================
# Database helpers
# ==========================================================

def get_goal(db, goal_id):
    """
    Busca uma meta pelo ID.
    """

    goal = db.get(Goal, goal_id)

    if goal is None:

        return None, (
            jsonify(
                {
                    "error":
                    "Meta não encontrada"
                }
            ),
            404,
        )

    return goal, None


def get_week_goal(
    db,
    user_id,
    year,
    week_number,
):
    """
    Retorna a meta da semana.
    """

    return (
        db.query(Goal)
        .filter(
            Goal.user_id == user_id,
            Goal.year == year,
            Goal.week_number == week_number,
        )
        .first()
    )


# ==========================================================
# Business validations
# ==========================================================

def validate_goal_owner(goal, user_id):
    """
    Garante que a meta pertence ao usuário.
    """

    if goal.user_id != user_id:

        return (
            jsonify(
                {
                    "error":
                    "Meta não pertence ao usuário."
                }
            ),
            400,
        )

    return None


def validate_current_week(
    goal,
    current_year,
    current_week,
):
    """
    Permite alterações apenas na semana atual.
    """

    if (
        goal.year != current_year
        or goal.week_number != current_week
    ):

        return (
            jsonify(
                {
                    "error":
                    (
                        "Apenas a meta da semana atual "
                        "pode ser alterada."
                    )
                }
            ),
            400,
        )

    return None


def validate_goal_not_exists(goal):
    """
    Evita duas metas para a mesma semana.
    """

    if goal is not None:

        return (
            jsonify(
                {
                    "error":
                    "Já existe uma meta para esta semana."
                }
            ),
            409,
        )

    return None


# ==========================================================
# Serialization
# ==========================================================

def serialize_goal(goal):
    """
    Serializa uma meta.
    """

    return {
        "id": goal.id,

        "user_id": goal.user_id,

        "year": goal.year,
        "week_number": goal.week_number,

        "target_hours": (
            float(goal.target_hours)
            if goal.target_hours is not None
            else None
        ),

        "target_questions": goal.target_questions,

        "created_at": (
            goal.created_at.isoformat()
            if goal.created_at
            else None
        ),
    }