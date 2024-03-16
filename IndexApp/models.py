from django.db import models
from django_resized import ResizedImageField


# Create your models here.

class SiteInfo(models.Model):
    logo = ResizedImageField(upload_to='site_info', crop=['middle', 'center'], size=[41, 41], quality=90,
                             verbose_name='لوگو')
    title = models.CharField(max_length=40, verbose_name='عنوان')
    short_description = models.CharField(max_length=250, verbose_name='توضیحات کوتاه')
    main_description = models.CharField(max_length=1000, verbose_name='توضیحات اصلی')
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    address = models.CharField(max_length=250, verbose_name='آدرس')
    email = models.EmailField(verbose_name='ایمیل')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')
    about_us_picture = ResizedImageField(upload_to='about_us', null=True, crop=['middle', 'center'], size=[451, 271],
                                         quality=100,
                                         verbose_name='تصویر درباره ما')

    class Meta:
        verbose_name = 'اطلاعات سایت'
        verbose_name_plural = 'اطلاعات سایت'


    def __str__(self):
        return self.title


class MainPictures(models.Model):
    site_info = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, related_name='main_pictures')
    picture = ResizedImageField(upload_to='main_picture', null=True, crop=['middle', 'center'], size=[966, 353],
                                quality=100,
                                verbose_name='تصویر اصلی')

class SidePicture(models.Model):
    site_info = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, related_name='side_pictures')
    picture = ResizedImageField(upload_to='side_picture', null=True, crop=['middle', 'center'], size=[261, 106],
                                     quality=100,
                                     verbose_name='تصویر کناری')


class TeamMember(models.Model):
    site_info = models.ForeignKey(SiteInfo, on_delete=models.CASCADE, related_name='team_members')
    profile_pic = ResizedImageField(upload_to='team_member', blank=True, null=True, size=[185, 115],
                                    crop=['middle', 'center'], quality=90, verbose_name='تصویر')
    fullname = models.CharField(max_length=35, verbose_name='نام و نام خانوادگی')
    job = models.CharField(max_length=35, verbose_name='شغل')
    description = models.CharField(max_length=250, verbose_name='توضیحات')

    def __str__(self):
        return self.fullname
