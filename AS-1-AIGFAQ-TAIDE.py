#!/usr/bin/env python3

import os  # Used for interacting with the operating system
import requests  # For making HTTP requests to web servers
import pandas as pd  # Powerful data analysis and manipulation library
import re  # For regular expression matching operations
import time  # For time-related tasks
import config  # Importing custom configuration settings
from tqdm import tqdm  # For adding progress bars to loops
from datetime import datetime  # For handling dates and times


# Load host, username, and password from the config module
host = config.TAIDE_host
username = config.TAIDE_username
password = config.TAIDE_password

# Get authentication token by sending a POST request with the username and password
r = requests.post(host+"/token", data={"username":username, "password":password})
token = r.json()["access_token"]  # Extract the access token from the response

# Set up the authorization header with the obtained token
headers = {
    "Authorization": "Bearer "+token
}

# Initially define a SOURCES dictionary with name and HTML title mappings (for demonstration)
SOURCES = {
    # Example: 'AS-ITS' : '中央研究院 資訊服務 FAQ',
    'AS-iptt' : '中央研究院 智財技轉 FAQ',
}

# Load the actual SOURCES dictionary from the config module
SOURCES = config.SOURCES

# Initialize tqdm progress bar support for pandas operations
tqdm.pandas()



def TAIDE_get_questions(row):
    try:
        # Prepare the prompt by formatting with the service item and description from the input row
        question = "請根據以下的服務項目與服務說明，使用日常說話的語氣，提出以問號為結尾的問題\n\n服務項目：{"+row.title+"}\n\n服務說明：{"+row.context+"}\n\n問題：\n1."
        prompt_1 = f"[INST] {question} [/INST]"  # Format the prompt with markers for the model to interpret
        
        # Define the data payload for the POST request, including model settings
        data = {
            "model": "TAIDE/b.1.0.0",  # Specify the model version
            "prompt": prompt_1,  # The prepared prompt
            "temperature": 0.2,  # Low temperature for less randomness
            "top_p": 0.9,  # High top_p for more diverse outputs
            "presence_penalty": 1,  # Penalty for repeated content
            "frequency_penalty": 1,  # Penalty for frequent content
            "max_tokens": 100,  # Limit the output length
        }
        # Send the request to the TAIDE API with the specified headers and data
        r = requests.post(host+"/completions", json=data, headers=headers)
        # Extract the generated text from the response, trimming any leading or trailing spaces
        res = r.json()["choices"][0]["text"].lstrip().rstrip()
        
        # Wait for a short period to comply with rate limits or API guidelines
        time.sleep(6)
        
        # Return the processed result
        return res
    except Exception as e:
        # Catch any exceptions, print the error, and return an empty string to avoid crashing
        print(e)
        return ""


def TAIDE_get_answers(row):
    try:
        # Construct the prompt using the provided context and question from the input row
        question = "請根據下列的文字說明，使用日常說話的語氣，並且避免使用語助詞來回答問題\n\n文字說明： \n\n"+row.context+"\n\n問題：\n\n"+row.question+"\n\n答案："
        prompt_1 = f"[INST] {question} [/INST]"  # Format the prompt for the model
        
        # Define the data payload for the POST request, including model settings
        data = {
            "model": "TAIDE/b.1.0.0",  # Specify the model version
            "prompt": prompt_1,  # The prepared prompt
            "temperature": 0.2,  # Low temperature for less randomness
            "top_p": 0.9,  # High top_p for more diverse outputs
            "presence_penalty": 1,  # Penalty for repeated content
            "frequency_penalty": 1,  # Penalty for frequent content
            "max_tokens": 100,  # Limit the output length
        }
        # Send the request to the TAIDE API with the specified headers and data
        r = requests.post(host+"/completions", json=data, headers=headers)
        # Extract the generated answer from the response, trimming any leading or trailing spaces
        res = r.json()["choices"][0]["text"].lstrip().rstrip()
        
        # Wait for a short period to comply with rate limits or API guidelines
        time.sleep(6)
        
        # Return the processed answer
        return res
    except Exception as e:
        # Catch any exceptions, print the error, and return an empty string to avoid crashing
        print(e)
        return ""

# Loop through each source in the SOURCES dictionary
for name in SOURCES:
    # Record the start time of processing this source
    start_time = datetime.now()
    print("Dealing with " + name)  # Print the name of the current source being processed

    # Get the HTML title associated with the current source
    HTML_title = SOURCES[name]

    # Define filenames for reading the source CSV and saving the QA CSV
    fname = './' + name + '.csv'  # Original data file
    faq_name = './' + name + '-QA-TAIDE.csv'  # File to save questions and answers

    # Read the source CSV into a pandas DataFrame
    df = pd.read_csv(fname)

    print("\tgenerating questions...")

    # Generate questions for each row in the DataFrame using TAIDE_get_questions function
    # and using progress_apply to show progress bar
    df['questions'] = df.progress_apply(TAIDE_get_questions, axis=1)

    # Prefix each question with "1." to number them
    df['questions'] = "1." + df.questions

    # Create a new DataFrame to store the QA pairs with additional info
    df2 = pd.DataFrame(columns=['category', 'title', 'context', 'question', 'group', 'url', 'contact'])

    # Split the questions by newline and populate the new DataFrame
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        questions = row['questions'].split("\n")
        for q in questions:
            if len(q) != 0:
                # Remove the leading number and space from each question
                q = re.sub("\d.", "", q, count=1).lstrip()
                # Create a new row for the QA DataFrame
                new_df = pd.DataFrame(data={'category': [row['category']], 'title': [row['title']], 'context': [row['context']], 'question': [q], 'group': [row['group']], 'url': [row['url']], 'contact': [row['contact']]})
                # Append the new row to the QA DataFrame
                df2 = pd.concat([df2, new_df], axis=0, ignore_index=True)

    print("\tgenerating answers...")
    # Generate answers for each question in the QA DataFrame using TAIDE_get_answers function
    df2['answer'] = df2.progress_apply(TAIDE_get_answers, axis=1)
    
    # Drop the 'context' column from the QA DataFrame
    df2 = df2.drop(columns=['context'])
    # Save the QA DataFrame to a CSV file
    df2.to_csv(faq_name, index=False)

    # Record the end time of processing and print the duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

