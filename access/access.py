import os
from getpass import getpass
from datetime import date
# from datetime import time
from datetime import datetime,timedelta


print('Welcome to the access monitor')
user = input('Enter Username: ')
password = getpass('Enter the Password: ')
if user == 'vedant' and password=='123':
    while True:
        print('\n')
        print('The functionalities of the access monitor includes: ')
        print('1. See the complete access log')
        print('2. Print only the successful access requests')
        print('3. Requests received today')
        print('4. Requests received in past 1 hr')
        print('5. Block an IP')
        print('6. Unblock an IP address')
        print('7. Requests received in past N days')
        print('8. Requests received in a specific period')


        # print('4. Requests received in past 1 hr')
        print('Q to Quit')
        n=input('Enter your choice: ')
        if n=='1':
            os.system('cat /var/log/apache2/access.log')
        elif n.lower()=='q':
            print('Adios Amigo!!')
            break
        elif n=='2':
            # log = open('/var/log/apache2/access.log', 'r')
            # reader = list(log.readlines())
            # log.close()
            # printables = []
            # for line in reader:
            #     if line.count('200') >=1:
            #         l1 = line.split()
            #         # print(l1)
            #         if l1[8] == '200':
            #             # printables.append(line.split())
            #             print(line,end="")
            # os.system("grep 'HTTP[^"]*" 200 ' /var/log/apache2/access.log")
            cmd = "grep 'HTTP[^" + '"]*" 200 ' + "' /var/log/apache2/access.log"
            print(cmd)
            os.system(cmd)
        elif n=='3':
            dt = date.today().strftime('%d/%b/%Y')
            os.system(f'grep -i "{dt}" /var/log/apache2/access.log')
        elif n=='4':
            # log = open('/var/log/apache2/access.log', 'r')
            # reader = list(log.readlines())
            # log.close()
            # dt = datetime.now()
            # # print(dt)
            # for line in reader:
            #     l1 = line.split()
            #     dt1 = datetime.strptime(l1[3][1:],'%d/%b/%Y:%H:%M:%S')
            #     # print(dt1,type(dt1))
            #     if (dt-dt1).total_seconds() / 3600 <= 1:
            #         print(line,end='')
            dt = datetime.now()
            # print(dt)
            # dt1 = dt - timedelta(hours=1)
            # print(dt1)
            # dt = dt.strftime('%d/%b/%Y:%H')
            print(dt)
            hours = dt.strftime('%H')
            minutes = dt.strftime('%M')
            dat = dt.strftime('%d/%b/%Y')
            dt1 = dt - timedelta(hours=1)
            dat1 = dt1.strftime('%d/%b/%Y')
            h1,m1 = dt1.strftime('%H'),dt1.strftime('%M')
            if dat == dat1:
                os.system(f'egrep "{dat}:{h1}:[{m1}-59]" /var/log/apache2/access.log')
                os.system(f'egrep "{dat}:{hours}:[0-{minutes}]" /var/log/apache2/access.log')
        elif n=='5':
            ip = input('Enter the IP address to be blocked: ')
            os.system(f'iptables -A INPUT -s {ip} -j DROP')
            os.system('service iptables save')
        elif n=='6':
            os.system('iptables -L INPUT -v -n')
            ip = input('Enter the IP to be unblocked: ')
            os.system(f'iptables -D INPUT -s {ip} -j DROP')
            os.system('service iptables save')
        elif n=='7':
            n_of_days = int(input('Enter the number of days: '))
            # dt = date.today()
            # dt = dt+timedelta(days=1)
            # dt2 = dt.strftime('%d\/%b\/%Y')
            dt = date.today()-timedelta(days=n_of_days)
            dt1 = dt.strftime('%d\/%b\/%Y')
            # print(dt1,dt2)

            # for i in range(n_of_days+1):
            #     os.system(f'grep {dt1} /var/log/apache2/access.log')
            #     dt = dt+timedelta(days=1)
            #     dt1 = dt.strftime('%d/%b/%Y')
            # cmd = f'sed -n "/{dt1}/,/{dt2}/p" /var/log/apache2/access.log'
            # print(cmd)
            cmd = 'egrep "('
            for i in range(n_of_days+1):
                if i != n_of_days:
                    cmd += f'{dt1}.*|'
                else:
                    cmd += f'{dt1}.*'
                dt+=timedelta(days=1)
                dt1 = dt.strftime('%d\/%b\/%Y')
            cmd+=')" /var/log/apache2/access.log'

            # print(cmd)
            os.system(cmd)

            # os.system(f'sed -n "/{dt1}/,/{dt2}/p" /var/log/apache2/access.log')
            # os.system(f'sudo grep -E "{dt2} | {dt1}" /var/log/apache2/access.log')
            # os.system(f"awk '/^{dt2}.*/,/{dt1}.*/' /var/log/apache2/access.log")
                # print(dt1)
                # print(dt)
        elif n=='8':
            s = input('Enter the start date for the period (format: dd/mm/yyyy): ')
            e = input('Enter the end date for the period (format: dd/mm/yyyy): ')
            dts = datetime.strptime(s,'%d/%m/%Y')
            dte = datetime.strptime(e,'%d/%m/%Y')
            dt1, dt2 = dts.strftime('%d\/%b\/%Y'), dte.strftime('%d\/%b\/%Y')
            # n_of_days = ((dte-dts).total_seconds() // 3600)//24 
            delta = timedelta(days=1)
            # print(n_of_days) x
            if dte < dts:
                print('Incorrect Range')
            else:
                # os.system(f'sed -n "/{dt1}/,/{dt2}/p" /var/log/apache2/access.log')
                cmd = 'egrep "('
                while dts<dte:
                    cmd += f'{dt1}.*|'
                    dts+=delta
                    dt1 = dts.strftime('%d\/%b\/%Y')
                cmd += f'{dt2}.*)" /var/log/apache2/access.log'
                os.system(cmd)


        else:
            print('Invalid Input')
else:
    print('Sorry! Invalid Credentials. Try again Later')

# os.system('cat /var/log/apache2/access.log')