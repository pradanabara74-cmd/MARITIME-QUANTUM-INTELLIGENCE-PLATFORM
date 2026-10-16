from __future__ import annotations
"""MQEIP Integrated Core v2.0. Shared operational records; SQLite persistence; 16 connected module views. AIS, AI-provider, and n8n services are not marked live until verified. """
import io, os, sqlite3, uuid
from datetime import date, datetime
from typing import Any
import numpy as np
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="Maritime Quantum Intelligence Platform", page_icon="⚓", layout="wide")
st.markdown("""<style> /* MQEIP premium navy/gold theme — tablet readability pass */ .stApp { background: #07111f; color: #e8eef7; } [data-testid="stSidebar"] { background: #0b1729; border-right: 1px solid #30445f; min-width: 285px !important; width: 285px !important; } [data-testid="stSidebar"] > div { padding-top: 1.1rem; } [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #f0d69a !important; font-size: 1.25rem !important; line-height: 1.35 !important; } [data-testid="stSidebar"] [data-testid="stRadio"] label { color: #f0f5ff !important; font-size: 1rem !important; line-height: 1.45 !important; padding-top: 0.22rem !important; padding-bottom: 0.22rem !important; } [data-testid="stSidebar"] [data-testid="stRadio"] label p { color: #f0f5ff !important; font-size: 1rem !important; line-height: 1.45 !important; } [data-testid="stSidebar"] [data-testid="stCaptionContainer"], [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: #c6d4e8 !important; font-size: 0.9rem !important; line-height: 1.45 !important; } [data-testid="stSidebar"] [data-testid="stAlert"] { border: 1px solid #30445f; } h1, h2, h3 { color: #f0d69a !important; line-height: 1.25 !important; } h1 { font-size: clamp(1.8rem, 3vw, 2.6rem) !important; } h2 { font-size: clamp(1.45rem, 2.5vw, 2rem) !important; } h3 { font-size: clamp(1.2rem, 2vw, 1.5rem) !important; } p, label, .stMarkdown, .stCaption { line-height: 1.5; } [data-testid="stMetric"] { background: #102139; border: 1px solid #30445f; padding: 14px; border-radius: 12px; } [data-testid="stMetricLabel"] { color: #d3deef !important; font-size: 0.92rem !important; } [data-testid="stMetricValue"] { color: #ffffff !important; } div[data-testid="stForm"] { background: #0b1729; padding: 16px; border: 1px solid #30445f; border-radius: 12px; } button, input, textarea, select { font-size: 1rem !important; } /* Match Streamlit's top header and decoration to MQEIP navy */ header[data-testid="stHeader"] { background: #07111f !important; color: #e8eef7 !important; } header[data-testid="stHeader"] [data-testid="stToolbar"] { background: transparent !important; } [data-testid="stDecoration"] { background: #07111f !important; } /* Responsive layout across desktop, tablet and Android phones */ [data-testid="stAppViewContainer"] .main .block-container { width: 100%; max-width: 1600px; padding-top: 1.6rem; padding-left: clamp(1rem, 3vw, 2.5rem); padding-right: clamp(1rem, 3vw, 2.5rem); padding-bottom: 2rem; } [data-testid="stDataFrame"], [data-testid="stTable"] { max-width: 100%; } [data-testid="stHorizontalBlock"] { gap: clamp(0.55rem, 1.5vw, 1.25rem); } [data-testid="stMetric"] { min-width: 0; overflow-wrap: anywhere; } .stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] > button { min-height: 2.75rem; border-radius: 0.55rem; } footer { visibility: hidden; } @media (min-width: 1100px) { [data-testid="stAppViewContainer"] .main .block-container { max-width: 1600px; padding-top: 2rem; } } @media (min-width: 701px) and (max-width: 1099px) { [data-testid="stAppViewContainer"] .main .block-container { padding-left: 1.15rem; padding-right: 1.15rem; } [data-testid="stSidebar"] { min-width: 270px !important; width: 270px !important; } } @media (max-width: 700px) { [data-testid="stAppViewContainer"] .main .block-container { padding-top: 1rem; padding-left: 0.8rem; padding-right: 0.8rem; } [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 0.65rem !important; } [data-testid="stHorizontalBlock"] > [data-testid="column"] { min-width: min(100%, 145px) !important; flex: 1 1 145px !important; } [data-testid="stMetric"] { padding: 0.7rem; } [data-testid="stMetricLabel"] { font-size: 0.82rem !important; } [data-testid="stMetricValue"] { font-size: 1.35rem !important; } [data-testid="stSidebar"] { min-width: 260px !important; width: 260px !important; } [data-testid="stSidebar"] [data-testid="stRadio"] label, [data-testid="stSidebar"] [data-testid="stRadio"] label p { font-size: 0.96rem !important; } h1 { font-size: 1.65rem !important; } h2 { font-size: 1.35rem !important; } h3 { font-size: 1.15rem !important; } } @media (max-width: 420px) { [data-testid="stHorizontalBlock"] > [data-testid="column"] { min-width: 100% !important; flex-basis: 100% !important; } } /* Keep the sidebar readable on every screen size */ @media (max-width: 700px) { [data-testid="stSidebar"] { min-width: 260px !important; width: 260px !important; } [data-testid="stSidebar"] [data-testid="stRadio"] label, [data-testid="stSidebar"] [data-testid="stRadio"] label p { font-size: 0.96rem !important; } } 
[data-testid="stForm"] label,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #f0d69a !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

[data-testid="stForm"] input,
[data-testid="stForm"] select,
[data-testid="stForm"] textarea {
    color: #102139 !important;
    font-size: 1rem !important;
}</style>""", unsafe_allow_html=True)

