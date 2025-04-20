# import streamlit as st
# import requests
# from geopy.geocoders import Nominatim
# from geopy.exc import GeocoderTimedOut

# API_KEY = "6837309590d309b04a447bfd5a40cb427edfbf02"

# def fetch_air_quality(lat, lon):
#     url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={API_KEY}"
#     try:
#         response = requests.get(url, timeout=10).json()
#         if response["status"] == "ok":
#             data = response["data"]
#             iaqi = data.get("iaqi", {})
#             return {
#                 "city": data.get("city", {}).get("name", "Unknown"),
#                 "aqi": data.get("aqi", "N/A"),
#                 "co": iaqi.get("co", {}).get("v", "N/A"),
#                 "no2": iaqi.get("no2", {}).get("v", "N/A"),
#                 "timestamp": data.get("time", {}).get("s", "N/A")
#             }
#     except Exception as e:
#         st.error(f"Error fetching data: {e}")
#     return None

# def get_coordinates(location_name):
#     try:
#         geolocator = Nominatim(user_agent="air_quality_app")
#         location = geolocator.geocode(location_name)
#         if location:
#             return location.latitude, location.longitude
#     except GeocoderTimedOut:
#         st.warning("Geocoding service timed out.")
#     return None, None

# st.set_page_config(page_title="Live Air Quality Monitor", layout="centered")

# st.title("🌍 Live Air Quality Monitor")
# location_input = st.text_input("Enter your city or location", "New Delhi")

# if st.button("Check Air Quality"):
#     lat, lon = get_coordinates(location_input)
#     if lat is not None and lon is not None:
#         data = fetch_air_quality(lat, lon)
#         if data:        st.success(f"📍 Location: {data['city']}")
#         st.metric(label="AQI", value=data["aqi"])
#         st.metric(label="CO (Carbon Monoxide)", value=data["co"])
#         st.metric(label="NO₂ (Nitrogen Dioxide)", value=data["no2"])
#         st.caption(f"Last Updated: {data['timestamp']}")

#         # ---------------- LOGGING + CHARTS BELOW ---------------- #
#         import os
#         import pandas as pd
#         import plotly.express as px
#         from datetime import datetime, timedelta

#         log_file = "air_quality_log.csv"
#         today = datetime.today().strftime('%Y-%m-%d')
#         city = data['city']

#         # Load logs
#         if os.path.exists(log_file):
#             df_log = pd.read_csv(log_file)
#         else:
#             df_log = pd.DataFrame(columns=["date", "city", "no2", "co", "aqi"])

#         # Check if already logged today
#         already_logged = ((df_log["date"] == today) & (df_log["city"] == city)).any()

#         if not already_logged:
#             df_log = pd.concat([
#                 df_log,
#                 pd.DataFrame([{
#                     "date": today,
#                     "city": city,
#                     "no2": data["no2"],
#                     "co": data["co"],
#                     "aqi": data["aqi"]
#                 }])
#             ])
#             df_log.to_csv(log_file, index=False)

#         # Filter to last 3 months
#         st.subheader("📈 Air Quality Trend (Past 3 Months)")
#         df_city = df_log[df_log["city"] == city].copy()
#         df_city["date"] = pd.to_datetime(df_city["date"])
#         three_months_ago = datetime.today() - timedelta(days=90)
#         df_city = df_city[df_city["date"] >= three_months_ago]
#         df_city = df_city.sort_values("date")

#         df_melted = df_city.melt(id_vars="date", value_vars=["no2", "co", "aqi"],
#                                  var_name="Pollutant", value_name="Value")
#         fig = px.line(df_melted, x="date", y="Value", color="Pollutant", markers=True,
#                       title=f"{city} - NO₂, CO, AQI Trend")
#         st.plotly_chart(fig, use_container_width=True)

#         with st.expander("📊 View Past Data Table"):
#             st.dataframe(df_city.set_index("date"))

#     else:
#             st.error("No data available for this location.")
# else:
#         st.error("Could not determine coordinates. Try a different location.")




