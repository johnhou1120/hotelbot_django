from datetime import timedelta, date
from pyexpat import model
from django.db import models
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
# Create your models here.

class Users(models.Model):
    lineid = models.CharField(max_length=40, unique=True, primary_key= True)    # line用戶ID
    name = models.CharField(max_length=25, blank=True, null=True)               # 姓名
    nick_name = models.CharField(max_length=30, blank=True, null=True)          # line用戶name
    image_url = models.TextField(blank=True, null=True)                         # line用戶大頭貼
    phone = models.CharField(max_length=20, blank= True, null= True)            # 電話號碼
    address = models.TextField(blank= True, null= True)                         # 地址
    birthday = models.DateField(blank= True, null= True)                        # 生日
    email = models.TextField(blank= True, null= True)                           # 地址
    ewallet = models.TextField(blank= True, null= True)                         # 錢包帳號
    einvoice = models.CharField(max_length=20, blank= True, null= True)         # 電子發票
    GUInumber = models.CharField(max_length=20,blank= True, null= True)         # 統一編號
    followdate = models.DateTimeField(default=timezone.now)                     # line追蹤時間
    unfollow = models.BooleanField(default=False, verbose_name="封鎖")
    promotable = models.BooleanField(default=False, verbose_name="promotable")
    comments = models.TextField(blank= True, null= True)

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return "%s, %s" % (self.lineid, self.name)

class RoomType(models.Model):
    rt_id = models.CharField(max_length=50, unique=True, primary_key= True)
    rt_name = models.CharField(max_length=255)
    rt_price = models.IntegerField(default=0)
    rt_limit = models.IntegerField(default=2)
    rt_image = models.TextField(blank= True, null= True)
    rt_description = models.TextField(blank= True, null= True)
    comments = models.TextField(blank= True, null= True)

    def __str__(self):
        return "%s, %s" % (self.rt_name, self.rt_price)

class Room (models.Model):
    r_id = models.CharField(max_length=50, unique=True, primary_key= True)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    comments = models.TextField(blank= True, null= True)

    def __str__(self):
        return "%s, %s" % (self.r_id, self.room_type.rt_name)

class Order(models.Model):
    o_id = models.CharField(max_length=50, unique=True, primary_key= True)
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=False)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    o_date = models.DateTimeField()
    o_status = models.CharField(max_length=10)
    comments = models.TextField(blank= True, null= True)
    
    def __str__(self):
        # return "Order: %s" % (self.o_date)
        return "%s, (%s)%s" % (self.o_date.date(), self.user.lineid, self.user.name)

class BookingRoom(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    booked_date = models.DateTimeField()
    comments = models.TextField(blank= True, null= True)

    def __str__(self):
        return "%s, %s, %s" % (self.order, self.room, self.booked_date.date())

class Transactions(models.Model):
    t_number = models.TextField()
    t_amount = models.IntegerField(default=0)
    t_method = models.CharField(max_length=50)
    t_date = models.DateTimeField()
    t_status = models.BooleanField(default=False)
    t_invoice_type = models.CharField(max_length=50, null=True)
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    comments = models.TextField(blank= True, null= True)
    
    def __str__(self):              # __unicode__ on Python 2
        return "%s, %s, %s, %s" % (self.t_number, self.t_amount, self.t_date, self.order)

class Activities(models.Model):
    a_name = models.TextField(blank= True, null= True)
    a_img = models.TextField(blank= True, null= True)
    a_date = models.TextField(blank= True, null= True)
    a_address = models.TextField(blank= True, null= True)
    a_price = models.TextField(blank= True, null= True)
    a_organizer = models.TextField(blank= True, null= True)
    a_url = models.TextField(blank= True, null= True)
    comments = models.TextField(blank= True, null= True)
    
    def __str__(self):              # __unicode__ on Python 2
        return "%s" % (self.a_name)