#-*-coding:utf-8-*-
#pip install pandas paramiko 
import datetime, sys, time
import pandas       #docs : https://pandas.pydata.org/docs/user_guide/index.html
import paramiko     #docs : http://docs.paramiko.org/en/stable/

shell_str = ""
now=datetime.datetime.now()
nowDate = now.strftime('%Y%m%d')


def logging(logmsg) :
    f = open("ssh-log-"+nowDate+".log",'a')
    print(logmsg)
    f.write(logmsg+"\r\n")
    f.close()


def ssh_connect(ipaddr, userid, userpw):
    try :
        tmp_client = paramiko.SSHClient()
        tmp_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        tmp_client.load_system_host_keys()
        tmp_client.connect(ipaddr, username=userid, password=userpw, allow_agent=False,look_for_keys=False, banner_timeout=200)

        if tmp_client :
            res = tmp_client.invoke_shell()
            time.sleep(3)

            login_info = send_cmd(res, 'no page')
            #logging("login_info : %s " % login_info)

            global shell_str
            shell_str = send_cmd(res, "")
            #logging("shell_str : %s " % shell_str)


    except paramiko.ssh_exception.AuthenticationException as e:
        res = "인증실패!(%s)" % e
    except paramiko.ssh_exception.SSHException as e:
        res = "SSH접속불가!(%s)" % e
    except e:
        res = "[%s] Unexpected error(%s)" % (sys._getframe(0).f_code.co_name, e)

    return res


def send_cmd(ch, cmd):
    ch.send(cmd+"\n")
    outdata, errdata = waitStrems(ch)
    #print(outdata)
    #print(errdata)
    return outdata[:-1]+" "


def waitStrems(ch): 
    outdata = ""
    errdata = "" 

    time.sleep(1) 
    while ch.recv_ready():
       outdata += ch.recv(1000).decode()

    while ch.recv_stderr_ready(): 
       errdata += ch.recv_stderr(1000).decode()

    return outdata, errdata

 

def main(filename):
    try:
        data = pandas.read_csv(filename)
    except FileNotFoundError as e :
        print("FileNotFoundError(%s)" % (e))
        exit(0)
    except pandas.errors.ParserError as e :
        print("ParserError(%s)" % (e))
        exit(0)
    except e:
        print("[%s] Unexpected error(%s)" % (sys._getframe(0).f_code.co_name, e))
        exit(0)


    for i in range(len(data)) :
        #print(data.iloc[i])
        ip = data.iloc[i].ip
        userid = data.iloc[i].userid
        userpw = data.iloc[i].userpw
        enable = data.iloc[i].enable
        print("//======= start connect [%s] =========" % ip)
        ch = ssh_connect(ip, userid, userpw)
        #print(type(ch))

        if isinstance(ch, paramiko.channel.Channel) :

            output = shell_str 
            output += send_cmd(ch, "configure")
            output += send_cmd(ch, "show ssh server")
            output += send_cmd(ch, "end")
            logging(output)

            ch.close()
        else :
            #ERROR
            print(ch)
        print("//======= end of connect [%s] =========" % ip)


if __name__ == "__main__": 
    if len(sys.argv) != 2 :
        print("ex) python %s filename" % sys.argv[0])
        exit()
    filename = sys.argv[1]

    start_time = datetime.datetime.now()
    main(filename)
    end_time = datetime.datetime.now()

    print('Duration: {}'.format(end_time - start_time))
