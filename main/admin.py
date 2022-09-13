from django.contrib import admin
from .models import Tutorial, TutorialSeries, TutorialCategory
from tinymce.widgets import TinyMCE
from django.db import models

class TutorialAdmin(admin.ModelAdmin):
    """ Ordenar los campos como quieras
    fields = [
        "title",
        "published",
        "content"
    ]
    """

    fieldsets = [
        ("Title/date", {"fields": ["title", "published"]}),
        ("URL", {"fields": ["slug"]}),
        ("Series", {"fields": ["series"]}),
        ("Content", {"fields": ["content"]})
    ]

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

# Register your models here.
admin.site.register(TutorialSeries)
admin.site.register(TutorialCategory)
admin.site.register(Tutorial, TutorialAdmin)