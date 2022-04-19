# Authentication Exercise

This repository contains my work from an assignment from Springboard. In this exercise I created an application that lets users sign up, log in to their own accounts. Once logged in they will be able to add feedback, update feedback and delete. This assignment was written in python using the following tools: Flask, SQLAlchemy. 


# Authentication
I generated and authenticated passwords for users using Flask-Bcrypt. Under models.py where I created the User  model, there are two class methods: register() and authenticate() that are used when creating a User and also to check password during login. 
