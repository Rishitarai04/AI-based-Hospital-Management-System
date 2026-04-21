import streamlit as st
from datetime import date, datetime, timedelta
import random

st.set_page_config(
    page_title="MediCare+ Hospital",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background: linear-gradient(135deg, #f4f9ff 0%, #eafaf1 100%);
    }

    /* Hide default header padding */
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #0a84ff 0%, #34c759 100%);
        color: white;
        padding: 2.2rem 2rem;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(10, 132, 255, 0.25);
        margin-bottom: 1.5rem;
    }
    .hero h1 { color: white; margin: 0; font-size: 2.1rem; }
    .hero p  { color: #e8f4ff; margin: 0.4rem 0 0 0; font-size: 1.05rem; }

    /* Generic card */
    .card {
        background: white;
        padding: 1.4rem 1.4rem;
        border-radius: 16px;
        box-shadow: 0 4px 18px rgba(20, 80, 160, 0.08);
        border: 1px solid #e6eef8;
        margin-bottom: 1rem;
    }
    .card h3 { margin-top: 0; color: #0a84ff; }

    /* Role selection card */
    .role-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 6px 22px rgba(10, 132, 255, 0.10);
        border: 2px solid transparent;
        transition: all .2s ease;
    }
    .role-card:hover {
        border-color: #0a84ff;
        transform: translateY(-4px);
    }
    .role-icon { font-size: 3.5rem; margin-bottom: .5rem; }
    .role-title { font-size: 1.4rem; font-weight: 700; color: #1c3d5a; }
    .role-sub  { color: #5a7184; font-size: .95rem; }

    /* Specialist tile */
    .spec-tile {
        background: white;
        padding: 1.2rem;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0 3px 14px rgba(0,0,0,0.05);
        border: 1px solid #e6eef8;
        height: 100%;
    }
    .spec-tile .ico { font-size: 2.2rem; }
    .spec-tile .name { font-weight: 600; color: #1c3d5a; margin-top: .3rem; }
    .spec-tile .fee  { color: #34c759; font-size: .85rem; }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0a84ff 0%, #34c759 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: .55rem 1.2rem;
        font-weight: 600;
        transition: all .2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(10, 132, 255, 0.3);
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #eafaf1 100%);
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0;
        font-size: 1.6rem;
        font-weight: 800;
        color: #0a84ff;
        border-bottom: 2px solid #e6eef8;
        margin-bottom: 1rem;
    }

    /* Chat bubbles */
    .chat-user {
        background: #0a84ff; color: white; padding: .7rem 1rem;
        border-radius: 14px 14px 2px 14px; margin: .4rem 0 .4rem auto;
        max-width: 75%; width: fit-content;
    }
    .chat-bot {
        background: white; color: #1c3d5a; padding: .7rem 1rem;
        border-radius: 14px 14px 14px 2px; margin: .4rem auto .4rem 0;
        max-width: 75%; width: fit-content;
        border: 1px solid #e6eef8;
    }

    /* Status pills */
    .pill { padding: .25rem .7rem; border-radius: 999px; font-size: .8rem; font-weight: 600; }
    .pill-green { background:#e6f9ed; color:#1f8a3b; }
    .pill-blue  { background:#e6f0ff; color:#0a4fb3; }
    .pill-amber { background:#fff4e0; color:#a86b00; }
    </style>
    """,
    unsafe_allow_html=True,
)

def init_state():
    defaults = {
        "page": "landing",          
        "auth_mode": "login",       
        "role": None,               
        "user_name": "",
        "appointments": [],         
        "doctor_appointments": [    
            {"patient": "Rahul Sharma", "age": 32, "time": "10:00 AM", "date": str(date.today()), "reason": "Fever & cough", "status": "Upcoming"},
            {"patient": "Priya Verma", "age": 28, "time": "11:30 AM", "date": str(date.today()), "reason": "Skin rash", "status": "Upcoming"},
            {"patient": "Amit Kumar", "age": 45, "time": "02:00 PM", "date": str(date.today() + timedelta(days=1)), "reason": "Back pain", "status": "Upcoming"},
        ],
        "prescriptions": [],
        "doctor_notes": [],
        "availability": {"start": "09:00", "end": "17:00", "days": "Mon–Sat"},
        "chat_history": [
            {"role": "bot", "msg": "👋 Hi! I'm MediBot. How can I help you today?"}
        ],
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

SPECIALISTS = [
    {"name": "General Physician", "icon": "🩺", "fee": "₹500",  "doctor": "Dr. Anil Mehta"},
    {"name": "Dermatologist",     "icon": "🧴", "fee": "₹700",  "doctor": "Dr. Neha Sharma"},
    {"name": "Cardiologist",      "icon": "❤️", "fee": "₹1200", "doctor": "Dr. Rajesh Iyer"},
    {"name": "Orthopedic",        "icon": "🦴", "fee": "₹900",  "doctor": "Dr. Sandeep Rao"},
    {"name": "Pediatrician",      "icon": "👶", "fee": "₹600",  "doctor": "Dr. Kavita Joshi"},
    {"name": "ENT Specialist",    "icon": "👂", "fee": "₹650",  "doctor": "Dr. Manish Gupta"},
]

TIME_SLOTS = ["09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
              "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"]

DUMMY_REPORTS = [
    {"date": "2025-03-12", "type": "Blood Test (CBC)",  "doctor": "Dr. Anil Mehta",   "status": "Normal"},
    {"date": "2025-02-04", "type": "X-Ray Chest",       "doctor": "Dr. Sandeep Rao",  "status": "Normal"},
    {"date": "2024-12-20", "type": "Skin Allergy Test", "doctor": "Dr. Neha Sharma",  "status": "Mild"},
    {"date": "2024-10-15", "type": "ECG",               "doctor": "Dr. Rajesh Iyer",  "status": "Normal"},
]

CHATBOT_REPLIES = [
    "🩺 Please consult a doctor for an accurate diagnosis.",
    "💊 Make sure to take prescribed medicines on time.",
    "💧 Stay hydrated and get enough rest.",
    "📅 You can book an appointment from the 'Book Appointment' section.",
    "🚑 In case of emergency, please dial your local helpline immediately.",
    "🥗 A balanced diet supports faster recovery.",
    "🧘 Mild exercise and good sleep improve overall health.",
]


def go(page):
    st.session_state.page = page
    st.rerun()

def logout():
    for k in ["page", "role", "user_name"]:
        st.session_state[k] = "landing" if k == "page" else (None if k == "role" else "")
    st.rerun()

def hero(title, subtitle):
    st.markdown(
        f"""<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )


def landing_page():
    st.markdown(
        """
        <div style="text-align:center; padding: 1.5rem 0 1rem 0;">
            <div style="font-size:3.5rem;">🏥</div>
            <h1 style="margin:0; color:#0a84ff;">MediCare+ Hospital</h1>
            <p style="color:#5a7184; font-size:1.05rem;">
                AI-powered Hospital Management System • Trusted Care, Smarter Health
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 👋 Welcome! Please choose your role to continue")
    st.write("")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown(
            """
            <div class="role-card">
                <div class="role-icon">🧑‍⚕️</div>
                <div class="role-title">I'm a Patient</div>
                <div class="role-sub">Book appointments, view reports & chat with MediBot</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Continue as Patient", use_container_width=True, key="role_patient"):
            st.session_state.role = "patient"
            go("patient_auth")

    with c2:
        st.markdown(
            """
            <div class="role-card">
                <div class="role-icon">👨‍⚕️</div>
                <div class="role-title">I'm a Doctor</div>
                <div class="role-sub">Manage appointments, prescriptions & availability</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Continue as Doctor", use_container_width=True, key="role_doctor"):
            st.session_state.role = "doctor"
            go("doctor_auth")

    st.write("")
    st.markdown(
        """
        <div style="text-align:center; color:#7d92a8; font-size:.85rem; margin-top:1rem;">
            🛡️ Secure • 🤖 AI-Assisted • 📱 Responsive — © 2025 MediCare+
        </div>
        """,
        unsafe_allow_html=True,
    )

def patient_auth_page():
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Back"):
            go("landing")

    hero("🧑‍⚕️ Patient Portal", "Login or create a new account to continue")

    tab_login, tab_signup = st.tabs(["🔐 Login", "📝 Sign Up"])

    with tab_login:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Patient Login")
            email = st.text_input("📧 Email", key="p_login_email", placeholder="you@example.com")
            pwd   = st.text_input("🔒 Password", type="password", key="p_login_pwd")
            if st.button("Login", use_container_width=True, key="p_login_btn"):
                if email and pwd:
                    st.session_state.user_name = email.split("@")[0].title()
                    st.success(f"Welcome back, {st.session_state.user_name}! ✅")
                    go("patient_app")
                else:
                    st.error("Please fill in all fields.")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab_signup:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Create Patient Account")
            name  = st.text_input("👤 Full Name", key="p_su_name")
            email = st.text_input("📧 Email", key="p_su_email")
            phone = st.text_input("📱 Phone", key="p_su_phone")
            pwd   = st.text_input("🔒 Password", type="password", key="p_su_pwd")
            if st.button("Sign Up", use_container_width=True, key="p_su_btn"):
                if name and email and pwd:
                    st.session_state.user_name = name
                    st.success(f"Account created! Welcome, {name} 🎉")
                    go("patient_app")
                else:
                    st.error("Please fill in all required fields.")
            st.markdown('</div>', unsafe_allow_html=True)

def doctor_auth_page():
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Back"):
            go("landing")

    hero("👨‍⚕️ Doctor Portal", "Login to access your dashboard")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Doctor Login")
    doc_id = st.text_input("🆔 Doctor ID / Email", key="d_id", placeholder="doctor@medicare.com")
    pwd    = st.text_input("🔒 Password", type="password", key="d_pwd")
    if st.button("Login", use_container_width=True, key="d_login_btn"):
        if doc_id and pwd:
            st.session_state.user_name = "Dr. " + doc_id.split("@")[0].title()
            st.success(f"Welcome, {st.session_state.user_name} 🩺")
            go("doctor_app")
        else:
            st.error("Please enter your credentials.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.info("💡 Demo tip: enter any email and password to log in.")

def patient_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🏥 MediCare+</div>', unsafe_allow_html=True)
        st.caption(f"👤 Logged in as **{st.session_state.user_name or 'Patient'}**")
        st.markdown("---")
        choice = st.radio(
            "Navigation",
            ["🏠 Dashboard", "📅 Book Appointment", "📋 My Appointments",
             "📄 Medical Reports", "🤖 AI Chatbot", "⚙️ Profile"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        return choice

def patient_dashboard_home():
    hero(f"Welcome back, {st.session_state.user_name or 'Patient'} 👋",
         "Your health dashboard at a glance")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📅 Upcoming", len([a for a in st.session_state.appointments if a["status"] == "Upcoming"]))
    c2.metric("📄 Reports", len(DUMMY_REPORTS))
    c3.metric("🩺 Specialists", len(SPECIALISTS))
    c4.metric("🤖 AI Support", "24/7")

    st.markdown("### 🚀 Quick Actions")
    q1, q2, q3 = st.columns(3)
    with q1:
        st.markdown('<div class="card"><h3>📅 Book</h3><p>Schedule a new appointment with a specialist.</p></div>', unsafe_allow_html=True)
    with q2:
        st.markdown('<div class="card"><h3>📄 Reports</h3><p>View your latest medical reports & history.</p></div>', unsafe_allow_html=True)
    with q3:
        st.markdown('<div class="card"><h3>🤖 MediBot</h3><p>Ask quick health questions to our AI assistant.</p></div>', unsafe_allow_html=True)

    st.markdown("### 💡 Health Tip of the Day")
    tips = [
        "💧 Drink at least 8 glasses of water daily.",
        "🚶 A 30-minute walk improves heart health.",
        "🥦 Add more greens to your meals.",
        "😴 7–8 hours of sleep keeps you sharp.",
    ]
    st.info(random.choice(tips))

def patient_book_appointment():
    hero("📅 Book Appointment", "Choose a specialist and pick a convenient slot")

    st.markdown("#### 🩺 Select a Specialist")
    cols = st.columns(3)
    for i, sp in enumerate(SPECIALISTS):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="spec-tile">
                    <div class="ico">{sp['icon']}</div>
                    <div class="name">{sp['name']}</div>
                    <div style="color:#5a7184;font-size:.85rem;">{sp['doctor']}</div>
                    <div class="fee">Fee: {sp['fee']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Select", key=f"sel_{i}", use_container_width=True):
                st.session_state["selected_spec"] = sp

    selected = st.session_state.get("selected_spec")
    if selected:
        st.markdown("---")
        st.markdown(f"### 🗓️ Booking with **{selected['doctor']}** — {selected['name']} {selected['icon']}")

        c1, c2 = st.columns(2)
        with c1:
            appt_date = st.date_input("📅 Choose Date",
                                      min_value=date.today(),
                                      max_value=date.today() + timedelta(days=30))
        with c2:
            slot = st.selectbox("⏰ Available Slots", TIME_SLOTS)

        reason = st.text_area("📝 Reason for visit (optional)", height=80)

        if st.button("✅ Confirm Booking", use_container_width=True):
            st.session_state.appointments.append({
                "specialist": selected["name"],
                "doctor": selected["doctor"],
                "date": str(appt_date),
                "time": slot,
                "reason": reason or "General consultation",
                "fee": selected["fee"],
                "status": "Upcoming",
            })
            st.success(f"🎉 Appointment confirmed with {selected['doctor']} on {appt_date} at {slot}")
            st.balloons()
            st.session_state["selected_spec"] = None

def patient_my_appointments():
    hero("📋 My Appointments", "All your upcoming and past visits in one place")

    if not st.session_state.appointments:
        st.info("You have no appointments yet. Book one from the **Book Appointment** section.")
        return

    for i, a in enumerate(st.session_state.appointments):
        pill_class = "pill-green" if a["status"] == "Upcoming" else "pill-blue"
        st.markdown(
            f"""
            <div class="card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <h3 style="margin:0;">🩺 {a['specialist']}</h3>
                  <div style="color:#5a7184;">{a['doctor']}</div>
                  <div style="margin-top:.4rem;">📅 <b>{a['date']}</b> &nbsp; ⏰ <b>{a['time']}</b></div>
                  <div style="color:#5a7184; margin-top:.3rem;">📝 {a['reason']}</div>
                </div>
                <div style="text-align:right;">
                  <span class="pill {pill_class}">{a['status']}</span>
                  <div style="margin-top:.5rem; color:#34c759; font-weight:600;">{a['fee']}</div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"❌ Cancel", key=f"cancel_{i}"):
            st.session_state.appointments.pop(i)
            st.rerun()

def patient_reports():
    hero("📄 Medical Reports", "Your recent diagnostic reports & history")
    for r in DUMMY_REPORTS:
        color = "pill-green" if r["status"] == "Normal" else "pill-amber"
        st.markdown(
            f"""
            <div class="card">
              <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                  <h3 style="margin:0;">🧪 {r['type']}</h3>
                  <div style="color:#5a7184;">{r['doctor']} • {r['date']}</div>
                </div>
                <span class="pill {color}">{r['status']}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.expander("View report details"):
            st.write(f"**Test:** {r['type']}")
            st.write(f"**Date:** {r['date']}")
            st.write(f"**Doctor:** {r['doctor']}")
            st.write(f"**Result:** {r['status']}")
            st.write("**Notes:** All values are within normal medical range. Continue current routine.")
            st.download_button("⬇️ Download (demo)", data=f"MediCare+ Report\n{r}".encode(),
                               file_name=f"report_{r['date']}.txt")

def patient_chatbot():
    hero("🤖 MediBot — AI Health Assistant", "Ask quick health questions (demo responses)")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        cls = "chat-user" if msg["role"] == "user" else "chat-bot"
        prefix = "🧑 " if msg["role"] == "user" else "🤖 "
        st.markdown(f'<div class="{cls}">{prefix}{msg["msg"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    user_msg = st.chat_input("Type your health question…")
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "msg": user_msg})
        reply = random.choice(CHATBOT_REPLIES)
        st.session_state.chat_history.append({"role": "bot", "msg": reply})
        st.rerun()

    if st.button("🧹 Clear chat"):
        st.session_state.chat_history = [{"role": "bot", "msg": "👋 Chat cleared. How can I help?"}]
        st.rerun()

def patient_profile():
    hero("⚙️ Profile", "Manage your personal details")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("👤 Full Name", value=st.session_state.user_name or "Patient")
        st.text_input("📧 Email", value="patient@medicare.com")
        st.number_input("🎂 Age", min_value=1, max_value=120, value=28)
    with c2:
        st.text_input("📱 Phone", value="+91 98765 43210")
        st.selectbox("🩸 Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
        st.text_input("🏠 Address", value="Mumbai, India")
    if st.button("💾 Save Changes"):
        st.success("Profile updated successfully ✅")
    st.markdown('</div>', unsafe_allow_html=True)

def patient_app():
    choice = patient_sidebar()
    if   choice == "🏠 Dashboard":         patient_dashboard_home()
    elif choice == "📅 Book Appointment":  patient_book_appointment()
    elif choice == "📋 My Appointments":   patient_my_appointments()
    elif choice == "📄 Medical Reports":   patient_reports()
    elif choice == "🤖 AI Chatbot":        patient_chatbot()
    elif choice == "⚙️ Profile":           patient_profile()

def doctor_sidebar():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">🏥 MediCare+</div>', unsafe_allow_html=True)
        st.caption(f"👨‍⚕️ {st.session_state.user_name or 'Doctor'}")
        st.markdown("---")
        choice = st.radio(
            "Navigation",
            ["🏠 Dashboard", "📅 Appointments", "👥 Patients",
             "📄 Past Reports", "💊 Prescriptions",
             "⏰ Availability", "📝 Notes"],
            label_visibility="collapsed",
        )
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            logout()
        return choice

def doctor_home():
    hero(f"Welcome, {st.session_state.user_name or 'Doctor'} 🩺",
         "Today's overview of your practice")

    today_appts = [a for a in st.session_state.doctor_appointments if a["date"] == str(date.today())]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📅 Today", len(today_appts))
    c2.metric("👥 Total Patients", len(st.session_state.doctor_appointments))
    c3.metric("💊 Prescriptions", len(st.session_state.prescriptions))
    c4.metric("📝 Notes", len(st.session_state.doctor_notes))

    st.markdown("### 📋 Today's Schedule")
    if today_appts:
        st.table([{"Time": a["time"], "Patient": a["patient"],
                   "Reason": a["reason"], "Status": a["status"]} for a in today_appts])
    else:
        st.info("No appointments scheduled for today.")

def doctor_appointments():
    hero("📅 Upcoming Appointments", "Manage your patient bookings")
    st.dataframe(
        [{"Date": a["date"], "Time": a["time"], "Patient": a["patient"],
          "Age": a["age"], "Reason": a["reason"], "Status": a["status"]}
         for a in st.session_state.doctor_appointments],
        use_container_width=True,
        hide_index=True,
    )

def doctor_patients():
    hero("👥 Patient Details", "Quick view of patient profiles")
    for p in st.session_state.doctor_appointments:
        st.markdown(
            f"""
            <div class="card">
              <h3>🧑 {p['patient']} <span style="color:#5a7184; font-size:.9rem;">• Age {p['age']}</span></h3>
              <div>📅 {p['date']} • ⏰ {p['time']}</div>
              <div style="color:#5a7184; margin-top:.3rem;">📝 {p['reason']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

def doctor_past_reports():
    hero("📄 Past Reports", "Recent reports across patients")
    st.dataframe(DUMMY_REPORTS, use_container_width=True, hide_index=True)

def doctor_prescriptions():
    hero("💊 Write Prescription", "Create a prescription for a patient")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    patient = st.selectbox("👤 Select Patient",
                           [p["patient"] for p in st.session_state.doctor_appointments])
    diagnosis = st.text_input("🔍 Diagnosis", placeholder="e.g. Viral Fever")
    medicines = st.text_area("💊 Medicines (one per line)",
                             placeholder="Paracetamol 500mg — 1 tab x 3 times/day x 5 days\nCetirizine 10mg — 1 tab at night x 3 days",
                             height=130)
    advice = st.text_area("📝 Advice", placeholder="Plenty of fluids, rest, follow up after 5 days.", height=80)

    if st.button("💾 Save Prescription", use_container_width=True):
        if patient and diagnosis and medicines:
            st.session_state.prescriptions.append({
                "patient": patient, "diagnosis": diagnosis,
                "medicines": medicines, "advice": advice,
                "date": str(date.today()),
            })
            st.success(f"✅ Prescription saved for {patient}")
        else:
            st.error("Please fill patient, diagnosis and medicines.")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.prescriptions:
        st.markdown("### 📜 Recent Prescriptions")
        for rx in reversed(st.session_state.prescriptions[-5:]):
            with st.expander(f"💊 {rx['patient']} — {rx['diagnosis']} ({rx['date']})"):
                st.write("**Medicines:**")
                st.code(rx["medicines"])
                st.write(f"**Advice:** {rx['advice'] or '—'}")

def doctor_availability():
    hero("⏰ Set Availability", "Define your consultation hours")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        start = st.time_input("🕘 Start Time", value=datetime.strptime(st.session_state.availability["start"], "%H:%M").time())
    with c2:
        end = st.time_input("🕔 End Time", value=datetime.strptime(st.session_state.availability["end"], "%H:%M").time())
    days = st.multiselect("📅 Working Days",
                          ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                          default=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
    if st.button("💾 Save Availability", use_container_width=True):
        st.session_state.availability = {
            "start": start.strftime("%H:%M"),
            "end": end.strftime("%H:%M"),
            "days": ", ".join(days),
        }
        st.success("✅ Availability updated")
    st.markdown('</div>', unsafe_allow_html=True)

    st.info(f"🟢 Current: **{st.session_state.availability['start']} – {st.session_state.availability['end']}** "
            f"on **{st.session_state.availability['days']}**")

def doctor_notes():
    hero("📝 Doctor's Notes", "Quick personal notes & patient history")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    note = st.text_area("✏️ Add a note", placeholder="e.g. Follow up with Mr. Sharma next week regarding BP report.", height=100)
    if st.button("➕ Add Note", use_container_width=True):
        if note.strip():
            st.session_state.doctor_notes.append({
                "note": note.strip(),
                "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            })
            st.success("Note added ✅")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.doctor_notes:
        st.markdown("### 📚 Saved Notes")
        for n in reversed(st.session_state.doctor_notes):
            st.markdown(
                f"""<div class="card">📝 {n['note']}
                <div style="color:#5a7184; font-size:.8rem; margin-top:.3rem;">🕒 {n['time']}</div></div>""",
                unsafe_allow_html=True,
            )
    else:
        st.info("No notes yet. Add your first note above.")

def doctor_app():
    choice = doctor_sidebar()
    if   choice == "🏠 Dashboard":     doctor_home()
    elif choice == "📅 Appointments":  doctor_appointments()
    elif choice == "👥 Patients":      doctor_patients()
    elif choice == "📄 Past Reports":  doctor_past_reports()
    elif choice == "💊 Prescriptions": doctor_prescriptions()
    elif choice == "⏰ Availability":  doctor_availability()
    elif choice == "📝 Notes":         doctor_notes()

page = st.session_state.page
if   page == "landing":      landing_page()
elif page == "patient_auth": patient_auth_page()
elif page == "doctor_auth":  doctor_auth_page()
elif page == "patient_app":  patient_app()
elif page == "doctor_app":   doctor_app()
else:                        landing_page()