TITLE="⚓ MARITIME QUANTUM INTELLIGENCE PLATFORM"
MODULES=["Executive Dashboard","MQEIP & ERP","Marine Operations","Fuel Efficiency & BBM","QHSSE & Risk","AIS Vessel Tracking","DPR Master Database","Bunker Intelligence","Cargo Intelligence","Crew & Certificates","Maintenance & Defects","Document Intelligence","Data Analytics","AI Intelligence Center","N8N Workflow Automation","Client Management"]
VESSEL_TYPES=["Tugboat","Ocean Tug","AHT","AHTS","Tanker","Cargo Vessel"]
DB=os.getenv("MQEIP_DB_PATH","mqeip_data.db")

# Table definitions are the shared data contract between modules.
COLS={
"vessels":["id","name","vessel_type","imo_mmsi","flag","status","created_at"],
"voyages":["id","vessel_id","voyage_no","origin","destination","departure_date","arrival_date","status","notes","created_at"],
"fuel_logs":["id","vessel_id","log_date","operating_mode","rpm","me_left_lph","me_right_lph","ae_lph","hours","total_liters","notes","created_at"],
"hsse_records":["id","vessel_id","record_date","category","risk_level","description","action_owner","due_date","status","created_at"],
"dpr_records":["id","vessel_id","report_date","report_no","work_activity","weather","opening_fuel_l","received_fuel_l","consumed_fuel_l","closing_fuel_l","remarks","created_at"],
"bunker_records":["id","vessel_id","record_date","fuel_type","quantity_l","supplier","unit_price","reference_no","notes","created_at"],
"cargo_records":["id","vessel_id","record_date","cargo_name","quantity","unit","origin","destination","status","reference_no","created_at"],
"crew_records":["id","vessel_id","full_name","rank","nationality","join_date","leave_date","certificate","certificate_expiry","status","created_at"],
"maintenance_records":["id","vessel_id","record_date","equipment","record_type","priority","description","assigned_to","due_date","status","cost","created_at"],
"documents":["id","vessel_id","document_name","document_type","reference_no","issue_date","expiry_date","owner","status","notes","created_at"],
"clients":["id","company_name","contact_person","email","phone","country","status","notes","created_at"],
"ais_positions":["id","vessel_id","mmsi","latitude","longitude","speed_knots","course","position_time","source","created_at"],
"automation_jobs":["id","job_name","trigger","target_module","webhook_url","enabled","last_status","created_at"],
"ai_analyses":["id","module","question","analysis","created_at"],
}
SCHEMA={
"vessels":"id TEXT PRIMARY KEY,name TEXT NOT NULL,vessel_type TEXT,imo_mmsi TEXT,flag TEXT,status TEXT,created_at TEXT",
"voyages":"id TEXT PRIMARY KEY,vessel_id TEXT,voyage_no TEXT,origin TEXT,destination TEXT,departure_date TEXT,arrival_date TEXT,status TEXT,notes TEXT,created_at TEXT",
"fuel_logs":"id TEXT PRIMARY KEY,vessel_id TEXT,log_date TEXT,operating_mode TEXT,rpm REAL,me_left_lph REAL,me_right_lph REAL,ae_lph REAL,hours REAL,total_liters REAL,notes TEXT,created_at TEXT",
"hsse_records":"id TEXT PRIMARY KEY,vessel_id TEXT,record_date TEXT,category TEXT,risk_level TEXT,description TEXT,action_owner TEXT,due_date TEXT,status TEXT,created_at TEXT",
"dpr_records":"id TEXT PRIMARY KEY,vessel_id TEXT,report_date TEXT,report_no TEXT,work_activity TEXT,weather TEXT,opening_fuel_l REAL,received_fuel_l REAL,consumed_fuel_l REAL,closing_fuel_l REAL,remarks TEXT,created_at TEXT",
"bunker_records":"id TEXT PRIMARY KEY,vessel_id TEXT,record_date TEXT,fuel_type TEXT,quantity_l REAL,supplier TEXT,unit_price REAL,reference_no TEXT,notes TEXT,created_at TEXT",
"cargo_records":"id TEXT PRIMARY KEY,vessel_id TEXT,record_date TEXT,cargo_name TEXT,quantity REAL,unit TEXT,origin TEXT,destination TEXT,status TEXT,reference_no TEXT,created_at TEXT",
"crew_records":"id TEXT PRIMARY KEY,vessel_id TEXT,full_name TEXT,rank TEXT,nationality TEXT,join_date TEXT,leave_date TEXT,certificate TEXT,certificate_expiry TEXT,status TEXT,created_at TEXT",
"maintenance_records":"id TEXT PRIMARY KEY,vessel_id TEXT,record_date TEXT,equipment TEXT,record_type TEXT,priority TEXT,description TEXT,assigned_to TEXT,due_date TEXT,status TEXT,cost REAL,created_at TEXT",
"documents":"id TEXT PRIMARY KEY,vessel_id TEXT,document_name TEXT,document_type TEXT,reference_no TEXT,issue_date TEXT,expiry_date TEXT,owner TEXT,status TEXT,notes TEXT,created_at TEXT",
"clients":"id TEXT PRIMARY KEY,company_name TEXT,contact_person TEXT,email TEXT,phone TEXT,country TEXT,status TEXT,notes TEXT,created_at TEXT",
"ais_positions":"id TEXT PRIMARY KEY,vessel_id TEXT,mmsi TEXT,latitude REAL,longitude REAL,speed_knots REAL,course REAL,position_time TEXT,source TEXT,created_at TEXT",
"automation_jobs":"id TEXT PRIMARY KEY,job_name TEXT,trigger TEXT,target_module TEXT,webhook_url TEXT,enabled INTEGER,last_status TEXT,created_at TEXT",
"ai_analyses":"id TEXT PRIMARY KEY,module TEXT,question TEXT,analysis TEXT,created_at TEXT",
}
def connect():
    c=sqlite3.connect(DB,timeout=15); c.row_factory=sqlite3.Row; return c