# import os
# import pandas as pd
# import plotly.express as px
# from datetime import datetime

# # --- Logging data per day ---
# log_file = "air_quality_log.csv"

# # Get today's date and location
# today = datetime.today().strftime('%Y-%m-%d')
# city = data['city']

# # Load existing logs
# if os.path.exists(log_file):
#     df_log = pd.read_csv(log_file)
# else:
#     df_log = pd.DataFrame(columns=["date", "city", "no2", "co", "aqi"])

# # Check if already logged for today
# already_logged = ((df_log["date"] == today) & (df_log["city"] == city)).any()

# # Append today's data if not already logged
# if not already_logged:
#     df_log = pd.concat([
#         df_log,
#         pd.DataFrame([{
#             "date": today,
#             "city": city,
#             "no2": data["no2"],
#             "co": data["co"],
#             "aqi": data["aqi"]
#         }])
#     ])
#     df_log.to_csv(log_file, index=False)

# # --- Show recent monthly trend ---
# st.subheader("📈 Air Quality Trend (Past Month)")
# df_city = df_log[df_log["city"] == city].copy()
# df_city["date"] = pd.to_datetime(df_city["date"])
# df_city = df_city.sort_values("date")

# # Melt for plotting
# df_melted = df_city.melt(id_vars="date", value_vars=["no2", "co", "aqi"], var_name="Pollutant", value_name="Value")
# fig = px.line(df_melted, x="date", y="Value", color="Pollutant", markers=True, title=f"{city} - NO₂, CO, AQI Trend")
# st.plotly_chart(fig, use_container_width=True)

# # Optional: Show table
# with st.expander("📊 View Past Data Table"):
#     st.dataframe(df_city.set_index("date"))
import streamlit as st
import requests
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import os
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

API_KEY = "6837309590d309b04a447bfd5a40cb427edfbf02"

def fetch_air_quality(lat, lon):
    url = f"https://api.waqi.info/feed/geo:{lat};{lon}/?token={API_KEY}"
    try:
        response = requests.get(url, timeout=10).json()
        if response["status"] == "ok":
            data = response["data"]
            iaqi = data.get("iaqi", {})
            return {
                "city": data.get("city", {}).get("name", "Unknown"),
                "aqi": data.get("aqi", "N/A"),
                "co": iaqi.get("co", {}).get("v", "N/A"),
                "no2": iaqi.get("no2", {}).get("v", "N/A"),
                "timestamp": data.get("time", {}).get("s", "N/A")
            }
    except Exception as e:
        st.error(f"Error fetching data: {e}")
    return None

def get_coordinates(location_name):
    try:
        geolocator = Nominatim(user_agent="air_quality_app")
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
    except GeocoderTimedOut:
        st.warning("Geocoding service timed out.")
    return None, None

st.set_page_config(page_title="Live Air Quality Monitor", layout="centered")

st.title("🌍 Live Air Quality Monitor")
location_input = st.text_input("Enter your city or location", "New Delhi")

