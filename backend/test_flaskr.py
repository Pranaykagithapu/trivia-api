import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = (
            "postgresql://postgres:PranayNew@localhost:5432/trivia_test"
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_paginate_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

    def test_404_invalid_page_numbers(self):
        res = self.client().get("/questions?page=10000")
        data = json.loads(res.data)

        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])

    def test_404_invalid_categories(self):
        res = self.client().get("/categories=8")
        data = json.loads(res.data)

        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertFalse(data["categories"])
        self.assertFalse(data["total_categories"])

    def test_404_invalid_questions(self):
        res = self.client().get("/questions=80")
        data = json.loads(res.data)

        self.assertEqual(data["error"], 404)
        self.assertEqual(data["success"], False)

    def test_delete_question(self):
        res = self.client().delete("/questions/2/json/")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)
        self.assertTrue(data["error"], 404)
        self.assertTrue(data["error"], 404)
        self.assertEqual(question, None)

    def test_422_question_not_exist(self):
        res = self.client().delete("/questions/1000/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_add_question(self):
        res = self.client().post("/question/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])
        self.assertTrue(data["error"])

    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post("/question/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_get_question_search_with_results(self):
        res = self.client().post("/questions/search/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])
        self.assertTrue(data["error"])

    def test_404_get_search_unavailable_question(self):
        res = self.client().post("/questions/search/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_get_questions_by_category(self):
        res = self.client().get("categories/1/questions/json")
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])
        self.assertTrue(data["error"])

    def test_404_get_questions_by_category(self):
        res = self.client().get("categories/1000/questions/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_get_quiz(self):
        res = self.client().post("/quizzes/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])

    def test_422_get_quiz(self):
        res = self.client().post("/quizzes/json")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"])


if __name__ == "__main__":
    unittest.main()
