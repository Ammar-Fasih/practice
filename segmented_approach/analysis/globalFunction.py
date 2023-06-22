import datetime
import os
import json
import pandas as pd
import requests

def findElement(base,by,value):
    try:
        element = base.find_element(by,value)
    except:
        element = None
    return element

def findElements(base,by,value):
    try:
        element = base.find_elements(by,value)
    except:
        element = None
    return element

def masterLogging(success,fail,jsonlog_fileName):

    # getting current date and time
    time = datetime.datetime.now()
    time = time.strftime('Date: %d-%b-%Y  \nTime: %X')

    # check if the folder exist, if no then it creates
    folder = f'logging/'
    filename = f'masterLog.log'
    filePath = folder + filename
    if os.path.exists(folder) == False:
        os.makedirs(folder)

    # updating masterlog
    masterLog = open(filePath,'a')
    masterLog.write(f'''
{'='*50}\n
{time}\n
Logging stored in file name as: {jsonlog_fileName}
Total number of requests: {success + fail}
Number of successfull requests: {success}
Number of unsuccessfull requests: {fail}\n
{'='*50}
    ''')
    masterLog.close()

    print('masterlog has been updated')

def jsonLogging(jsonlog_fileName,pirlUID,responseDict,status):

    # getting current date and time
    time = datetime.datetime.now()
    date = time.strftime('%d-%b-%Y')
    time = time.strftime('%X')

    # appending new key value pair in dictionary
    responseDict['docID'] = pirlUID
    responseDict['status'] = status
    responseDict['pushTime'] = time
    responseDict['pushDate'] = date

    if responseDict['entity'] == "":
        responseDict['entity'] = {}

    if responseDict['i18nMessagesMap'] == {}:
        responseDict['i18nMessagesMap'] = []


    # converts dict into json
    response = json.dumps(responseDict)
    
    # check if the folder exist, if no then it creates
    folder = f'logging/'
    filePath = folder + jsonlog_fileName
    if os.path.exists(folder) == False:
        os.makedirs(folder)

    # Logging of pirlID and response text
    logFile = open(filePath,'a')
    logFile.write(f'{response}\n')
    logFile.close()

def fileDownload_log(id,status,url,download_filename,log_filename):

    # getting current date and time
    time = datetime.datetime.now()
    date = time.strftime('%d-%b-%Y')
    time = time.strftime('%X')

    # check if the folder exist, if no then it creates
    folder = f'logging/'
    log_filename = f'fileDownload_log.csv'
    filePath = folder + log_filename
    if os.path.exists(folder) == False:
        os.makedirs(folder)

    # logging of docID, status, url, filepath, date, time
    logFile = open(filePath,'a')
    logFile.write(f'{id},{status},{url},{download_filename},{date},{time}\n')
    logFile.close()

def urlExtract(sourceFile):
    urls = []
    df = pd.read_csv(sourceFile)

    for index,i in df.iterrows():
        urls.append(i['URL'])
    print('Total number of urls extracted are: ',len(urls))
    return urls

def download(url,download_filename,status,success,failure):
    try:
        response = requests.get(url)
        # If response is successfull, download and save file
        if response.status_code == 200:
            open('downloads/'+download_filename,'wb').write(response.content)
            status = 'Success'
            success+=1
            # print(f'{download_filename} = Success')
        else:
            status = 'Failure'
            failure+=1
            # print(f'{download_filename} = Failed')
    
    except:
        status = 'Failure'
        failure+=1
        print(f'{download_filename} = Failed, {response.text}')
    fileDownload_log(status,url,download_filename)

def pushData(payload):
    url = "https://lnx-commercial.nebbiu.net/api/v1/workflow/actions/default/fire/PUBLISH"

    if blob.exists() == True:
        final_payload = {'json':f'{payload}'}
        files=[
            ('file',(f'{blob.name}',blob.open("rb")))
        ]
        headers = {
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcGljMWUzMzE5NC02M2Q1LTQ3YmYtOWIwOS01MTgwNmMyY2Y3MjIiLCJ4bW9kIjoxNjY2ODc4NTI3MDAwLCJuYmYiOjE2NjY4Nzg1MjcsImlzcyI6ImI2ODVkMzdiMmQiLCJsYWJlbCI6InBpcmwiLCJleHAiOjE3NjE1MTk2MDAsImlhdCI6MTY2Njg3ODUyNywianRpIjoiMDliMWE1NTAtOWExMS00MDZiLWJjMWQtZjdhNjFiNmEyYTViIn0.eHPWJuvqQYW-cvCBBt9RRYuS-JDr9-52Ge3eXWh1nz4',
    'Cookie': 'JSESSIONID=A390A68D5D87D26047AF8990A8DED8B8'
    }

        response = requests.request("PUT", url, headers=headers, data=final_payload, files=files)

    elif blob.exists() == False:
        headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhcGljMWUzMzE5NC02M2Q1LTQ3YmYtOWIwOS01MTgwNmMyY2Y3MjIiLCJ4bW9kIjoxNjY2ODc4NTI3MDAwLCJuYmYiOjE2NjY4Nzg1MjcsImlzcyI6ImI2ODVkMzdiMmQiLCJsYWJlbCI6InBpcmwiLCJleHAiOjE3NjE1MTk2MDAsImlhdCI6MTY2Njg3ODUyNywianRpIjoiMDliMWE1NTAtOWExMS00MDZiLWJjMWQtZjdhNjFiNmEyYTViIn0.eHPWJuvqQYW-cvCBBt9RRYuS-JDr9-52Ge3eXWh1nz4',
        'Content-Type': 'application/json',
        'Cookie': 'JSESSIONID=A390A68D5D87D26047AF8990A8DED8B8'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        
