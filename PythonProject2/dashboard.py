import streamlit as st
import sqlite3
from datetime import datetime, timezone
try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # Fallback if not available (unlikely on modern Python)
    ZoneInfo = None
import pandas as pd
from PIL import Image
import os
from db import delete_result

DB_PATH = "malaria.db"
UPLOAD_FOLDER = "uploads"

def dashboard_page():
    st.title("📊 Detection Results Dashboard")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if st.session_state["role"]=="Admin":
        c.execute("SELECT * FROM results ORDER BY date DESC")
    else:
        c.execute("SELECT * FROM results WHERE username=? ORDER BY date DESC",(st.session_state["username"],))
    rows = c.fetchall()
    conn.close()

    if rows:
        df = pd.DataFrame(rows, columns=["ID","Username","Image","Result","Confidence","Date"])
        # Convert UTC timestamps from SQLite to EAT for display
        def to_eat(ts: str) -> str:
            if not ts:
                return ts
            try:
                dt = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                dt = dt.replace(tzinfo=timezone.utc)
                if ZoneInfo:
                    eat_dt = dt.astimezone(ZoneInfo("Africa/Nairobi"))
                    return eat_dt.strftime("%Y-%m-%d %H:%M:%S EAT")
                # Simple +3h fallback
                return (dt.astimezone()).strftime("%Y-%m-%d %H:%M:%S")
            except Exception:
                return ts
        if "Date" in df.columns:
            df["Date"] = df["Date"].map(to_eat)
        st.markdown("### Table View")
        df_display = df.drop(columns=["Result"]) if "Result" in df.columns else df
        st.dataframe(df_display, use_container_width=True)

        st.markdown("---")
        st.markdown("### Gallery View")
        for i in range(0,len(rows),2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i+j < len(rows):
                    row = rows[i+j]
                    img_path = os.path.join(UPLOAD_FOLDER, row[2])
                    image = Image.open(img_path) if os.path.exists(img_path) else Image.new("RGB",(400,300),(220,220,220))
                    # Caption: convert timestamp to EAT
                    date_eat = to_eat(row[5])
                    with col:
                        col.image(image, caption=f"{row[1]} | Conf: {row[4]:.2f} | Date: {date_eat}", use_container_width=True)
                        can_delete = st.session_state.get("role") == "Admin"
                        if can_delete:
                            if st.button("🗑️ Delete", key=f"del_{row[0]}"):
                                delete_result(row[0])
                                st.success("Result deleted ✅")
                                st.rerun()
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", csv, "results.csv", "text/csv")
    else:
        st.info("ℹ️ No results found")