def init_db():
    with connect() as c:
        for t,s in SCHEMA.items(): c.execute(f"CREATE TABLE IF NOT EXISTS {t} ({s})")
        c.execute("CREATE INDEX IF NOT EXISTS idx_fuel_vessel_date ON fuel_logs(vessel_id,log_date)")
        c.execute("CREATE INDEX IF NOT EXISTS idx_dpr_vessel_date ON dpr_records(vessel_id,report_date)")
        c.commit()
def read(t):
    if t not in COLS: raise ValueError("Unknown table")
    with connect() as c: return pd.read_sql_query(f"SELECT * FROM {t} ORDER BY created_at DESC",c)
def add(t,r:dict[str,Any]):
    if t not in COLS: raise ValueError("Unknown table")
    x={k:v for k,v in r.items() if k in COLS[t]}
    x.setdefault("id",str(uuid.uuid4()))
    if "created_at" in COLS[t]: x.setdefault("created_at",datetime.now().isoformat(timespec="seconds"))
    with connect() as c:
        c.execute(f"INSERT INTO {t} ({','.join(x)}) VALUES ({','.join(['?']*len(x))})",[x[k] for k in x]); c.commit()
def names():
    v=read("vessels")
    if v.empty:return [],{}
    labels=[f"{r['name']} · {r['vessel_type'] or 'Unspecified'}" for _,r in v.iterrows()]
    return labels,{label:str(row["id"]) for label,(_,row) in zip(labels,v.iterrows())}
def vessel_select(label):
    labels,mapping=names()
    if not labels:
        st.warning("Daftarkan kapal dahulu di Marine Operations agar data modul dapat terhubung."); return None
    return mapping[st.selectbox(label,labels,key="vessel_"+label)]
def with_vessel(t):
    d=read(t)
    if "vessel_id" in d and not d.empty:
        v=read("vessels"); mapping=dict(zip(v.id.astype(str),v.name.astype(str))) if not v.empty else {}
        d.insert(1,"Vessel",d.vessel_id.astype(str).map(mapping).fillna("Unassigned"))
    return d
def records(t,title):
    d=with_vessel(t); st.subheader(title)
    if d.empty: st.info("Belum ada data."); return
    st.dataframe(d,use_container_width=True,hide_index=True)
    st.download_button(f"⬇️ Export {title} CSV",d.to_csv(index=False).encode("utf-8-sig"),f"mqeip_{t}.csv","text/csv",key="export_"+t)
