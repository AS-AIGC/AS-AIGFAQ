#!/usr/bin/env python3
import openai  # Import the OpenAI library for interacting with the GPT models
import pandas as pd  # Import pandas for data manipulation and analysis
import re  # Import the regular expression module for text manipulation
from datetime import datetime  # Import datetime for handling date and time data
import config  # Import a configuration module, usually for API keys or settings


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
        #rsp = openai.ChatCompletion.create(
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "一般大眾"},
                {"role": "user", "content": q}
            ]
        )

        # Return the answer content
        #return rsp.get("choices")[0]["message"]["content"]
        return completion.choices[0].message.content
    except Exception as e:
        # Return an empty string if there is an error
        print(e)
        return ""

def chatGPT_get_answers(row):
    try:
        # Create a question and answer text based on the provided description
        q = "請根據下列的文字說明，使用日常說話的語氣，並且避免使用語助詞來回答問題\n\n文字說明： \n\n"+row.context+"\n\n問題：\n\n"+row.question+"\n\n答案："
        
        # Request an answer from OpenAI using the GPT-4 model
        completion = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "中研院"},
                {"role": "user", "content": q}
            ]
        )
        
        # Return the generated answer with leading and trailing whitespaces removed
        return completion.choices[0].message.content.lstrip().rstrip()
    except Exception as e:
        # Return an empty string if there is an error
        print(e)
        return ""

for name in SOURCES:
    start_time = datetime.now()  # Start timing the process
    print("Dealing with " + name)  # Print the name of the current source being processed

    HTML_title = SOURCES[name]  # Get the HTML title for the current source

    fname = "./examples/" + name + '.csv'  # Define the file name for the source CSV
    faq_name = "./output/" + name + '-QA.csv'  # Define the file name for the output CSV

    df = pd.read_csv(fname)  # Read the source CSV file

    # Generate questions for each row in the DataFrame
    df['questions'] = df.apply(chatGPT_get_questions, axis=1)

    # Prepend '1.' to each question
    df['questions'] = "1." + df.questions

    # Create a new DataFrame to store the processed data
    df2 = pd.DataFrame(columns=['category', 'title', 'context', 'question', 'group', 'url', 'contact'])

    # Process each row in the original DataFrame
    for index, row in df.iterrows():
        questions = row['questions'].split("\n")  # Split the questions by new line
        for q in questions:
            if len(q) != 0:  # Check if the question is not empty
                q = re.sub("\d.", "", q, count=1).lstrip()  # Remove the question number
                # Create a new row with the processed data
                new_df = pd.DataFrame(data={'category': [row['category']], 'title': [row['title']], 'context': [row['context']], 'question': [q], 'group': [row['group']], 'url': [row['url']], 'contact': [row['contact']]})
                df2 = pd.concat([df2, new_df], axis=0, ignore_index=True)  # Add the new row to the new DataFrame

    # Generate answers for each row in the new DataFrame
    df2['answer'] = df2.apply(chatGPT_get_answers, axis=1)
    df2 = df2.drop(columns=['context'])  # Drop the context column
    df2.to_csv(faq_name, index=False)  # Save the new DataFrame to a CSV file

    end_time = datetime.now()  # End timing the process
    print('Duration: {}'.format(end_time - start_time))  # Print the duration of the process


