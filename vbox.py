####################################################################################################################################################
#                                                                                                                                                  #
# Description: Script for start, stop, reset virtual machines in virtual box. Also have the possibility of connect by ssh and execute a command    #
#                                                                                                                                                  #
# author: manuel boluda gonzalez                                                                                                                   #
#                                                                                                                                                  #
#####################################################################################################################################################

import os
import sys
import paramiko

# os.system('VBoxManage list vms')

vm = os.popen('VBoxManage list vms').read() # List of all the virtual machines
vm = vm.split('\n')
vm.pop()

names = []
ids = []

for v in vm:
    tid = str(v) 
    tid = tid.split('{')
    counter = 1

    for t in tid: # Take the virtual machines ids
        if (counter % 2 == 0):
            t = t[:-1]
            ids.append(t)
        else: # Take the virtual machines names
            names.append(t)

        counter += 1

print('Select the VM:')
print('')

counter = 0

for n in names:
    print(str(counter) + ') ' + n) # Showing the virtual machines in the console
    counter +=1

vm = input('Select the vm ') 

if vm is None:
    print('Exit')
    sys.exit()

vm = vm + ',' # Put an extra comma  

print('What do you want to do with these vms? (Only one at the same time)')
print('')
print('0) Start')
print('1) Execute acceptance test in gems')
print('2) Reload')
print('3) Poweroff')
print('')

action = input('Select the action: ') # Select what we need to do with the vm already selected

if action is None:
    print('Exit')
    sys.exit()

if action == '0': # Start virtual machines
    print ( 'Starting the vms...')
    vm = vm.split(',')
    vm.pop()

    for v in vm:
        os.system('VBoxManage startvm ' + names[int(v)] + ' --type headless')

elif action == '1': # Start script by ssh but the ip should be put manually
    print ( 'Connecting to ssh...')
    
    listOfIp = [
        '192.168.10.1',
        '192.168.10.2',
        '192.168.10.3',
        '192.168.10.4',
        '192.168.10.5',
        '192.168.10.6',
        '192.168.10.7'
    ]
    
    for ip in listOfIp:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(ip, 22, 'tester', 'arsenic00')

        stdin, stdout, stderr = client.exec_command('cd /home/tester/acceptancetest && python3.5 gemstest.py')

    print('In a few minutes students start to login in GEMS Online administrator screen')

elif action == '2': # Reload virtual machines
    print ( 'Reload the vms...')
    vm = vm.split(',')
    vm.pop()

    for v in vm:
        os.system('VBoxManage controlvm ' + names[int(v)] + ' reset')

elif action == '3': # Poweroff virtual machines
    print ( 'Poweroff the vms...')
    vm = vm.split(',')
    vm.pop()

    for v in vm:
        os.system('VBoxManage controlvm ' + names[int(v)] + ' poweroff')

#########################################################################################################################################