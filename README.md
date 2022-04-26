# Authentication Exercise

This repository contains my work from an assignment from Springboard. In this exercise I created an application that lets users sign up, log in to their own accounts. Once logged in they will be able to add feedback, update feedback and delete. This assignment was written in python using the following tools: Flask, SQLAlchemy. 


# Authentication
I generated and authenticated passwords for users using Flask-Bcrypt. Under models.py where I created the User  model, there are two class methods: register() and authenticate() that are used when creating a User and also to check password during login. 
![carbon (1)](https://user-images.githubusercontent.com/97858179/164064024-3b3c45f1-3b10-4298-9b05-3c08c6fff376.png)

![carbon (2)](https://user-images.githubusercontent.com/97858179/164064248-54a7d982-ee08-4f68-beb0-6b924e932198.png)
# Register or Login
Users when first prompted to home will be sent to login page. 
![login](https://user-images.githubusercontent.com/97858179/164064448-1b80404a-031b-4882-88fc-49a206c42ee6.PNG)

From the navbar there is also a link to the register page where users can create a profile.
![register cat](https://user-images.githubusercontent.com/97858179/164064495-20d40896-b496-4695-acae-5af48452e5ea.PNG)

After a new profile is created, the user is now prompted to their profile page which displays all their information.
![newuser](https://user-images.githubusercontent.com/97858179/165264126-64a2347d-c43d-4563-b14e-4dcb4395ad4f.PNG)

# Adding Feedback
Users are then allowed to create feedback, which are linked only to the current user. 

![add feed](https://user-images.githubusercontent.com/97858179/164064847-db056500-fde1-4766-abf2-910c059b05a8.PNG)

All feedbacks are displayed in the user profile page, where they are allowed to edit and delete any feedback they created.
![profilleee](https://user-images.githubusercontent.com/97858179/164064882-63db3927-24e5-4a79-9742-5fea6192686f.PNG)

