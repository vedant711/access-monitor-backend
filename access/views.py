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
# from .serializers import MyTokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from django.contrib.auth.models import User
# from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate,login,logout

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def testEndPoint(request):
#     if request.method == 'GET':
#         data = f"Congratulation {request.user}, your API just responded to GET request"
#         return Response({'response': data}, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         text = request.POST.get('text')
#         data = f'Congratulation your API just responded to POST request with text: {text}'
#         return Response({'response': data}, status=status.HTTP_200_OK)
#     return Response({}, status.HTTP_400_BAD_REQUEST)

# # Create your views here.

# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# @api_view(['GET'])
# def getRoutes(request):
#     routes = [
#         '/token/',
#         '/token/refresh/'
#     ]
#     return Response(routes)

def error404(request):
    return render(request,'404.html')

@csrf_exempt
def login_view(request):
    if request.user.is_authenticated: return redirect('/')
    else:
        nxt = request.GET.get('next','/')
        if '/show_custom/' in nxt:
            nxt = nxt.replace('/show_custom/','/access/')
        context = {'next':nxt}
        if request.method == "POST":
            username, password = request.POST['username'],request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return redirect(nxt)
            else:messages.info(request,'Incorrect Username or Password')
        return render(request,'login.html',context)

@csrf_exempt
def logout_view(request):
    try:
        logout(request)
        return redirect('/login/')
    except:
        messages.info(request,'Unable to logout')
        

@staff_member_required(login_url='/login/')
def index_home(request):
    return render(request,'select.html')

@staff_member_required(login_url='/login/')
def index_server_home(request,server):
    context = {'server':server}
    return render(request,'index.html', context)

# @login_required
@staff_member_required(login_url='/login/')
def complete_logs(request,server):
    # a = os.popen('cat /var/log/{server}/access.log').read()
    # print(a,type(a))
    # print(server)
    try:
        returned_text = subprocess.check_output(f"sudo cat /var/log/{server}/access.log", shell=True, universal_newlines=True)
        # print("dir command to list file and directory")
        # print(returned_text)
        context={'data':returned_text,'server':server}

        # print(a.split('\n'))
        # print(context)
        # return render(request,'index.html',context=context)
        # return JsonResponse(context)
    except:
        os.system(f'chmod ugo+rwx /var/log/{server}/access.log')
        returned_text = subprocess.check_output(f"cat /var/log/{server}/access.log", shell=True, universal_newlines=True)
        # print("dir command to list file and directory")
        # print(returned_text)
        context={'data':returned_text,'server':server}
    return render(request,'complete-log.html',context)

@staff_member_required(login_url='/login/')
@csrf_exempt
def show_custom(request,server):
    try:
        context = {}
        if request.method == "POST":
            # formData = request.body
            # form = ast.literal_eval(formData.decode('utf-8'))
            # print(form)
            fil = request.POST['filter']
            if fil!='':
                fil=int(fil)
                dt = datetime.now()
                hr = dt.hour
                # print(dt)
                final_arr ={200:'0',404:'0',301:'0',302:'0',500:'0'}
                # print(hr)
                past=hr - fil
                dt1 = dt.strftime('%d\/%b\/%Y')
                if past >0:
                    if hr<10 and past<10:
                        cmd = f"awk -e '$4 ~/{dt1}:0[{past}-{hr}]/ "+"{print $9}' " + f'/var/log/{server}/access.log | sort | uniq -c'
                        # cmd = f'egrep "{dt1}:(0[{past}-{hr}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif hr >=10 and past>=10 and hr<20 and past<20:
                        cmd = f"awk -e '$4 ~/{dt1}:1[{str(past)[1]}-{str(hr)[1]}]/ "+"{print $9}' " + f'/var/log/{server}/access.log | sort | uniq -c'
                        # cmd = f'egrep "{dt1}:(1[{str(past)[1]}-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif hr>=20 and past>=20:
                        cmd = f"awk -e '$4 ~/{dt1}:2[{str(past)[1]}-{str(hr)[1]}]/ "+"{print $9}' " + f'/var/log/{server}/access.log | sort | uniq -c'
                        # cmd = f'egrep "{dt1}:(2[{str(past)[1]}-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif past<10 and hr >=10 and hr<20:
                        cmd = f"awk -e '$4 ~/{dt1}:0[{past}-9]|1[0-{str(hr)[1]}]/ "+"{print $9}' " + f'/var/log/{server}/access.log | sort | uniq -c'
                        # cmd = f'egrep "{dt1}:(0[{past}-9]|1[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif past<10 and hr >=20:
                        cmd = f"awk -e '$4 ~/{dt1}:0[{past}-9]|1[0-9]|2[0-{str(hr)[1]}]/ "+"{print $9}' " + f'/var/log/{server}/access.log | sort | uniq -c'
                        
                        # cmd = f'egrep "{dt1}:(0[{past}-9]|1[0-9]|2[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    elif past>=10 and hr>=20 and past<20:
                        cmd = f"awk -e '$4 ~/{dt1}:1[{past}-9]|2[0-{str(hr)[1]}]/ "+"{print $9}' " + f'/var/log/{server}/access.log | sort | uniq -c'
                        # cmd = f'egrep "{dt1}:(1[{past}-9]|2[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log'
                    else:
                        cmd = f"awk -e '$4 ~/{dt1}:0[{past}-9]|1[0-{str(hr)[1]}]/ "+"{print $9}' " + f'/var/log/{server}/access.log | sort | uniq -c'
                        # cmd = f'egrep "{dt1}:(0[0-9]|1[0-9]|2[0-4]).*HTTP.*{code}" /var/log/{server}/access.log'
                else:
                    cmd = f"awk -e '$4 ~/{dt1}:0[0-9]|1[0-9]|2[0-4]/ "+"{print $9}' " + f'/var/log/{server}/access.log | sort | uniq -c'
                    # cmd = f'egrep "{dt1}:(0[0-9]|1[0-9]|2[0-4]).*HTTP.*{code}" /var/log/{server}/access.log'
                # print(cmd)
                # codes 
                # cmd = "awk -e '$4 ~/22\/Feb\/2023:0[4-5]/ {print $9}' /var/log/apache2/access.log | sort | uniq -c"
                # print(cmd)
                op = subprocess.check_output('sudo ' + cmd, shell=True, universal_newlines=True)
                op1 = op.splitlines()
                for ops in op1:
                    arr = ops.split()
                    if '200' in ops:
                        if arr[1] == '200':
                            final_arr[200] = arr[0]
                    if '404' in ops:
                        if arr[1] == '404':
                            final_arr[404] = arr[0]
                    if '500' in ops:
                        if arr[1] == '500':
                            final_arr[500] = arr[0]
                    if '301' in ops:
                        if arr[1] == '301':
                            final_arr[301] = arr[0]
                    if '302' in ops:
                        if arr[1] == '302':
                            final_arr[302] = arr[0]


                        
                # if code not in final_arr:
                #     try:final_arr[code] = subprocess.check_output(cmd, shell=True, universal_newlines=True)
                #     except:final_arr[code] = ''
                # else:
                #     try:final_arr[code] += subprocess.check_output(cmd, shell=True, universal_newlines=True)
                #     except: final_arr[code] += ''
                context={'data':final_arr,'server':server,'filter':fil}
        # return JsonResponse(context)
    except:
        messages.info(request,'Unable to fetch logs')
        context={'server':server}
    return render(request,'summary.html',context)

