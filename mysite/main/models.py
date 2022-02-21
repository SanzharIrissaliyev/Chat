from django.db import models
from django.core.validators import FileExtensionValidator


class Siteuser(models.Model):
    last_name = models.CharField(max_length=200, blank=True)
    first_name = models.CharField(max_length=200, blank=True)
    middle_name = models.CharField(max_length=200, blank=True)
    iin = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    email = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='upload', blank=True)

    def __str__(self):
        return self.last_name + ' ' + self.phone


class Group(models.Model):
    title = models.CharField(max_length=300)
    members_count = models.IntegerField(default=0)
    status = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class GroupUser(models.Model):
    title = models.CharField(max_length=300, default='test')
    members_count = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    group = models.ForeignKey(Group, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(Siteuser, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Sms(models.Model):
    from_user_id = models.IntegerField(default=0)
    to_user_id = models.IntegerField(default=0)
    group_id = models.IntegerField(default=0)
    date_time = models.DateTimeField(blank=True)
    image = models.ImageField(upload_to='upload', blank=True)
    file = models.FileField(upload_to='upload', blank=True)
    #video = models.FileField(upload_to='videos_uploaded', null=True, validators=[
    #    FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    status = models.IntegerField(default=0) # -1 deleted, 0 - dostavleno, 1 prochteno
    sms = models.TextField(default="", blank=True)

    def __str__(self):
        return self.sms
