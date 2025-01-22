import pandas as pd
from bs4 import BeautifulSoup
import requests

# URL of the webpage
url = "https://www.surf-forecast.com/breaks/Bajamar-El-Lobo/forecasts/latest/six_day"

# Fetch the HTML content of the page
response = requests.get(url)
if response.status_code != 200:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
    exit()

soup = BeautifulSoup(response.content, "html.parser")

# Extract relevant information
def extract_forecast_table(soup):
    forecast_table = soup.find("table", class_="js-forecast-table-content")
    if not forecast_table:
        print("Forecast table not found.")
        return None

    rows = forecast_table.find_all("tr")
    headers = []
    data = []

    # Extract headers (e.g., days and times)
    days_row = rows[0]
    times_row = rows[1]

    time_labels = []
    for cell in times_row.find_all("td", class_="forecast-table-time__cell"):
        time_label = cell.get_text(strip=True)
        time_labels.append(time_label)

    for cell in days_row.find_all("td", class_="forecast-table-days__cell"):
        day = cell.get_text(strip=True)
        headers.extend([day + " - AM", day + " - PM", day + " - Night"])

    if time_labels[0] == "PM":
        headers = headers[1:-2]
    elif time_labels[0] == "Night":
        headers = headers[2:-1]

    # Extract data rows
    for row in rows[2:]:
        label = row.find("th").get_text(strip=True)  # Label for the row (e.g., "Wave Height")
        # split label at "(?)":
        label = label.split("(?)")[0]

        if "wave height" in label.lower():
            # Extract wave height values
            values = [cell.find(class_="swell-icon__val").get_text(strip=True) for cell in row.find_all("td")]
            data.append(["Wave Height (m)"] + values)

            # Extract wave direction values
            directions = [cell.find(class_="swell-icon__letters").get_text(strip=True) for cell in row.find_all("td")]
            data.append(["Wave Direction"] + directions)
        elif "wind(km/h)" in label.lower():
            # Extract wind speed values
            values = [cell.find(class_="wind-icon__val").get_text(strip=True) for cell in row.find_all("td")]
            data.append(["Wind Speed (km/h)"] + values)

            # Extract wind direction values
            directions = [cell.find(class_="wind-icon__letters").get_text(strip=True) for cell in row.find_all("td")]
            data.append(["Wind Direction"] + directions)
        elif "energy" in label.lower():
            # Extract energy values
            values = [cell.get_text(strip=True) for cell in row.find_all("td")]
            data.append(["Energy (kJ)"] + values)
        else:
            # Extract other metrics normally
            values = [cell.get_text(strip=True) for cell in row.find_all("td")]
            data.append([label] + values)

    # get rid of row number 1
    data = data[:1] + data[2:5] + data[6:]

    # Combine headers and data into a DataFrame
    df = pd.DataFrame(data, columns=["Metric"] + headers)
    return df

if __name__ == "__main__":
    forecast_df = extract_forecast_table(soup)
    print(forecast_df)
    # save as csv
    forecast_df.to_csv("forecast_data.csv", index=False)
    # save as json
    forecast_df.to_json("forecast_data.json", orient="records")
    # save as txt
    with open("forecast_data.txt", "w") as f:
        f.write(forecast_df.to_string(index=False))