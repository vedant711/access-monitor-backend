from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib import messages
import os
import subprocess
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
import ast
from datetime import datetime,timedelta

# Create your views here.

def index(request,server):
    # a = os.popen('cat /var/log/{server}/access.log').read()
    # print(a,type(a))
    # print(server)
    returned_text = subprocess.check_output(f"cat /var/log/{server}/access.log", shell=True, universal_newlines=True)
    # print("dir command to list file and directory")
    # print(returned_text)
    context={'status':200,'data':returned_text}

    # print(a.split('\n'))
    # print(context)
    # return render(request,'index.html',context=context)
    return JsonResponse(context)

@csrf_exempt
def show_custom(request,server):
    if request.method == "POST":
        formData = request.body
        form = ast.literal_eval(formData.decode('utf-8'))
        # print(form)
        fil = form['filter']
        # print(fil)
        if fil != '':
            final_arr = {}
            codes = [200,404,500]
            fil = int(fil)
            # for i in range(fil,-1,-1):
            #     if i != 1:
            #         for code in codes:
            #             cmd = f'grep -E "$(date "+%d\/%b\/%Y:%H" -d' + f"'{i} hours ago').*" + f'HTTP.*{code} " /var/log/{server}/access.log'
            #             if code not in final_arr:
            #                 try:final_arr[code] = subprocess.check_output(cmd, shell=True, universal_newlines=True)
            #                 except:final_arr[code] = ''
            #             else:
            #                 try:final_arr[code] += subprocess.check_output(cmd, shell=True, universal_newlines=True)
            #                 except: final_arr[code] += ''
            #     else:
            #         for code in codes:
            #             cmd = f'grep -E "$(date "+%d\/%b\/%Y:%H" -d' + f"'{i} hour ago').*" + f'HTTP.*{code} " /var/log/{server}/access.log'
            #             if code not in final_arr:
            #                 try:final_arr[code] = subprocess.check_output(cmd, shell=True, universal_newlines=True)
            #                 except:final_arr[code] = ''
            #             else:
            #                 try:final_arr[code] += subprocess.check_output(cmd, shell=True, universal_newlines=True)
            #                 except: final_arr[code] += ''
            # #print(final_arr)
            dt = datetime.now()
            hr = dt.hour
            # print(dt)
            # print(hr)
            past=hr - fil
            dt1 = dt.strftime('%d/%b/%Y')
            # print(dt1)
            # past = str(past)
            # if len(past) !=2:past1 = '0'+past
            # else:past1 =past
            for code in codes:
                if past >0:
                    if hr<10 and past<10:
                        cmd = f'egrep "{dt1}:(0[{past}-{hr}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif hr >=10 and past>=10 and hr<20 and past<20:
                        cmd = f'egrep "{dt1}:(1[{str(past)[1]}-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif hr>=20 and past>=20:
                        cmd = f'egrep "{dt1}:(2[{str(past)[1]}-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif past<10 and hr >=10 and hr<20:
                        cmd = f'egrep "{dt1}:(0[{past}-9]|1[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif past<10 and hr >=20:
                        cmd = f'egrep "{dt1}:(0[{past}-9]|1[0-9]|2[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif past>=10 and hr>=20 and past<20:
                        cmd = f'egrep "{dt1}:(1[{past}-9]|2[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    else:
                        cmd = f'egrep "{dt1}:(0[0-9]|1[0-9]|2[0-4]).*HTTP.*{code}" /var/log/{server}/access.log'
                else:
                    cmd = f'egrep "{dt1}:(0[0-9]|1[0-9]|2[0-4]).*HTTP.*{code}" /var/log/{server}/access.log'
                # print(cmd)
                if code not in final_arr:
                    try:final_arr[code] = subprocess.check_output(cmd, shell=True, universal_newlines=True)
                    except:final_arr[code] = ''
                else:
                    try:final_arr[code] += subprocess.check_output(cmd, shell=True, universal_newlines=True)
                    except: final_arr[code] += ''
            context={'status':200,'data':final_arr}

    return JsonResponse(context)

@csrf_exempt
def show_ipwise(request,server):
    cmd = "awk '{ print $1 } '" +  f" /var/log/{server}/access.log | sort | uniq -c"
    # print(cmd)
    total_ip = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    cmd = "awk '{ print $1,$9 } '"+ f" /var/log/{server}/access.log | sort | uniq -c"
    r = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    cmd = "awk -e '$7 ~/^408/ {print $1,$7}'" +  f" /var/log/{server}/access.log | sort | uniq -c"
    r_408 = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    # print(r)
    context={'status':200,'data':[total_ip,r,r_408]}
    return JsonResponse(context)

@csrf_exempt
def block_ip(request,server):
    if request.method == "POST":
        formData = request.body
        form = ast.literal_eval(formData.decode('utf-8'))
        ip = form['ip']
        os.system(f'iptables -A INPUT -s {ip} -j DROP')
        os.system('service iptables save')
        # blocked_ips = subprocess.check_output("iptables -L INPUT -v -n", shell=True, universal_newlines=True)
        context = {'status':200,'msg':'successfully blocked'}
        return JsonResponse(context)

@csrf_exempt
def blocked_ips(request,server):
    blocked_ip = subprocess.check_output("iptables -L INPUT -v -n", shell=True, universal_newlines=True)
    # print(blocked_ip)
    context={'status':200,'data':blocked_ip}
    return JsonResponse(context)

@csrf_exempt
def unblock_ips(request,server):
    if request.method == "POST":
        formData = request.body
        form = ast.literal_eval(formData.decode('utf-8'))
        ip = form['ip']
        # print(ip)
        os.system(f'iptables -D INPUT -s {ip} -j DROP')
        os.system('service iptables save')
        context = {'status':200,'msg':'successfully unblocked'}
        return JsonResponse(context)

@csrf_exempt
def firewall(request,server):
    blocked_ip = subprocess.check_output("iptables -L INPUT -v -n | grep DROP | awk '{ print $8 }'", shell=True, universal_newlines=True)
    context = {'status':200,'data':blocked_ip}
    return JsonResponse(context)