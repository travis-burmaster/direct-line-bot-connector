# Direct Line Azure Co-Pilot Agent API 
A Python-based connector for interacting with Azure Co-Pilot Agent through the Direct Line API, featuring OAuth authentication support and response handling.
This connector can be integrated with AutoGen or Langgraph.
## Features
- Direct Line token generation
- Conversation management
- OAuth authentication flow
- Message sending and receiving
- Markdown content extraction from bot responses
## Prerequisites
- Python 3.6+
- Azure Bot Service account
- Direct Line channel enabled in your bot
- OAuth configuration (if using authentication)
## Setup Instructions
### 1. Create and Activate Virtual Environment
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
### 2. Install Dependencies
```bash
pip install -r requirements.txt
```
### 3. Configure Environment Variables
Create a `.env` file in the project root with your credentials:
```dotenv
DIRECT_LINE_SECRET=your_direct_line_secret_from_azure_portal
BotIdentifier=your_bot_id
USER_TOKEN=your_oauth_user_token
AppClientId=your_azure_ad_app_client_id
TenantId=your_azure_ad_tenant_id
```
### 4. Token Generation Utility (get_token.py)
The project includes a Streamlit-based utility for generating OAuth tokens:
```bash
streamlit run get_token.py
```
This utility will:
- Provide a login button that redirects to Microsoft's authentication page
- Allow you to paste the redirect URL after successful login
- Generate and display your access token
- Handle the complete OAuth2 flow using MSAL (Microsoft Authentication Library)
Key features of get_token.py:
- Streamlit-based user interface
- MSAL integration for secure authentication
- Automatic token acquisition and display
- Support for custom tenant and client configurations
## Usage
1. Activate your virtual environment (if not already activated)
2. Run the script:
```bash
python agent_connector.py
```
The script will:
- Generate a Direct Line token
- Start a new conversation
- Send your test message
- Process authentication
- Display bot responses
## Script Structure
`bot_connector.py` contains several key functions:
- `start_conversation()`: Initiates a new bot conversation
- `send_message()`: Sends messages to the bot with OAuth attachments
- `get_responses()`: Retrieves and processes bot responses
- `extract_markdown_content()`: Parses markdown content from responses
## Development Notes
- Timeout is set to 120 seconds for response handling
- OAuth flow is implemented with token exchange
- Markdown content is automatically extracted from responses
- Error handling is implemented for API calls
## Error Handling
The script includes error handling for:
- Token generation failures
- Connection timeouts
- Message sending failures
- Response parsing errors
## Troubleshooting
Common issues:
1. Token generation fails: Check your DIRECT_LINE_SECRET
2. Authentication errors: Verify USER_TOKEN is valid
3. Timeout errors: Check network connection and bot response time
4. OAuth errors: Ensure AppClientId and TenantId are correctly configured in .env file
