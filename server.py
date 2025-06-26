# ===== server.py =====
import logging
import os

import requests
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    filename="mcp_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
from dotenv import load_dotenv

load_dotenv()
mcp = FastMCP(
    name="Dashboard"
)

SALES_API_URL = "https://s1-account-api.dev.kwickmetrics.com/api/v1/account/mallow-int-test/reports/dashboard/details"
RETURN_API_URL = "https://s1-account-api.dev.kwickmetrics.com/api/v2/account/mallow-int-test/reports/dashboard/returns/details"


# Load auth values from environment
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
AUTH_TENANT = os.environ.get("AUTH_TENANT")

# Allowed purchase_date values
VALID_PURCHASE_DATES = {
    "today": "Today (TD)",
    "yesterday": "Yesterday (YD)",
    "last_seven_days": "Last 7 Days (7D)",
    "last_thirty_days": "Last 30 Days (30D)",
    "this_week": "This Week (TW)",
    "last_week": "Last Week (LW)",
    "this_month": "This Month (TM)",
    "last_month": "Last Month (LM)",
    "last_6_months": "Last 6 Months (6M)",
    "last_12_months": "Last 12 Months (12M)",
    "this_year": "Year To Date (YTD)",
    "last_year": "Last Year (LYR)",
    "custom": "Custom Range",
}


@mcp.tool()
def sales_overview(
    purchase_date: str = "last_year",
    currency: str = "USD",
    is_walmart: bool = False,
    date_from: str = None,
    date_to: str = None,
):
    """
    Retrieve a detailed summary of sales performance from the KwickMetrics dashboard.

    This tool fetches order and revenue data for a specified time range, currency, and channel (Walmart or not).
    It returns key performance metrics including total revenue, orders, units sold, profit, profit margin,
    and comparisons to the previous period.

    ### Parameters:
    - `purchase_date` (str): Predefined time period to filter the sales data. Choose from:
        - "today", "yesterday", "last_seven_days", "last_thirty_days"
        - "this_week", "last_week", "this_month", "last_month"
        - "last_6_months", "last_12_months", "this_year", "last_year"
        - "custom": Use this when specifying `date_from` and `date_to`
    - `date_from` (str): Start date in format "YYYY-MM-DD" (used only when `purchase_date="custom"`)
    - `date_to` (str): End date in format "YYYY-MM-DD" (used only when `purchase_date="custom"`)
    - `currency` (str): ISO currency code (e.g., "USD", "INR", "EUR"). Required.
    - `is_walmart` (bool): Whether to include only Walmart-related sales data. Set to `True` for Walmart-only data. Required.

    ### Returns:
    A dictionary with:
    - `total_orders`: Number of orders
    - `total_units`: Units sold
    - `total_amount`: Total sales revenue
    - `total_net_profit`: Net profit
    - `total_profit_margin`: Profit margin percentage
    - `period`: The reporting period
    - Each metric includes a comparison to the previous period and % change.

    ### Usage Examples:
    - "What were our sales last year in USD?"
    - "Show me Walmart orders from 2024-01-01 to 2024-12-31."
    - "Get profit margin in EUR for Jan 1 to Jun 30, 2023."
    - "Compare units sold in the last 12 months to the previous year."

    The LLM should extract and map:
    - `purchase_date` OR (`date_from` and `date_to`)
    - `currency`
    - `is_walmart`
    """

    if not AUTH_TOKEN or not AUTH_TENANT:
        return {"error": "Missing AUTH_TOKEN or AUTH_TENANT in environment variables."}

    if purchase_date != "custom" and purchase_date not in VALID_PURCHASE_DATES:
        return {
            "error": f"Invalid 'purchase_date'. Valid options are: {', '.join(VALID_PURCHASE_DATES.keys())}"
        }

    if purchase_date == "custom":
        if not date_from or not date_to:
            return {
                "error": "Both 'date_from' and 'date_to' must be provided for custom date range."
            }
        purchase_date_filter = {"date_from": date_from, "date_to": date_to}
    else:
        purchase_date_filter = purchase_date

    cookies = {"token": AUTH_TOKEN, "X-Tenant": AUTH_TENANT}

    payload = {
        "filters": [
            {"key": "purchase_date", "value": purchase_date_filter},
            {
                "key": "sales_channel",
                "value": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    15,
                    17,
                    18,
                    19,
                    23,
                    26,
                ],
            },
        ],
        "currency": currency,
        "is_walmart": is_walmart,
    }

    try:
        logging.debug(f"Request Cookies: {cookies}")
        logging.debug(f"Request Payload: {payload}")
        response = requests.post(SALES_API_URL, json=payload, cookies=cookies)
        response.raise_for_status()
        logging.debug(f"Response : {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {e}")
        return {"error": str(e)}


