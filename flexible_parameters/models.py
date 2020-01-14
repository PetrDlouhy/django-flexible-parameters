
from author.decorators import with_author

from django import forms
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from djchoices import ChoiceItem, DjangoChoices

from polymorphic.models import PolymorphicModel


@with_author
class ParameterType(TimeStampedModel):
    class DataType(DjangoChoices):
        integer = ChoiceItem('integer', _("Integer"))
        positive_integer = ChoiceItem('positive_integer', _("PositiveInteger"))
        float_type = ChoiceItem('float_type', _("Float"))
        char = ChoiceItem('char', _("Character"))
        boolean = ChoiceItem('boolean', _("Boolean"))
        array = ChoiceItem('array', _("Char array"))

    name = models.CharField(
        _("name"),
        max_length=255,
    )
    slug = models.SlugField(
        _("identifier"),
    )
    data_type = models.CharField(
        _("data type"),
        choices=DataType.choices,
        max_length=100,
    )
    order = models.PositiveIntegerField(
        _("Order"),
    )
    es_parameter = models.BooleanField(
        _("add as Elasticsearch parameter"),
        default=False,
    )
    es_fulltext = models.BooleanField(
        _("add to Elasticsearch fulltext"),
        default=False,
    )
    show_in_detail = models.BooleanField(
        _("Show in detailed outputs"),
        default=True,
    )

    def get_parameter_class(self):
        return {
            self.DataType.positive_integer: PositiveIntegerParameter,
            self.DataType.integer: IntegerParameter,
            self.DataType.float_type: FloatParameter,
            self.DataType.char: CharParameter,
            self.DataType.boolean: BooleanParameter,
            self.DataType.array: ArrayParameter,
        }[self.data_type]

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ParameterType.DataType.labels[self.data_type],
        )

    class Meta:
        ordering = ('order',)


class Choice(models.Model):
    name = models.CharField(
        _("name"),
        max_length=255,
    )
    value = models.SlugField(
        _("value"),
        max_length=255,
    )
    parameter_type = models.ForeignKey(
        ParameterType,
        on_delete=models.CASCADE,
    )


@with_author
class BaseParameter(TimeStampedModel, PolymorphicModel):
    data_type = None

    parameter_type = models.ForeignKey(
        ParameterType,
        on_delete=models.PROTECT,
    )

    def get_value(self):
        return self.value

    def clean(self):
        if (
                hasattr(self, 'parameter_type') and
                self.parameter_type.data_type != self.data_type
        ):
            raise ValidationError(
                {
                    'parameter_type': _(
                        'Please choose %s parameter type' %
                        ParameterType.DataType.labels[self.data_type],
                    ),
                },
            )

        param_choices = self.parameter_type.choice_set
        if param_choices.exists():
            if self.data_type == 'array':
                values = self.value
            else:
                values = [self.value]
            for value in values:
                if not param_choices.filter(value=value).exists():
                    raise forms.ValidationError(
                        "Value %s not in allowed choices %s" % (
                            value,
                            ', '.join(param_choices.values_list('value', flat=True)),
                        ),
                    )

    def __str__(self):
        if type(self) == BaseParameter:
            return "--base parameter--"
        return "%s = %s" % (
            self.parameter_type.name,
            self.get_value(),
        )

    class Meta:
        ordering = ('parameter_type__order',)


class IntegerParameter(BaseParameter):
    data_type = ParameterType.DataType.integer
    value = models.IntegerField(
        _("value"),
    )


class CharParameter(BaseParameter):
    data_type = ParameterType.DataType.char
    value = models.CharField(
        _("value"),
        max_length=255,
        blank=True,
    )


class BaseParameterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parameter_type'].queryset = self.fields['parameter_type'].queryset.filter(
            data_type=self._meta.model.data_type,
        )

    class Meta:
        fields = ('parameter_type', 'value')


class CharParameterForm(BaseParameterForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.initial:
            param_choices = kwargs['instance'].parameter_type.choice_set
            if param_choices.exists():
                self.fields['value'] = forms.ChoiceField(
                    choices=param_choices.values_list('value', 'name'),
                    required=False,
                )

    class Meta(BaseParameterForm.Meta):
        model = CharParameter


class PositiveIntegerParameter(BaseParameter):
    data_type = ParameterType.DataType.positive_integer
    value = models.PositiveIntegerField(
        _("value"),
    )


class FloatParameter(BaseParameter):
    data_type = ParameterType.DataType.float_type
    value = models.FloatField(
        _("value"),
    )


class BooleanParameter(BaseParameter):
    data_type = ParameterType.DataType.boolean
    value = models.BooleanField(
        _("value"),
    )


class ArrayParameter(BaseParameter):
    data_type = ParameterType.DataType.array
    value = ArrayField(
        models.CharField(max_length=255),
        verbose_name=_("value"),
        blank=True,
    )
