from netmiko import ConnectHandler
from netmiko import NetmikoTimeoutException
from netmiko import NetMikoAuthenticationException
from netmiko import ReadTimeout
from netmiko import SSHException
import re
import csv
import pwinput

user = input("Username: ")
passwd = pwinput("Password: ")

#Enter name of csv file that contains the list of network devices you want to iterate through                 
filename = input("filename: ")
                 
with open(filename, 'r') as device_list:
#Create a new csv file where you augment original csv with new column  
    with open("new_"+filename, 'w', newline='') as new_device_list:
        writer = csv.writer(new_device_list)
        csv_reader = csv.reader(device_list)
        all = []
        row = next(csv_reader)
        row.append('device_model')
        all.append(row)
        dev_count = 1

        for row in csv_reader:
            print('*'*10 + str(dev_count) + '*'*10)
            dev_count += 1
            hostname = row[0]
            host_ip = row[1]

            device = {
                "device_type": "cisco_ios",
                "host": host_ip,
                "username": user,
                "password": passwd,
                "port": 22
            }
            try:
                with ConnectHandler(**device) as devconn:
                    output = devconn.send_command("show version", read_timeout=10)
                    if (re.search(r"Model [Nn]umber \s*\:(.*)", output)):
                        search_result = re.search(r"Model [Nn]umber \s*\:(.*)", output)
                        result = search_result.group(1)
                        print(result)
                        row.append(result)
                        all.append(row)
                    elif (re.search(r"cisco (Nexus .*\))", output)):
                        search_result = re.search(r"cisco (Nexus .*\))", output)
                        result = search_result.group(1)
                        print(result)
                        row.append(result)
                        all.append(row)
                    elif (re.search(r"Software, Version (.*\))", output)):
                        search_result = re.search(r"Software, Version (.*\))", output)
                        result = search_result.group(1)
                        print(result)
                        row.append(result)
                        all.append(row)
                    elif (re.search(r"Software Version (.*\d\))", output)):
                        search_result = re.search(r"Software Version (.*\d\))", output)
                        result = search_result.group(1)
                        print(result)
                        row.append(result)
                        all.append(row)
                    else: 
                        all.append(row)
            except NetmikoTimeoutException:
                print(f"{host_ip} has timed out")
                all.append(row)
                continue
            except NetMikoAuthenticationException:
                print(f"{host_ip} has wrong username\password")
                all.append(row)
                continue
            except SSHException:
                print(f"{host_ip} has raised an SSH exception")
                all.append(row)
                continue
            except ReadTimeout:
                print(f"{host_ip} connection has timed out")
                all.append(row)
                continue
            except:
                print(f"{host_ip} is not a cisco device")
                all.append(row)
                continue
        writer.writerows(all)