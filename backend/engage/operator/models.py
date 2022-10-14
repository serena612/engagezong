from tabnanny import verbose
import uuid

from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify

from common.models import TimeStampedModel, MetadataModel
from engage.operator.constants import AdType, Currencies


class Region(TimeStampedModel):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64)
    default_language = models.CharField(max_length=2)
    # default_currency = models.CharField(max_length=3,
    #                                     choices=Currencies.choices,
    #                                     default=Currencies.NGN)
    default_currency = models.CharField(max_length=3)
    # time_compared_to_gmt = models.CharField(max_length=64,verbose_name='Time Compared to GMT',default='0',blank=False)
    # time_label = models.CharField(max_length=250,verbose_name='Time to be displayed next to Time')
    def __str__(self):
        return self.name


class Operator(TimeStampedModel):
    uuid = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=128, unique=True)
    schema = models.SlugField(unique=True)
    logo = models.ImageField(upload_to='operators/', blank=True, null=True)
    description = RichTextField(blank=True, null=True)
    region = models.OneToOneField(Region, on_delete=models.PROTECT, null=True)

    def save(self, *args, **kwargs):
        self.schema = slugify(self.region.code)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class OperatorWebsite(TimeStampedModel):
    operator = models.OneToOneField(Operator, on_delete=models.CASCADE)
    first_section_image = models.ImageField(upload_to='home_page_image/',
                                            null=True,verbose_name='First section image (desktop)')
    second_section_image = models.ImageField(upload_to='home_page_image/',
                                            null=True,verbose_name='Second section image (mobile)')                                         
    first_section_description = RichTextField(blank=True, null=True)
    first_section_button_title = models.CharField(max_length=64, blank=True, null=True)
    first_section_url = models.URLField(blank=True, null=True)
    about_us_description = RichTextField(blank=False, null=True)
    terms_description = RichTextField('Terms & Conditions', blank=False, null=True)
    

class OperatorHomeSection(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    image = models.ImageField('Main Image', upload_to='sections/')
    title = models.CharField(max_length=256,blank=True)
    summary = models.TextField(blank=True, null=True)
    background_image = models.ImageField(upload_to='sections/background/',
                                         blank=True, null=True)
    image_link = models.URLField(blank=False, null=True)
    button_label = models.CharField(max_length=400,blank=True, null=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['id']


class OperatorFaq(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    title = models.TextField(blank=False)
    description = RichTextField(blank=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


class OperatorAd(TimeStampedModel):
    name = models.CharField(max_length=64)
    ad_file = models.FileField(upload_to='ads/',verbose_name="Dektop Ad file")
    ad_file_mobile = models.FileField(upload_to='ads/',verbose_name="Mobile Ad file")
    ad_type = models.CharField(max_length=32, choices=AdType.choices)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    regions = models.ManyToManyField(Region)

    def __str__(self):
        return f'[{self.ad_type}] - {self.name}'

    class Meta:
        verbose_name = 'Ad'
        verbose_name_plural = 'Ads'


class RedeemPackage(TimeStampedModel):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=256)
    image = models.ImageField(upload_to='packages/')
    coins = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Redeem Packages'


class PurchaseCoin(TimeStampedModel):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    uid = models.UUIDField(default=uuid.uuid4)
    icon = models.ImageField(upload_to='purchase_coins/')
    coins = models.PositiveIntegerField()
    bonus = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    class Meta:
        verbose_name = 'Purchase Coins'
        verbose_name_plural = 'Purchase Coins'
        ordering = ('-coins',)

    def __str__(self):
        return f'{self.coins} coins'

    @property
    def total(self):
        return self.coins + int(self.coins * (self.bonus / 100))
