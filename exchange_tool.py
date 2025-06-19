import argparse
import requests
from datetime import datetime, timedelta
import json
from bs4 import BeautifulSoup
import re

class ExchangeTool:
    def __init__(self):
        pass

    def parse_date_range(self, query: str) -> tuple:
        """Parse date range from query string."""
        # Try to match "last X months/years" format
        last_match = re.search(r'last\s+(\d+)\s+(month|year)s?', query.lower())
        if last_match:
            number = int(last_match.group(1))
            unit = last_match.group(2)
            end_date = datetime.now()
            if unit == 'month':
                start_date = end_date - timedelta(days=30 * number)
            else:  # year
                start_date = end_date - timedelta(days=365 * number)
            return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
        
        # Try to match date range format "YYYY-MM-DD~YYYY-MM-DD"
        date_range_match = re.search(r'(\d{4}-\d{2}-\d{2})~(\d{4}-\d{2}-\d{2})', query)
        if date_range_match:
            return date_range_match.group(1), date_range_match.group(2)
        
        # Default to last 1 month if no range specified
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def get_exchange_rate(self, from_currency: str, to_currency: str, query: str) -> dict:
        """Get exchange rate data from Taiwan Bank."""
        try:
            # Parse date range
            start_date, end_date = self.parse_date_range(query)
            print(f"Debug: Date range: {start_date} to {end_date}")
            
            # Taiwan Bank website
            url = "https://rate.bot.com.tw/xrt/quote/ltm/CNY"
            
            # Get the data
            response = requests.get(url)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the table with exchange rates
            table = soup.find('table', {'class': 'table table-striped table-bordered table-condensed table-hover'})
            if not table:
                print("Debug: Could not find table with class 'table table-striped table-bordered table-condensed table-hover'")
                # Try to find any table
                table = soup.find('table')
                if not table:
                    return {
                        "error": "Could not find exchange rate table",
                        "current_rate": None,
                        "statistics": None,
                        "historical_data": []
                    }
                print("Debug: Found a table, but not the expected one")
            
            # Process historical data
            historical_data = []
            rates = []
            
            # Get all rows except header
            rows = table.find_all('tr')[1:]  # Skip header row
            print(f"Debug: Found {len(rows)} rows in the table")
            
            for row in rows:
                try:
                    cols = row.find_all('td')
                    if len(cols) >= 3:  # We need at least 3 columns: date, currency name, and rate
                        date = cols[0].text.strip()
                        rate_text = cols[2].text.strip()  # The rate is in the third column
                        
                        # Convert date format from YYYY/MM/DD to YYYY-MM-DD
                        date = date.replace('/', '-')
                        
                        # Skip if date is outside our range
                        if date < start_date or date > end_date:
                            continue
                        
                        print(f"Debug: Processing row - Date: {date}, Rate text: {rate_text}")
                        
                        # Remove any non-numeric characters from rate_text except decimal point
                        rate_text = ''.join(c for c in rate_text if c.isdigit() or c == '.')
                        if rate_text:
                            rate = float(rate_text)
                            rates.append(rate)
                            
                            historical_data.append({
                                "date": date,
                                "rate": rate
                            })
                except (ValueError, IndexError) as e:
                    print(f"Debug: Error processing row: {e}")
                    continue
            
            if not historical_data:
                return {
                    "error": "No exchange rate data available for the specified period",
                    "current_rate": None,
                    "statistics": None,
                    "historical_data": []
                }
            
            # Calculate statistics
            current_rate = rates[-1]
            average_rate = sum(rates) / len(rates)
            min_rate = min(rates)
            max_rate = max(rates)
            
            # Determine trend
            first_rate = rates[0]
            last_rate = rates[-1]
            if last_rate > first_rate * 1.02:
                trend = "up"
            elif last_rate < first_rate * 0.98:
                trend = "down"
            else:
                trend = "stable"
            
            return {
                "current_rate": current_rate,
                "statistics": {
                    "average_rate": average_rate,
                    "min_rate": min_rate,
                    "max_rate": max_rate,
                    "trend": trend,
                    "period": f"{historical_data[0]['date']} to {historical_data[-1]['date']}"
                },
                "historical_data": historical_data
            }
        except Exception as e:
            print(f"Debug: Error in get_exchange_rate: {str(e)}")
            return {
                "error": str(e),
                "current_rate": None,
                "statistics": None,
                "historical_data": []
            }

    def print_result(self, result):
        """Print exchange rate information in a formatted way."""
        if "error" in result and result["error"]:
            print(f"Error: {result['error']}")
            return
        print("\n=== Exchange Rate Information ===")
        print(f"Current Rate: {result['current_rate']:.4f}")
        stats = result['statistics']
        print("\nStatistics:")
        print(f"Average Rate: {stats['average_rate']:.4f}")
        print(f"Minimum Rate: {stats['min_rate']:.4f}")
        print(f"Maximum Rate: {stats['max_rate']:.4f}")
        print(f"Trend: {stats['trend']}")
        print(f"Period: {stats['period']}")
        print("\nHistorical Data (last 10 entries):")
        for rate in result['historical_data'][-10:]:
            print(f"Date: {rate['date']}, Rate: {rate['rate']:.4f}")

    def run(self, query=None):
        if query is None:
            parser = argparse.ArgumentParser(description="Exchange Rate Query Tool")
            parser.add_argument(
                "query",
                nargs="?",
                default="CNY to TWD",
                help="Query in format 'CURRENCY1 to CURRENCY2 [last X months/years]' or 'CURRENCY1 to CURRENCY2 YYYY-MM-DD~YYYY-MM-DD'"
            )
            args = parser.parse_args()
            query = args.query
        try:
            query_parts = query.upper().split(" TO ")
            if len(query_parts) != 2:
                return {"error": "Invalid query format. Use 'CURRENCY1 to CURRENCY2 [last X months/years]' or 'CURRENCY1 to CURRENCY2 YYYY-MM-DD~YYYY-MM-DD'"}
            from_currency = query_parts[0].strip()
            to_currency = query_parts[1].strip()
            result = self.get_exchange_rate(from_currency, to_currency, query)
            return result
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    # tool = ExchangeTool()
    # result = tool.run()
    # tool.print_result(result)

    tool = ExchangeTool()
    result = tool.run("CNY to TWD last 3 months")
    tool.print_result(result) 