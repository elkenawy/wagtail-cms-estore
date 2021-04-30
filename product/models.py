
from rest_framework import serializers
from django.db import models
from django import forms
from modelcluster.models import ClusterableModel
from rest_framework.fields import Field
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.models import TranslatableMixin
from django.conf import settings
from wagtail.contrib.modeladmin.options import ModelAdmin
from wagtail.admin.forms import WagtailAdminModelForm
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from django_extensions.db.fields import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from wagtail.core.fields import StreamField
from wagtail.api import APIField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TagBase, ItemBase, TaggedItemBase

# Create your models here.


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


class ProductTag(TaggedItemBase):
    content_object = ParentalKey(
        'product.ProductDetailPage',
        related_name='tagged_items',
        on_delete=models.CASCADE,
    )

# class ProductTag(TagBase):
#     class Meta:
#         verbose_name = "Product tag"
#         verbose_name_plural = "Product tags"


# class TaggedProduct(ItemBase):
#     tag = models.ForeignKey(
#         ProductTag, related_name="tagged_Products", on_delete=models.CASCADE
#     )
#     content_object = ParentalKey(
#         to='product.ProductDetailPage',
#         on_delete=models.CASCADE,
#         related_name='tagged_items'
#     )

@register_snippet
class Brand(models.Model):
    title = models.CharField(max_length=255)

    api_fields = [
        APIField("title")
    ]

    panels = [
        FieldPanel('title'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Brands"


@register_snippet
class Collections(models.Model):
    title = models.CharField(max_length=255)

    panels = [
        FieldPanel('title'),
    ]
    api_fields = [
        APIField("title")
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Collections"


@register_snippet
class Color(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    api_fields = [
        APIField("name")
    ]

    def __str__(self):
        return self.name


@register_snippet
class Size(models.Model):
    name = models.CharField(max_length=20)
    code = models.CharField(max_length=10, blank=True, null=True)

    api_fields = [
        APIField("name")
    ]

    def __str__(self):
        return self.name


@register_snippet
class Category(TranslatableMixin, MPTTModel, models.Model):
    # parent = models.ForeignKey(
    #     'self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='children')
    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from='title',
        editable=True,
        # verbose_name='slug',
        # allow_unicode=True,
        # max_length=255,
        # help_text='A Slug to identify posts by this Category'
    )
    icon = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+', blank=True, null=True
    )

    class MPTTMeta:
        order_insertion_by = ['title']

    api_fields = [
        APIField("parent"),
        APIField("title"),
        APIField("slug"),
        APIField("icon"),
    ]
    panels = [
        FieldPanel('parent'),
        FieldPanel('title'),
        FieldPanel('slug'),
        ImageChooserPanel('icon'),

    ]

    def __str__(self):
        return self.title


class Store(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]


class ProductIndexPage(Page):
    intro = RichTextField(blank=True)

    subpage_types = ['ProductDetailPage']

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]
    templates = 'product/product_index_page.html'

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        products_list = self.get_children().live().order_by('-first_published_at')
        context['products_list'] = products_list

        return context


class ProductDetailPage(Page):
    """parental Product detail page"""
    template = 'product/product_detail_page.html'
    tags = ClusterTaggableManager(through='product.ProductTag', blank=True)
    brand = models.ForeignKey(
        'product.brand',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    # categories = ParentalManyToManyField('product.ProductCategory', blank=True)
    category = ParentalManyToManyField(
        'product.Category', blank=True, )
    # name = models.CharField(max_length=250)
    discount = models.CharField(max_length=250, blank=True, null=True)
    description = RichTextField(blank=True)
    price = models.DecimalField(
        blank=False, null=True, max_digits=9, decimal_places=2)
    sale = models.BooleanField(default=False, verbose_name='Sale')
    new = models.BooleanField(default=True, verbose_name='New')
    collection = ParentalManyToManyField(Collections, blank=True)
    stock = models.PositiveIntegerField(default=0)

    parent_page_types = ['ProductIndexPage']
    subpage_types = []

    # def clean(self):
    #     super(ProductDetailPage, self).clean()
    #     self.tags = "{} {}".format(self.collection, self.brand)

    # def main_image(self):
    #     gallery_item = self.gallery_images.first()
    #     if gallery_item:
    #         return gallery_item.image
    #     else:
    #         return None

    # def get_context(self, request):
    #     context = super().get_context(request)
    #     fields = []
    #     for f in self.product_Variant.get_object_list():
    #         if f.options:
    #             f.options_array = f.options.split('|')
    #             fields.append(f)
    #         else:
    #             fields.append(f)

    #     context['product_Variant'] = fields
    #     return context

    # content = StreamField([
    #     ('variant', blocks.VariantBlock()),

    # ])
    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('description'),

    ]
    api_fields = [
        # APIField('name'),
        APIField('description'),
        APIField('slug'),

        APIField('tags'),
        APIField('new'),
        APIField('sale'),
        APIField('price'),
        APIField('stock'),
        APIField('brand', serializer=serializers.StringRelatedField()),
        APIField(
            'collection', serializer=serializers.StringRelatedField(many=True)),
        APIField(
            'category', serializer=serializers.StringRelatedField(many=True)),
        APIField('images'),
        APIField('variants'),
    ]

    # @property
    # def a_custom_api_respnse(self):
    #     return [self.images]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('category', widget=forms.CheckboxSelectMultiple),
        ], heading='category'),
        MultiFieldPanel([
            # FieldPanel('category'),
            # FieldPanel('name'),
            FieldPanel('description'),
            FieldPanel('tags'),
            FieldPanel('new'),
            FieldPanel('sale'),
            FieldPanel('price'),
            FieldPanel('stock'),
            FieldPanel('brand'),
            FieldPanel('collection', widget=forms.CheckboxSelectMultiple),
            # StreamFieldPanel('content'),
        ], heading="Product information"),


        InlinePanel('images', label="images"),
        InlinePanel('variants', label='Variants'),


    ]


class ProductPageGalleryImage(Orderable):
    page = ParentalKey(ProductDetailPage, on_delete=models.CASCADE,
                       related_name='images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    # alt = models.CharField(blank=True, max_length=250)

    api_fields = [
        APIField("image", serializer=ImageSerializedField()),
        APIField("caption"),
    ]

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
        # FieldPanel('alt'),
    ]

    # def varints_images(self):
    #     images = ProductVariantField.objects.values('page_id','image_id')
    #     self.gallery_images = images


class ProductVariantField(Orderable):
    page = ParentalKey(ProductDetailPage, on_delete=models.CASCADE,
                       related_name='variants')
    color = models.ForeignKey(
        'product.Color', on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(
        'product.Size', on_delete=models.CASCADE, blank=True, null=True)
    sku = models.CharField(max_length=100, blank=True, null=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    alt = models.CharField(blank=True, max_length=250)

    api_fields = [
        APIField("color", serializer=serializers.StringRelatedField()),
        APIField(
            'size', serializer=serializers.StringRelatedField()),
        APIField("sku"),
        # APIField("alt"),
        APIField("image", serializer=ImageSerializedField()),

    ]
    panels = [
        SnippetChooserPanel('color'),
        FieldPanel('size'),
        FieldPanel('sku'),
        MultiFieldPanel([
            ImageChooserPanel('image'),

            # InlinePanel('gallery_images', label="Gallery images"),
        ], heading='Image'),

    ]
