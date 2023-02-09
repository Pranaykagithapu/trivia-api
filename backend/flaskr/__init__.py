import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, que):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * 10
    end = start + 10

    questions = [question.format() for question in que]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "GET, POST, PATCH, DELETE, OPTIONS"
        )
        return response

    @app.route("/categories")
    def get_categories():

        categories = Category.query.all()

        if categories:
            response = {
                "success": True,
                "categories": {category.id: category.type for category in categories},
            }
        else:
            abort(404)

        return jsonify(response)

    @app.route("/questions")
    def get_questions():

        que = Question.query.all()
        pag_que = paginate_questions(request, que)
        categories = Category.query.all()

        if pag_que:

            response = {
                "success": True,
                "questions": pag_que,
                "total_questions": len(que),
                "categories": {category.id: category.type for category in categories},
                "total_categories": None,
            }

        else:
            abort(404)
        return jsonify(response)

    @app.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        question = db.session.query(Question).get(question_id)
        db.session.delete(question)
        db.session.commit()
        return jsonify(success=True, deleted=question_id)

    @app.route("/questions", methods=["GET", "POST"])
    def add_question():
        questions_data = json.loads(request.data)

        new_question = questions_data.get("question")
        new_answer = questions_data.get("answer")
        new_difficulty = questions_data.get("difficulty")
        new_category = questions_data.get("category")

        if (
            questions_data,
            new_question,
            new_answer,
            new_category,
            new_difficulty,
        ) == None:
            abort(422)

        question = Question(
            question=new_question,
            answer=new_answer,
            difficulty=new_difficulty,
            category=new_category,
        )
        question.insert()

        return jsonify(
            success=True,
            created=question.id,
            answer=new_answer,
            difficulty=new_difficulty,
            category=new_category,
        )

    @app.route("/questions/search", methods=["GET", "POST"])
    def search_questions():
        questions_data = json.loads(request.data)
        search_term = questions_data.get("searchTerm")
        if search_term:
            questions = (
                db.session.query(Question)
                .filter(Question.question.ilike("%" + search_term + "%"))
                .all()
            )
            return jsonify(
                success=True,
                questions=[question.format() for question in questions],
                total_questions=len(questions),
                current_category=None,
            )

    @app.route("/categories/<int:category_id>/questions", methods=["GET", "POST"])
    def get_questions_by_category(category_id):
        questions_id = (
            db.session.query(Question)
            .filter(Question.category == str(category_id))
            .all()
        )

        return jsonify(
            success=True,
            questions=[question.format() for question in questions_id],
            total_questions=len(questions_id),
            current_category=category_id,
        )

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():

        try:
            body = json.loads(request.data)
            if not all(key in body for key in ["quiz_category", "previous_questions"]):
                abort(422)
            category = body["quiz_category"]
            pre_que = body["previous_questions"]
            if category["type"] == "click":
                available_questions = [
                    question
                    for question in Question.query.all()
                    if question.id not in pre_que
                ]
            else:
                available_questions = [
                    question
                    for question in Question.query.all()
                    if question.category == category["id"]
                    and question.id not in pre_que
                ]
            new_question = (
                random.choice(available_questions).format()
                if available_questions
                else None
            )

            return jsonify({"success": True, "question": new_question})
        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "error": 404, "message": "Not found"}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app
