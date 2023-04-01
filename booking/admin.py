from django.contrib import admin
from booking.models import *
# Register your models here.

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('lineid', 'name')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('rt_id', 'rt_name', 'rt_price')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('r_id', 'room_type')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('o_id', 'user')

@admin.register(BookingRoom)
class OptionsAdmin(admin.ModelAdmin):
    list_display = ('order', 'room', 'booked_date')

@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('t_number', 't_amount', 't_method', 't_date', 't_status', 'order')

@admin.register(Activities)
class ActivitiesAdmin(admin.ModelAdmin):
    list_display = ('a_name', 'a_date')