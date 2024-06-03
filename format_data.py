import json
import os
from openai import OpenAI
import pandas as pd




def save_formatted_data(organized_data, sitename, timestamp, formatted_data, output_folder='output'):
    
    # Ensure the output folder exists
    root_output_folder = os.path.join(output_folder, sitename, timestamp)
    os.makedirs(output_folder, exist_ok=True)
    output_folder = os.path.join(root_output_folder,'processed_data')
    os.makedirs(output_folder, exist_ok=True)

    # Check if data is a dictionary and contains exactly one key
    if isinstance(organized_data, dict) and len(organized_data) == 1:
        key = next(iter(organized_data))  # Get the single key
        organized_data = organized_data[key]

    
    # Convert the formatted data to a pandas DataFrame
    df = pd.DataFrame(organized_data)

    # Convert the formatted data to a pandas DataFrame
    if isinstance(organized_data, dict):
        organized_data = [organized_data]

    df = pd.DataFrame(organized_data)

    # Save the DataFrame to an Excel file
    excel_output_path = os.path.join(output_folder, f'sorted_data_{timestamp}.xlsx')
    df.to_excel(excel_output_path, index=False)
    print(f"Formatted data saved to Excel at {excel_output_path}")


def format_data(data):
    # Instantiate the OpenAI client
    print("API Key: ", os.getenv('OPENAI_API_KEY'))
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    # Assign default fields if not provided
    # if fields is None:
    # fields = ["Address", "Real Estate Agency", "Price", "Beds", "Baths", "Sqft", "Home Type", "Listing Age", "Picture of home URL", "Listing URL"]

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
        print(f"Formatted data received from API: {formatted_data}")

        # try:
        #     parsed_json = json.loads(formatted_data)
        # except json.JSONDecodeError as e:
        #     print(f"JSON decoding error: {e}")
        #     print(f"Formatted data that caused the error: {formatted_data}")
        #     raise ValueError("The formatted data could not be decoded into JSON.")

        return formatted_data
    else:
        raise ValueError("The OpenAI API response did not contain the expected choices data.")
    

    # # Check if the response contains the expected data
    # if response and response.choices:
    #     formatted_data = response.choices[0].message.content.strip()
    #     print(f"Formatted data received from API: {formatted_data}")

    #     try:
    #         parsed_json = json.loads(formatted_data)
    #     except json.JSONDecodeError as e:
    #         print(f"JSON decoding error: {e}")
    #         print(f"Formatted data that caused the error: {formatted_data}")
    #         raise ValueError("The formatted data could not be decoded into JSON.")

    #     return parsed_json
    # else:
    #     raise ValueError("The OpenAI API response did not contain the expected choices data.")
    
