from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)

@receiver(post_save, sender=User)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_teacher_profile(sender, instance, **kwargs):
    print(instance)
    instance.profile.save()


class Student(models.Model):
    student_firstname = models.CharField(max_length = 100)
    student_lastname = models.CharField(max_length = 100)
    student_section = models.CharField(default = 'A', max_length = 100)
    student_batch = models.CharField(max_length=10, default='2019')
    student_dept = models.CharField(max_length = 10, default='EE')
    student_enrollnumber = models.IntegerField()
    student_registrationdate = models.DateField()

