final_arr={}
import subprocess
cmd = "awk -e '$4 ~/22\/Feb\/2023:0[4-5]/ {print $9}' /var/log/apache2/access.log | sort | uniq -c"
op = subprocess.check_output(cmd, shell=True, universal_newlines=True)
print(op)
op1 = op.splitlines()
# print(op1)
for ops in op1:
    if '200' in ops:
        arr = ops.split()
        if arr[1] == '200':
            final_arr[200] = arr[0]
    if '404' in ops:
        arr = ops.split()
        if arr[1] == '404':
            final_arr[404] = arr[0]
    if '500' in ops:
        arr = ops.split()
        if arr[1] == '500':
            final_arr[500] = arr[0]
    if '301' in ops:
        arr = ops.split()
        if arr[1] == '301':
            final_arr[301] = arr[0]
    if '302' in ops:
        arr = ops.split()
        if arr[1] == '302':
            final_arr[302] = arr[0]
print(final_arr)
