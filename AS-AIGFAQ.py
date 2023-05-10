import openai
import pandas as pd
import re
from datetime import datetime
import config

# Set the environment variable for OpenAI API key
#%env OPENAI_API_KEY=YOUR_OPENAI_API_KEY

# Set organization and API key for OpenAI
openai.organization = ""
openai.api_key = "YOUR_OPENAI_API_KEY"
openai.api_key = config.OpenAI_Key

SOURCES = {
        # fname : HTML_title
        'AS-ITS' : '中央研究院 資訊服務 FAQ',
        'AS-general' : '中央研究院 總務相關 FAQ',
        'AS-proposal' : '中央研究院 學術相關 FAQ',
        'AS-dgbas' : '中央研究院 經費核銷 FAQ',
        }



def chatGPT_get_questions(row):
    try:
        # Create a question based on the service item and service description
        q = "請根據以下的服務項目與服務說明，使用日常說話的語氣，提出以問號為結尾，並且清楚說明服務項目的問題\n\n服務項目：{"+row.title+"}\n\n服務說明：{"+row.context+"}\n\n問題：\n1."

        # Request an answer from OpenAI using the GPT-4 model
        rsp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "使用者"},
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
        q = "請根據下列的文字說明，以日常說話的語氣來回答問題\n\n文字說明： {"+row.context+"}\n\n問題：\n{"+row.question+"}\n\n答案："
        
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


for fname in SOURCES:
    start_time = datetime.now()
    print("Dealing with " + fname)

    HTML_title = SOURCES[fname]

    fname = "examples/" + fname
    faq_name = fname + '-QA.csv'
    df = pd.read_csv(fname + ".csv")

    #df.dropna(inplace = True)

    df['questions'] = df.apply(chatGPT_get_questions, axis=1)

    df['questions'] = "1." + df.questions

    df2 = pd.DataFrame(columns=['category', 'title', 'context', 'question'])

    for index, row in df.iterrows():
        questions = row['questions'].split("\n")
        i = 1
        for q in questions:
            if len(q) != 0:
                q = re.sub("\d.", "", q, count=1).lstrip()
                new_df = pd.DataFrame(data={'category': [row['category']], 'title': [row['title']], 'context': [row['context']], 'question': [q]})
                df2 = pd.concat([df2, new_df], axis=0, ignore_index=True)
                i = i + 1

    df2['answer'] = df2.apply(chatGPT_get_answers, axis=1)
    df2['answer'] = df2.answer
    df2 = df2.dropna().reset_index().drop('index', axis=1)
    df2.to_csv(faq_name, index=False)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

    df = pd.read_csv(faq_name)
    df.dropna(inplace=True)

    FAQ = {}
    for index, row in df.iterrows():
        if row.category not in FAQ:
            FAQ[row.category] = {}
        FAQ[row.category]["["+row.title+"] " +row.question] = row.answer

    html = '<html><head>'
    html += '<meta charset="utf-8"><script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>'
    html += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">'
    html += '<link rel="stylesheet" href="FAQ.css">'
    html += '<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.bundle.min.js"></script>'
    html += '</head><body>'

    html += '<div class="container">'
    html += '<center><h1>' + HTML_title + '</h1><p></center>'

    html += '<div class="accordion_one"><div id="accordion">'
    num = 1
    for category in FAQ:
        html += '<div class="card">'
        if num==1:
            html += '<div class="card-header" id="heading-'+str(num)+'"><h5 class="mb-0"><button class="btn btn-link" data-toggle="collapse" data-target="#collapse-'+str(num)+'" aria-expanded="true" aria-controls="collapse-'+str(num)+'">'
        else:
            html += '<div class="card-header" id="heading-'+str(num)+'"><h5 class="mb-0"><button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapse-'+str(num)+'" aria-expanded="false" aria-controls="collapse-'+str(num)+'">'
        html += "<h2>" + category + "</h2>"
        html += '</button></h5>'
        html += '</div>'
        if num==1:
            html += '<div id="collapse-'+str(num)+'" class="collapse show" aria-labelledby="heading-'+str(num)+'" data-parent="#accordion">'
        else:
            html += '<div id="collapse-'+str(num)+'" class="collapse" aria-labelledby="heading-'+str(num)+'" data-parent="#accordion">'
        html += '<div class="card-body">'

        html += '<div class="panel-group" id="accordionFourLeft">'
        for question in FAQ[category]:
            html += '<div class="panel panel-default"><div class="panel-heading"><h4 class="panel-title"><a data-toggle="collapse" data-parent="#accordion_oneLeft" href="#collapseFiveLeft-'+str(num)+'" aria-expanded="false" class="collapsed">'
            html += question
            html += '</a></h4></div><div id="collapseFiveLeft-'+str(num)+'" class="panel-collapse collapse" aria-expanded="false" role="tablist" style="height: 0px;"><div class="panel-body"><div class="text-accordion"><p>'
            html += FAQ[category][question]
            html += '</p></div></div></div></div>'
            num = num + 1
            html += '</div>'

            html += '</div></div></div>'
    html += '</div></div>'
    html += '</div>'
    html += '</body></html>'

    with open(faq_name + '.html', 'w') as writefile:
        writefile.write(html)
        writefile.close()


