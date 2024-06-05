import os
from openai import OpenAI
from time import sleep


def clean_data_with_ai(url, data, rateLimit=20):
    # Instantiate the OpenAI client
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Define system message content
    system_message = os.getenv('AI_SYSTEM_MESSAGE')

    # Define user message content
    user_message = os.getenv('AI_USER_MESSAGE')
    user_message = user_message + "Page Content:\n\n" + data


    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "text" },
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    # Check if the response contains the expected data
    if response and response.choices:
        formatted_data = response.choices[0].message.content
        return url, formatted_data
    elif response and response.error:
        if response.error.code == "rate_limit_exceeded":
            print(f"Rate limit exceeded. Waiting {rateLimit} seconds before retrying.")
            sleep(rateLimit)
            url, formatted_data = clean_data_with_ai(url, data, rateLimit*2)
            return url, formatted_data
    else:
        raise ValueError("The OpenAI API response did not contain the expected choices data.")
    

def clean_data_test(url, page_data):
    sleep(4)
    clean = f"this is cleaned data for the page: {url}"
    return(url, clean)
