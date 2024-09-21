from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, get_object_or_404
from .models import Event
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .models import EventBooking
from .forms import EventBookingForm
from django.contrib.auth.decorators import login_required
#from .models import EventUserWishList
#from .forms import EventFeedbackForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView , ListView
from events.models import Event, EventCategory, JobCategory, EventAgenda, EventJobCategoryLinking, EventMember


def index(request):
    # If the user is not logged in, redirect to login page
   return render(request, 'user/index.html')

def redirect_to_admin_login(request):
    return redirect('login')  # Assuming 'login' is the name for the login URL in admin site

def redirect_to_admin_register(request):
    return redirect('register')

@login_required(login_url='login')
def logout_view(request):
    auth_logout(request)
    messages.success(request, 'You have logged out successfully!')
    return redirect('login')

def about(request):
    return render(request, 'user/about.html')

def contact(request):
    return render(request, 'user/contact.html')


class UserEventListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Event
    template_name = 'user/event_list.html'
    context_object_name = 'events'
    paginate_by = 10

@login_required(login_url='login')
class UserEventDetailView(LoginRequiredMixin, DetailView):
    login_url = 'login'
    model = Event
    template_name = 'user/event_detail.html'
    context_object_name = 'event'


# Booking an event
@login_required(login_url='login')
def book_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        # Check if an EventMember already exists for this event and user (including canceled bookings)
        try:
            event_member = EventMember.objects.get(event=event, user=request.user)
            
            if event_member.canceled:
                # If the event was canceled, rebook by updating the existing record
                event_member.canceled = False
                event_member.attend_status = 'waiting'
                event_member.status = 'active'
                event_member.save()
                messages.success(request, 'Event re-booked successfully!')
            else:
                # If already booked and not canceled, the user can cancel the event
                event_member.canceled = True
                event_member.attend_status = 'canceled'
                event_member.status = 'inactive'
                event_member.save()
                messages.success(request, 'Event canceled successfully!')

        except EventMember.DoesNotExist:
            # If no booking exists, create a new EventMember entry
            EventMember.objects.create(
                event=event,
                user=request.user,
                created_user=request.user,
                updated_user=request.user,
                attend_status='waiting',
                status='active',
                canceled=False  # Ensure event is active upon booking
            )
            messages.success(request, 'Event booked successfully!')

        return render(request,'user/book_event.html')  # Redirect to dashboard after booking/canceling
    else:
        # Handle the GET request or render form if needed
        event_member = EventMember.objects.filter(event=event, user=request.user).first()
        return render(request, 'user/book_event.html', {'event': event, 'event_member': event_member})



    
def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'user/event_detail.html', {'event': event})


"""@login_required(login_url='login')  
def event_already_booked(request):  
    return render(request, 'user/event_already_booked.html')  # Create this template

@login_required(login_url='login')  
def event_booked_success(request):  
    return render(request, 'user/event_booked_success.html')  # Create this template

@login_required
def add_to_wishlist(request, pk):
    event = get_object_or_404(Event, pk=pk)
    wishlist, created = EventUserWishList.objects.get_or_create(user=request.user, event=event)
    if created:
        wishlist.status = 'wishlist'
        wishlist.save()
    return redirect('event-detail', pk=pk)

@login_required
def submit_feedback(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.event = event
            feedback.save()
            return redirect('event-detail', pk=pk)
    else:
        form = EventFeedbackForm()
    return render(request, 'user/submit_feedback.html', {'form': form, 'event': event})"""


class UserDashboardView(LoginRequiredMixin, ListView):
    template_name = 'user/dashboard.html'
    context_object_name = 'booked_events'

    def get_queryset(self):
        return EventMember.objects.filter(user=self.request.user)

# views.py in userapp

from events.models import Event, EventDiscussionTopic, EventDiscussionComment
from .forms import DiscussionTopicForm, DiscussionCommentForm

def event_discussion_topics(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    topics = EventDiscussionTopic.objects.filter(event=event)
    return render(request, 'user/event_discussion_topics.html', {'event': event, 'topics': topics})

def add_discussion_topic(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = DiscussionTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.event = event
            topic.created_by = request.user
            topic.save()
            return render(request, 'user/event_discussion_topics.html', {'event': event})
    else:
        form = DiscussionTopicForm()
    return render(request, 'user/add_discussion_topic.html', {'form': form})
