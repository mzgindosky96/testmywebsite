import os
import sys
required_modules = [
    'random',
    "requests",
    "getuseragent"
]

for module in required_modules:
    try:
        exec(f"import {module}")
    except ImportError:
        os.system(f"pip install {module}")
        os.system('clear')
from getuseragent import UserAgent
ua = UserAgent("ios").Random()
user=input('[+] TikTok UserName : ')
link=input('[+] Video Link : ')
res=requests.post('https://api.likesjet.com/freeboost/3',json={"link":link,"tiktok_username":user,"email":f"fox{random.randint(100000,999999)}@gmail.com"},headers={"Host": "api.likesjet.com","content-length": "137","sec-ch-ua": "\"Google Chrome\";v\u003d\"119\", \"Chromium\";v\u003d\"119\", \"Not?A_Brand\";v\u003d\"24\"","accept": "application/json, text/plain, */*","content-type": "application/json","sec-ch-ua-mobile": "?1","user-agent":ua,"sec-ch-ua-platform": "\"Android\"","origin": "https://likesjet.com","sec-fetch-site": "same-site","sec-fetch-mode": "cors","sec-fetch-dest": "empty","referer": "https://likesjet.com/","accept-language": "en-XA,en;q\u003d0.9,ar-XB;q\u003d0.8,ar;q\u003d0.7,en-GB;q\u003d0.6,en-US;q\u003d0.5"}).json()
if res.get('message') == 'Success! You will receive views on your tiktok video within next few minutes.':
    print('done send')
elif res.get('errors'):
    print('user and link wrong')
elif res.get('message') == 'Please wait few minutes for boosting video views again.':
    remaining_seconds = res.get('remainingSeconds', 0)
    print(f'Try Again After {remaining_seconds} Seconds')
else:
    print(res)
