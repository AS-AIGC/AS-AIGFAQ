#!/usr/bin/env python3
import openai
import pandas as pd
import re
from datetime import datetime
import config

# Set the environment variable for OpenAI API key
#%env OPENAI_API_KEY=YOUR_OPENAI_API_KEY

# Set organization and API key for OpenAI
openai.organization = "YOUR_OPENAI_ORGANIZATION"
openai.organization = config.OpenAI_Organization
openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_key = config.OpenAI_Key

SOURCES = {
        ## name : HTML_title
        #'AS-ITS' : '中央研究院 資訊服務 FAQ',
        }
SOURCES = config.SOURCES


def chatGPT_get_questions(row):
    try:
        # Create a question based on the service item and service description
        q = "請根據以下的服務項目與服務說明，使用日常說話的語氣，提出以問號為結尾的問題\n\n服務項目：{"+row.title+"}\n\n服務說明：{"+row.context+"}\n\n問題：\n1."

        # Request an answer from OpenAI using the GPT-4 model
        rsp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "一般大眾"},
                {"role": "user", "content": q}
            ]
        )

        # Return the answer content
        return rsp.get("choices")[0]["message"]["content"]
    except:
        # Return an empty string if there is an error
        return ""

def chatGPT_get_answers(row):
    try:
        # Create a question based on the text description to answer the question
        q = "請根據下列的文字說明，使用日常說話的語氣，並且避免使用語助詞來回答問題\n\n文字說明： {"+row.context+"}\n\n問題：\n{"+row.question+"}\n\n答案："
        
        # Request an answer from OpenAI using the GPT-4 model
        rsp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "中研院"},
                {"role": "user", "content": q}
            ]
        )
        
        # Return the answer content with leading and trailing whitespaces removed
        return rsp.get("choices")[0]["message"]["content"].lstrip().rstrip()
    except:
        # Return an empty string if there is an error
        return ""


for name in SOURCES:
    start_time = datetime.now()
    print("Dealing with " + name)

    HTML_title = SOURCES[name]

    fname = "/home/ec2-user/OpenAI/AS-AIGFAQ/examples/" + name + '.csv'
    faq_name = "/home/ec2-user/OpenAI/AS-AIGFAQ/output/" + name + '-QA.csv'


    df = pd.read_csv(fname)

    #df.dropna(inplace = True)

    df['questions'] = df.apply(chatGPT_get_questions, axis=1)

    df['questions'] = "1." + df.questions

    df2 = pd.DataFrame(columns=['category', 'title', 'context', 'question','group','url','contact'])

    for index, row in df.iterrows():
        questions = row['questions'].split("\n")
        i = 1
        for q in questions:
            if len(q) != 0:
                q = re.sub("\d.", "", q, count=1).lstrip()
                new_df = pd.DataFrame(data={'category': [row['category']], 'title': [row['title']], 'context': [row['context']], 'question': [q], 'group': [row['group']], 'url': [row['url']], 'contact': [row['contact']]})
                df2 = pd.concat([df2, new_df], axis=0, ignore_index=True)
                i = i + 1

    df2['answer'] = df2.apply(chatGPT_get_answers, axis=1)
    df2['answer'] = df2.answer
    df2 = df2.drop(columns=['context'])
    df2 = df2.dropna().reset_index().drop('index', axis=1)
    df2.to_csv(faq_name, index=False)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

