from http import client
from app import app
import os
from flask import session
from unittest import TestCase
from models import db, User, Feedback, bcrypt


class Flasktests(TestCase):
    def setUp(self):
        """Set Up Function. Will run before any test"""
        self.client = app.test_client()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback-test'
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True

        db.drop_all()
        db.create_all()

        testuser = User.register(
            username='testuser',
            password='password',
            email='test@email.com',
            first_name='first',
            last_name='last')

        testuser_2 = User.register(
            username='testuser2',
            password='password',
            email='test2@email.com',
            first_name='first2',
            last_name='last2')

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp

    def test_home_page(self):

        with self.client as c:
            resp = c.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_login(self):
        """test to check if user logged, """
        with self.client as c:
            with c.session_transaction() as sess:
                sess["user"] = 'testuser'

            resp = c.get("/users/testuser")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h3 class="text-center" style="font-size: 2.5em;">Hello first last </h3>', html)

    def test_unauthorized(self):
        """test to check unauthorized user can view others profile"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess["user"] = 'testuser'

            resp = c.get("/users/testuser2", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # message flash letting user know that they do not have access to this page
            self.assertIn(
                '<div class="alert alert-danger">DO NOT have access to this page!</div>', html
            )
            # due to redirects, home page will still display information about current user
            self.assertIn(
                '<h3 class="text-center" style="font-size: 2.5em;">Hello first last </h3>', html)

    def test_authenticated_delete(self):
        """test to check random user can delete someones account"""
        with self.client as c:
            resp = c.get("/users/testuser/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            # will display message to log in first
            self.assertIn(
                '<div class="alert alert-warning">Please login first!</div>', html
            )

    def test_unauthorized_delete(self):
        """test to check if user logged in can delete another account """
        with self.client as c:
            with c.session_transaction() as sess:
                sess["user"] = 'testuser'

            resp = c.get("/users/testuser2/delete", follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # will recieve flashed message displaying they do not have access
            self.assertIn(
                '<div class="alert alert-danger">DO NOT HAVE ACCESS</div>', html
            )