@staff_member_required(login_url='/login/')
@csrf_exempt
def show_detailed_codewise(request,server):
    try:
        context ={}
        if request.method == "POST":
            # formData = request.body
            # form = ast.literal_eval(formData.decode('utf-8'))
            form = request.POST
            # print(form)
            fil = form['filter']
            code = form['code']
            # print(fil)
            # final_arr = []
            if fil != '' and code != '':
                final_arr = []
                # codes = [200,404,500,301,302]
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
                # for code in codes:
                if past >0:
                    if hr<10 and past<10:
                        cmd = f'egrep "{dt1}:(0[{past}-{hr}]).*HTTP.*${code}" /var/log/{server}/access.log' + f" | awk -e '$9 ~/{code}/'"
                    elif hr >=10 and past>=10 and hr<20 and past<20:
                        cmd = f'egrep "{dt1}:(1[{str(past)[1]}-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log' + f" | awk -e '$9 ~/{code}/'"
                    elif hr>=20 and past>=20:
                        cmd = f'egrep "{dt1}:(2[{str(past)[1]}-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log' + f" | awk -e '$9 ~/{code}/'"
                    elif past<10 and hr >=10 and hr<20:
                        cmd = f'egrep "{dt1}:(0[{past}-9]|1[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log' + f" | awk -e '$9 ~/{code}/'"
                    elif past<10 and hr >=20:
                        cmd = f'egrep "{dt1}:(0[{past}-9]|1[0-9]|2[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log' + f" | awk -e '$9 ~/{code}/'"
                    elif past>=10 and hr>=20 and past<20:
                        cmd = f'egrep "{dt1}:(1[{past}-9]|2[0-{str(hr)[1]}]).*HTTP.*{code}" /var/log/{server}/access.log' + f" | awk -e '$9 ~/{code}/'"
                    else:
                        cmd = f'egrep "{dt1}:(0[0-9]|1[0-9]|2[0-4]).*HTTP.*{code}" /var/log/{server}/access.log' + f" | awk -e '$9 ~/{code}/'"
                else:
                    cmd = f'egrep "{dt1}:(0[0-9]|1[0-9]|2[0-4]).*HTTP.*{code}" /var/log/{server}/access.log' + f" | awk -e '$9 ~/{code}/'"
                # print(cmd)
                # if code not in final_arr:
                #     try:final_arr[code] = subprocess.check_output(cmd, shell=True, universal_newlines=True)
                #     except:final_arr[code] = ''
                # else:
                #     try:final_arr[code] += subprocess.check_output(cmd, shell=True, universal_newlines=True)
                #     except: final_arr[code] += ''
                print(cmd)
                print(code)
                try: final_arr.append(subprocess.check_output('sudo ' + cmd,shell=True,universal_newlines=True))
                except:pass
                context={'data':final_arr[0],'server':server}

        # return JsonResponse(context)
    except:
        messages.info(request,'Unable to fetch logs')
        context={'server':server}
    return render(request,'codewise.html',context)

