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

def index(request):
    # a = os.popen('cat /var/log/apache2/access.log').read()
    # print(a,type(a))
    returned_text = subprocess.check_output("cat /var/log/apache2/access.log", shell=True, universal_newlines=True)
    # print("dir command to list file and directory")
    # print(returned_text)
    context={'status':200,'data':returned_text}

    # print(a.split('\n'))
    # print(context)
    # return render(request,'index.html',context=context)
    return JsonResponse(context)

@csrf_exempt
def show_custom(request):
    if request.method == "POST":
        formData = request.body
        form = ast.literal_eval(formData.decode('utf-8'))
        # print(form)
        fil = form['filter']
        print(fil)
        if fil != '':
            final_arr = {}
            codes = [200,404,500]
            fil = int(fil)
            for i in range(fil,-1,-1):
                if i != 1:
                    for code in codes:
                        cmd = f'grep -E "$(date "+%d\/%b\/%Y:%H" -d' + f"'{i} hours ago').*" + f'HTTP.*{code} " /var/log/apache2/access.log'
                        if code not in final_arr:
                            try:final_arr[code] = subprocess.check_output(cmd, shell=True, universal_newlines=True)
                            except:final_arr[code] = ''
                        else:
                            try:final_arr[code] += subprocess.check_output(cmd, shell=True, universal_newlines=True)
                            except: final_arr[code] += ''
                else:
                    for code in codes:
                        cmd = f'grep -E "$(date "+%d\/%b\/%Y:%H" -d' + f"'{i} hour ago').*" + f'HTTP.*{code} " /var/log/apache2/access.log'
                        if code not in final_arr:
                            try:final_arr[code] = subprocess.check_output(cmd, shell=True, universal_newlines=True)
                            except:final_arr[code] = ''
                        else:
                            try:final_arr[code] += subprocess.check_output(cmd, shell=True, universal_newlines=True)
                            except: final_arr[code] += ''
            # print(final_arr)
            context={'status':200,'data':final_arr}

    return JsonResponse(context)

@csrf_exempt
def show_ipwise(request):
    cmd = "awk '{ print $1 } ' /var/log/apache2/access.log | sort | uniq -c"
    total_ip = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    cmd = "awk '{ print $1,$9 } ' /var/log/apache2/access.log | sort | uniq -c"
    r = subprocess.check_output(cmd, shell=True, universal_newlines=True)
    context={'status':200,'data':[total_ip,r]}
    return JsonResponse(context)

@csrf_exempt
def block_ip(request):
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
def blocked_ips(request):
    blocked_ip = subprocess.check_output("iptables -L INPUT -v -n", shell=True, universal_newlines=True)
    # print(blocked_ip)
    context={'status':200,'data':blocked_ip}
    return JsonResponse(context)

@csrf_exempt
def unblock_ips(request):
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
def firewall(request):
    blocked_ip = subprocess.check_output("iptables -L INPUT -v -n | grep DROP | awk '{ print $8 }'", shell=True, universal_newlines=True)
    context = {'status':200,'data':blocked_ip}
    return JsonResponse(context)