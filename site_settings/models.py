from django.db import models

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
# Create your models here.


@register_setting
class SocialMediaSettings(BaseSetting):
    """social media setting for cutom website """

    facebook = models.URLField(blank=True, null=True, help_text='Facebook URL')
    twitter = models.URLField(blank=True, null=True, help_text='Twitter URL')
    youtube = models.URLField(blank=True, null=True, help_text='YouTube URL')

    panels = [
        MultiFieldPanel([
            FieldPanel('facebook'),
            FieldPanel('twitter'),
            FieldPanel('youtube'),
        ], heading='social Medaia Setting'),
    ]


@register_setting
class SnipcartSettings(BaseSetting):
    api_key = models.CharField(
        max_length=255,
        help_text='Your Snipcart public API key'
    )