if st.button("Check Air Quality"):
    lat, lon = get_coordinates(location_input)
    if lat is not None and lon is not None:
        data = fetch_air_quality(lat, lon)
        if data:
            st.success(f"📍 Location: {data['city']}")
            st.metric(label="AQI", value=data["aqi"])
            st.metric(label="CO (Carbon Monoxide)", value=data["co"])
            st.metric(label="NO₂ (Nitrogen Dioxide)", value=data["no2"])
            st.caption(f"Last Updated: {data['timestamp']}")

            # === AQI Health Message ===
            def get_aqi_message(aqi):
                try:
                    aqi = int(aqi)
                except:
                    return None

                if 0 <= aqi <= 50:
                    return ("🟢 Good", "Air quality is satisfactory.", "No risk for the general public.")
                elif 51 <= aqi <= 100:
                    return ("🟡 Moderate", "Air quality is acceptable.", "Sensitive individuals should limit prolonged outdoor exertion.")
                elif 101 <= aqi <= 150:
                    return ("🟠 Unhealthy for Sensitive Groups", "Members of sensitive groups may experience health effects.", "Active children and adults with respiratory issues should limit prolonged outdoor exertion.")
                elif 151 <= aqi <= 200:
                    return ("🔴 Unhealthy", "Everyone may begin to experience health effects.", "Sensitive groups should avoid prolonged exertion; others should limit it.")
                elif 201 <= aqi <= 300:
                    return ("🟣 Very Unhealthy", "Health warnings of emergency conditions.", "Everyone should avoid prolonged outdoor exertion.")
                else:
                    return ("⚫ Hazardous", "Serious health effects for all.", "Everyone should avoid all outdoor exertion.")
            aqi_msg = get_aqi_message(data["aqi"])
            if aqi_msg:
                st.markdown(f"### {aqi_msg[0]}")
                st.write(f"**Health Implication:** {aqi_msg[1]}")
                st.write(f"**Caution:** {aqi_msg[2]}")

            # ---------------- LOGGING + CHARTS BELOW ---------------- #
            log_file = "air_quality_log.csv"
            today = datetime.today().strftime('%Y-%m-%d')
            city = data['city']

            # Load logs
            if os.path.exists(log_file):
                df_log = pd.read_csv(log_file)
            else:
                df_log = pd.DataFrame(columns=["date", "city", "no2", "co", "aqi"])

            # Check if already logged today
            already_logged = ((df_log["date"] == today) & (df_log["city"] == city)).any()

            if not already_logged:
                df_log = pd.concat([df_log, pd.DataFrame([{
                    "date": today,
                    "city": city,
                    "no2": data["no2"],
                    "co": data["co"],
                    "aqi": data["aqi"]
                }])])
                df_log.to_csv(log_file, index=False)

            # --- Past 3 Months Chart ---
            st.subheader("📈 Air Quality Trend (Past 3 Months)")
            df_city = df_log[df_log["city"] == city].copy()
            df_city["date"] = pd.to_datetime(df_city["date"])
            three_months_ago = datetime.today() - timedelta(days=90)
            df_city = df_city[df_city["date"] >= three_months_ago]
            df_city = df_city.sort_values("date")

            df_melted = df_city.melt(id_vars="date", value_vars=["no2", "co", "aqi"],
                                     var_name="Pollutant", value_name="Value")
            fig = px.line(df_melted, x="date", y="Value", color="Pollutant", markers=True,
                          title=f"{city} - NO₂, CO, AQI Trend")
            st.plotly_chart(fig, use_container_width=True, key="three_month_trend")

            with st.expander("📊 View Past Data Table"):
                st.dataframe(df_city.set_index("date"))

            # --- Past Month Trend ---
            st.subheader("📈 Air Quality Trend (Past Month)")
            one_month_ago = datetime.today() - timedelta(days=30)
            df_month = df_city[df_city["date"] >= one_month_ago]
            df_melted_month = df_month.melt(id_vars="date", value_vars=["no2", "co", "aqi"],
                                            var_name="Pollutant", value_name="Value")
            fig_month = px.line(df_melted_month, x="date", y="Value", color="Pollutant", markers=True,
                                title=f"{city} - NO₂, CO, AQI Trend (1 Month)")
            st.plotly_chart(fig_month, use_container_width=True, key="one_month_trend")

            with st.expander("📊 View Monthly Data Table"):
                st.dataframe(df_month.set_index("date"))

        else:
            st.error("No data available for this location.")
    else:
        st.error("Could not determine coordinates. Try a different location.")
from datetime import date

# Compare dates
if data.get("time", {}).get("s"):
    data_date = data["time"]["s"][:10]
    if data_date != str(date.today()):
        st.warning(f"⚠️ Note: The data is from {data_date}, not live.")


st.write("Debug - Raw Timestamp:", data["timestamp"])


st.write("Full data received from API:", data)
