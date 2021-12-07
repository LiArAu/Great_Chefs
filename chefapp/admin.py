from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.ShareZone)
admin.site.register(models.RecipeContent)
admin.site.register(models.Comment)
admin.site.register(models.SearchFields)
admin.site.register(models.SearchPreference)
admin.site.register(models.UserProfile)
