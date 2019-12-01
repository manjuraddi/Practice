import os
from pexpect import pxssh
import re
from datetime import datetime
import pdb
import paramiko


def ssh_file_data():
    log_file_path = ["/home/mraddi/ml_env/log1.log", "/home/mraddi/ml_env/log2.log", "/home/mraddi/ml_env/log3.log"]
    search_list = ["HOST-1A", "HOST-1B"]

    #SSH cont
    ssh_client =paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname='127.0.0.1',username='mraddi',password='mraddi')
    ftp_client=ssh_client.open_sftp()
    #pdb.set_trace()
    remote_file_data = ""
    try:
        for temp_file in log_file_path:
            remote_file = ftp_client.open(temp_file)
            remote_file_data += remote_file.read().decode("utf-8") + "\n"
            remote_file.close()
    except:
        pass
    finally:
        ftp_client.close()
    return remote_file_data


def filter_constr_file(file1):
    #pdb.set_trace()
    search_list = ["HOST-1A", "HOST-1B"]
    const_log = ""
    spu_list = ', '.join(re.findall(r'spurious.* (\d.+)', file1))
    for temp_srh in search_list:
        host_list = re.findall(r'(.*)(\d*)(.-)(.*)('+ re.escape(temp_srh) +')(.*)', file1)

        for tpl in host_list:
            if tpl[5].lower().strip() == "connected":
                const_log += tpl[4] + ' - ' + tpl[5] + ' at ' + datetime.strptime(tpl[0], '%b %d %Y %I:%M:%S%p').strftime('%d/%m/%y %H:%M:%S')
            elif tpl[5].split(' ')[1].lower().strip() == "disconnected":
                const_log += ' and ' + tpl[5].split(' ')[1] + ' at ' + datetime.strptime(tpl[0], '%b %d %Y %I:%M:%S%p').strftime('%d/%m/%y %H:%M:%S')+"\n"


    const_log += "Spurious activities from: " + spu_list

    with open("data_filt.txt", 'w') as wrt_data:
        wrt_data.write(const_log)

if __name__ == "__main__":
    rmt_data = ssh_file_data()
    filter_constr_file(rmt_data)


