from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from .models import normal_module, temp_module, general_module, settingS
from datetime import datetime
from django.db import models
from .forms import FORM
import urllib.request

mail_addr = ['']
addr = ''

def index(request):
	all_entries=[]
	for x in range(100):
		try:
			all_entries.append(general_module.objects.filter(module_id=x).latest('pub_date'))
			E=all_entries[-1]
			if E.module_type == 0:
				all_entries[-1].humidity = int(all_entries[-1].humidity)
				all_entries[-1].val = int(all_entries[-1].val)
		except general_module.DoesNotExist:
			pass
	return render(request, 'index.html', {'entries' : all_entries, 'critical1' : settingS.objects.get(pk=1).critical_humidity + 40, 'critical' : settingS.objects.get(pk=1).critical_humidity, 'Now' : datetime.now()})

def settings(request):
	form = FORM(request.POST)
	Settings = settingS.objects.get(pk=1)
	if request.method == "POST":
		ip1 = ['192.168.1.10']
		ip0 = ['192.168.1.11', '192.168.1.12', '192.168.1.13', '192.168.1.14', '192.168.1.15', '192.168.1.16', '192.168.1.17', '192.168.1.18', '192.168.1.19', '192.168.1.20', ]
		Settings = settingS.objects.get(pk=1)
		if request.POST.get('temp_high', '') != '':
			Settings.temp_high = request.POST.get('temp_high')
			for ip in ip1:
				url='http://' + ip + '/t_h=' + str(Settings.temp_high)
				try:
					urllib.request.urlopen(url)
				except urllib.error.URLError as e:
					pass
		if request.POST.get('temp_high2', '') != '':
			Settings.temp_high2 = request.POST.get('temp_high2')
			for ip in ip1:
				url='http://' + ip + '/t_h2=' + str(Settings.temp_high2)
				try:
					urllib.request.urlopen(url)
				except urllib.error.URLError as e:
					pass
		if request.POST.get('temp_low','') != '':
			Settings.temp_low = request.POST.get('temp_low')
			for ip in ip1:
				url='http://' + ip + '/t_l=' + str(Settings.temp_low)
				try:
					urllib.request.urlopen(url)
				except urllib.error.URLError as e:
					pass
		if request.POST.get('temp_low2','') != '':
			Settings.temp_low2 = request.POST.get('temp_low2')
			for ip in ip1:
				url='http://' + ip + '/t_l2=' + str(Settings.temp_low2)
				try:
					urllib.request.urlopen(url)
				except urllib.error.URLError as e:
					pass
		if request.POST.get('night_diff','') != '':
			Settings.night_diff = request.POST.get('night_diff')
			for ip in ip1:
				url='http://' + ip + '/night_thresh=' + str(Settings.night_diff)
				try:
					urllib.request.urlopen(url)
				except urllib.error.URLError as e:
					pass
		if request.POST.get('high_hour','') != '':
			Settings.high_hour = request.POST.get('high_hour')
			for ip in ip1:
				url='http://' + ip + '/high_hour=' + str(Settings.high_hour)
				try:
					urllib.request.urlopen(url)
				except urllib.error.URLError as e:
					pass
		if request.POST.get('low_hour','') != '':
			Settings.low_hour = request.POST.get('low_hour')
			for ip in ip1:
				url='http://' + ip + '/low_hour=' + str(Settings.low_hour)
				try:
					urllib.request.urlopen(url)
				except urllib.error.URLError as e:
					pass
		if request.POST.get('thresh','') != '':
			Settings.thresh = request.POST.get('thresh')
			for ip in ip0:
				url='http://' + ip + '/temperature_threshold=' + str(int(Settings.thresh) - 2)
				try:
					urllib.request.urlopen(url)
				except urllib.error.URLError as e:
					pass
		if request.POST.get('critical_humidity','') != '':
			print("found")
			Settings.critical_humidity = request.POST.get('critical_humidity')
		Settings.save()
	Settings = settingS.objects.get(pk=1)
	form.temp_high = Settings.temp_high
	form.temp_low = Settings.temp_low
	form.night_diff = Settings.night_diff
	form.high_hour = Settings.high_hour
	form.low_hour = Settings.low_hour
	form.threshold = Settings.thresh
	form.critical_humidity = Settings.critical_humidity
#	form.save()
	return render(request,'settings.html', {'form' : form, 'settings' : Settings})

