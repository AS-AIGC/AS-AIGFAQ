#!/usr/bin/env python3

"""
這是一段 Python 程式碼，用於將 FAQ 資料進行多語言翻譯。
程式碼中使用了 pandas 套件來讀取和處理資料，並使用了 googletrans 
套件來進行翻譯。程式根據設定文件中的資訊進行多語言翻譯，
並將翻譯後的結果存儲在新的 CSV 文件中。

This is a Python code snippet for translating FAQ data 
into multiple languages. The code uses the pandas 
library to read and process the data, and the 
googletrans library for translation. The code performs 
multilingual translation based on the information 
provided in the configuration file and saves the 
translated results in new CSV files.
"""

import pandas as pd
from googletrans import Translator, LANGUAGES
import config

SOURCES = config.SOURCES
languages = config.LANGUAGES

translator = Translator()

# Loop through each source file
for name in SOURCES:
    print("Dealing with " + name)

    fname = "/home/ec2-user/OpenAI/AS-AIGFAQ/output/" + name
    faq_name = fname + '-QA.csv'

    # Read the FAQ data from the CSV file
    data = pd.read_csv(faq_name)
    data.dropna(inplace=True)
    data.reset_index(inplace=True)

    # Loop through each target language
    for lang in languages:
        try:
            translated_data = data.copy()
            vocabulary = {}

            # Translate each column in the FAQ data
            for col in data.columns:
                if col == 'index':
                    continue
                for row in range(len(data)):
                    original_text = data.loc[row, col]
                    if col in ['category', 'title', 'group', 'contact', 'url']:
                        if data.loc[row, col] not in vocabulary:
                            vocabulary[data.loc[row, col]] = translator.translate(original_text, dest=lang).text
                        translated_text = vocabulary[data.loc[row, col]]
                    else:
                        translated_text = translator.translate(original_text, dest=lang).text

                    translated_data.loc[row, col] = translated_text

            # Save the translated data to a new CSV file
            translated_data.to_csv(f"{fname}-QA_{lang}.csv", index=False)
        except Exception as e:
            print(f"Error ({name},{lang}): " + type(e).__name__)
