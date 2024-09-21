"""from django import forms
from .models import EventBooking, EventFeedback

class EventBookingForm(forms.ModelForm):
    class Meta:
        model = EventBooking
        fields = ['event']

class EventFeedbackForm(forms.ModelForm):
    class Meta:
        model = EventFeedback
        fields = ['event', 'feedback', 'rating']
"""

from django import forms
from events.models import EventMember

class EventBookingForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ['attend_status']  # Include fields that are relevant for booking
        widgets = {
            'attend_status': forms.HiddenInput()  # Or other widget if needed
        }

# forms.py in userapp

from events.models import EventDiscussionTopic, EventDiscussionComment

class DiscussionTopicForm(forms.ModelForm):
    class Meta:
        model = EventDiscussionTopic
        fields = ['title']

class DiscussionCommentForm(forms.ModelForm):
    class Meta:
        model = EventDiscussionComment
        fields = ['content']
