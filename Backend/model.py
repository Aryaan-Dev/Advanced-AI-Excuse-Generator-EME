import cohere
from rich import print
from dotenv import dotenv_values

env_vars = dotenv_values('.env')

CohereAPIKey = env_vars.get('CohereAPIKey')

co = cohere.Client(api_key = CohereAPIKey)

funcs = [
    'exit', 'general',
    'realtime','generate image','content','reminder'
]

messages = []

preamble = """
You are a very accurate Decision-Making Model, which decides what kind of a query is given to you.
You will decide whether a query is a 'general' query, a 'realtime' query, or is asking to perform any task , 'can you write a application'
*** Do not answer any query, just decide what kind of query is given to you. ***
-> Respond with 'general ( query )' if a query can be answered by a llm model (conversational ai chatbot) and doesn't require any up to date information like if the query is 'who was akbar?' respond with 'general who was akbar?', if the query is 'how can i study more effectively?' respond with 'general how can i study more effectively?', if the query is 'can you help me with this math problem?' respond with 'general can you help me with this math problem?', if the query is 'Thanks, i really liked it.' respond with 'general thanks, i really liked it.' , if the query is 'what is python programming language?' respond with 'general what is python programming language?', etc. Respond with 'general (query)' if a query doesn't have a proper noun or is incomplete like if the query is 'who is he?' respond with 'general who is he?', if the query is 'what's his networth?' respond with 'general what's his networth?', if the query is 'tell me more about him.' respond with 'general tell me more about him.', and so on even if it require up-to-date information to answer. Respond with 'general (query)' if the query is asking about time, day, date, month, year, etc like if the query is 'what's the time?' respond with 'general what's the time?'.
-> Respond with 'realtime ( query )' if a query can not be answered by a llm model (because they don't have realtime data) and requires up to date information like if the query is 'who is indian prime minister' respond with 'realtime who is indian prime minister', if the query is 'tell me about facebook's recent update.' respond with 'realtime tell me about facebook's recent update.', if the query is 'tell me news about coronavirus.' respond with 'realtime tell me news about coronavirus.', etc and if the query is asking about any individual or thing like if the query is 'who is akshay kumar' respond with 'realtime who is akshay kumar', if the query is 'what is today's news?' respond with 'realtime what is today's news?', if the query is 'what is today's headline?' respond with 'realtime what is today's headline?', etc.
-> Respond with 'close (application name)' if a query is asking to close any application like 'close notepad', 'close facebook', etc. but if the query is asking to close multiple applications or websites, respond with 'close 1st application name, close 2nd application name' and so on.
-> Respond with 'generate image (image prompt)' if a query is requesting to generate a image with given prompt like 'generate image of a lion', 'generate image of a cat', etc. but if the query is asking to generate multiple images, respond with 'generate image 1st image prompt, generate image 2nd image prompt' and so on.
-> Respond with 'reminder (datetime with message)' if a query is requesting to set a reminder like 'set a reminder at 9:00pm on 25th june for my business meeting.' respond with 'reminder 9:00pm 25th june business meeting'.
-> Respond with 'content (topic)' if a query is asking to write any type of content like application, codes, emails or anything else about a specific topic but if the query is asking to write multiple types of content, respond with 'content 1st topic, content 2nd topic' and so on.

*** If the user is saying goodbye or wants to end the conversation like 'bye EME' respond with 'exit'.***
*** Respond with 'general (query)' if you can't decide the kind of query or if a query is asking to perform a task which is not mentioned above. ***
"""

ChatHistory = [
    {'role' : 'User', 'message': 'how are you?'},
    {'role' : 'Chatbot', 'message': 'general how are you?'},
    {'role' : 'user', 'message': 'do you like pizza?'},
    {'role' : 'chatbot', 'message': 'general do you like pizza?'},
    {'role' : 'user', 'message': 'open chrome and tell me about mahatma gandhi.'},
    {'role' : 'chatbot', 'message': 'open chrome, general tell me about mahatma gandhi.'},
    {'role' : 'user', 'message': "what is today's date"},
    {'role' : 'chatbot', 'message': "general what is today's date"},
    {'role' : 'user', 'message': "chat with me."},
    {'role' : 'chatbot', 'message': "general chat with me."}
]

def FirstlayerDMM(prompt: str = "test"):
    messages.append({'role': 'user', 'content': f'{prompt}'})

    stream = co.chat_stream(
        model = 'command-r-plus',
        message = prompt,
        temperature = 0.7,
        chat_history = ChatHistory,
        prompt_truncation = 'OFF',
        connectors = [],
        preamble = preamble
    )

    response = ""

    for event in stream:
        if event.event_type == 'text-generation':
            response += event.text

    response = response.replace('\n','')
    response = response.split(',')

    response = [i.strip() for i in response]

    temp = []

    for task in response:
        for func in funcs:
            if task.startswith(func):
                temp.append(task)
    
    response = temp

    if '(query)' in response:
        newresponse = FirstlayerDMM(prompt=prompt)
        return newresponse
    else:
        return response

if __name__ == '__main__':
    while True:
        print(FirstlayerDMM(input('>>> ')))
