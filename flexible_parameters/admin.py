from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from polymorphic.admin import StackedPolymorphicInline

from . import models


class ChoiceInline(admin.TabularInline):
    model = models.Choice


@admin.register(models.ParameterType)
class ParameterTypeAdmin(SortableAdminMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = (
        'slug',
        'name',
        'auto_generated',
        'data_type',
        'es_parameter',
        'es_fulltext',
        'show_in_detail',
    )
    inlines = (ChoiceInline,)


class ParameterInline(StackedPolymorphicInline):
    class IntegerParameterInline(StackedPolymorphicInline.Child):
        model = models.IntegerParameter
        form = models.BaseParameterForm

    class CharParameterInline(StackedPolymorphicInline.Child):
        model = models.CharParameter
        form = models.CharParameterForm

    class PositiveIntegerParameter(StackedPolymorphicInline.Child):
        model = models.PositiveIntegerParameter
        form = models.BaseParameterForm

    class FloatParameter(StackedPolymorphicInline.Child):
        model = models.FloatParameter
        form = models.BaseParameterForm

    class BooleanParameter(StackedPolymorphicInline.Child):
        model = models.BooleanParameter
        form = models.BaseParameterForm

    class ArrayParameter(StackedPolymorphicInline.Child):
        model = models.ArrayParameter
        form = models.BaseParameterForm

    model = models.BaseParameter
    child_inlines = (
        IntegerParameterInline,
        CharParameterInline,
        PositiveIntegerParameter,
        FloatParameter,
        BooleanParameter,
        ArrayParameter,
    )
