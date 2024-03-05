# Arash Blog

### Content management system with Flask

</br>

My goal in this project is just to have fun and learn new things, that's why I think it needs extensive optimizations.
I hope that my time will help me and I can optimize this project and solve its various problems, I will be very happy if you take a look at the codes and make them better, thank you, friend.


[note: Basic optimizations in the database section, especially website information, must be done]


### --- Images of the software environment ---
![HomePage](https://github.com/alireza01100011/Arash-Blog/assets/95130614/b3e4bab0-4ba7-463f-bca7-700ff16b349e)

</br></br>
<img alt="Posts-Page" src="https://github.com/alireza01100011/Arash-Blog/assets/95130614/b7151e18-dd61-43f0-b9fe-c475b89d163d" width="49%"></img>
<img alt="Post-Page" src="https://github.com/alireza01100011/Arash-Blog/assets/95130614/cb34b4fd-5dd9-4c8f-978b-d450369c5c58" width="49%"></img>
</br></br>
<img alt="Profile-Page" src="https://github.com/alireza01100011/Arash-Blog/assets/95130614/39e039bf-86d9-4d07-a1b8-06e178c39601" width="49%"></img>
<img alt="AdminPanel-Page" src="https://github.com/alireza01100011/Arash-Blog/assets/95130614/44120b9a-8457-4454-b84e-675a41135157" width="49%"></img>
</br></br>

<img  src="https://github.com/alireza01100011/Arash-Blog/assets/95130614/bc834d57-d1f2-4ed1-9b64-0e37e10e0f04" width="100%"></img>
</br></br>

## Description and purpose of this project

</br>

```
English :

This project is a blog with common features and obvious and hidden weaknesses!

The goal of this project is to create a medium-sized project with Flask, and at this stage, without security developments,
 it is not ready to be used in a high-risk production environment.
(Here I mean high-risk areas where hackers are constantly trying to hack your service)

But yes, it can be used for normal environments!

I am trying to create a regular update cycle to continuously make the code better and safer!

I would be happy if you look at the codes and help me! thanks a lot


Persian:

این پروژه یک وبلاگ با امکانات رایج و نقطه ضعف هایی اشکار و پنهان است !

هدف این پروژه پیدا سازی یک پروزه متوسط با فلسک بوده و در این مرحله بدون توسعه هایی امنیتی آمادگی استفاده در محیط پروداکشن پر خطر رو را نداره 
(در اینجا منظور من از پر خطر حوضه هایی است که هکر ها مدام قصد هک کردن سرویس شما رو دارن )

اما برای محیط های معمولی بله میشه استفاده کرد !

من دارم سیع میکنم یک سیکل اپدیت منظم ایجاد کنم تا به صورت مستمر کدهارو بهتر و امن تر کنم !

خوشحال میشم شما هم به کدها نگاهی کنید و به من کمک کنید! خیلی ممنونم 

```

</br></br>

## Technical

</br>

### Technologies used in this WebApplication (docker-compose) : 
  * Python 3.10
  * Flask
  * sqlalchemy -- flask-sqlalchemy
  * MySQL
  * Nginx
  * Redis
  * gunicorn

</br></br>

### Database Models

</br>

```
Note : 
  ORM (flask-sqlalchemy) is used to communicate with the database.
  In the version (0.9), I adapted the codes related to the database with MySQL,
    before that I used to develop the project with SQLlite.

I tried my best to use the relationships in the database optimally, but I believe there are better solutions!
I would be happy if you have any comments...



```

</br></br>

> ### Tables (SITE, INDEXPAGE)

</br>

```
Tables (SITE) and (INDEXPAGE) are used for website settings. I know this method is like a joke,
 but I will soon replace it with another method and these tables will be deleted!
```

</br>
<img alt="Databse-SettingSite" title="Databse-SettingSite" src="https://github.com/alireza01100011/Arash-Blog/assets/95130614/d4114cad-8a6e-4c89-a32f-c7fb810b5f86" width="50%" />

</br>

> ### Tables (The rest of the tables)


```
The rest of the tables are essential tables

File address: './Docts/DataBaseModel.drawio'
```
</br>
<img alt="Databse" title="Databse" src="https://github.com/alireza01100011/Arash-Blog/assets/95130614/4c8427d5-8aae-48be-b3cf-a4f9cd21567f" width="100%" />
</br>


> ### Simple execution model in Docker


```
In this image, I tried to simplify the Docker Compose file for modern development.

It is quite obvious that you can create a more complex structure with multiple instances of a container and
 make the application scalable, as I have tried to make this possible.

An example of my effort:
 creating a common space for storing application files (user and media profiles) see all examples and web server (nginx)
   "because these files are handled by nginx to optimize traffic"

File address: './Docts/SimpleDocker.drawio'
```
</br>
<img alt="Dacker" title="Dacker" src="https://github.com/alireza01100011/Arash-Blog/assets/95130614/9518b90c-4ead-4880-8b69-1a3d5711b0f3" width="100%" />
</br></br>

## Use and setup

</br>

> ### Common steps :
 + Download the latest version of the software <a href="https://github.com/alireza01100011/Arash-Blog/releases/" title="">Click here</a>
 + Copy .env.example to .env
 + Configure the .env file
   + "Almost all settings are in this file"
  




Documents are being completed ....
