import requests
import json
import re
from simple_chalk import chalk

# 
sitesJson = './data/sites.json'
notAccurate = './data/notaccurate.txt'

name: any

inputMsg = f"""
    {chalk.green('================================================================')}
    
                    {chalk.blueBright.underline.bold('Enter a Name to Search or Track Anyone!')}
        
        {chalk.green.bold('[!] ')} Means User was found.
        {chalk.yellow.bold('[!] ')} Something went wrong.
        {chalk.magenta.bold('[!] ')} User found (May not be Accurate).
        {chalk.red.bold('[!] ')} Can't find this User.
        
        {chalk.black.bold('GitHub')} : {chalk.blue('http://github.com/xvpc/trackthis')} 
        
    {chalk.green('================================================================')}
    {chalk.greenBright('Name => ')} 
    """

def getName():
    name = input(inputMsg)
    if name != '':
        checkName(name)

def fetchData(link):
    notAccurateLinks = []
    extractUrl = "https://" + link.split('/')[2] + "/"
    with open(notAccurate, 'r') as file:
        notAccurateLinks = filter(lambda item: item == extractUrl, file.read().split('\n'))
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    
    try:
        req = requests.get(link, headers=headers)
    except Exception as err: 
        return 500
    else:
        if len(list(notAccurateLinks)) > 0:
            return 611
        else:
            return req.status_code

def checkName(n):
    i = 0
    content = ''
    with open(sitesJson, 'r') as file:
        content = file.read()
    
    jsonObj = json.loads(content)
    mappedUrl = list(map(lambda item: item + n, jsonObj["links"]))
    
    while i < len(mappedUrl):
        fetchStatus = fetchData(mappedUrl[i])
        if fetchStatus == 200:
            regex = chalk.green.bold('[!] ') + chalk.blue.bold(re.search('https://([^/.]+)', mappedUrl[i])[1].capitalize())
            print(f"{regex or '-'} {chalk.cyan(mappedUrl[i])}")
        elif fetchStatus == 403:
            regex = chalk.yellow('[!] ') + chalk.blue.bold(re.search('https://([^/.]+)', mappedUrl[i])[1].capitalize())
            print(f"{regex or '-'} {chalk.cyan(mappedUrl[i])}")
        elif fetchStatus == 611:
            regex = chalk.magenta('[!] ') + chalk.blue.bold(re.search('https://([^/.]+)', mappedUrl[i])[1].capitalize())
            print(f"{regex or '-'} {chalk.cyan(mappedUrl[i])}")
        else:
            regex = chalk.red.bold('[!] ') + chalk.blue.bold(re.search('https://([^/.]+)', mappedUrl[i])[1].capitalize())
            print(f"{regex or '-'} {chalk.cyan(mappedUrl[i])}")
        i+=1
    
    getName()


getName()