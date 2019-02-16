# -*- coding: utf-8 -*-
from django.db import models
from.models import User
from.models import Consumption
from datetime import datetime as dt
import calendar
import pytz
import json


def summary_count():#summaryページの合計kWhとユーザ数を計算
    total_amount = Consumption.objects.aggregate(sum=models.Sum('kWh'))['sum']
    user_count = User.objects.aggregate(count=models.Count('user_id'))['count']
    return '{:,}'.format(int(total_amount)), user_count

def summary_chart():#summaryページのグラフを描画
    #データの年月を集計
    months = set()
    data = Consumption.objects.values('usage_time').distinct().order_by('usage_time')
    for entry in data:
        months.add((entry['usage_time'].year, entry['usage_time'].month))
    months = list(months)
    months.sort()

    #月ごとの合計kWhを計算
    kWh_summary = []
    for month in months:
        start = dt(month[0], month[1],1,0,0,0).astimezone(pytz.timezone('Asia/Tokyo'))
        end = dt(month[0],month[1],calendar.monthrange(month[0],month[1])[1],23,59,59).astimezone(pytz.timezone('Asia/Tokyo'))
        usage_amount = Consumption.objects.filter(usage_time__range=(start,end)).aggregate(sum=models.Sum('kWh'))
        kWh_summary.append(usage_amount['sum'])

    #highchartsでグラフを描画
    series = {
        'name': 'kWh',
        'data': kWh_summary,
        'color':'turquoise'
    }
    chart = {
        'chart': {'type': 'column'},
        'title': {'text': None},
        'xAxis': {'categories': ['{}-{}'.format(month[0],month[1]) for month in months]},
        'yAxis': {'title':False},
        'series': [series],
        }
    dump = json.dumps(chart)
    return dump, '{:,}'.format(int(sum(kWh_summary)/len(months)))

def detail_count(request):#detailページのユーザリストとユーザ数を計算
    if request.method == 'POST':
        area = request.POST['area_choice']
        tariff = request.POST['tariff_choice']
        if area == 'all' and tariff == 'all':
            data = User.objects.all().order_by('user_id')
            return data, data.count()
        elif area != 'all' and tariff == 'all':
            data = User.objects.filter(area=area).order_by('user_id')
            return data, data.count()
        elif area == 'all' and tariff != 'all':
            data = User.objects.filter(tariff=tariff).order_by('user_id')
            return data, data.count()
        else:
            data = User.objects.filter(area=area, tariff=tariff).order_by('user_id')
            return data, data.count()
    else:
        data = User.objects.all().order_by('user_id')
        return data, data.count()

def detail_chart(request):#detailページのグラフを描画
    if request.method == 'POST':#リクエストのメソッドがPOSTだった場合、フォーム内の値を利用
        month = list(map(int, request.POST['month_choice'].split()))
        area = request.POST['area_choice']
        tariff = request.POST['tariff_choice']
    else:#PSOTではない場合、12月分、area,tariffは全種類を集計
        month = [2016, 12]
        area = 'all'
        tariff = 'all'
    start = dt(month[0], month[1], 1, 0, 0, 0).astimezone(pytz.timezone('Asia/Tokyo'))
    end = dt(month[0], month[1], calendar.monthrange(month[0], month[1])[1], 23, 59, 59).astimezone(pytz.timezone('Asia/Tokyo'))
    data = Consumption.objects.filter(usage_time__range=(start, end)).values('usage_time').distinct().order_by('usage_time')

    #30分毎の時刻とユーザの合計kWhを集計
    time_line = []
    kWh_list = []
    for entry in data:
        time = entry['usage_time'].astimezone(pytz.timezone('Asia/Tokyo'))
        if time.hour == 0 and time.minute == 0 and time.second == 0:#時刻が0時0分0秒のときのみ日付を表示
            time_line.append(dt.strftime(time,'%Y-%m-%d %H:%M'))
        else:#それ以外の場合は時分のみ表示
            time_line.append(dt.strftime(time, '%H:%M'))
        #areaとtariffごとに合計kWhを集計
        if area != 'all' and tariff != 'all':
            usage_amount = Consumption.objects.filter(usage_time=entry['usage_time'],user__area=area, user__tariff=tariff).aggregate(sum=models.Sum('kWh'))
        elif area == 'all' and tariff != 'all':
            usage_amount = Consumption.objects.filter(usage_time=entry['usage_time'],user__tariff=tariff).aggregate(sum=models.Sum('kWh'))
        elif area != 'all' and tariff == 'all':
            usage_amount = Consumption.objects.filter(usage_time=entry['usage_time'], user__area=area).aggregate(sum=models.Sum('kWh'))
        else:
            usage_amount = Consumption.objects.filter(usage_time=entry['usage_time']).aggregate(sum=models.Sum('kWh'))
        kWh_list.append(usage_amount['sum'])
        total_kWh = sum(kWh_list)
        ave_kWh = total_kWh/calendar.monthrange(month[0], month[1])[1]

    #グラフを描画
    series = {
        'name': 'kWh',
        'data': kWh_list,
        'color':'steelblue'
    }
    chart = {
        'chart': {'type': 'line', 'zoomType': 'x'},
        'title': {'text': None},
        'xAxis': {'categories': time_line},
        'yAxis': {'title':False},
        'series': [series],
        'plotOptions':{'line':{'marker':{'enabled':False}},'series':{'lineWidth':1.5}},
    }
    dump = json.dumps(chart)
    return dump, '{:,}'.format(int(total_kWh)), '{:,}'.format(int(ave_kWh))

def user_detail_chart(request, pk):#ユーザごとのグラフを描画
    if request.method == 'POST':#リクエストのメソッドがPOSTだった場合、フォーム内の値を利用
        month = list(map(int, request.POST['month_choice'].split()))
    else:#PSOTではない場合、12月分を集計
        month = [2016, 12]
    start = dt(month[0], month[1], 1, 0, 0, 0).astimezone(pytz.timezone('Asia/Tokyo'))
    end = dt(month[0], month[1], calendar.monthrange(month[0], month[1])[1], 23, 59, 59).astimezone(pytz.timezone('Asia/Tokyo'))
    data = Consumption.objects.filter(user__pk=pk, usage_time__range=(start, end)).values('usage_time').order_by('usage_time')

    #30分毎の時刻とユーザのkWhを集計
    time_line = []
    kWh_list = []
    for entry in data:
        time = entry['usage_time'].astimezone(pytz.timezone('Asia/Tokyo'))
        if time.hour == 0 and time.minute == 0 and time.second == 0:#時刻が0時0分0秒のときのみ日付を表示
            time_line.append(dt.strftime(time, '%Y-%m-%d %H:%M'))
        else:#それ以外の場合は時分のみ表示
            time_line.append(dt.strftime(time, '%H:%M'))
        kWh_list.append(Consumption.objects.filter(user__pk=pk, usage_time=entry['usage_time']).get().kWh)
    total_kWh = sum(kWh_list)
    ave_kWh = total_kWh/calendar.monthrange(month[0], month[1])[1]

    # グラフを描画
    series = {
        'name': 'kWh',
        'data': kWh_list,
        'color':'salmon'
    }
    chart = {
        'chart': {'type': 'line', 'zoomType': 'x'},
        'title': {'text': None},
        'xAxis': {'categories': time_line},
        'yAxis': {'title':False},
        'series': [series],
        'plotOptions':{'line':{'marker':{'enabled':False}},'series':{'lineWidth':1.5}},
    }
    dump = json.dumps(chart)
    return dump, '{:,}'.format(int(total_kWh)), '{:,}'.format(int(ave_kWh))