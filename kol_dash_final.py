import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import streamlit.components.v1 as components
from streamlit_calendar import calendar as st_calendar

# -----------------------------------------------------------------
# 0. Auth & Page Config
# -----------------------------------------------------------------
st.set_page_config(
    page_title="MEDIT KOL Performance Cockpit",
    page_icon="🟦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# [설정] 색상 및 변수 정의
ACCESS_CODE = "medit2026"
COLOR_PRIMARY = "#0044CC"  # MEDIT Blue
COLOR_DANGER = "#DC2626"   # Red (Delayed)
COLOR_WARNING = "#F59E0B"  # Orange (Warning)
COLOR_BG = "#F5F7FA"       
COLOR_CARD = "#FFFFFF"     

# 세션 상태 초기화
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def check_password():
    """로그인 화면"""
    
    def password_entered():
        entered = st.session_state.get("password", "")
        if entered == ACCESS_CODE:
            st.session_state["authenticated"] = True
        else:
            st.session_state["authenticated"] = False
            st.session_state["auth_error"] = True

    if not st.session_state.get("authenticated", False):
        st.markdown(
            f"""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
            
            .stApp {{
                background-color: #FFFFFF;
                font-family: 'Inter', sans-serif;
            }}
            
            .login-container {{
                max-width: 520px;
                margin: 15vh auto 0 auto; 
                padding: 60px 50px;
                background-color: transparent; 
                border: none;
                box-shadow: none; 
                text-align: center;
            }}
            
            .login-title {{
                color: {COLOR_PRIMARY};
                font-size: 2.2rem;
                font-weight: 800;
                margin-bottom: 50px;
                letter-spacing: -0.5px;
                white-space: nowrap;
                line-height: 1.2;
            }}
            
            .stTextInput {{
                width: 320px !important;
                margin: 0 auto;
            }}
            
            .stTextInput > div > div > input {{
                text-align: center;
                font-size: 1.3rem;
                padding: 14px;
                border: 2px solid #E0E0E0 !important;
                border-radius: 12px;
                background-color: #FAFAFA;
                color: #333;
                font-weight: 600;
                transition: all 0.3s ease;
            }}
            
            .stTextInput > div > div > input:focus {{
                border-color: {COLOR_PRIMARY} !important;
                background-color: #FFFFFF;
                box-shadow: 0 0 0 4px rgba(0, 68, 204, 0.1);
            }}

            .input-label {{
                font-size: 1rem;
                color: {COLOR_PRIMARY};
                font-weight: 700;
                margin-bottom: 8px;
                display: block;
            }}

            .error-msg {{
                color: #D32F2F;
                background-color: #FFEBEE;
                padding: 12px;
                border-radius: 8px;
                font-size: 0.9rem;
                margin-top: 25px;
                font-weight: 600;
            }}
            
            .login-footer {{
                margin-top: 80px;
                color: #A0AEC0;
                font-size: 0.8rem;
                font-weight: 500;
            }}

            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            </style>
            """, unsafe_allow_html=True
        )
        
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">MEDIT KOL Performance Cockpit</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-label">Access Code:</div>', unsafe_allow_html=True)
        st.text_input("Password", type="password", key="password", on_change=password_entered, label_visibility="collapsed")
        
        if st.session_state.get("auth_error"):
            st.markdown('<div class="error-msg">⚠️ Incorrect Access Code</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="login-footer">powered by DWG Inc. 2025.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        return False
    return True

if not check_password():
    st.stop()


# -----------------------------------------------------------------
# 1. CSS Styles (Main Dashboard)
# -----------------------------------------------------------------
def local_css():
    st.markdown(
        f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');
        
        .stApp {{
            background-color: #F5F7FA;
            color: #111;
            font-family: 'Segoe UI', sans-serif;
        }}

        .block-container {{
            padding-top: 6rem !important; 
            padding-bottom: 4rem !important;
        }}

        /* Header Box */
        .app-header {{
            background: linear-gradient(135deg, {COLOR_PRIMARY} 0%, #003399 100%);
            border-radius: 12px;
            padding: 24px 32px;
            box-shadow: 0 4px 20px rgba(0, 68, 204, 0.15);
            color: #FFFFFF; 
            margin-bottom: 30px;
            margin-top: 10px; 
        }}
        .app-title {{
            font-size: 1.8rem;
            font-weight: 700; 
            color: #FFFFFF !important;
            margin-bottom: 4px;
        }}
        .app-subtitle {{
            font-size: 0.95rem;
            opacity: 0.9;
            font-weight: 300;
        }}
        
        /* Table Headers */
        thead tr th {{
            background-color: {COLOR_PRIMARY} !important; 
            color: #FFFFFF !important; 
            font-size: 13px !important;
            font-weight: 600 !important;
            text-transform: uppercase;
        }}

        /* Common Info Box (Shared UI) */
        .info-box {{
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 12px;
            border: 1px solid #E5E7EB;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
            margin-bottom: 20px;
        }}
        
        .profile-label {{
            font-size: 0.85rem;
            color: #6B7280;
            font-weight: 600;
            margin-bottom: 5px;
            text-transform: uppercase;
        }}
        
        .profile-value {{
            font-size: 1.1rem;
            color: #111;
            font-weight: 700;
        }}

        .info-label {{
            font-size: 0.8rem;
            color: #6B7280;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 4px;
        }}
        .info-val {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #111827;
            margin-bottom: 16px;
        }}

        .section-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 15px;
            margin-top: 10px;
        }}

        /* Box Button */
        .box-btn {{
            display: inline-block;
            padding: 8px 16px;
            font-size: 0.9rem;
            font-weight: 600;
            color: {COLOR_PRIMARY};
            background-color: #EFF6FF;
            border: 1px solid {COLOR_PRIMARY};
            border-radius: 6px;
            text-decoration: none;
            margin-right: 10px;
            transition: all 0.2s;
        }}
        .box-btn:hover {{
            background-color: {COLOR_PRIMARY};
            color: #FFFFFF;
        }}
        
        /* Status Headers (Admin) */
        .status-section-header {{
            font-size: 1.2rem;
            font-weight: 700;
            color: #333;
            margin-top: 30px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
        }}
        .status-indicator {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )

local_css()

# -----------------------------------------------------------------
# 2. Data & Helper Functions
# -----------------------------------------------------------------
FILE_SETTINGS = {
    "FILE_PATH": "KOL_consolidated_251208(V).xlsx",
    "MASTER_TAB": "kol_master",
    "CONTRACT_TAB": "contract_tasks",
    "ACTIVITY_TAB": "activity_log",
}

GOOGLE_MAPS_API_KEY = "AIzaSyAVIHGVbAa47uwyQvo0OKW7Hu7M1DVrpYI" 
MONTH_NAME_MAP = {1:"Jan",2:"Feb",3:"Mar",4:"Apr",5:"May",6:"Jun",7:"Jul",8:"Aug",9:"Sep",10:"Oct",11:"Nov",12:"Dec"}
MONTH_NAME_TO_NUM = {v: k for k, v in MONTH_NAME_MAP.items()}
TASK_COLOR_MAP = {"Lecture":"#1D4ED8","Case Report":"#0EA5E9","SNS Posting":"#EC4899","Article":"#F97316","Webinar":"#22C55E","Testimonial":"#6366F1"}

STATUS_COLORS = {
    "TBD": "#9CA3AF",
    "Planned": "#3B82F6",
    "On Progress": "#F59E0B",
    "Done": "#10B981"
}

def find_col(df, candidates):
    cols = list(df.columns)
    norm = {c: c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_") for c in cols}
    normalized_candidates = [c.strip().lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_") for c in candidates]
    for original, n in norm.items():
        for nc in normalized_candidates:
            if nc in n: return original
    return None

def normalize_status(val: str) -> str:
    if pd.isna(val): return "Planned"
    s = str(val).strip().lower().replace("_", " ").replace("-", " ")
    if s in ["planned", "plan"]: return "Planned"
    if any(x in s for x in ["on progress", "in progress", "ongoing", "doing"]): return "On Progress"
    if any(x in s for x in ["done", "finished", "complete", "completed", "end"]): return "Done"
    if any(x in s for x in ["tbd", "to be determined"]): return "TBD"
    return s.title()

def delayed_to_bool(val) -> bool:
    if pd.isna(val): return False
    s = str(val).strip().lower()
    return s in ["1", "y", "yes", "true", "delayed", "delay", "o"]

def warning_to_bool(val) -> bool:
    if pd.isna(val): return False
    s = str(val).strip().lower()
    return "warning" in s

def highlight_critical_rows(row):
    style = ''
    status_val = ""
    # Dataframe에 Warning/Delayed 컬럼이 있는지 확인 후 스타일 적용
    if "Delayed" in row.index: # Display용 이름
         status_val = str(row["Delayed"]).lower()
    elif "Warning/Delayed" in row.index: # 원본 로직 이름
         status_val = str(row["Warning/Delayed"]).lower()

    if "delayed" in status_val: style = 'background-color: #FEE2E2; color: #991B1B; font-weight: bold;'
    elif "warning" in status_val: style = 'background-color: #FEF3C7; color: #92400E; font-weight: bold;'
    return [style] * len(row)

def create_warning_delayed_col(row):
    if row.get("Delayed_flag") is True: return "Delayed"
    elif row.get("Warning_flag") is True: return "Warning"
    return "-"

def kpi_text(label: str, value: str, color: str = COLOR_PRIMARY):
    st.markdown(
        f"""
        <div style="font-size:0.85rem; color:#666; font-weight:600; margin-bottom:2px;">{label}</div>
        <div style="font-size:2.0rem; font-weight:800; color:{color}; line-height:1.1;">{value}</div>
        """,
        unsafe_allow_html=True,
    )

# [Google Maps]
def render_google_map(df_master, area_filter=None):
    api_key = GOOGLE_MAPS_API_KEY
    lat_col = find_col(df_master, ["lat", "latitude", "Latitude"])
    lon_col = find_col(df_master, ["lon", "longitude", "Longitude"])
    if lat_col is None or lon_col is None: return "<div style='padding:8px;'>No location data available.</div>"

    df_map = df_master.dropna(subset=[lat_col, lon_col]).copy()
    if area_filter and area_filter != "All": df_map = df_map[df_map["Area"] == area_filter]
    
    if df_map.empty:
        map_center_lat, map_center_lng = 37.5665, 126.9780
        markers_json = "[]"
    else:
        df_map["Latitude_Raw"] = pd.to_numeric(df_map[lat_col], errors="coerce")
        df_map["Longitude_Raw"] = pd.to_numeric(df_map[lon_col], errors="coerce")
        df_map = df_map.dropna(subset=["Latitude_Raw", "Longitude_Raw"])
        df_map["Longitude"] = df_map["Latitude_Raw"]
        df_map["Latitude"] = df_map["Longitude_Raw"]
        map_center_lat = df_map["Longitude"].mean()
        map_center_lng = df_map["Latitude"].mean()

        markers_list = []
        for _, row in df_map.iterrows():
            name = row.get("Name", "Unknown")
            info_content = f"<b>{name}</b><br>{row.get('Hospital','')}"
            markers_list.append({"name": name, "lat": float(row["Longitude"]), "lng": float(row["Latitude"]), "info": info_content})
        import json as _json
        markers_json = _json.dumps(markers_list)

    html_code = f"""
    <!DOCTYPE html><html><head><style>#map {{ height: 100%; width: 100%; border-radius: 12px; }} html, body {{ height: 100%; margin: 0; padding: 0; }}</style></head>
    <body><div id="map"></div><script>
    function initMap() {{
        const map = new google.maps.Map(document.getElementById("map"), {{ zoom: {3 if area_filter == 'All' else 4}, center: {{ lat: {map_center_lat}, lng: {map_center_lng} }}, mapTypeControl: false, streetViewControl: false }});
        const markersData = {markers_json};
        const infoWindow = new google.maps.InfoWindow();
        markersData.forEach((data) => {{
            const marker = new google.maps.Marker({{ position: {{ lat: data.lat, lng: data.lng }}, map: map, title: data.name }});
            marker.addListener("click", () => {{ infoWindow.setContent(data.info); infoWindow.open(map, marker); }});
        }});
    }}</script><script src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap" async defer></script></body></html>
    """
    return html_code

@st.cache_data(ttl=600)
def load_data(file_path, master_tab, contract_tab, activity_tab):
    try:
        df_master_raw = pd.read_excel(file_path, sheet_name=master_tab, engine="openpyxl")
        df_contract = pd.read_excel(file_path, sheet_name=contract_tab, engine="openpyxl")
        df_act = pd.read_excel(file_path, sheet_name=activity_tab, engine="openpyxl")
        df_act = df_act.drop_duplicates()

        # Master
        col_name_m = find_col(df_master_raw, ["Name"])
        col_area_m = find_col(df_master_raw, ["Area"])
        col_country_m = find_col(df_master_raw, ["Country"])
        col_notion_m = find_col(df_master_raw, ["Notion", "Link"])
        col_pdf_m = find_col(df_master_raw, ["PDF_Link", "Google_Sheet_Link", "PDF", "Sheet"]) 
        # Scanner & Serial Columns
        col_scanner_m = find_col(df_master_raw, ["Delivered Scanner", "Scanner", "Device"])
        col_serial_m = find_col(df_master_raw, ["Serial No", "Serial", "SN"])
        
        rename_m = {
            col_name_m: "Name", 
            col_area_m: "Area", 
            col_country_m: "Country", 
            col_notion_m: "Notion_Link"
        }
        if col_pdf_m: rename_m[col_pdf_m] = "PDF_Link"
        if col_scanner_m: rename_m[col_scanner_m] = "Delivered_Scanner"
        if col_serial_m: rename_m[col_serial_m] = "Serial_No"
        
        df_master = df_master_raw.rename(columns=rename_m)
        
        # Ensure columns exist
        for col in ["Notion_Link", "PDF_Link", "Delivered_Scanner", "Serial_No"]:
            if col not in df_master.columns:
                df_master[col] = "-"

        # Contract
        col_name_c = find_col(df_contract, ["Name"])
        col_cstart = find_col(df_contract, ["Contract_Start"])
        col_cend = find_col(df_contract, ["Contract_End"])
        col_times = find_col(df_contract, ["Times", "Time", "Contract Type"])
        df_contract = df_contract.rename(columns={col_name_c: "Name", col_cstart: "Contract_Start", col_cend: "Contract_End", col_times: "Times"})
        df_contract["Contract_Start"] = pd.to_datetime(df_contract["Contract_Start"], errors="coerce")
        df_contract["Contract_End"] = pd.to_datetime(df_contract["Contract_End"], errors="coerce")
        if "Times" not in df_contract.columns: df_contract["Times"] = "-"

        # Activity
        col_name_a = find_col(df_act, ["Name"])
        col_date = find_col(df_act, ["Date"])
        col_task_a = find_col(df_act, ["Task"])
        col_activity_a = find_col(df_act, ["Activity", "Details"])
        col_status = find_col(df_act, ["Status"])
        col_delayed = find_col(df_act, ["Delayed"])
        col_source = find_col(df_act, ["Source", "Evidence"])
        
        df_act = df_act.rename(columns={col_name_a: "Name", col_date: "Date", col_task_a: "Task", col_activity_a: "Activity", col_status: "Status", col_delayed: "Delayed"})
        if col_source: df_act = df_act.rename(columns={col_source: "Source"})
        else: df_act["Source"] = ""

        df_act["Date"] = pd.to_datetime(df_act["Date"], errors="coerce")
        df_act = df_act.dropna(subset=["Date"])
        df_act["Status_norm"] = df_act["Status"].apply(normalize_status)
        df_act["Delayed_flag"] = df_act["Delayed"].apply(delayed_to_bool)
        df_act["Warning_flag"] = df_act["Delayed"].apply(warning_to_bool)
        df_act = df_act.merge(df_master[["Name", "Area", "Country"]].drop_duplicates("Name"), on="Name", how="left")
        
        return df_master, df_contract, df_act
    except Exception as e:
        st.error(f"Data Load Error: {e}")
        return None, None, None

def render_kol_info_box(kol_name: str, df_master: pd.DataFrame, df_contract: pd.DataFrame):
    """Performance Board 및 Admin Board용 통합 KOL 정보 박스 (HTML 변수 분리)"""
    info = df_master[df_master["Name"] == kol_name].head(1)
    
    contract_info = df_contract[df_contract["Name"] == kol_name].copy()
    contract_period_str = "-"
    contract_times_str = "-"
    if not contract_info.empty:
        start_date = contract_info["Contract_Start"].min()
        end_date = contract_info["Contract_End"].max()
        if pd.notna(start_date) and pd.notna(end_date):
            contract_period_str = f"{start_date.strftime('%Y.%m.%d')} ~ {end_date.strftime('%Y.%m.%d')}"
        times_list = contract_info["Times"].dropna().astype(str).unique().tolist()
        if times_list: contract_times_str = ", ".join(times_list)

    area = info.iloc[0]["Area"] if not info.empty else "-"
    country = info.iloc[0]["Country"] if not info.empty else "-"
    
    # Scanner Info
    scanner = info.iloc[0]["Delivered_Scanner"] if not info.empty else "-"
    serial_no = info.iloc[0]["Serial_No"] if not info.empty else "-"

    notion_url = info.iloc[0]["Notion_Link"] if not info.empty else None
    pdf_url = info.iloc[0]["PDF_Link"] if not info.empty else None 

    pdf_btn_html = ""
    if pdf_url and "http" in str(pdf_url):
        pdf_btn_html = f'<a href="{pdf_url}" target="_blank" class="box-btn">📄 Open Google Sheet (PDF)</a>'
    else:
        pdf_btn_html = f'<span style="color:#999; font-size:0.85rem; margin-right:10px;">📄 No PDF Link</span>'
    
    notion_btn_html = ""
    if notion_url and "http" in str(notion_url):
        notion_btn_html = f'<a href="{notion_url}" target="_blank" class="box-btn">🔗 Notion Page</a>'
    else:
        notion_btn_html = f'<span style="color:#999; font-size:0.85rem;">🔗 No Notion Link</span>'

    # [수정됨] HTML을 문자열 변수로 먼저 생성 후 markdown 호출
    html_content = f"""
    <div class="info-box">
        <div style="display:flex; justify-content: space-between; flex-wrap: wrap; margin-bottom: 20px;">
            <div style="margin-right:20px;">
                <div class="info-label">Name</div>
                <div class="info-val">{kol_name}</div>
            </div>
            <div style="margin-right:20px;">
                <div class="info-label">Region</div>
                <div class="info-val">{area}</div>
            </div>
            <div style="margin-right:20px;">
                <div class="info-label">Country</div>
                <div class="info-val">{country}</div>
            </div>
            <div style="margin-right:20px;">
                <div class="info-label">Contract Period</div>
                <div class="info-val">{contract_period_str}</div>
            </div>
            <div style="margin-right:20px;">
                <div class="info-label">Contract Type</div>
                <div class="info-val" style="color:{COLOR_PRIMARY}">{contract_times_str}</div>
            </div>
        </div>
        <div style="display:flex; justify-content: flex-start; flex-wrap: wrap; margin-bottom: 20px; border-top: 1px dashed #eee; padding-top: 15px;">
            <div style="margin-right:40px;">
                <div class="info-label">Delivered Scanner</div>
                <div class="info-val">{scanner}</div>
            </div>
            <div style="margin-right:40px;">
                <div class="info-label">Serial No.</div>
                <div class="info-val">{serial_no}</div>
            </div>
        </div>
        <div style="padding-top:15px; border-top:1px solid #eee;">
            {pdf_btn_html} {notion_btn_html}
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

def render_kol_detail_admin(kol_name: str, df_master: pd.DataFrame, df_contract: pd.DataFrame, df_activity: pd.DataFrame):
    """Admin Page용 상세 뷰"""
    
    # 1. KOL Information (Use common function for consistent UI)
    render_kol_info_box(kol_name, df_master, df_contract)
    
    # 2. Contract Progress Rates Table
    st.markdown('<div class="section-title">Contract Progress Rates</div>', unsafe_allow_html=True)
    
    log = df_activity[df_activity["Name"] == kol_name].copy()
    if not log.empty:
        # Status 기준 정렬 -> 그 다음 Date 내림차순
        log = log.sort_values(by=["Status_norm", "Date"], ascending=[True, False])
        log["Date"] = log["Date"].dt.strftime("%Y-%m-%d")
        log["Warning/Delayed"] = log.apply(create_warning_delayed_col, axis=1)
        
        # 컬럼 순서: Status, Date, Task, Activity
        cols_req = ["Status_norm", "Date", "Task", "Activity", "Warning/Delayed"]
        cols_disp = [c for c in cols_req if c in log.columns]
        
        st.dataframe(
            log[cols_disp].rename(columns={"Status_norm": "Status", "Warning/Delayed": "Delayed"}).style.apply(highlight_critical_rows, axis=1),
            use_container_width=True, hide_index=True
        )
    else:
        st.info("No activity records found.")

# -----------------------------------------------------------------
# 3. Main Logic
# -----------------------------------------------------------------
df_master, df_contract, df_activity = load_data(
    FILE_SETTINGS["FILE_PATH"], FILE_SETTINGS["MASTER_TAB"], FILE_SETTINGS["CONTRACT_TAB"], FILE_SETTINGS["ACTIVITY_TAB"]
)

if df_master is None: st.stop()

# Date Parsing
df_activity["Year"] = df_activity["Date"].dt.year
df_activity["Month_Num"] = df_activity["Date"].dt.month
available_years = sorted(df_activity["Year"].dropna().unique().tolist())
today = datetime.date.today()
default_year = today.year if today.year in available_years else (max(available_years) if available_years else today.year)
available_month_names = list(MONTH_NAME_MAP.values())

# -----------------------------------------------------------------
# 4. HEADER & CONTROLS
# -----------------------------------------------------------------
st.markdown(
    f"""
    <div class="app-header">
        <div class="app-title">MEDIT KOL Performance Cockpit</div>
        <div class="app-subtitle">Global KOL Management System</div>
    </div>
    """,
    unsafe_allow_html=True,
)

c_page, c_year, c_month, c_area = st.columns([1.5, 0.8, 0.8, 1.0])

with c_page:
    page = st.selectbox("Select Board", ["Performance Board", "Admin Board"])

with c_year:
    selected_year = st.selectbox("Year", options=available_years, index=available_years.index(default_year) if default_year in available_years else 0)

with c_month:
    month_options = ["All"] + available_month_names
    current_month_str = MONTH_NAME_MAP.get(today.month, "Jan")
    default_ix = month_options.index(current_month_str) if current_month_str in month_options else 0
    selected_month_name = st.selectbox("Month", options=month_options, index=default_ix)

with c_area:
    area_options = ["All"] + sorted(df_master["Area"].dropna().unique().tolist())
    selected_area = st.selectbox("Area", options=area_options, index=0)

# Filter Logic
mask = df_activity["Year"] == selected_year
if selected_month_name != "All":
    mask &= df_activity["Month_Num"] == MONTH_NAME_TO_NUM[selected_month_name]
if selected_area != "All":
    mask &= df_activity["Area"] == selected_area

df_filtered = df_activity[mask].copy()

# -----------------------------------------------------------------
# 5. Performance Board
# -----------------------------------------------------------------
if page == "Performance Board":
    st.markdown(f"### Performance Overview ({selected_year} {selected_month_name})")
    
    total_kols = df_master["Name"].nunique() if selected_area == "All" else df_master[df_master["Area"] == selected_area]["Name"].nunique()
    planned_tasks = df_filtered.shape[0]
    onprogress = df_filtered[df_filtered["Status_norm"] == "On Progress"].shape[0]
    done = df_filtered[df_filtered["Status_norm"] == "Done"].shape[0]
    delayed = df_filtered[df_filtered["Delayed_flag"] == True].shape[0]
    warning = df_filtered[df_filtered["Warning_flag"] == True].shape[0]

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1: kpi_text("Active KOLs", f"{total_kols}")
    with k2: kpi_text("Total Tasks", f"{planned_tasks}")
    with k3: kpi_text("On Progress", f"{onprogress}")
    with k4: kpi_text("Done", f"{done}")
    with k5: kpi_text("Delayed", f"{delayed}", color=COLOR_DANGER)
    with k6: kpi_text("Warning", f"{warning}", color=COLOR_WARNING)

    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

    st.markdown("### Active & Delayed Tasks")
    status_df = df_filtered[
        (df_filtered["Status_norm"] == "On Progress") | 
        (df_filtered["Delayed_flag"] == True) |
        (df_filtered["Warning_flag"] == True)
    ].copy()
    
    if not status_df.empty:
        status_df["Warning/Delayed"] = status_df.apply(create_warning_delayed_col, axis=1)
        status_cols = ["Date", "Name", "Task", "Activity", "Status_norm", "Warning/Delayed", "Area"]
        status_disp = status_df[status_cols].rename(columns={"Status_norm": "Status"})
        status_disp["Date"] = status_disp["Date"].dt.strftime("%Y-%m-%d")
        status_disp = status_disp.sort_values(by=["Warning/Delayed", "Date"], ascending=[False, True])
        st.dataframe(status_disp.style.apply(highlight_critical_rows, axis=1), use_container_width=True, hide_index=True)
    else:
        st.info("No active or delayed tasks.")

    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

    st.markdown("### Schedule")
    if selected_month_name == "All":
        st.info("Please select a specific month to view the Daily Schedule.")
    else:
        events = []
        for _, row in df_filtered.iterrows():
            delayed_flag = bool(row["Delayed_flag"])
            color = COLOR_DANGER if delayed_flag else TASK_COLOR_MAP.get(str(row["Task"]).strip(), COLOR_PRIMARY)
            title = f"{row['Name']} : {row['Task']}"
            if delayed_flag: title = "[Delay] " + title
            
            events.append({
                "title": title,
                "start": row["Date"].strftime("%Y-%m-%d"),
                "end": row["Date"].strftime("%Y-%m-%d"),
                "allDay": True,
                "backgroundColor": color,
                "borderColor": color,
                "extendedProps": {"kol_name": row["Name"]}
            })
        
        m_num = MONTH_NAME_TO_NUM[selected_month_name]
        init_date = f"{selected_year}-{m_num:02d}-01"

        cal_state = st_calendar(
            events=events,
            options={
                "initialDate": init_date,
                "headerToolbar": {"left": "", "center": "title", "right": ""},
                "height": 700,
            },
            key=f"cal_{selected_year}_{selected_month_name}"
        )

        if cal_state and cal_state.get("eventClick"):
            clicked_kol = cal_state["eventClick"]["event"]["extendedProps"].get("kol_name")
            if clicked_kol:
                st.markdown("---")
                st.markdown("### KOL Information")
                render_kol_info_box(clicked_kol, df_master, df_contract)

    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    st.markdown("### Location Map")
    map_html = render_google_map(df_master, area_filter=selected_area)
    components.html(map_html, height=500)

# -----------------------------------------------------------------
# 6. Admin Board
# -----------------------------------------------------------------
else: # Admin Board
    
    # 1. KOL Information (Moved to Top)
    st.markdown("### KOL Information")
    
    all_kol_names = sorted(df_master["Name"].dropna().unique().tolist())
    target_kol = st.selectbox("Select KOL to view Details", ["-"] + all_kol_names)
    
    if target_kol != "-":
        render_kol_detail_admin(target_kol, df_master, df_contract, df_activity)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    st.markdown("---")

    # 2. Activity Log Viewer
    st.markdown("### Activity Log Viewer")
    
    # 2-1. Split Tables by Status
    df_log = df_filtered.copy()
    df_log["Warning/Delayed"] = df_log.apply(create_warning_delayed_col, axis=1)
    df_log["Date"] = df_log["Date"].dt.strftime("%Y-%m-%d")
    
    cols_admin = ["Date", "Name", "Area", "Country", "Task", "Activity", "Warning/Delayed"]
    
    statuses = ["TBD", "Planned", "On Progress", "Done"]
    
    for status in statuses:
        color = STATUS_COLORS.get(status, "#333")
        st.markdown(
            f"""
            <div class="status-section-header">
                <div class="status-indicator" style="background-color: {color};"></div>
                {status}
            </div>
            """, unsafe_allow_html=True
        )
        
        subset = df_log[df_log["Status_norm"] == status].copy()
        subset = subset.sort_values(by="Date", ascending=True) 
        
        if not subset.empty:
            cols_real = [c for c in cols_admin if c in subset.columns]
            st.dataframe(
                subset[cols_real].style.apply(highlight_critical_rows, axis=1),
                use_container_width=True, hide_index=True
            )
        else:
            st.caption(f"No {status} tasks.")