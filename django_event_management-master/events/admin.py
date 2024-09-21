from django.contrib import admin
from mapbox_location_field.admin import MapAdmin
from .models import EventDiscussionTopic, EventDiscussionComment

from .models import (
    EventCategory,
    Event,
    JobCategory,
    EventJobCategoryLinking,
    EventMember,
    EventUserWishList,
    UserCoin,
)

admin.site.register(EventCategory)
admin.site.register(Event, MapAdmin)
admin.site.register(JobCategory)
admin.site.register(EventJobCategoryLinking)
admin.site.register(EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'status', 'attend_status', 'canceled')
admin.site.register(EventUserWishList)
admin.site.register(UserCoin)
admin.site.register(EventDiscussionTopic)
admin.site.register(EventDiscussionComment)
