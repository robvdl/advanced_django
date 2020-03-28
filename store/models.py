from django.utils import timezone
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from timezone_field import TimeZoneField


class Person(models.Model):
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    phone_number = PhoneNumberField()
    email = models.EmailField()
    team = models.ForeignKey('Team', related_name='members', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Team(models.Model):
    name = models.CharField(max_length=254, unique=True)
    timezone = TimeZoneField(default='Pacific/Auckland')
    email = models.EmailField()

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=254, unique=True)
    teams = models.ManyToManyField('Team', related_name='projects')

    def __str__(self):
        return self.name

    def get_team(self):
        current_time = timezone.now()
        local_times = ((team, current_time.astimezone(team.timezone)) for team in self.teams.all())
        team_working = ((team, 8 < time.hour < 17) for team, time in local_times)
        try:
            return next(team for team, working in team_working if working)
        except StopIteration:
            return None


class Site(models.Model):
    name = models.CharField(max_length=254, unique=True)
    project = models.ForeignKey('Project', related_name='sites', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class SensorType(models.Model):
    name = models.CharField(max_length=254, unique=True)
    units = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Sensor(models.Model):
    name = models.CharField(max_length=254)
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    type = models.ForeignKey('SensorType', on_delete=models.CASCADE)
    warning_upper = models.FloatField()
    warning_lower = models.FloatField()

    class Meta:
        unique_together = ('name', 'site')

    def __str__(self):
        return self.name

    @property
    def warnings(self):
        # Should return True if currently active warnings
        return None


class Measurement(models.Model):
    timestamp = models.DateTimeField()
    sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE)
    value = models.FloatField()

    class Meta:
        unique_together = ('timestamp', 'sensor')

    def save(self, *args, **kwargs):
        if self.value > self.sensor.warning_upper or self.value < self.sensor.warning_lower:
            self.raise_alarm()
        self.save(*args, **kwargs)

    def raise_alarm(self):
        team = self.sensor.site.project.get_team()
        if team:
            # Send an email to the team.
            pass
        else:
            # Send an email to the project admins.
            pass
