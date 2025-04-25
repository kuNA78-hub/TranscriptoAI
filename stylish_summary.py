
import requests
import json
import sys

# Check if a URL is provided as a command-line argument
if len(sys.argv) < 2:
    print("Please provide a YouTube URL as a command-line argument.")
    print("Example: python stylish_summary.py https://www.youtube.com/watch?v=n32PYg7oAQg")
    input("Press Enter to exit...")
    sys.exit(1)

# Construct the API URL with the provided YouTube URL
youtube_url = sys.argv[1]
api_url = f"http://localhost:8000/summarize?url={youtube_url}"

# Fetch the summary
try:
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"Error fetching summary: {e}")
    input("Press Enter to exit...")
    sys.exit(1)

# Print styled output
print("Points to be Noted")
print()
if "error" in data:
    print(data["error"])
else:
    print(data["title"])
print()
if "summary" in data:
    for point in data["summary"]["summary"]:
        print(point)
print()
print("Summary Over")
input("Press Enter to exit...")
