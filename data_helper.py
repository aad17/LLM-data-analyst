import pandas as pd
from validation_helper import QueryIntent, Entity, Metric, Aggregation, SortDirection, RequestStatus

ENTITY_COLUMN_MAP = {
    Entity.PRODUCT: "product",
    Entity.CUSTOMER: "customer"
}

METRIC_COLUMN_MAP = {
    Metric.ORDERS: "order_id",
    Metric.REVENUE: "revenue"
}

AGGREGATION_OP_MAP = {
    Aggregation.SUM: "sum",
    Aggregation.AVG: "mean",
    Aggregation.COUNT: "count"
}

def execute_query(df: pd.DataFrame, intent: QueryIntent) -> pd.DataFrame:
    if intent.status != RequestStatus.SUPPORTED:
        print(f"Execution Aborted [Status: {intent.status}]. Reason: {intent.reason}")
        return pd.DataFrame()
    
    if not intent.entity:
        print("Execution Aborted: SUPPORTED status requires a target entity.")
        return pd.DataFrame()

    entity = ENTITY_COLUMN_MAP.get(intent.entity)
    metric = METRIC_COLUMN_MAP.get(intent.metric)
    aggregation = AGGREGATION_OP_MAP.get(intent.aggregation)

    print(entity, metric, aggregation)

    if entity == "product" and metric == "revenue" and aggregation == "sum":
        aggregated_df = df.groupby("product")["revenue"].sum().reset_index()
        sort_by_column = "revenue"

    elif entity == "customer" and metric == "revenue" and aggregation == "sum":
        aggregated_df = df.groupby("customer")["revenue"].sum().reset_index()
        sort_by_column = "revenue"

    elif entity == "customer" and metric == "order_id" and aggregation == "count":
        # Counts the total number of transactions/order rows for each customer
        aggregated_df = df.groupby("customer")["order_id"].count().reset_index()
        aggregated_df.rename(columns={"order_id": "orders_count"}, inplace=True)
        sort_by_column = "orders_count"

    elif entity == "product" and metric == "revenue" and aggregation == "mean":
        aggregated_df = df.groupby("product")["revenue"].mean().reset_index()
        aggregated_df.rename(columns={"revenue": "revenue_avg"}, inplace=True)
        sort_by_column = "revenue_avg"

    else:
        raise ValueError(
            f"Execution Aborted: Combination ({entity} + {metric} + {aggregation}) is out of scope."
        )

    if intent.sort_direction:
        is_ascending = True if intent.sort_direction == SortDirection.ASC else False
        aggregated_df = aggregated_df.sort_values(by=sort_by_column, ascending=is_ascending)

    if intent.limit is not None:
        aggregated_df = aggregated_df.head(intent.limit)

    return aggregated_df.reset_index(drop=True)