def form_save(msg): st.success(msg); st.rerun()
init_db()
st.title(TITLE); st.caption("Unified Maritime ERP | Marine Operations | Fuel Efficiency | QHSSE | AIS | AI | Automation | Analytics"); st.divider()
st.sidebar.title("⚓ PLATFORM NAVIGATION")
module=st.sidebar.radio("Select Module",MODULES,key="platform_navigation")
st.sidebar.divider(); st.sidebar.caption(f"MASTER PLATFORM | {len(MODULES)} modules | {len(read('vessels'))} vessels")
st.sidebar.info("Core records are shared in a SQLite database. For reliable persistence across hosted restarts/replicas, configure managed database storage.")
st.sidebar.caption("External services are not marked active before successful tests.")

if module=="Executive Dashboard":
    v,f,h,m,d,c=read("vessels"),read("fuel_logs"),read("hsse_records"),read("maintenance_records"),read("dpr_records"),read("crew_records")
    cols=st.columns(5)
    for col,label,value in zip(cols,["Registered Vessels","Fuel Records","Open HSSE","Maintenance Records","DPR Reports"],[len(v),len(f),int((h.status.astype(str).str.lower()!="closed").sum()) if not h.empty else 0,len(m),len(d)]):col.metric(label,value)
    a,b=st.columns(2)
    with a:
        st.subheader("Fleet Register")
        if not v.empty: st.dataframe(v[["name","vessel_type","status","flag"]],use_container_width=True,hide_index=True)
        else: st.info("Tambahkan kapal di Marine Operations.")
        if not f.empty:
            agg=f.groupby("vessel_id",as_index=False).total_liters.sum()
            nm=dict(zip(v.id,v.name)) if not v.empty else {}; agg["Vessel"]=agg.vessel_id.map(nm).fillna("Unknown")
            st.plotly_chart(px.bar(agg,x="Vessel",y="total_liters",title="Recorded Fuel Consumption (L)"),use_container_width=True)
    with b:
        st.subheader("Operational Attention")
        st.metric("Open HSSE",int((h.status.astype(str).str.lower()!="closed").sum()) if not h.empty else 0)
        st.metric("Open Maintenance",int(m.status.astype(str).str.lower().isin(["open","planned","in progress"]).sum()) if not m.empty else 0)
        if not c.empty:
            ex=pd.to_datetime(c.certificate_expiry,errors="coerce"); now=pd.Timestamp.today().normalize()
            st.metric("Certificates Expiring in 30 Days",int(((ex>=now)&(ex<=now+pd.Timedelta(days=30))).sum()))
        st.write("AIS: not verified"); st.write("AI external provider: not configured"); st.write("n8n: not configured")

elif module=="MQEIP & ERP":
    st.subheader("🧭 MQEIP & ERP")
    tabs=st.tabs(["Operations","Business Records","Database Status"])
    with tabs[0]:
        st.metric("Fleet",len(read("vessels"))); st.metric("Voyages",len(read("voyages"))); records("voyages","Voyage Register")
    with tabs[1]:
        for t in ["clients","bunker_records","cargo_records","documents"]:st.write(f"**{t.replace('_',' ').title()}:** {len(read(t))} records")
    with tabs[2]:
        st.write(f"Database path: `{DB}`"); st.write(f"Shared tables: {len(COLS)}")
        st.warning("For Streamlit Cloud production, confirm persistent storage or use a managed database; local SQLite may not persist across restarts.")

elif module=="Marine Operations":
    t1,t2=st.tabs(["Vessel Register","Voyage Operations"])
    with t1:
        with st.form("vessel_form",clear_on_submit=True):
            name=st.text_input("Vessel Name"); typ=st.selectbox("Vessel Type",VESSEL_TYPES)
            a,b,c=st.columns(3); imo=a.text_input("IMO / MMSI (optional)"); flag=b.text_input("Flag"); status=c.selectbox("Status",["Active","Standby","In Port","Maintenance","Inactive"])
            sub=st.form_submit_button("➕ Add Vessel",use_container_width=True)
        if sub:
            v=read("vessels"); n=name.strip()
            if not n:st.warning("Vessel Name wajib diisi.")
            elif not v.empty and v.name.astype(str).str.casefold().eq(n.casefold()).any():st.warning("Nama kapal sudah terdaftar.")
            else:add("vessels",dict(name=n,vessel_type=typ,imo_mmsi=imo.strip(),flag=flag.strip(),status=status)); form_save(f"Kapal {n} disimpan.")
        records("vessels","Registered Vessels")
    with t2:
        vid=vessel_select("Voyage vessel")
        if vid:
            with st.form("voyage_form",clear_on_submit=True):
                no=st.text_input("Voyage / Job Number"); origin=st.text_input("Origin"); dest=st.text_input("Destination")
                a,b=st.columns(2); dep=a.date_input("Departure Date"); arr=b.date_input("Expected Arrival")
                status=st.selectbox("Status",["Planned","In Progress","Completed","Cancelled"]); notes=st.text_area("Notes")
                sub=st.form_submit_button("Save Voyage")
            if sub:
                if not no.strip():st.warning("Voyage Number wajib diisi.")
                else:add("voyages",dict(vessel_id=vid,voyage_no=no.strip(),origin=origin,destination=dest,departure_date=str(dep),arrival_date=str(arr),status=status,notes=notes));form_save("Voyage tersimpan.")

