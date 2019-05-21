from django.db import models

# Student
class Student(models.Model):
    full_name = models.CharField(max_length=250, default='')
    score = models.IntegerField(default=0)
    last_ts = models.IntegerField(default=0)
    current_ts = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, default='')
    prof_img = models.CharField(max_length=250, default='')
    id_num = models.CharField(max_length=250, default='')
    
    def __str__(self):
        return self.full_name + ' - ' + str(self.score)

# US Distance Data
class UsDistance(models.Model):
    us_one = models.IntegerField(default=0)
    us_two = models.IntegerField(default=0)
    us_three = models.IntegerField(default=0)

    def __str__(self):
        return str(self.us_one) + ' - ' + str(self.us_two) + ' - ' + str(self.us_three)
