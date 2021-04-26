#-*-coding:utf-8-*-
#pip install pandas puresnmp 
import datetime, sys
import pandas as pd      #docs : https://pandas.pydata.org/docs/user_guide/index.html
import puresnmp          #docs : https://puresnmp.readthedocs.io/en/latest/index.html


now=datetime.datetime.now()
nowDate = now.strftime('%Y%m%d')


def logging(logmsg) :
    f = open("snmp-log-"+nowDate+".log",'a')
    print(logmsg)
    f.write(logmsg+"\r\n")
    f.close()

def main(filename):
    try:
        data = pd.read_csv(filename)
    except FileNotFoundError as e :
        logging("FileNotFoundError(%s)" % (e))
        exit(0)
    except e:
        logging("Unexpected error(%s)" % (e))
        exit(0)

    for i in range(len(data)) :
        #print(data.iloc[i])
        ip = data.iloc[i].ip
        community = data.iloc[i].community
        oid = data.iloc[i].oid
        logging("//======= start connect [%s] =========" % ip)
        try:
            result = puresnmp.get(ip, community, oid, timeout=1).decode('UTF-8')
            logging(result)
        except puresnmp.exc.Timeout as e:
            logging("[%s] SNMP 접속불가!(%s)" % (ip, e))
        except e:
            logging("[%s] Unexpected error(%s)" % (ip, e))
        logging("//======= end of connect [%s] =========" % ip)


if __name__ == "__main__": 
    if len(sys.argv) != 2 :
        print("ex) python %s filename" % sys.argv[0])
        exit()
    filename = sys.argv[1]

    start_time = datetime.datetime.now()
    main(filename)
    end_time = datetime.datetime.now()

    logging('Duration: {}'.format(end_time - start_time))