elif module=="Fuel Efficiency & BBM":
    st.subheader("⛽ Fuel Efficiency & BBM"); vid=vessel_select("Fuel vessel")
    if vid:
        with st.form("fuel_form",clear_on_submit=True):
            dt=st.date_input("Report Date"); mode=st.selectbox("Operating Mode",["Free Sailing","Economical Sailing","Maneuvering","Towing","Anchor Handling","DP Operation","Standby","Port / Idle"])
            rpm=st.number_input("Main Engine RPM",0,3000,800,50)
            a,b,c,d=st.columns(4); left=a.number_input("ME Kiri (L/h)",0.0); right=b.number_input("ME Kanan (L/h)",0.0); ae=c.number_input("AE Total (L/h)",0.0); hours=d.number_input("Hours",0.0,24.0,24.0,.5)
            notes=st.text_area("Notes"); sub=st.form_submit_button("Save Fuel Record")
        if sub:
            total=(left+right+ae)*hours
            add("fuel_logs",dict(vessel_id=vid,log_date=str(dt),operating_mode=mode,rpm=rpm,me_left_lph=left,me_right_lph=right,ae_lph=ae,hours=hours,total_liters=total,notes=notes))
            st.success(f"Total consumption saved: {total:,.2f} L");st.rerun()
    f=read("fuel_logs")
    if not f.empty:st.metric("Total Consumption (L)",f"{f.total_liters.sum():,.2f}");st.plotly_chart(px.line(f.sort_values("log_date"),x="log_date",y="total_liters",color="vessel_id",markers=True),use_container_width=True)
    records("fuel_logs","Fuel Records")

elif module=="QHSSE & Risk":
    vid=vessel_select("HSSE vessel")
    if vid:
        with st.form("hsse_form",clear_on_submit=True):
            dt=st.date_input("Record Date"); cat=st.selectbox("Category",["Safety","Health","Environment","Security","Quality","Near Miss","Incident","Audit Finding"]); risk=st.selectbox("Risk Level",["Low","Medium","High","Critical"])
            desc=st.text_area("Finding / Hazard"); owner=st.text_input("Action Owner"); due=st.date_input("Due Date"); status=st.selectbox("Status",["Open","In Progress","Closed"]); sub=st.form_submit_button("Save QHSSE")
        if sub:
            if not desc.strip():st.warning("Description wajib diisi.")
            else:add("hsse_records",dict(vessel_id=vid,record_date=str(dt),category=cat,risk_level=risk,description=desc,action_owner=owner,due_date=str(due),status=status));form_save("QHSSE record tersimpan.")
    records("hsse_records","QHSSE Register")
    h=read("hsse_records")
    if not h.empty:st.plotly_chart(px.histogram(h,x="risk_level",color="status"),use_container_width=True)

elif module=="AIS Vessel Tracking":
    st.subheader("📡 AIS Vessel Tracking");st.warning("Live AIS hanya aktif setelah provider dan endpoint berhasil diverifikasi.")
    base=os.getenv("MQEIP_AIS_BACKEND_URL","").strip().rstrip("/"); endpoint=os.getenv("MQEIP_AIS_POSITIONS_ENDPOINT","/api/v1/ais/positions")
    if base:
        if st.button("Test AIS Backend"):
            try:
                r=requests.get(base+endpoint,timeout=12);st.write("HTTP status:",r.status_code)
                if r.ok:
                    st.success("Endpoint merespons sukses; payload masih perlu diverifikasi."); 
                    try:st.json(r.json())
                    except ValueError:st.code(r.text[:3000])
                else:st.error("Endpoint tidak merespons sukses. Periksa URL/auth/log backend.")
            except requests.RequestException as e:st.error(f"Connection failed: {e}")
    else:st.info("Set MQEIP_AIS_BACKEND_URL pada secrets/environment setelah endpoint backend yang benar dikonfirmasi.")
    records("ais_positions","Stored AIS Positions")

