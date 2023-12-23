from django.contrib import admin
from .models import Category, Ad, News
from django.urls import reverse
from django.utils.html import format_html

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Ad, CategoryAdmin)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date', 'send_notification_button')

    def send_notification_button(self, obj):
        news_id = obj.id
        url = reverse('send_news_notification', args=[news_id])
        return format_html('<a class="button" href="{}">Send Notification</a>', url)

    send_notification_button.short_description = 'Send Notification'