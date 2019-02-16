# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
import pytz

class User(models.Model):
    AREA_CHOICES = (
        ('a1', 'a1'),
        ('a2', 'a2'),
    )
    TARIFF_CHOICES = (
        ('t1', 't1'),
        ('t2', 't2'),
        ('t3', 't3'),
    )
    user_id = models.CharField('user_id', max_length=4, primary_key=True, null=False, blank=False)
    area = models.CharField('area', max_length=2, choices=AREA_CHOICES, null=False, blank=False, db_index=True)
    tariff = models.CharField('tariff', max_length=2, choices=TARIFF_CHOICES, null=False, blank=False, db_index=True)
    def __str__(self):
        return self.user_id

class Consumption(models.Model):
    usage_time = models.DateTimeField('usage_time', null=False, blank=False, default=now, db_index=True)
    kWh = models.FloatField('kWh', null=False, blank=False, default=0, db_index=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, db_index=True)
    def __str__(self):
        return 'User ID:{} {}'.format(self.user, self.usage_time)