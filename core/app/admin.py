from django.contrib import admin
from .models import Question, BodyPartQuestions, Profile, Appointment

# Register your models here.
admin.site.register(Question)
admin.site.register(BodyPartQuestions)
admin.site.register(Profile)
admin.site.register(Appointment)
