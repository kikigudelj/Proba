from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Drive(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    type = models.CharField(max_length=128,blank=True,null=True)
    details = models.TextField(max_length=1000,blank=True,null=True)
    number_of_seats = models.IntegerField(default=3)
    price = models.FloatField(max_length=10, null=True)
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='images', blank=True, null=True)
    status = models.CharField(max_length=128,default="Active")
    def __str__(self):
        return f"{self.id}: {self.title}"
    
    def has_date_passed(self):
        return self.date < timezone.now()
    
    def accept_drive(self, application):
        application.accepted = True
        application.save()
    
    def change_number_of_seats(self, application):
        total_seats_taken = application.seats
        self.number_of_seats -= total_seats_taken
        self.save()

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    driver = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id}: {self.user.username}"

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    drive = models.ForeignKey(Drive, on_delete=models.CASCADE)
    seats = models.IntegerField(default=1)
    accepted = models.BooleanField(default=False)

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.CharField(max_length=128)
    
class Notification(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,related_name="receiver")
    title = models.CharField(max_length=128,blank=True,null=True)
    text = models.TextField(max_length=1000)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"
    
   
