import os
import asyncio
import requests
from autogen import AssistantAgent, UserProxyAgent

API_ENDPOINT = os.environ.get("API_ENDPOINT")
API_KEY = os.environ.get("API_KEY")

def is_valid_api_key(key):
 
  return key == "YOUR_REAL_API_KEY"  

async def query_legal_api(question):
    try:
        if not is_valid_api_key(API_KEY):
            raise ValueError("Invalid API key")

        if not API_ENDPOINT.startswith("http") or not ("/" in API_ENDPOINT):
            raise ValueError("Invalid legal information API URL format. Please provide a valid URL.")

        api_url = f"{API_ENDPOINT}?question={question}"

        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  
        data = response.json()
        
        return data.get("answer", "Sorry, couldn't find legal information related to your question.")
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Error accessing legal API: {e}")
        return "There seems to be a problem with the legal information service. Please try again later."

async def main():
    assistant = AssistantAgent(
        name="legal_assistant",
        llm_config={
            "name": "text-davinci-003",
            "temperature": 0.7,
            "max_tokens": 100,
            "stop": None,
            "capabilities": {"api_call": query_legal_api},
        },
    )

    user_proxy = UserProxyAgent(name="user")

    async def handle_user_query(query):
        answer = await assistant.call("api_call", query)
        await user_proxy.respond(answer)

    user_proxy.add_task(handle_user_query)

    await user_proxy.a_initiate_chat(assistant)


if __name__ == "__main__":
    asyncio.run(main())
