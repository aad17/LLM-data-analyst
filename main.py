from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

messages = [
    'Which product generated the most revenue?',
    'How much revenue did we generate last month?',
    'Which customer placed the most orders?',
    "Which product category contributed most to last month's growth?",
    "Show me our best performers."
]

exp_a, exp_b, exp_c = 0, 0, 0

for message in messages:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Categorize this analytics question:"},
            {"role": "user", "content": message}
        ]
    )

    print(f'EXP A message: {message}')
    print(f'EXP A response:{response.choices[0].message.content}')
    exp_a += response.usage.total_tokens

    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Categorize this analytics question. Return exactly one of SALES, PRODUCT, CUSTOMER"},
                {"role": "user", "content": message}
            ]
        )

    print(f'EXP B message: {message}')
    print(f'EXP B response:{response.choices[0].message.content}')
    exp_b += response.usage.total_tokens

    response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "Categorize this analytics question. \
                        Return exactly one of SALES, PRODUCT, CUSTOMER \
                        for example \
                        How much revenue did we generate? \
                        → SALES \
                        Which SKU sold the most units? \
                        → PRODUCT \
                        Which customer spent the most? \
                        → CUSTOMER"
                },
                {"role": "user", "content": message}
            ]
        )

    print(f'EXP C message: {message}')
    print(f'EXP C response:{response.choices[0].message.content}')
    exp_c += response.usage.total_tokens

print(f'EXP A total tokens: {exp_a}')
print(f'EXP B total tokens: {exp_b}')
print(f'EXP C total tokens: {exp_c}')
