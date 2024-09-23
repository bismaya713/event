from django.urls import path
from . import views
from .views import profile_view
from .views import book_event ,UserEventListView, UserEventDetailView
from .views import UserDashboardView,logout_view
app_name = 'userapp'

urlpatterns = [
    path('', views.index, name='userapp_index'),
    path('login/', views.redirect_to_admin_login, name='login'),
    path('register/', views.redirect_to_admin_register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('events/', UserEventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.event_detail, name='event-detail'),
    path('events/<int:pk>/book/', views.book_event, name='book-event'),
    #path('events/<int:pk>/wishlist/', views.add_to_wishlist, name='add-to-wishlist'),
    #path('events/<int:pk>/feedback/', views.submit_feedback, name='submit-feedback'),
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('events/<int:event_id>/discussion/', views.event_discussion_topics, name='event-discussion-topics'),
    path('events/<int:event_id>/discussion/add/', views.add_discussion_topic, name='add-discussion-topic'),
    path('events/<int:event_id>/polls/', views.event_polls, name='event-polls'),
    path('polls/<int:poll_id>/vote/', views.vote_poll, name='vote-poll'),
    path('events/<int:event_id>/questions/', views.event_questions, name='event-questions'),
    path('events/<int:event_id>/questions/ask/', views.ask_question, name='ask-question'),
    path('events/<int:event_id>/questions/<int:question_id>/delete/', views.delete_question, name='delete-question'),
    path('profile/', profile_view, name='profile'),
]