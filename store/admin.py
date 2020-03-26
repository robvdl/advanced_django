from django.contrib import admin

from . import models


admin.site.register(models.Person)
admin.site.register(models.Team)
admin.site.register(models.Project)
admin.site.register(models.Site)
admin.site.register(models.SensorType)
admin.site.register(models.Sensor)
