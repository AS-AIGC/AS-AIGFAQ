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

import pandas as pd  # Import pandas for data manipulation
from googletrans import Translator, LANGUAGES  # Import the Google Translate API
import config  # Import configuration settings

SOURCES = config.SOURCES  # Retrieve the source files from the configuration
languages = config.LANGUAGES  # Retrieve the target languages from the configuration

translator = Translator()  # Create a translator object

# Loop through each source file
for name in SOURCES:
    print("[i18n] Dealing with " + name)  # Print the current file being processed

    fname = "./output/" + name  # Define the file name
    faq_name = fname + '-QA.csv'  # Define the output file name

    # Read the FAQ data
    data = pd.read_csv(faq_name)
    data.dropna(inplace=True)  # Remove any rows with missing data
    data.reset_index(inplace=True)  # Reset the DataFrame index

    # Loop through each target language
    for lang in languages:
        try:
            translated_data = data.copy()  # Create a copy of the data for translation
            vocabulary = {}  # Initialize a dictionary to store translated terms

            # Translate each column
            for col in data.columns:
                if col in ['index', 'url']:  # Skip certain columns
                    continue
                for row in range(len(data)):
                    original_text = data.loc[row, col]
                    if col in ['category', 'title', 'group', 'contact']:
                        # Translate using a vocabulary to avoid redundancy
                        if data.loc[row, col] not in vocabulary:
                            vocabulary[data.loc[row, col]] = translator.translate(original_text, dest=lang).text
                        translated_text = vocabulary[data.loc[row, col]]
                    else:
                        # Direct translation
                        translated_text = translator.translate(original_text, dest=lang).text

                    translated_data.loc[row, col] = translated_text  # Update the translated data

            # Save the translated data to a CSV file
            translated_data.to_csv(f"{fname}-QA_{lang}.csv", index=False)
        except Exception as e:
            # Print any errors encountered
            print(f"Error ({name},{lang}): " + type(e).__name__)