def upload(request):
	if request.method == "GET":
		Type = request.GET.get('type')
		if Type == 'normal_module':
			print("normal")
			Settings = settingS.objects.get(pk=1)
			Module_type = 0
			Module_id = request.GET.get('id')
			Module_ip = request.GET.get('ip')
			Module_temperature = request.GET.get('temperature')
			Module_humidity1 = request.GET.get('humidity1')
			Module_humidity2 = request.GET.get('humidity2')
			Module_err = request.GET.get('err')
			Module_time_on = request.GET.get('time_on')
			Module_hours = int(int(Module_time_on)/3600)
			Module_minutes = int((int(Module_time_on)%3600)/60)
			Module_seconds = int(Module_time_on)%60
			Module = general_module(module_type=Module_type, module_id=Module_id, ip=Module_ip, temperature=Module_temperature, humidity=Module_humidity1, val=Module_humidity2, err=Module_err, pub_date=datetime.now(), time_on=Module_time_on, hours=Module_hours, minutes=Module_minutes, seconds=Module_seconds)
			Module.save()
			if int(Module_humidity1) < Settings.critical_humidity or int(Module_humidity2) < Settings.critical_humidity:
				subject = 'Tava '+ str(Module_id) + ' trebuie udata'
				message = 'link spre site:http://chilli.go.ro/module/' + str(Module_id)
				send_mail(subject,message,addr,mail_addr,fail_silently=False)
			if float(Module_temperature) <10:
				subject = 'Probleme la tava ' + str(Module_id)
				message = 'Probleme cu incalzirea http://chilli.go.ro/module/' + str(Module_id)
				send_mail(subject,message,addr,mail_addr,fail_silently=False)
			if int(Module_err) == 2:
				subject = 'Erorre la tava ' + str(Module_id)
				message = 'Senzorul de temperatura are probleme http://chilli.go.ro/module/' + str(Module_id)
				send_mail(subject,message,addr,mail_addr,fail_silently=False)
			return HttpResponse("hour="+str(datetime.now().hour)+'!')
		elif Type == 'temp_module':
			print("temp")
			Settings = settingS.objects.get(pk=1)
			Settings.temp_high = request.GET.get('temperature_high')
			Settings.temp_low = request.GET.get('temperature_low')
			Settings.night_diff = request.GET.get('night_diff')
			Settings.high_hour = request.GET.get('high_hour')
			Settings.low_hour = request.GET.get('low_hour')
			Settings.save()
			Module_type = 1
			Module_id = request.GET.get('id')
			Module_ip = request.GET.get('ip')
			Module_temperature1 = request.GET.get('temperature1')
			Module_temperature2 = request.GET.get('temperature2')
			Module_humidity = request.GET.get('humidity')
			Module_err = request.GET.get('err')
			Module_time_on = request.GET.get('time_on')
			Module_time_on2 = request.GET.get('time_on2')
			Module_hours = int(int(Module_time_on)/3600)
			Module_minutes = int((int(Module_time_on)%3600)/60)
			Module_seconds = int(Module_time_on)%60
			Module_hours2 = int(int(Module_time_on2)/3600)
			Module_minutes2 = int((int(Module_time_on2)%3600)/60)
			Module_seconds2 = int(Module_time_on2)%60
			Module_count = request.GET.get('count')
			Module = general_module(module_type=Module_type, module_id=Module_id, ip=Module_ip, temperature=Module_temperature1, val=Module_temperature2, humidity=Module_humidity ,err=Module_err, pub_date=datetime.now(), time_on=Module_time_on, time_on2=Module_time_on2, hours=Module_hours, minutes=Module_minutes, seconds=Module_seconds, hours2=Module_hours2, minutes2=Module_minutes2, seconds2=Module_minutes2, count=Module_count)
			Module.save()
			if float(Module_temperature1) < 5 or float(Module_temperature1) > 40: #10 initial
				subject = 'Probleme cu controlul aerului'
				message = 'Probleme la controlul aerului http://chilli.go.ro/module/' + str(Module_id)
				send_mail(subject,message,addr,mail_addr,fail_silently=False)
			if int(Module_err) != 0:
				subject = 'Eroare la senzorul de temperatura al aerului'
				message = 'Senzorul de temperatura a al aerului nu mai merge: http://chilli.go.ro/module' + str(Module_id)
				send_mail(subject,message,addr,mail_addr,fail_silently=False)
			return HttpResponse("hour="+str(datetime.now().hour)+'!')
		else:
			return render(request, '404.html', {})
	else:
		return render(request, '404.html', {})

def module(request,Number):
	err = 0
	try:
		entry = general_module.objects.filter(module_id=Number).latest('pub_date')
	except general_module.DoesNotExist:
		err = 1
		return render(request, '404.html', {})
	if err == 0:
		if entry.module_type == 0:
			entry.humidity = int(entry.humidity)
			entry.val = int(entry.val)
			return render(request, 'module.html', {'entry' : entry})
		else:
			return render(request, 'air.html', {'entry' : entry})

def details(request,Number):
	err = 0
	try:
		entry = general_module.objects.filter(module_id=Number).latest('pub_date')
	except general_module.DoesNotExist:
		err = 1
		return render(request, '404.html', {})
	if err == 0:
		not_ordered = general_module.objects.filter(module_id=Number)
		all_entries = not_ordered.order_by('-pub_date')
		E = all_entries[:300]
		if entry.module_type == 0:
			for p in E:
				p.humidity = int(p.humidity)
				p.val = int(p.val)
			return render(request, 'log.html', {'entry' : E, 'Number' : Number})
		else:
			return render(request, 'air_log.html', {'entry' : E, 'Number' : Number})
