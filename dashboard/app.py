import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import time
import altair as alt

# Page setup
st.set_page_config(page_title="IoT Sensor Dashboard", layout="wide")

# PostgreSQL connection
engine = create_engine("psql -h db.vdyssjivlmdqhytitblh.supabase.co -p 5432 -d postgres -U postgres")

st.title("📡 IoT Sensor Monitoring Dashboard")

# Live updating container
placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            # Load data
            df = pd.read_sql(
                "SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 100",
                engine
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            if df.empty:
                st.warning("⚠️ No data available. Make sure your pipeline is running.")
                time.sleep(1)
                continue

            # KPIs
            k1, k2, k3 = st.columns(3)
            k1.metric("📟 Devices", df["device_id"].nunique())
            k2.metric("🌡 Avg Temp", f"{df['temperature'].mean():.2f} °C")
            k3.metric("💧 Avg Humidity", f"{df['humidity'].mean():.2f} %")

            st.markdown("---")

            # Helper to create Altair charts
            def create_line_chart(df_chart, value_col, title, y_title):
                return alt.Chart(df_chart).mark_line().encode(
                    x=alt.X("timestamp:T", title="Time"),
                    y=alt.Y(f"{value_col}:Q", title=y_title, scale=alt.Scale(zero=False)),
                    color=alt.Color("device_id:N", title="Device ID"),
                    tooltip=["timestamp", "device_id", value_col]
                ).properties(
                    title=title,
                    height=300
                ).interactive()

            # Charts
            st.altair_chart(
                create_line_chart(df, "temperature", "🌡 Temperature by Device", "Temperature (°C)"),
                use_container_width=True
            )

            st.altair_chart(
                create_line_chart(df, "humidity", "💧 Humidity by Device", "Humidity (%)"),
                use_container_width=True
            )

            st.altair_chart(
                create_line_chart(df, "battery", "🔋 Battery Level by Device", "Battery (%)"),
                use_container_width=True
            )

            st.markdown("---")

            # Status distribution
            df = pd.read_sql(
                "SELECT * FROM sensor_readings ORDER BY timestamp DESC",
                engine
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            st.subheader("📊 Status Distribution")
            status_count = df.groupby(["device_id", "status"]).size().reset_index(name="count")
            status_chart = alt.Chart(status_count).mark_bar().encode(
                x=alt.X("device_id:N", title="Device"),
                y=alt.Y("count:Q", title="Count"),
                color=alt.Color("status:N", title="Status"),
                tooltip=["device_id", "status", "count"]
            ).properties(height=300).interactive()
            st.altair_chart(status_chart, use_container_width=True)

            # Raw data and download
            with st.expander("🗃 Raw Sensor Data"):
                st.dataframe(df.sort_values("timestamp", ascending=False), use_container_width=True)
                st.download_button(
                    label="⬇️ Download as CSV",
                    data=df.to_csv(index=False),
                    file_name="sensor_data.csv",
                    mime="text/csv",
                    key=f"download-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                )


            st.caption(f"🔄 Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        except Exception as e:
            st.error(f"❌ Error loading dashboard: {e}")

    time.sleep(1)
