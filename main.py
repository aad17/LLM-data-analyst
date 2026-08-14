from dotenv import load_dotenv
from openai import OpenAI
from validation_helper import QueryIntent

load_dotenv()

client = OpenAI()

messages = [
    "Show me the top 3 products by revenue.",
    "Which customer generated the most revenue?",
    "Show me customers by number of orders.",
    "What is the average revenue per product?",
    "Which supplier has the highest profit margin?"
]

for message in messages:
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are the data analyst and your task is to \
                    understand the user query and convert it into the schema \
                    specified."
                },
            {"role": "user", "content": message}
        ],
        response_format=QueryIntent
    )

    result = response.choices[0].message.parsed
    print(f'Message: {message}')
    print(f'Entity: {result.entity}')
    print(f'Metric: {result.metric}')
    print(f'Aggregation: {result.aggregation}')
    print(f'Sort Direction: {result.sort_direction}')
    print(f'Limit: {result.limit}')