elif module=="DPR Master Database":
    vid=vessel_select("DPR vessel")
    if vid:
        with st.form("dpr_form",clear_on_submit=True):
            dt=st.date_input("Report Date"); no=st.text_input("DPR Number"); activity=st.text_area("Work Activity"); weather=st.selectbox("Weather",["Good","Moderate","Bad","Not Recorded"])
            a,b,c,d=st.columns(4); opening=a.number_input("Opening Fuel L",0.0); received=b.number_input("Received L",0.0); consumed=c.number_input("Consumed L",0.0); closing=d.number_input("Closing Fuel L",0.0); remarks=st.text_area("Remarks"); sub=st.form_submit_button("Save DPR")
        if sub:
            if not no.strip():st.warning("DPR Number wajib diisi.")
            else:add("dpr_records",dict(vessel_id=vid,report_date=str(dt),report_no=no,work_activity=activity,weather=weather,opening_fuel_l=opening,received_fuel_l=received,consumed_fuel_l=consumed,closing_fuel_l=closing,remarks=remarks));form_save("DPR tersimpan.")
    records("dpr_records","DPR Master Database")

elif module=="Bunker Intelligence":
    vid=vessel_select("Bunker vessel")
    if vid:
        with st.form("bunker_form",clear_on_submit=True):
            dt=st.date_input("Bunker Date"); ft=st.selectbox("Fuel Type",["HSD / MGO","MFO","VLSFO","Other"]); qty=st.number_input("Quantity (L)",0.0,step=100.0); supplier=st.text_input("Supplier"); price=st.number_input("Unit Price per L",0.0); ref=st.text_input("Reference"); notes=st.text_area("Notes"); sub=st.form_submit_button("Save Bunker")
        if sub:
            if qty<=0:st.warning("Quantity harus lebih besar dari nol.")
            else:add("bunker_records",dict(vessel_id=vid,record_date=str(dt),fuel_type=ft,quantity_l=qty,supplier=supplier,unit_price=price,reference_no=ref,notes=notes));form_save("Bunker record tersimpan.")
    b=read("bunker_records")
    if not b.empty:st.metric("Bunker Received (L)",f"{b.quantity_l.sum():,.2f}")
    records("bunker_records","Bunker Records")

elif module=="Cargo Intelligence":
    vid=vessel_select("Cargo vessel")
    if vid:
        with st.form("cargo_form",clear_on_submit=True):
            dt=st.date_input("Record Date"); cargo=st.text_input("Cargo / Job"); qty=st.number_input("Quantity",0.0); unit=st.selectbox("Unit",["MT","m³","Units","Containers","Jobs","Other"]); origin=st.text_input("Origin"); dest=st.text_input("Destination"); status=st.selectbox("Status",["Planned","Loading","In Transit","Discharging","Completed","On Hold"]); ref=st.text_input("Reference"); sub=st.form_submit_button("Save Cargo")
        if sub:
            if not cargo.strip():st.warning("Cargo description wajib diisi.")
            else:add("cargo_records",dict(vessel_id=vid,record_date=str(dt),cargo_name=cargo,quantity=qty,unit=unit,origin=origin,destination=dest,status=status,reference_no=ref));form_save("Cargo record tersimpan.")
    records("cargo_records","Cargo Records")

elif module=="Crew & Certificates":
    vid=vessel_select("Crew vessel")
    if vid:
        with st.form("crew_form",clear_on_submit=True):
            name=st.text_input("Crew Full Name"); rank=st.text_input("Rank"); nationality=st.text_input("Nationality"); joined=st.date_input("Join Date"); cert=st.text_input("Certificate"); expiry=st.date_input("Certificate Expiry"); status=st.selectbox("Status",["Active","On Leave","Signed Off","Pending"]); sub=st.form_submit_button("Save Crew")
        if sub:
            if not name.strip():st.warning("Nama crew wajib diisi.")
            else:add("crew_records",dict(vessel_id=vid,full_name=name,rank=rank,nationality=nationality,join_date=str(joined),certificate=cert,certificate_expiry=str(expiry),status=status));form_save("Crew record tersimpan.")
    c=read("crew_records")
    if not c.empty:
        ex=pd.to_datetime(c.certificate_expiry,errors="coerce");now=pd.Timestamp.today().normalize()
        a,b=st.columns(2);a.metric("Expired Certificates",int((ex<now).sum()));b.metric("Expiring in 30 Days",int(((ex>=now)&(ex<=now+pd.Timedelta(days=30))).sum()))
    records("crew_records","Crew Records")

