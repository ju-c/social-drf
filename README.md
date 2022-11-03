# Simple Social Media App with Django Rest Framework

The final aim:
- User can register & login.
- User can create posts with photos and videos.
- Other users can comment (with photos and videos) on posts.
- User can follow and/or unfollow another users.
- User can like and/or unlike a post.
- Runs on PostgreSQL backend.
- Tested ([Code coverage](#code-coverage)).  

**It is not meant for production**,but just provides some starting points for building a real-world project.

## Running Social DRF on your local machine
You must have `Docker` and `Docker Compose`.
If it's not the case:
- [Install Docker](https://docs.docker.com/engine/install/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)  

Run `docker-compose`:  
```bash
docker-compose build
```  
Then
```bash
docker-compose up -d
```  
Execute management command inside docker-compose  
```bash
docker-compose exec social-drf python manage.py makemigrations
docker-compose exec social-drf python manage.py migrate
docker-compose exec social-drf python manage.py createsuperuser
```  
Then
```bash
docker-compose down
docker-compose up -d
```  

now you can open the browser to http://localhost:8000/api/v1/swagger/ to view the project documentation.

## Code Coverage  

Social DRF has a code coverage of **91%**.  

To run code coverage inside docker:  
```bash
docker-compose exec social-drf coverage run --source='.' manage.py test
```  
You can see the report by typing the following command:  
```bash
docker-compose exec social-drf coverage report
```