import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Lyric, Save, Rating


os.environ['DATABASE_URL'] = "postgresql:///lyrically-test"


from app import app, CURR_USER

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserModelTestCase(TestCase):
    """Test views for user."""

    def setUp(self):

        db.drop_all()
        db.create_all()

        u1 = User.signup("testuser1@email.com", "password", "testuser1", "Test", "User1", "I am Test User 1!")
        uid1 = 11
        u1.id = uid1

        u2 = User.signup("testuser2@email.com", "password", "testuser2", "Test", "User2", "I am Test User 2!")
        uid2 = 22
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()


    def tearDown(self):

        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Check if basic model works."""

        u = User(email="test@test.com", password="hashed_password", username="usertester", first_name="User", last_name="Tester", bio="I am the User Tester.")

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.saves), 0)
        self.assertEqual(len(u.ratings), 0)

    def test_valid_signup(self):
        """Test user sign up"""

        user_test = User.signup(email="testytest@test.com", password="password", username="testytester", first_name="Testy", last_name="Tester", bio="I am the Testy Tester.")
        uid = 999
        user_test.id = uid
        db.session.commit()

        user_test = User.query.get(uid)
        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.username, "testytester")
        self.assertEqual(user_test.email, "testytest@test.com")
        self.assertNotEqual(user_test.password, "password")
        self.assertTrue(user_test.password.startswith("$2b$"))

    def test_invalid_email_signup(self):
        """Test sign up with email is invalid."""

        invalid = User.signup(None, "password", "testman123", "Test", "Man", "I am test man.")
        uid = 456
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_username_signup(self):
        """Test sign up when username is invalid."""

        invalid = User.signup("test@test.com", "password", None, "Joe", "Tester", "I am Joe Tester.")
        uid = 123
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    
    def test_invalid_password_signup(self):
        """Test sign up with password is invalid."""

        with self.assertRaises(ValueError) as context:
            User.signup("email@email.com", "", "testtest", "Jane", "Test", "I am Jane Test.")
        
        with self.assertRaises(ValueError) as context:
            User.signup("email@email.com", None, "testtest", "Jane", "Test", "I am Jane Test.")


    def test_valid_authentication(self):
        """Test that authenticate class works."""

        u = User.authenticate(self.u1.email, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        """Test authenticate when invalid username is given."""

        self.assertFalse(User.authenticate("bademail", "password"))

    def test_wrong_password(self):
        """Test authenticate when invalid password is given."""

        self.assertFalse(User.authenticate(self.u1.email, "badpassword"))


    