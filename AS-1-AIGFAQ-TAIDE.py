#!/usr/bin/env python3

import os
import requests
import pandas as pd
import re
import time
import config
from tqdm import tqdm
from datetime import datetime

host = config.TAIDE_host
username = config.TAIDE_username
password = config.TAIDE_password

#get token
r = requests.post(host+"/token", data={"username":username, "password":password})
token = r.json()["access_token"]


headers = {
	"Authorization": "Bearer "+token
}

SOURCES = {
        ## name : HTML_title
        #'AS-ITS' : '中央研究院 資訊服務 FAQ',
        'AS-iptt' : '中央研究院 智財技轉 FAQ',
        }

SOURCES = config.SOURCES
tqdm.pandas()

def TAIDE_get_questions(row):
    try:
        #question = "你剛剛參加了一場關於環保的公共演講,感受良多,希望能寫一封信給演講者表示感謝。請根據你的感受和收穫,寫出一封感謝信的內容。"
        question = "請根據以下的服務項目與服務說明，使用日常說話的語氣，提出以問號為結尾的問題\n\n服務項目：{"+row.title+"}\n\n服務說明：{"+row.context+"}\n\n問題：\n1."
        prompt_1 = f"[INST] {question} [/INST]"
        data = {
            "model": "TAIDE/b.1.0.0",
            "prompt": prompt_1,
            "temperature": 0.2,
            "top_p": 0.9,
            "presence_penalty": 1,
            "frequency_penalty": 1,
            "max_tokens": 100,
        }
        r = requests.post(host+"/completions", json=data, headers=headers)
        res = r.json()["choices"][0]["text"].lstrip().rstrip()
        time.sleep(6)
        return res
    except Exception as e:
        # Return an empty string if there is an error
        print(e)
        return ""

def TAIDE_get_answers(row):
    try:
        #question = "你剛剛參加了一場關於環保的公共演講,感受良多,希望能寫一封信給演講者表示感謝。請根據你的感受和收穫,寫出一封感謝信的內容。"
        question = "請根據下列的文字說明，使用日常說話的語氣，並且避免使用語助詞來回答問題\n\n文字說明： \n\n"+row.context+"\n\n問題：\n\n"+row.question+"\n\n答案："
        prompt_1 = f"[INST] {question} [/INST]"
        data = {
            "model": "TAIDE/b.1.0.0",
            "prompt": prompt_1,
            "temperature": 0.2,
            "top_p": 0.9,
            "presence_penalty": 1,
            "frequency_penalty": 1,
            "max_tokens": 100,
        }
        r = requests.post(host+"/completions", json=data, headers=headers)
        res = r.json()["choices"][0]["text"].lstrip().rstrip()
        time.sleep(6)
        return res
    except Exception as e:
        # Return an empty string if there is an error
        print(e)
        return ""

for name in SOURCES:
    start_time = datetime.now()
    print("Dealing with " + name)

    HTML_title = SOURCES[name]

    fname =  './' + name + '.csv'
    faq_name =  './' + name + '-QA-TAIDE.csv'


    df = pd.read_csv(fname)

    print("\tgenerating questions...")

    #df['questions'] = df.apply(chatGPT_get_questions, axis=1)
    df['questions'] = df.progress_apply(TAIDE_get_questions, axis=1)

    df['questions'] = "1." + df.questions


    df2 = pd.DataFrame(columns=['category', 'title', 'context', 'question','group','url','contact'])

    for index, row in tqdm(df.iterrows()):
        questions = row['questions'].split("\n")
        i = 1
        for q in questions:
            if len(q) != 0:
                q = re.sub("\d.", "", q, count=1).lstrip()
                new_df = pd.DataFrame(data={'category': [row['category']], 'title': [row['title']], 'context': [row['context']], 'question': [q], 'group': [row['group']], 'url': [row['url']], 'contact': [row['contact']]})
                df2 = pd.concat([df2, new_df], axis=0, ignore_index=True)
                i = i + 1
    print("\tgenerating answers...")
    df2['answer'] = df2.progress_apply(TAIDE_get_answers, axis=1)
    
    df2 = df2.drop(columns=['context'])
    df2.to_csv(faq_name, index=False)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