elif module=="Maintenance & Defects":
    vid=vessel_select("Maintenance vessel")
    if vid:
        with st.form("maint_form",clear_on_submit=True):
            dt=st.date_input("Report Date"); equipment=st.text_input("Equipment"); typ=st.selectbox("Record Type",["Planned Maintenance","Breakdown","Defect","Inspection","Repair"]); priority=st.selectbox("Priority",["Low","Medium","High","Critical"]); desc=st.text_area("Description"); owner=st.text_input("Assigned To"); due=st.date_input("Due Date"); status=st.selectbox("Status",["Open","Planned","In Progress","Completed","Closed"]); cost=st.number_input("Estimated Cost",0.0);sub=st.form_submit_button("Save Maintenance")
        if sub:
            if not equipment.strip() or not desc.strip():st.warning("Equipment dan description wajib diisi.")
            else:add("maintenance_records",dict(vessel_id=vid,record_date=str(dt),equipment=equipment,record_type=typ,priority=priority,description=desc,assigned_to=owner,due_date=str(due),status=status,cost=cost));form_save("Maintenance record tersimpan.")
    records("maintenance_records","Maintenance & Defects")

elif module=="Document Intelligence":
    vid=vessel_select("Document vessel")
    if vid:
        with st.form("doc_form",clear_on_submit=True):
            name=st.text_input("Document Name"); typ=st.selectbox("Type",["Vessel Certificate","Safety","Technical","Crew Certificate","Cargo","Commercial","Audit","Other"]); ref=st.text_input("Reference"); issue=st.date_input("Issue Date"); expiry=st.date_input("Expiry Date"); owner=st.text_input("Owner"); status=st.selectbox("Status",["Valid","Pending Review","Expired","Archived"]);notes=st.text_area("Notes");sub=st.form_submit_button("Register Document")
        if sub:
            if not name.strip():st.warning("Document name wajib diisi.")
            else:add("documents",dict(vessel_id=vid,document_name=name,document_type=typ,reference_no=ref,issue_date=str(issue),expiry_date=str(expiry),owner=owner,status=status,notes=notes));form_save("Document terdaftar.")
    d=read("documents")
    if not d.empty:
        ex=pd.to_datetime(d.expiry_date,errors="coerce");now=pd.Timestamp.today().normalize()
        a,b=st.columns(2);a.metric("Expired Documents",int((ex<now).sum()));b.metric("Expiring in 30 Days",int(((ex>=now)&(ex<=now+pd.Timedelta(days=30))).sum()))
    records("documents","Document Register")

elif module=="Data Analytics":
    st.subheader("📈 Data Analytics & Data Quality");file=st.file_uploader("Upload CSV",type=["csv"])
    if file:
        try:
            try:df=pd.read_csv(io.BytesIO(file.getvalue()))
            except UnicodeDecodeError:df=pd.read_csv(io.BytesIO(file.getvalue()),encoding="latin-1")
            a,b,c,d=st.columns(4);a.metric("Rows",len(df));b.metric("Columns",len(df.columns));c.metric("Missing Cells",int(df.isna().sum().sum()));d.metric("Duplicate Rows",int(df.duplicated().sum()))
            st.dataframe(df.head(500),use_container_width=True,hide_index=True)
            quality=pd.DataFrame({"Column":df.columns.astype(str),"Data Type":df.dtypes.astype(str).values,"Missing Values":df.isna().sum().values,"Missing (%)":(df.isna().mean().values*100).round(2),"Unique Values":df.nunique().values})
            st.subheader("Quality Summary");st.dataframe(quality,use_container_width=True,hide_index=True)
            dedup=st.checkbox("Remove duplicate rows");fill=st.checkbox("Fill missing values")
            cleaned=df.drop_duplicates() if dedup else df.copy()
            if fill:
                for col in cleaned:
                    if pd.api.types.is_numeric_dtype(cleaned[col]):cleaned[col]=cleaned[col].fillna(cleaned[col].median() if cleaned[col].notna().any() else 0)
                    else:cleaned[col]=cleaned[col].fillna("")
            st.download_button("⬇️ Download analyzed / cleaned CSV",cleaned.to_csv(index=False).encode("utf-8-sig"),"mqeip_analyzed_data.csv","text/csv")
            numeric=cleaned.select_dtypes(include=np.number).columns.tolist()
            if numeric:
                col=st.selectbox("Chart numeric column",numeric);st.plotly_chart(px.histogram(cleaned,x=col,title=f"Distribution: {col}"),use_container_width=True)
        except (pd.errors.ParserError,ValueError,UnicodeDecodeError) as e:st.error(f"CSV tidak dapat dibaca: {e}")

