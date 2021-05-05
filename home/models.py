from django.db import models

from wagtail.core.models import Page, Orderable, TranslatableMixin
from wagtail.core.fields import RichTextField, StreamField
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    StreamFieldPanel,
    PageChooserPanel,
)
from rest_framework import serializers
from rest_framework.fields import Field


from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.api import APIField

from home import block


class ImageSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""
        root = 'http://localhost:8000'
        return {
            "id": value.id,
            "src": root+value.file.url,
            "alt": value.title,
            "width": value.width,
            "height": value.height,
        }


class snippetSerializedField(Field):
    """A custom serializer used in Wagtails v2 API."""

    def to_representation(self, value):
        """Return the image URL, title and dimensions."""

        return {
            "id": value.id,
            "alt": value.title,
        }


class HomePageCarouselImages(TranslatableMixin, Orderable, models.Model):
    """Between 1 and 5 images for the home page carousel."""

    page = ParentalKey("home.HomePage", related_name="carousel_images")
    carousel_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content = StreamField([("cta", block.CTABlock())], null=True, blank=True)

    panels = [ImageChooserPanel("carousel_image"),
              StreamFieldPanel("content"),
              ]
    api_fields = [
        APIField("carousel_image", serializer=ImageSerializedField()),
        APIField("content"),
    ]


class CategoryBanner(TranslatableMixin, Orderable, models.Model):
    """Between 2 and 2 images """

    page = ParentalKey("home.HomePage", related_name="category_banner")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    content_cat = StreamField(
        [("cta", block.CTABlock())], null=True, blank=True)

    panels = [
        ImageChooserPanel("image"),
        StreamFieldPanel("content_cat"),
    ]
    api_fields = [
        APIField("image", serializer=ImageSerializedField()),
        APIField("content_cat"),
    ]


class HomePage(Page):
    """Home page model."""
    banner_title = models.CharField(max_length=100, blank=False, null=True)
    banner_subtitle = RichTextField(features=["bold", "italic"])
    parallax_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    banner_cta = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("banner_title"),
                FieldPanel("banner_subtitle"),
            ],
            heading="Banner Options",
        ),
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=5,
                         min_num=1, label="Image")],
            heading="Carousel Images",
        ),
        MultiFieldPanel([
            ImageChooserPanel("parallax_image"),
        ], heading="Parallax Image"),

        MultiFieldPanel([
            InlinePanel("category_banner", max_num=2,
                        min_num=2, label="Category Banner")

        ], heading="category Banner"),

    ]

    api_fields = [
        APIField("banner_title"),
        APIField("banner_subtitle"),
        APIField("parallax_image", serializer=ImageSerializedField()),
        APIField("carousel_images"),
        APIField("category_banner"),

    ]
