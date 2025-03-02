import pandas as pd

url = "https://api.alternative.me/fng/?format=csv&limit=0"

# Try different delimiters
fg_data = pd.read_csv(url, delimiter=";")  # Change delimiter if needed
print(fg_data)