@mcp.tool()
def return_overview(
    return_date: str = "last_6_months",
    currency: str = "USD",
    is_walmart: bool = False,
    date_from: str = None,
    date_to: str = None,
):
    """
    Retrieve a detailed summary of return performance from the KwickMetrics dashboard.

    This tool fetches return and refund data for a specified time range, currency, and channel (Walmart or not).
    It returns key return metrics including total returns, return value, return rate, refund units, refund amount,
    refund percentage, and comparisons to the previous period.

    ### Parameters:
    - `return_date` (str): Predefined time period to filter the return data. Choose from:
        - "today", "yesterday", "last_seven_days", "last_thirty_days"
        - "this_week", "last_week", "this_month", "last_month"
        - "last_6_months", "last_12_months", "this_year", "last_year"
        - "custom": Use this when specifying `date_from` and `date_to`
    - `date_from` (str): Start date in format "YYYY-MM-DD" (used only when `return_date="custom"`)
    - `date_to` (str): End date in format "YYYY-MM-DD" (used only when `return_date="custom"`)
    - `currency` (str): ISO currency code (e.g., "USD", "INR", "EUR"). Required.
    - `is_walmart` (bool): Whether to include only Walmart-related return data. Set to `True` for Walmart-only data. Required.

    ### Returns:
    A dictionary with:
    - `total_returns`: Number of returns
    - `return_value`: Total monetary value of returns
    - `return_rate`: Return percentage rate compared to total orders
    - `refund_units`: Number of refunded units
    - `refund_amount`: Total refund amount
    - `refund_percentage`: Percentage of total revenue refunded
    - `period`: The reporting period
    - Each metric includes a comparison to the previous period and % change.

    ### Usage Examples:
    - "How many returns did we have in the last 6 months?"
    - "Show me Walmart return value from Jan 1 to Jun 30, 2024."
    - "Get refund percentage for this year in EUR."
    - "Compare return rate to last month."

    The LLM should extract and map:
    - `return_date` OR (`date_from` and `date_to`)
    - `currency`
    - `is_walmart`
    """

    if not AUTH_TOKEN or not AUTH_TENANT:
        return {"error": "Missing AUTH_TOKEN or AUTH_TENANT in environment variables."}

    if return_date != "custom" and return_date not in VALID_PURCHASE_DATES:
        return {
            "error": f"Invalid 'return_date'. Valid options are: {', '.join(VALID_PURCHASE_DATES.keys())}"
        }

    if return_date == "custom":
        if not date_from or not date_to:
            return {
                "error": "Both 'date_from' and 'date_to' must be provided for custom return date range."
            }
        return_date_filter = {"date_from": date_from, "date_to": date_to}
    else:
        return_date_filter = return_date

    cookies = {"token": AUTH_TOKEN, "X-Tenant": AUTH_TENANT}

    payload = {
        "filters": [
            {"key": "return_date", "value": return_date_filter},
            {
                "key": "sales_channel",
                "value": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    15,
                    17,
                    18,
                    19,
                    23,
                    26,
                ],
            },
        ],
        "currency": currency,
        "is_walmart": is_walmart,
    }

    try:
        logging.debug(f"Request Cookies: {cookies}")
        logging.debug(f"Return Overview Payload: {payload}")
        response = requests.post(RETURN_API_URL, json=payload, cookies=cookies)
        response.raise_for_status()
        logging.debug(f"Return Overview Response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Return API request failed: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),  # Cloud platforms often inject PORT
        path="/mcp"  # Required for OpenAI remote MCP tool URL
    )

