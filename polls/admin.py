from django.contrib import admin

from .models import Applicant, Choice, Vote, Positions

# Register your models here.
admin.site.register(Applicant)

admin.site.register(Choice)

admin.site.register(Vote)

admin.site.register(Positions)