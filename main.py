from dotenv import load_dotenv
from openai import OpenAI
from validation_helper import QueryIntent, RequestStatus
from response_helper import user_response
from data_helper import execute_query
import pandas as pd

load_dotenv()

client = OpenAI()

DATA = pd.read_csv("data/sales.csv")

SYSTEM_PROMPT = """
You are an advanced Natural Language to SQL/API router. Your sole job is to analyze user requests and translate them into a structured query intent configuration.

### CORE CLASSIFICATIONS
Evaluate every incoming request against these three statuses:
1. SUPPORTED: The request can be fully answered using the exact Entities and Metrics tracked by this application.
2. UNSUPPORTED: The request explicitly asks for data, metrics, domains, or entities that are outside the scope of this application.
3. AMBIGUOUS: The request is a greeting, gibberish, completely lacking context, or missing critical clarity needed to identify a intent.

### APPLICATION METADATA & SCOPE
Our application strictly and exclusively supports the following data points:
- Entities: PRODUCT, CUSTOMER
- Metrics: REVENUE, ORDERS

### FIELD GENERATION RULES
- If status is SUPPORTED: Populate all applicable query fields (`entity`, `metric`, `aggregation`, etc.) based on the user's text. Leave optional fields null if the user did not specify them. Do not guess defaults.
- If status is UNSUPPORTED or AMBIGUOUS: You MUST leave all query execution fields (`entity`, `metric`, `aggregation`, `sort_direction`, `limit`) as null. Do not invent values or try to force-fit the request.

### REASON FIELD RULES
- For SUPPORTED requests: Keep the `reason` brief, summarizing what data is being fetched.
- For UNSUPPORTED or AMBIGUOUS requests: Provide a concise, helpful, and polite human-readable explanation explaining exactly why the request cannot be processed or what data is natively supported.
"""

queries = [
    "Show me the top 3 products by revenue.",
    # "Which customer generated the most revenue?",
    # "Show me customers by number of orders.",
    "What is the average revenue per product?",
    # "Which supplier has the highest profit margin?",
]

for message in queries:
    response = client.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": SYSTEM_PROMPT
                },
            {"role": "user", "content": message}
        ],
        response_format=QueryIntent
    )

    result = response.choices[0].message.parsed
    print(message)

    if result.status == RequestStatus.SUPPORTED:
        try:
            print("Route: EXECUTE")
            data = execute_query(DATA, result)
            print(f"Data Result: {data}")
            response = user_response(data, message)
            print(f"Final Answer: {response}")
        except ValueError as e:
            print(f"Caught expected failure {e}")
    elif result.status == RequestStatus.UNSUPPORTED:
        print("Route: REJECT")
        print(f"Reason: {result.reason}")
    else:
        print("Route: CLARIFY")
        print(f"Reason: {result.reason}")
