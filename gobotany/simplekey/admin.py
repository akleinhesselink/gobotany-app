from django.contrib import admin

from gobotany.admin import GoBotanyModelAdmin
from gobotany.core.models import Video
from gobotany.search.models import PlainPage

class VideosInline(admin.TabularInline):
    model = PlainPage.videos.through
    extra = 0

class PlainPageAdmin(GoBotanyModelAdmin):
    exclude = ('videos',)
    inlines = (VideosInline,)

admin.site.register(PlainPage, PlainPageAdmin)
admin.site.register(Video)