@staff_member_required(login_url='/login/')
@csrf_exempt
def show_ipwise(request,server):
    try:
        cmd = "awk '{ print $1 } '" +  f" /var/log/{server}/access.log | sort | uniq -c"
        # print(cmd)
        total_ip = subprocess.check_output('sudo ' + cmd, shell=True, universal_newlines=True)
        arr_total_ip = total_ip.split('\n')
        # final_total = arr_total_ip.split()
        cmd = "awk '{ print $1,$9 } '"+ f" /var/log/{server}/access.log | sort | uniq -c"
        r = subprocess.check_output('sudo ' + cmd, shell=True, universal_newlines=True)
        # cmd = "awk -e '$7 ~/^408/ {print $1,$7}'" +  f" /var/log/{server}/access.log | sort | uniq -c"
        # r_408 = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        # print(r)
        cmd = "sudo iptables -L INPUT -v -n | grep DROP | awk '{ print $8 }'"
        blocked_ip = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        # blocked_ip = ''
        # print(blocked_ip)
        blocked_ip = blocked_ip.split()
        # print(blocked_ip)
        context = {'total_ip':arr_total_ip,'detailed':r,'blocked_ips':blocked_ip,'server':server}
        # context={'status':200,'data':[total_ip,r,r_408]}
        # return JsonResponse(context)
    except:
        messages.info(request,'Unable to fetch logs')
        context={'server':server}
    return render(request,'ipwise.html',context)

@staff_member_required(login_url='/login/')
@csrf_exempt
def block_ip(request,server):
    try:
        if request.method == "POST":
            # formData = request.body
            # form = ast.literal_eval(formData.decode('utf-8'))
            ip = request.POST['ip']
            cmd = "sudo iptables -L INPUT -v -n | grep DROP | awk '{ print $8 }'"
            blocked_ip = subprocess.check_output(cmd, shell=True, universal_newlines=True)

            blocked_ip = blocked_ip.split()
            if ip not in blocked_ip:
            # print(ip)
            # print(cmd)
                os.system(f'sudo iptables -A INPUT -s {ip} -j DROP')
            # os.system('sudo service iptables save')

            # blocked_ips = subprocess.check_output("iptables -L INPUT -v -n", shell=True, universal_newlines=True)
            # context = {'status':200,'msg':'successfully blocked'}
            # return JsonResponse(context)
            messages.info(request,f'{ip} blocked successfully.')

    except:
        messages.info(request,'Unable to Block IP')

    return redirect(f'/show_ipwise/{server}/')

# @csrf_exempt
# def blocked_ips(request,server):
#     blocked_ip = subprocess.check_output("iptables -L INPUT -v -n | grep DROP | awk '{ print $8 }'", shell=True, universal_newlines=True)
#     # print(blocked_ip)
#     context={'status':200,'data':blocked_ip}
#     return JsonResponse(context)

@staff_member_required(login_url='/login/')
@csrf_exempt
def unblock_ips(request,server):
    try:
        if request.method == "POST":
            # formData = request.body
            # form = ast.literal_eval(formData.decode('utf-8'))
            ip = request.POST['ip']
            # print(ip)
            os.system(f'sudo iptables -D INPUT -s {ip} -j DROP')
            # os.system('service iptables save')
            # context = {'status':200,'msg':'successfully unblocked'}
            # return JsonResponse(context)
            messages.info(request,f'{ip} unblocked successfully.')
    except:
        messages.info(request,'Unable to Unblock IP')
    return redirect(f'/show_ipwise/{server}/')


@staff_member_required(login_url='/login/')
@csrf_exempt
def firewall(request,server):
    try:
        blocked_ip = subprocess.check_output("sudo iptables -L INPUT -v -n | grep DROP | awk '{ print $8 }'", shell=True, universal_newlines=True)
        context = {'data':blocked_ip.split(),'server':server}
    # return JsonResponse(context)
    except:
        messages.info(request,'Unable to fetch Blocked IPs')
        context={'server':server}

    return render(request,'firewall.html',context)

@staff_member_required(login_url='/login/')
@csrf_exempt
def unblock_ips_fw(request,server):
    try:
        if request.method == "POST":
            # formData = request.body
            # form = ast.literal_eval(formData.decode('utf-8'))
            ip = request.POST['ip']
            # print(ip)
            os.system(f'sudo iptables -D INPUT -s {ip} -j DROP')
            # os.system('service iptables save')
            # context = {'status':200,'msg':'successfully unblocked'}
            # return JsonResponse(context)
            messages.info(request,f'{ip} unblocked successfully.')
    except:
        messages.info(request,'Unable to Unblock IP')
    return redirect(f'/firewall/{server}/')