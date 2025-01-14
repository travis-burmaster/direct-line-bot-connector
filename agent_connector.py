import requests, time, os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Direct Line Secret from Azure Portal (Channel -> Direct Line)
DIRECT_LINE_SECRET = os.getenv('DIRECT_LINE_SECRET')
DIRECT_LINE_ENDPOINT = "https://directline.botframework.com/v3/directline/conversations"

direct_line_api_url = "https://directline.botframework.com/v3/directline/tokens/generate"
bot_id = os.getenv('BotIdentifier') 

# Request the token
header = {
    "Authorization": f"Bearer {DIRECT_LINE_SECRET}"
}

response = requests.post(direct_line_api_url, headers=header)

if response.status_code == 200:
    direct_line_token = response.json()["token"]
    print("Direct Line Token:", direct_line_token)
else:
    print("Error generating Direct Line token:", response.status_code)

#print("Direct Line Token:", direct_line_token)

# Function to start a new conversation
def start_conversation():
    headers = {
        "Authorization": f"Bearer {direct_line_token}"
    }

    payload = {
    "bot": {
        "id": bot_id
    }
    }

    response = requests.post(DIRECT_LINE_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code == 201:
        conversation = response.json()
        print("Conversation started:", conversation)
        return conversation["conversationId"]
    else:
        print("Failed to start conversation:", response.status_code, response.text)
        return None

# Function to send a message to the agent
def send_message(conversation_id, message_text):
    url = f"{DIRECT_LINE_ENDPOINT}/{conversation_id}/activities"
    headers = {
        "Authorization": f"Bearer {direct_line_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "message",
        "from": {"id": "user17609"},
        "text": message_text,
        "locale": "en-US",
        "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.oauth",
                    "content": {
                        "text": "To continue, please sign in.",
                        "connectionName": "my-oauth-connection",
                        "tokenExchangeResource": {
                            "uri": "https://token.botframework.com/api/oauth/signin?signin=user17609"
                        }
                    }
                }
        ]
    }
    print("url", url)

    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        #sign_in_link = response["activities"][0]["attachments"][0]["content"]["tokenExchangeResource"]["uri"]
        #print("sign_in_link", sign_in_link)
        print("Message sent:", response.json())
    else:
        print("Failed to send message:", response.status_code, response.text)


    # User's authentication token (e.g., from Azure AD after login)
    user_token = os.getenv('USER_TOKEN')

    # API endpoint to send the token to the bot
    send_token_url = f"https://directline.botframework.com/v3/directline/conversations/{conversation_id}/activities"

    # Construct the message with the token
    message_data = {
        "type": "event",
        "name": "tokens/response",
        "value": {"token": user_token},
        "from": {"id": "user17609"}
    }

    # Send the token to the bot
    headers = {
        "Authorization": f"Bearer {direct_line_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(send_token_url, headers=headers, json=message_data)

    if response.status_code == 200:
        print("Token sent successfully!")
    else:
        print("Error sending token:", response.status_code, response.text)


# Function to get responses from the agent
def get_responses(conversation_id):
    url = f"{DIRECT_LINE_ENDPOINT}/{conversation_id}/activities"
    headers = {
        "Authorization": f"Bearer {direct_line_token}"
    }
    try:
        time.sleep(10)
        response = requests.get(url, headers=headers, timeout=120)  # Increased timeout to 120 seconds
        if response.status_code == 200:
            activities = response.json()["activities"]
            #print("response:", response.json())
            activities = response.json().get("activities", [])
            for activity in activities:
                if activity.get("type") == "event" and activity.get("name") == "tokens/response":
                    user_token = activity.get("value", {}).get("token")
   
            # Get MarkdownContent
            markdown_content = extract_markdown_content(response.json())
            if markdown_content:
                print("Got a response!")
            else:
                print("MarkdownContent not found.")

            return markdown_content
        else:
            print("Failed to get responses:", response.status_code, response.text)
            return None
    except requests.exceptions.Timeout:
        print("The request timed out. Try again later.")
        return None

# Extract MarkdownContent
def extract_markdown_content(data):
    for activity in data.get("activities", []):
        if activity.get("type") == "event" and activity.get("valueType") == "DynamicPlanStepFinished":
            observation = activity.get("value", {}).get("observation", {})
            search_result = observation.get("search_result", {})
            text = search_result.get("Text", {})
            markdown_content = text.get("MarkdownContent")
            if markdown_content:
                return markdown_content
    return None

# Main function to interact with the agent
def main():
    conversation_id = start_conversation()
    if conversation_id:
        send_message(conversation_id, "what information do you have on Co-pilot studio agents?")
        response = get_responses(conversation_id)
        print("Agent:", response)

if __name__ == "__main__":
    main()
