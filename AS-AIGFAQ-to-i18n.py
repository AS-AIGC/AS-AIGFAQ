#!/usr/bin/env python3
import pandas as pd
from googletrans import Translator, LANGUAGES
import config

SOURCES = config.SOURCES
languages = ['en', 'ja', 'ko', 'fr', 'id', 'vi', 'th']

translator = Translator()


for name in SOURCES:
    print("Dealing with " + name)


    fname = "/home/ec2-user/OpenAI/AS-AIGFAQ/examples/" + name
    faq_name = fname + '-QA.csv'

    data = pd.read_csv(faq_name)
    data.dropna(inplace=True)

    for lang in languages:
        try:
            translated_data = data.copy()

            for col in data.columns:
                for row in range(len(data)):
                    original_text = data.loc[row, col]
                    translated_text = translator.translate(original_text, dest=lang).text
                    translated_data.loc[row, col] = translated_text

            translated_data.to_csv(f"{fname}-QA-{lang}.csv", index=False)
        except Exception as e:
            print(f"Error ({name},{lang}): " + str(e))
