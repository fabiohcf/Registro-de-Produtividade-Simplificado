# app/routes/api_goals.py

from datetime import datetime, timezone

from flask import Blueprint, request, jsonify

from app.models.goal import Goal
from app.models.user import User
from app.database import SessionLocal


api_goals_bp = Blueprint(
    "api_goals_bp",
    __name__,
    url_prefix="/api/goals"
)


def validate_goal_data(data):
    """Valida dados da meta semanal."""

    errors = []

    if not data.get("user_id"):
        errors.append("ID do usuário é obrigatório")

    elif (
        not isinstance(data["user_id"], int)
        or data["user_id"] <= 0
    ):
        errors.append(
            "ID do usuário deve ser um número inteiro positivo"
        )

    target_hours = data.get("target_hours")
    target_questions = data.get("target_questions")

    if target_hours is None and target_questions is None:
        errors.append(
            "Informe pelo menos uma meta: horas ou questões"
        )

    if target_hours is not None:
        if (
            not isinstance(target_hours, (int, float))
            or target_hours <= 0
        ):
            errors.append(
                "Horas alvo deve ser um número positivo"
            )

    if target_questions is not None:
        if (
            not isinstance(target_questions, int)
            or target_questions <= 0
        ):
            errors.append(
                "Quantidade de questões deve ser um inteiro positivo"
            )

    return errors


def validate_goal_update(data):
    """Valida atualização de meta semanal."""

    errors = []

    target_hours = data.get("target_hours")
    target_questions = data.get("target_questions")

    if target_hours is not None:

        if (
            not isinstance(target_hours, (int, float))
            or target_hours < 0
        ):
            errors.append(
                "Horas alvo deve ser um número positivo ou zero"
            )

    if target_questions is not None:

        if (
            not isinstance(target_questions, int)
            or target_questions < 0
        ):
            errors.append(
                "Quantidade de questões deve ser um inteiro positivo ou zero"
            )

    return errors


@api_goals_bp.route("/", methods=["GET"])
def list_goals():
    session = SessionLocal()

    try:
        goals = session.query(Goal).all()

        return jsonify(
            [
                {
                    "id": goal.id,
                    "user_id": goal.user_id,
                    "year": goal.year,
                    "week_number": goal.week_number,
                    "target_hours": goal.target_hours,
                    "target_questions": goal.target_questions,
                    "created_at": (
                        goal.created_at.isoformat()
                        if goal.created_at
                        else None
                    ),
                }
                for goal in goals
            ]
        ), 200

    finally:
        session.close()


@api_goals_bp.route("/", methods=["POST"])
def create_goal():

    data = request.json

    if not data:
        return jsonify(
            {
                "error": "Dados JSON são obrigatórios"
            }
        ), 400


    errors = validate_goal_data(data)

    if errors:
        return jsonify(
            {
                "error": "Dados inválidos",
                "details": errors
            }
        ), 400


    session = SessionLocal()

    try:

        user = session.get(User, data["user_id"])

        if not user:
            return jsonify(
                {
                    "error": "Usuário não encontrado"
                }
            ), 404


        year, week_number, _ = datetime.now(
            timezone.utc
        ).isocalendar()


        existing_goal = (
            session.query(Goal)
            .filter_by(
                user_id=data["user_id"],
                year=year,
                week_number=week_number,
            )
            .first()
        )


        if existing_goal:

            return jsonify(
                {
                    "error": (
                        "Já existe uma meta "
                        "para esta semana"
                    )
                }
            ), 409



        goal = Goal(
            user_id=data["user_id"],
            year=year,
            week_number=week_number,
            target_hours=data.get("target_hours"),
            target_questions=data.get(
                "target_questions"
            ),
        )


        session.add(goal)
        session.commit()


        return jsonify(
            {
                "message": (
                    "Meta semanal criada "
                    "com sucesso!"
                ),
                "goal": {
                    "id": goal.id,
                    "user_id": goal.user_id,
                    "year": goal.year,
                    "week_number": goal.week_number,
                    "target_hours": goal.target_hours,
                    "target_questions": (
                        goal.target_questions
                    ),
                },
            }
        ), 201


    finally:
        session.close()


@api_goals_bp.route("/<int:goal_id>", methods=["PUT"])
def update_goal(goal_id):

    data = request.json

    if not data:
        return jsonify(
            {
                "error": "Dados JSON são obrigatórios"
            }
        ), 400


    errors = validate_goal_update(data)

    if errors:
        return jsonify(
            {
                "error": "Dados inválidos",
                "details": errors
            }
        ), 400


    session = SessionLocal()

    try:

        goal = session.get(Goal, goal_id)

        if not goal:
            return jsonify(
                {
                    "error": "Meta não encontrada"
                }
            ), 404


        if "target_hours" in data:
            goal.target_hours = data["target_hours"]


        if "target_questions" in data:
            goal.target_questions = data["target_questions"]


        # Se todas as metas foram removidas,
        # elimina o registro
        if (
            (goal.target_hours is None or goal.target_hours == 0)
            and
            (
                goal.target_questions is None
                or goal.target_questions == 0
            )
        ):

            session.delete(goal)
            session.commit()

            return jsonify(
                {
                    "message":
                    "Meta semanal removida"
                }
            ), 200


        # Normaliza zeros para NULL
        if goal.target_hours == 0:
            goal.target_hours = None

        if goal.target_questions == 0:
            goal.target_questions = None


        session.commit()


        return jsonify(
            {
                "message":
                "Meta semanal atualizada com sucesso",
                "goal": {
                    "id": goal.id,
                    "user_id": goal.user_id,
                    "year": goal.year,
                    "week_number": goal.week_number,
                    "target_hours": goal.target_hours,
                    "target_questions":
                        goal.target_questions,
                }
            }
        ), 200


    finally:
        session.close()