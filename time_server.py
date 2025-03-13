# time_server.py
from mcp.server.fastmcp import FastMCP
from datetime import datetime
import time
import pytz

# Create an MCP server
mcp = FastMCP("TimeServer")


@mcp.tool()
def get_current_time(timezone: str = None) -> str:
    """
    Get the current time from the computer.

    Args:
        timezone: Optional timezone name (e.g., 'America/New_York', 'Europe/London', 'UTC').
                 If not provided, returns local time.

    Returns:
        A string with the formatted current time.
    """
    if timezone:
        try:
            tz = pytz.timezone(timezone)
            current_time = datetime.now(tz)
            return f"Current time in {timezone}: {current_time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
        except pytz.exceptions.UnknownTimeZoneError:
            return f"Error: Unknown timezone '{timezone}'. Please provide a valid timezone name."
    else:
        # Return local time
        current_time = datetime.now()
        return f"Current local time: {current_time.strftime('%Y-%m-%d %H:%M:%S')} (Computer's local timezone)"


@mcp.tool()
def get_unix_timestamp() -> str:
    """
    Get the current Unix timestamp (seconds since January 1, 1970).

    Returns:
        A string with the current Unix timestamp.
    """
    timestamp = int(time.time())
    return f"Current Unix timestamp: {timestamp}"


@mcp.tool()
def list_timezones(region: str = None) -> str:
    """
    List available timezones, optionally filtered by region.

    Args:
        region: Optional region filter (e.g., 'America', 'Europe', 'Asia')
                If not provided, returns a sample of common timezones.

    Returns:
        A string with available timezones.
    """
    all_timezones = pytz.all_timezones

    if region:
        filtered_timezones = [
            tz for tz in all_timezones if tz.startswith(region)]
        if not filtered_timezones:
            return f"No timezones found for region '{region}'"
        return f"Timezones in {region}:\n" + "\n".join(filtered_timezones)
    else:
        common_timezones = [
            "UTC", "America/New_York", "America/Los_Angeles", "Europe/London",
            "Europe/Paris", "Asia/Tokyo", "Australia/Sydney", "Pacific/Auckland"
        ]
        return "Common timezones:\n" + "\n".join(common_timezones) + "\n\nUse with a region name for more options."


# Run the server when executed directly
if __name__ == "__main__":
    mcp.run()
