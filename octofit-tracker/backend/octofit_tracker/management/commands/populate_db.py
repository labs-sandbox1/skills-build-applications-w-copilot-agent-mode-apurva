from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from django.db import connection

# Define models for teams, activities, leaderboard, and workouts
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user_email = models.EmailField()
    team = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'email': 'ironman@marvel.com', 'username': 'Iron Man', 'team': 'Marvel'},
            {'email': 'captain@marvel.com', 'username': 'Captain America', 'team': 'Marvel'},
            {'email': 'batman@dc.com', 'username': 'Batman', 'team': 'DC'},
            {'email': 'superman@dc.com', 'username': 'Superman', 'team': 'DC'},
        ]
        for u in users:
            User.objects.create_user(email=u['email'], username=u['username'], password='password')

        # Create activities
        Activity.objects.create(user_email='ironman@marvel.com', team='Marvel', type='Run', duration=30)
        Activity.objects.create(user_email='captain@marvel.com', team='Marvel', type='Swim', duration=45)
        Activity.objects.create(user_email='batman@dc.com', team='DC', type='Cycle', duration=60)
        Activity.objects.create(user_email='superman@dc.com', team='DC', type='Fly', duration=120)

        # Create leaderboard
        Leaderboard.objects.create(team='Marvel', points=75)
        Leaderboard.objects.create(team='DC', points=180)

        # Create workouts
        Workout.objects.create(name='Hero HIIT', description='High intensity workout for heroes', difficulty='Hard')
        Workout.objects.create(name='Sidekick Cardio', description='Cardio for sidekicks', difficulty='Medium')


        # Create unique index on email for users collection using pymongo
        from pymongo import MongoClient
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
