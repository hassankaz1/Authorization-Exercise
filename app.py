from distutils.command.build_scripts import first_line_re
import email
from click import password_option
from flask import Flask, redirect, render_template, request, flash, session
from models import db, connect_db, User, Feedback, bcrypt
from forms import RegisterForm, LoginForm, FeedbackForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
db.create_all()


@app.route("/")
def home_page():
    """Redirects to login page or User Profile"""
    # if user logged in, redirect to user profile
    if "user" in session:
        return redirect(f"/users/{session['user']}")
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Show Form to register User. Handle registration"""
    # if user already login do not show registration form
    if "user" in session:
        return redirect(f"/users/{session['user']}")

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username=username, password=password,
                             email=email, first_name=first_name, last_name=last_name)

        db.session.commit()
        session['user'] = user.username
        flash("Successfull Created Your Account!")
        return redirect(f"/users/{session['user']}")

    else:
        return render_template("registration.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Show Form to log in. Handle login"""

    # check to see if user already logged in
    if "user" in session:
        return redirect(f"/users/{session['user']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!")
            session['user'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template("login.html", form=form)

    return render_template("login.html", form=form)


@app.route('/logout')
def logout_user():
    """Log User out"""

    session.pop('user')
    return redirect('/')


@app.route("/users/<username>")
def user_page(username):
    """Display User Profile Page"""
    # if no user logged in we reroute to login page
    if "user" not in session:
        flash("Please login first!")
        return redirect("/")

    # handle unauthorized user in user profile
    if session["user"] != username:
        flash("DO NOT have access to this page!")
        return redirect("/")

    user = User.query.filter_by(username=username).first()

    return render_template("user_page.html", user=user)


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Display Form for adding new feedback, handle form"""
    # handle no logged in user
    if "user" not in session:
        flash("Please login first!")
        return redirect("/")

    # handle unauthorized user
    if session["user"] != username:
        flash("DO NOT have access to this page!")
        return redirect("/")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        flash(f"Feedback - {title} created!")
        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("add_feedback.html", form=form)


@app.route("/feedback/<feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Display Form for updating feedback, handle form"""
    # handle no user
    if "user" not in session:
        flash("Please login first!")
        return redirect("/")

    feedback = Feedback.query.filter_by(id=feedback_id).first()

    # handle unauthorized user
    if session["user"] != feedback.username:
        flash("DO NOT have access to this page!")
        return redirect("/")

    form = FeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        flash(f"Feedback {feedback.title} updated")
        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("update_feedback.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    if "user" not in session:
        flash("Please login first!")
        return redirect("/")

    feedback = Feedback.query.filter_by(id=feedback_id).first()

    if session["user"] != feedback.username:
        flash("DO NOT HAVE ACCESS")
        return redirect("/")

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")
