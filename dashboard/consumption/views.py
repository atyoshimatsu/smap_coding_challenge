# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from. models import User
from . import charts
from. import forms

def summary(request):
    context = {
        'total_amount': charts.summary_count()[0],
        'ave_amount': charts.summary_chart()[1],
        'user_count': charts.summary_count()[1],
        'summary_chart': charts.summary_chart()[0],
        'user_list': User.objects.all().order_by('user_id'),
    }
    return render(request, 'consumption/summary.html', context)

def detail(request):
    context = {
        'month_form': forms.monthChoice(),
        'area_form': forms.areaChoice(),
        'tariff_form': forms.tariffChoice,
        'detail_chart': charts.detail_chart(request)[0],
        'user_list': charts.detail_count(request)[0],
        'total_amount': charts.detail_chart(request)[1],
        'ave_amount': charts.detail_chart(request)[2],
        'user_count': charts.detail_count(request)[1],
    }
    if request.method == 'POST':
        context['month_form'] = forms.monthChoice(request.POST)
        context['area_form'] = forms.areaChoice(request.POST)
        context['tariff_form'] = forms.tariffChoice(request.POST)
    return render(request, 'consumption/detail.html', context)

def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)#Userモデルからpkを指定してクエリをgetする
    context = {
        'month_form': forms.monthChoice(),
        'user_detail_chart': charts.user_detail_chart(request, pk)[0],
        'total_amount': charts.user_detail_chart(request, pk)[1],
        'ave_amount': charts.user_detail_chart(request, pk)[2],
        'user': user,
    }
    if request.method == 'POST':
        context['month_form'] = forms.monthChoice(request.POST)
    return render(request, 'consumption/user_detail.html', context)