#!/usr/bin/env python3
import pandas as pd
from googletrans import Translator, LANGUAGES
import config

SOURCES = config.SOURCES
#languages = ['en', 'ja', 'ko', 'fr', 'de', 'it', 'es', 'id', 'vi', 'th', 'ru', 'uk']
languages = config.LANGUAGES

translator = Translator()


for name in SOURCES:
    print("Dealing with " + name)


    fname = "/home/ec2-user/OpenAI/AS-AIGFAQ/output/" + name
    faq_name = fname + '-QA.csv'

    data = pd.read_csv(faq_name)
    data.dropna(inplace=True)
    data.reset_index(inplace=True)


    for lang in languages:
        #try:
            translated_data = data.copy()
            vocabulary = {}

            for col in data.columns:
                if col=='index':
                    continue
                for row in range(len(data)):
                    original_text = data.loc[row, col]
                    if col in ['category','title','group','contact','url']:
                        if data.loc[row, col] not in vocabulary:
                            vocabulary[data.loc[row, col]] = translator.translate(original_text, dest=lang).text
                        translated_text = vocabulary[data.loc[row, col]]
                    else:
                        translated_text = translator.translate(original_text, dest=lang).text

                    translated_data.loc[row, col] = translated_text

            translated_data.to_csv(f"{fname}-QA_{lang}.csv", index=False)
        #except Exception as e:
        #    print(f"Error ({name},{lang}): " + type(e).__name__)
