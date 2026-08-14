from dotenv import load_dotenv
from openai import OpenAI
from validation_helper import ClassificationResult

load_dotenv()

client = OpenAI()

messages = [
    'Which product generated the most revenue?',
    'How much revenue did we generate last month?',
    'Which customer placed the most orders?',
    "Which product category contributed most to last month's growth?",
    "Show me our best performers."
]

response = client.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": "Categorize this analytics question into \
                SALES: \
                overall revenue/sales questions where product or customer \
                is not the primary entity \
                PRODUCT: \
                questions where product, SKU, or product category is the \
                primary entity \
                CUSTOMER: \
                questions where customer or customer segment is the \
                primary entity"
            },
        {"role": "user", "content": "Which product generated the most revenue?"}
    ],
    response_format=ClassificationResult
)

# print(response)
# print(f'response:{response.choices[0].message.content}')

result = response.choices[0].message.parsed
print(result)
print(result.category)
print(type(result))
print(type(result.category))