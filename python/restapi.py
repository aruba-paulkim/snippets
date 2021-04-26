#-*-coding:utf-8-*-
#pip install requests 
import datetime, sys, time, json
import requests   #docs : https://docs.python-requests.org/en/master/


def main():
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    cookies = {'sessionKey': 'sessionValue'}
    url = "https://www.google.com"

    #GET
    params = { "a" : "bbb", "b" : 123 }
    response = requests.get(url, params=params, verify=False)

    #POST(raw)
    #data = { "a" : "bbb", "b" : 123 }
    #response = requests.post(url, data=data, verify=False)

    #POST(json)
    #data = { "a" : "bbb", "b" : 123 }
    #response = requests.post(url, data=json.dumps(data), verify=False)


    print("status code :", response.status_code)
    print("encoding :", response.encoding)
    print("raw :", response.raw)
    print("content :", response.content)
    print("text :", response.text)
    #print("json :", response.json())
    print("raise_for_status() :", response.raise_for_status())
    print("headers :", response.headers)
    print("headers Content-Type :", response.headers['Content-Type'])
    print("cookies :", response.cookies)
    #print("cookies example_cookie_name :", response.cookies['example_cookie_name'])


if __name__ == "__main__": 
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()

    print('Duration: {}'.format(end_time - start_time))



