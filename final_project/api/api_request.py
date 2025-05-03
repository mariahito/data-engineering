import requests

base_url = "http://localhost:5000"

# output is home route
response = requests.get(f"{base_url}/")
print("Home:", response.json())

# output is average cases by state
response = requests.get(f"{base_url}/cases-by-state")
print("Cases by state:", response.json())

# output is average unemployment by state 
response = requests.get(f"{base_url}/avg-unemployment-by-state")
print("Avg unemployment:", response.json())

# avg temperature by state route
response = requests.get(f"{base_url}/avg-temp-by-state")
print("Avg temperature:", response.json())

# filter state
params = {
    "state": "New York",       
    "month": "1/1/2021"     
}
response = requests.get(f"{base_url}/filter", params=params)
print("Filtered data:", response.json())
