import os
from openai import OpenAI


def clean_data_with_ai(data):
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
        # response_format={ "type": "json_object" },
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
        # print(f"Formatted data received from API: {formatted_data}")
        return formatted_data
    else:
        raise ValueError("The OpenAI API response did not contain the expected choices data.")
    