elif module=="AI Intelligence Center":
    st.subheader("🧠 AI Intelligence Center");st.caption("Local data summaries only; this is not an external generative AI connection.")
    scope=st.selectbox("Data Scope",["Fleet","Fuel","QHSSE","DPR","Bunker","Cargo","Crew","Maintenance","Documents"]);question=st.text_area("Analysis question")
    table={"Fleet":"vessels","Fuel":"fuel_logs","QHSSE":"hsse_records","DPR":"dpr_records","Bunker":"bunker_records","Cargo":"cargo_records","Crew":"crew_records","Maintenance":"maintenance_records","Documents":"documents"}[scope]
    if st.button("Analyze Operational Data",type="primary"):
        df=with_vessel(table)
        if df.empty:analysis=f"No records available for {scope}. Add records first."
        else:
            analysis=f"Scope: {scope}. Records: {len(df)}. Available fields: {', '.join(df.columns.astype(str))}."
            if scope=="Fuel":analysis+=f" Total recorded fuel consumption: {df.total_liters.sum():,.2f} L."
            if scope=="Bunker":analysis+=f" Total recorded bunker: {df.quantity_l.sum():,.2f} L."
            if scope=="QHSSE":analysis+=f" Not closed: {(df.status.astype(str).str.lower()!='closed').sum()}."
            if question.strip():analysis+=f"\nQuestion: {question.strip()}\nThis is a data-based summary, not an external AI-generated answer."
        st.info(analysis);add("ai_analyses",dict(module=scope,question=question,analysis=analysis))
    records("ai_analyses","Analysis History")

elif module=="N8N Workflow Automation":
    st.subheader("🔁 N8N Workflow Automation");st.caption("Webhook registration and manual test; saved does not mean connected.")
    with st.form("automation_form",clear_on_submit=True):
        name=st.text_input("Workflow Name");trigger=st.selectbox("Trigger",["Manual","Scheduled","New DPR","High Risk HSSE","Maintenance Due","Certificate Expiry"]);target=st.selectbox("Target Module",MODULES);url=st.text_input("HTTPS Webhook URL");enabled=st.checkbox("Enable workflow record");sub=st.form_submit_button("Save Workflow")
    if sub:
        if not name.strip():st.warning("Workflow name wajib diisi.")
        elif url.strip() and not url.strip().startswith("https://"):st.warning("Webhook harus menggunakan HTTPS.")
        else:add("automation_jobs",dict(job_name=name,trigger=trigger,target_module=target,webhook_url=url,enabled=int(enabled),last_status="Not tested"));form_save("Workflow record tersimpan.")
    jobs=read("automation_jobs")
    if not jobs.empty:
        st.dataframe(jobs,use_container_width=True,hide_index=True);choices={f"{r.job_name} · {r.id[:8]}":r for _,r in jobs.iterrows()};sel=st.selectbox("Workflow to test",list(choices))
        if st.button("Test Webhook (POST)"):
            row=choices[sel];url=str(row.webhook_url or "")
            if not url.startswith("https://"):st.error("HTTPS webhook belum diisi.")
            else:
                try:
                    resp=requests.post(url,json={"source":"MQEIP","workflow":row.job_name,"test":True,"timestamp":datetime.now().isoformat()},timeout=15)
                    st.write("HTTP status:",resp.status_code)
                    st.success("Webhook HTTP sukses; verifikasi eksekusi di n8n.") if resp.ok else st.error("Webhook returned non-2xx.")
                    with connect() as con:con.execute("UPDATE automation_jobs SET last_status=? WHERE id=?",(f"HTTP {resp.status_code}",row.id));con.commit()
                except requests.RequestException as e:st.error(f"Webhook test failed: {e}")

elif module=="Client Management":
    st.subheader("🏢 Client Management")
    with st.form("client_form",clear_on_submit=True):
        company=st.text_input("Company Name");contact=st.text_input("Contact Person");a,b=st.columns(2);email=a.text_input("Email");phone=b.text_input("Phone");country=st.text_input("Country");status=st.selectbox("Status",["Prospect","Active","Onboarding","Inactive"]);notes=st.text_area("Notes");sub=st.form_submit_button("Save Client")
    if sub:
        if not company.strip():st.warning("Company name wajib diisi.")
        else:add("clients",dict(company_name=company,contact_person=contact,email=email,phone=phone,country=country,status=status,notes=notes));form_save("Client tersimpan.")
    records("clients","Client Register")

st.divider()
a,b=st.columns(2);a.caption("MQEIP | MARITIME QUANTUM INTELLIGENCE PLATFORM");b.caption("Integrated Core Edition | Version 2.0")
