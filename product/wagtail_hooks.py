from wagtail.contrib.modeladmin.options import (
    ModelAdminGroup ,
    ModelAdmin,
    modeladmin_register
    )
from wagtail.contrib.modeladmin.mixins import ThumbnailMixin
from .models import ProductDetailPage, CategoryPr






# modeladmin_register(CategoryAdmin)


class CategoryModelAdmin(ThumbnailMixin, ModelAdmin):

    """
    # Optionally override the filter spec used to create each thumb
    thumb_image_filter_spec = 'fill-100x100' # this is the default

    # Optionally override the 'width' attribute value added to each `<img>` tag
    thumb_image_width = 50 # this is the default

    # Optionally override the class name added to each `<img>` tag
    thumb_classname = 'admin-thumb' # this is the default

    # Optionally override the text that appears in the column header
    thumb_col_header_text = 'image' # this is the default

    # Optionally specify a fallback image to be used when the object doesn't
    # have an image set, or the image has been deleted. It can an image from
    # your static files folder, or an external URL.
    thumb_default = 'https://lorempixel.com/100/100' 
    """

    model = CategoryPr
    menu_icon = "group"
    menu_label = 'Category'
    list_per_page = 10 
    thumb_image_field_name = 'icon'
    list_filter = (['locale', 'parent'])
    thumb_image_filter_spec = 'fill-100x100'
    list_display = ('admin_thumb', 'title')


class ProductModelAdmin(ModelAdmin):
    model = ProductDetailPage
    menu_icon = "group"
    menu_label = 'Products'
    list_per_page = 10
    # list_display = ('name')

class StoreGroup(ModelAdminGroup):
    menu_label = 'Store'
    menu_icon = ''
    menu_order = 300
    items={
        ProductModelAdmin,
        CategoryModelAdmin,
    }

modeladmin_register(StoreGroup)


# -------------------------------------------------------------
