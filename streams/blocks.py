
# from django.db import models
# # Create your models here.
# # from product.models import Color, Size
# from wagtail.core import blocks
# from wagtail.images.blocks import ImageChooserBlock


# class VariantBlock(blocks.StructBlock):
#     """simple call to Action """
#     # title = blocks.CharBlock(required=True, max_length=100)
#     variant = blocks.ListBlock(
#         blocks.StructBlock([
#             ('image', ImageChooserBlock(required=False)),
#             ('title', blocks.CharBlock(required=False, max_length=100)),
#             ('quantity', blocks.IntegerBlock(required=False, default=1)),
#             ('price', blocks.DecimalBlock(required=False,
#                                           max_digits=12, decimal_places=2, default=0)),
#             # ('color', models.ForeignKey(
#             #     Color, on_delete=models.CASCADE, blank=True, null=True)),
#             # ('size', models.ForeignKey(
#             #     Size, on_delete=models.CASCADE, blank=True, null=True)),
#         ])
#     )
#     # color = models.ForeignKey(
#     #     Color, on_delete=models.CASCADE, blank=True, null=True)
#     # size = models.ForeignKey(
#     #     Size, on_delete=models.CASCADE, blank=True, null=True)

#     # quantity = models.IntegerField(default=1)
#     # price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

#     class Meta:
#         template = 'streams/Variant_block.html'
#         icon = 'placeholder'
#         label = 'Variant'
