#!/usr/bin/env python3
import pandas as pd
import config

SOURCES = {
        ## fname : HTML_title
        #'AS-ITS' : '中央研究院 資訊服務 FAQ',
        }

SOURCES = config.SOURCES


for fname in SOURCES:
    print("Dealing with " + fname)

    HTML_title = SOURCES[fname]

    fname = "/home/ec2-user/OpenAI/AS-AIGFAQ/output/" + fname
    faq_name = fname + '-QA.csv'
    html_name = fname + '-QA.html'

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

        html += '</div></div></div></div>'
    html += '</div></div>'
    html += '</div>'
    html += '</body></html>'

    with open(html_name, 'w') as writefile:
        writefile.write(html)
        writefile.close()


