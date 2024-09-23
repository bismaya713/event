from django.db import models  
from django.contrib.auth.models import User  
from django.utils import timezone  
from django.conf import settings
from events.models import Event


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    

class Event(models.Model):  
    name = models.CharField(max_length=200)  
    date = models.DateTimeField()  
    location = models.CharField(max_length=200, blank=True, null=True)  # Optional field  
    description = models.TextField(blank=True, null=True)  # Optional field  
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):  
        return self.name  

class EventBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)
    status_choices = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=10, choices=status_choices, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

"""class EventFeedback(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  
    feedback = models.TextField()  
    rating = models.PositiveIntegerField()  # Assuming rating out of 5  
    feedback_date = models.DateTimeField(default=timezone.now)  

    def __str__(self):  
        return f'Feedback by {self.user} for {self.event}'  

class EventUserWishList(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_user_wishlist')  
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  
    created_date = models.DateField(auto_now_add=True)  
    STATUS_CHOICES = (  
        ('wishlist', 'Wishlist'),  
        ('purchased', 'Purchased'),  
    )  
    status = models.CharField(choices=STATUS_CHOICES, max_length=10)  

    class Meta:  
        unique_together = ('user', 'event')  

    def __str__(self):  
        return f'{self.user} wishlisted {self.event}'"""
    

# userapp/models.py
class UserEventRegistration(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.event}"


