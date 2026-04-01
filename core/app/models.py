from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=300, 
                                     unique=True, 
                                     help_text="The full text of the question to be displayed to the user.")
    
    feature_name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The corresponding short feature name for the model (e.g., 'headache', 'back_pain')."
    )
    
    def __str__(self):
        return f"{self.id}: {self.question_text}"
    
    class Meta:
        ordering = ['id']


class BodyPartQuestions(models.Model):
    body_part = models.CharField(max_length=100, 
                                 unique=True, 
                                 help_text="The name of the body part (e.g., 'torso-lower', 'pelvis'). Must match the SVG ID."
    )
    
    questions = models.ManyToManyField(
        Question,
        help_text="Select the set of questions relevant to this body part."
    )

    def __str__(self):
        return self.body_part
    
    class Meta:
        verbose_name_plural = "Body Part Question Sets"


class Profile(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to="profile_photos/", null=True, blank=True, default='profile_photos/default.jpeg')
    family_doctor = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username
    

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    title = models.CharField(max_length=200, help_text="The name or description of the appointment.")
    date = models.DateField()

    def __str__(self):
        return f"'{self.title}' on {self.date} for {self.user.username}"

    class Meta:
        ordering = ['date']
    
    