import streamlit as st
import pandas as pd
import plotly.express as px

# Load placement data
placement_df = pd.read_csv("data/placements.csv")

# Page configuration
st.set_page_config(
    page_title="CampusInsight | College Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# PROFESSIONAL UI STYLING
# =========================
st.markdown("""
<style>
    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
        letter-spacing: -1px;
    }
    .main-subtitle {
        font-size: 1.05rem;
        opacity: 0.72;
        margin-bottom: 1.5rem;
    }
    [data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.22);
        border-radius: 14px;
        padding: 14px 16px;
        background: rgba(128,128,128,0.06);
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    [data-testid="stMetricValue"] {
        font-weight: 750;
    }
    .section-card {
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 14px;
        padding: 16px;
        margin: 8px 0 18px 0;
        background: rgba(128,128,128,0.035);
    }
    .sidebar-brand {
        text-align: center;
        padding: 8px 0 18px 0;
    }
    .sidebar-brand .icon {
        font-size: 2.5rem;
    }
    .sidebar-brand .name {
        font-size: 1.35rem;
        font-weight: 800;
    }
    .sidebar-brand .tagline {
        font-size: 0.78rem;
        opacity: 0.65;
    }
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 10px;
        font-weight: 650;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 650;
    }

    .hero-banner {
        border-radius: 20px;
        padding: 28px 30px;
        margin: 6px 0 22px 0;
        border: 1px solid rgba(128,128,128,0.22);
        background: linear-gradient(135deg, rgba(99,102,241,0.13), rgba(14,165,233,0.10));
    }
    .hero-banner h1 { margin: 0 0 8px 0; font-size: 2.25rem; }
    .hero-banner p { margin: 0; opacity: 0.75; font-size: 1.02rem; }
    .mini-card {
        border: 1px solid rgba(128,128,128,0.20);
        border-radius: 14px;
        padding: 16px;
        min-height: 105px;
        background: rgba(128,128,128,0.035);
    }
    .mini-card .emoji { font-size: 1.55rem; }
    .mini-card .title { font-weight: 750; margin-top: 5px; }
    .mini-card .text { font-size: 0.84rem; opacity: 0.68; margin-top: 3px; }
    .footer {
        text-align: center;
        padding: 28px 0 8px 0;
        opacity: 0.55;
        font-size: 0.82rem;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SIMPLE ADMIN AUTHENTICATION
# =========================
# Demo credentials for this college project
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "campus123"

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# Load student data
df = pd.read_csv("data/students.csv")

# Header
st.markdown('<div class="main-title">🎓 CampusInsight</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">College Data Analytics Platform • Student, Academic, Attendance & Placement Insights</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown(
    '''<div class="sidebar-brand">
        <div class="icon">🎓</div>
        <div class="name">CampusInsight</div>
        <div class="tagline">College Data Analytics</div>
    </div>''', unsafe_allow_html=True)
st.sidebar.markdown("### 🧭 Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Dashboard",
        "👨‍🎓 Students",
        "📊 Attendance",
        "📚 Academic Performance",
        "💼 Placement Analytics",
        "👨‍💼 Admin Dashboard"
    ]
)

# Admin login / logout
st.sidebar.divider()
if st.session_state.admin_logged_in:
    st.sidebar.success("🔓 Admin logged in")
    if st.sidebar.button("🚪 Logout", width="stretch"):
        st.session_state.admin_logged_in = False
        st.rerun()
else:
    st.sidebar.caption("🔒 Admin Dashboard is protected")

if page == "👨‍💼 Admin Dashboard" and not st.session_state.admin_logged_in:
    st.header("🔐 Admin Login")
    st.caption("Authorized administrators can manage student records and exports.")

    left, center, right = st.columns([1, 2, 1])
    with center:
        with st.form("admin_login_form"):
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter password")
            login_button = st.form_submit_button("🔓 Login", width="stretch")

            if login_button:
                if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                    st.session_state.admin_logged_in = True
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")

    st.info("Demo project credentials: username `admin` • password `campus123`")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Filters")

# Department filter
departments = ["All"] + sorted(df["Department"].dropna().astype(str).unique().tolist())

selected_department = st.sidebar.selectbox(
    "Select Department",
    departments
)
# Semester filter
semesters = ["All"] + sorted(df["Semester"].dropna().tolist(), key=lambda x: str(x))

selected_semester = st.sidebar.selectbox(
    "Select Semester",
    semesters
)
# Apply filters
filtered_df = df.copy()

if selected_department != "All":
    filtered_df = filtered_df[
        filtered_df["Department"] == selected_department
    ]

if selected_semester != "All":
    filtered_df = filtered_df[
        filtered_df["Semester"] == selected_semester
    ]


# =========================
# DASHBOARD
# =========================

if page == "🏠 Dashboard":

    st.markdown("""
    <div class="hero-banner">
        <h1>🎓 Welcome to CampusInsight</h1>
        <p>Turn college data into clear insights for students, academics, attendance and placements.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚡ Quick Access")
    q1, q2, q3, q4 = st.columns(4)
    with q1:
        st.markdown('<div class="mini-card"><div class="emoji">👨‍🎓</div><div class="title">Student Insights</div><div class="text">Search students and view individual performance.</div></div>', unsafe_allow_html=True)
    with q2:
        st.markdown('<div class="mini-card"><div class="emoji">📊</div><div class="title">Attendance</div><div class="text">Track attendance and identify warnings.</div></div>', unsafe_allow_html=True)
    with q3:
        st.markdown('<div class="mini-card"><div class="emoji">📚</div><div class="title">Academics</div><div class="text">Compare CGPA and academic performance.</div></div>', unsafe_allow_html=True)
    with q4:
        st.markdown('<div class="mini-card"><div class="emoji">💼</div><div class="title">Placements</div><div class="text">Explore companies, packages and placement rates.</div></div>', unsafe_allow_html=True)

    st.markdown("### 📊 College Overview")
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        "👨‍🎓 Total Students",
        len(filtered_df)
    )

    col2.metric(
        "📊 Average Attendance",
        f"{filtered_df['Attendance'].mean():.1f}%"
    )

    col3.metric(
        "📚 Average CGPA",
        f"{filtered_df['CGPA'].mean():.2f}"
    )

    col4.metric(
        "🏫 Departments",
        filtered_df["Department"].nunique()
    )

    high_performers = len(
        filtered_df[filtered_df["CGPA"] >= 8]
    )

    col5.metric(
        "⭐ High Performers",
        high_performers
    )

    low_attendance = len(
        filtered_df[filtered_df["Attendance"] < 75]
    )

    col6.metric(
        "⚠️ Low Attendance",
        low_attendance
    )
    st.divider()

    st.subheader("📈 Student Performance")

    fig = px.bar(
        filtered_df,
        x="Name",
        y="CGPA",
        color="Department",
        title="CGPA by Student"
    )

    st.plotly_chart(fig, width="stretch")

    st.subheader("🏆 Top 3 Students")

    top_students = filtered_df.nlargest(3, "CGPA")[
        ["Student ID", "Name", "Department", "CGPA"]
    ]

    st.dataframe(
        top_students,
        width="stretch",
        hide_index=True
    )

    st.divider()
    st.subheader("🎯 Advanced Student Insights")

    if len(filtered_df) > 0:
        insight_df = filtered_df.copy()

        # Risk classification based on attendance and CGPA
        def classify_risk(row):
            if row["Attendance"] < 75 and row["CGPA"] < 7:
                return "🔴 High Risk"
            elif row["Attendance"] < 75 or row["CGPA"] < 7:
                return "🟠 Needs Attention"
            return "🟢 On Track"

        insight_df["Risk Level"] = insight_df.apply(classify_risk, axis=1)

        i1, i2, i3, i4 = st.columns(4)
        i1.metric("🟢 On Track", int((insight_df["Risk Level"] == "🟢 On Track").sum()))
        i2.metric("🟠 Needs Attention", int((insight_df["Risk Level"] == "🟠 Needs Attention").sum()))
        i3.metric("🔴 High Risk", int((insight_df["Risk Level"] == "🔴 High Risk").sum()))
        correlation = insight_df["Attendance"].corr(insight_df["CGPA"])
        i4.metric("🔗 Attendance–CGPA", f"{correlation:.2f}" if pd.notna(correlation) else "N/A")

        insight_col1, insight_col2 = st.columns(2)

        with insight_col1:
            risk_counts = insight_df["Risk Level"].value_counts().reset_index()
            risk_counts.columns = ["Risk Level", "Students"]
            risk_fig = px.pie(
                risk_counts,
                names="Risk Level",
                values="Students",
                title="Student Risk Distribution",
                hole=0.45
            )
            st.plotly_chart(risk_fig, width="stretch")

        with insight_col2:
            dept_insights = insight_df.groupby("Department").agg(
                Students=("Student ID", "count"),
                Avg_Attendance=("Attendance", "mean"),
                Avg_CGPA=("CGPA", "mean")
            ).reset_index()
            dept_insights["Performance Score"] = (
                dept_insights["Avg_Attendance"] * 0.4
                + dept_insights["Avg_CGPA"] * 10 * 0.6
            )
            dept_insights = dept_insights.sort_values("Performance Score", ascending=False)

            dept_fig = px.bar(
                dept_insights,
                x="Department",
                y="Performance Score",
                text="Performance Score",
                title="Department Performance Score"
            )
            dept_fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            st.plotly_chart(dept_fig, width="stretch")

        st.subheader("⚠️ Students Needing Attention")
        attention_df = insight_df[insight_df["Risk Level"] != "🟢 On Track"].copy()
        if not attention_df.empty:
            attention_df = attention_df[
                ["Student ID", "Name", "Department", "Attendance", "CGPA", "Risk Level"]
            ].sort_values(["Risk Level", "CGPA"])
            st.dataframe(attention_df, width="stretch", hide_index=True)
        else:
            st.success("🎉 No students currently need attention based on the selected filters.")

        st.subheader("🔗 Attendance vs CGPA")
        scatter_fig = px.scatter(
            insight_df,
            x="Attendance",
            y="CGPA",
            color="Risk Level",
            hover_data=["Student ID", "Name", "Department"],
            size="CGPA",
            title="Relationship Between Attendance and Academic Performance"
        )
        scatter_fig.add_vline(x=75, line_dash="dash", annotation_text="75% Attendance")
        scatter_fig.add_hline(y=7, line_dash="dash", annotation_text="CGPA 7.0")
        st.plotly_chart(scatter_fig, width="stretch")

        with st.expander("ℹ️ How is the Performance Score calculated?"):
            st.write(
                "The project uses a simple demonstration score: 40% attendance + 60% CGPA "
                "(CGPA converted to a 100-point scale). This is an analytics indicator, "
                "not an official college grading rule."
            )
    else:
        st.info("No students match the selected filters, so advanced insights cannot be calculated.")

# =========================
# STUDENTS
# =========================

elif page == "👨‍🎓 Students":

    st.header("👨‍🎓 Student Details")
    st.caption("Search, compare and analyze individual student performance.")

    # Search
    search = st.text_input("🔎 Search by Student ID or Name", placeholder="Enter ID or student name...")
    student_df = filtered_df.copy()

    if search:
        student_df = student_df[
            student_df["Student ID"].astype(str).str.contains(search, case=False, na=False)
            | student_df["Name"].astype(str).str.contains(search, case=False, na=False)
        ]

    # Quick statistics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👨‍🎓 Students Found", len(student_df))
    col2.metric("📊 Avg Attendance", f"{student_df['Attendance'].mean():.1f}%" if len(student_df) else "0.0%")
    col3.metric("📚 Avg CGPA", f"{student_df['CGPA'].mean():.2f}" if len(student_df) else "0.00")
    col4.metric("⭐ CGPA ≥ 8", int((student_df["CGPA"] >= 8).sum()) if len(student_df) else 0)

    st.divider()

    if len(student_df) == 0:
        st.warning("🔍 No students found. Try another Student ID or Name.")
    else:
        # Individual student profile
        st.subheader("👤 Student Performance")
        student_options = student_df["Student ID"].astype(str) + " — " + student_df["Name"].astype(str)
        selected = st.selectbox("Select a student to view details", student_options)
        selected_id = selected.split(" — ")[0]
        student = student_df[student_df["Student ID"].astype(str) == selected_id].iloc[0]

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Student ID", str(student["Student ID"]))
        p2.metric("Department", str(student["Department"]))
        p3.metric("Attendance", f"{float(student['Attendance']):.1f}%")
        p4.metric("CGPA", f"{float(student['CGPA']):.2f}")

        if float(student["Attendance"]) < 75:
            st.error("⚠️ Attendance is below 75%. Student needs attendance improvement.")
        elif float(student["CGPA"]) >= 8:
            st.success("🌟 High-performing student!")
        else:
            st.info("📈 Student can improve performance further with consistent study.")

        st.divider()

        # Performance chart
        chart_data = pd.DataFrame({
            "Metric": ["Attendance (%)", "CGPA × 10"],
            "Value": [float(student["Attendance"]), float(student["CGPA"]) * 10]
        })
        fig = px.bar(
            chart_data,
            x="Metric",
            y="Value",
            title=f"Performance Overview — {student['Name']}",
            range_y=[0, 100],
            text="Value"
        )
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
        st.plotly_chart(fig, width="stretch")

        st.divider()

        # Student list
        st.subheader("📋 Student List")
        display_df = student_df[["Student ID", "Name", "Department", "Semester", "Attendance", "CGPA"]].copy()
        st.dataframe(display_df, width="stretch", hide_index=True)

        # Attendance warning
        low_attendance = student_df[student_df["Attendance"] < 75]
        if len(low_attendance) > 0:
            st.warning(f"⚠️ {len(low_attendance)} student(s) have attendance below 75%.")
            st.dataframe(
                low_attendance[["Student ID", "Name", "Department", "Semester", "Attendance", "CGPA"]],
                width="stretch",
                hide_index=True
            )

        # Performance categories
        st.subheader("🎯 Performance Summary")
        summary_df = student_df.copy()
        summary_df["Performance"] = summary_df["CGPA"].apply(
            lambda x: "Excellent" if x >= 8.5 else ("Good" if x >= 7 else "Needs Improvement")
        )
        summary = summary_df["Performance"].value_counts().reset_index()
        summary.columns = ["Performance", "Students"]
        summary_fig = px.pie(
            summary,
            names="Performance",
            values="Students",
            title="Student Performance Categories"
        )
        st.plotly_chart(summary_fig, width="stretch")

# =========================
# ATTENDANCE
# =========================

elif page == "📊 Attendance":
    st.header("📊 Attendance Analytics")
    st.caption("Monitor student attendance, identify risk areas, and compare department performance.")

    if filtered_df.empty:
        st.warning("No students match the selected filters.")
    else:
        # Attendance categories
        attendance = filtered_df["Attendance"].astype(float)

        avg_attendance = attendance.mean()
        above_75 = (attendance >= 75).sum()
        below_75 = (attendance < 75).sum()
        best_attendance = attendance.max()

        # KPI cards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 Average Attendance", f"{avg_attendance:.1f}%")
        col2.metric("✅ Above 75%", int(above_75))
        col3.metric("⚠️ Below 75%", int(below_75))
        col4.metric("🏆 Best Attendance", f"{best_attendance:.1f}%")

        st.divider()

        # Department-wise attendance
        st.subheader("🏫 Department-wise Attendance")
        dept_att = (
            filtered_df.groupby("Department", as_index=False)["Attendance"]
            .mean()
            .sort_values("Attendance", ascending=False)
        )

        fig_dept = px.bar(
            dept_att,
            x="Department",
            y="Attendance",
            text=dept_att["Attendance"].round(1),
            title="Average Attendance by Department",
            labels={"Attendance": "Average Attendance (%)", "Department": "Department"}
        )
        fig_dept.update_traces(texttemplate="%{text}%", textposition="outside")
        fig_dept.update_yaxes(range=[0, 100])
        st.plotly_chart(fig_dept, width="stretch")

        # Student attendance chart
        st.subheader("👨‍🎓 Student Attendance")
        student_att = filtered_df[["Student ID", "Name", "Attendance"]].copy()
        student_att["Student"] = student_att["Name"] + " (" + student_att["Student ID"] + ")"
        student_att = student_att.sort_values("Attendance", ascending=True)

        fig_student = px.bar(
            student_att,
            x="Attendance",
            y="Student",
            orientation="h",
            text=student_att["Attendance"].round(1),
            title="Attendance of Students",
            labels={"Attendance": "Attendance (%)", "Student": "Student"}
        )
        fig_student.update_traces(texttemplate="%{text}%", textposition="outside")
        fig_student.add_vline(
            x=75,
            line_dash="dash",
            annotation_text="75% Minimum",
            annotation_position="top"
        )
        fig_student.update_xaxes(range=[0, 100])
        st.plotly_chart(fig_student, width="stretch")

        # Attendance distribution
        st.subheader("📈 Attendance Distribution")
        category_df = filtered_df.copy()
        category_df["Attendance Category"] = pd.cut(
            category_df["Attendance"].astype(float),
            bins=[-float("inf"), 75, 80, 90, float("inf")],
            labels=["Critical (<75%)", "Warning (75–79%)", "Good (80–89%)", "Excellent (90%+)"] ,
            right=False
        )
        category_counts = (
            category_df["Attendance Category"]
            .value_counts()
            .reindex(["Excellent (90%+)", "Good (80–89%)", "Warning (75–79%)", "Critical (<75%)"])
            .fillna(0)
            .reset_index()
        )
        category_counts.columns = ["Attendance Category", "Students"]

        fig_pie = px.pie(
            category_counts,
            names="Attendance Category",
            values="Students",
            hole=0.4,
            title="Students by Attendance Category"
        )
        st.plotly_chart(fig_pie, width="stretch")

        # Low attendance students
        st.subheader("⚠️ Students Needing Attendance Improvement")
        low_att = filtered_df[filtered_df["Attendance"] < 75][
            ["Student ID", "Name", "Department", "Semester", "Attendance", "CGPA"]
        ].sort_values("Attendance")

        if low_att.empty:
            st.success("🎉 No students are below 75% attendance!")
        else:
            st.warning(f"{len(low_att)} student(s) are below the 75% attendance requirement.")
            st.dataframe(low_att, width="stretch", hide_index=True)

        # Department summary
        st.subheader("📋 Department Attendance Summary")
        dept_summary = (
            filtered_df.groupby("Department")
            .agg(
                Students=("Student ID", "count"),
                Average_Attendance=("Attendance", "mean"),
                Minimum_Attendance=("Attendance", "min"),
                Maximum_Attendance=("Attendance", "max")
            )
            .reset_index()
        )
        dept_summary["Average_Attendance"] = dept_summary["Average_Attendance"].round(1)
        dept_summary["Minimum_Attendance"] = dept_summary["Minimum_Attendance"].round(1)
        dept_summary["Maximum_Attendance"] = dept_summary["Maximum_Attendance"].round(1)
        dept_summary = dept_summary.rename(columns={
            "Average_Attendance": "Avg Attendance (%)",
            "Minimum_Attendance": "Min Attendance (%)",
            "Maximum_Attendance": "Max Attendance (%)"
        })
        st.dataframe(dept_summary, width="stretch", hide_index=True)

# =========================
# ACADEMIC PERFORMANCE
# =========================

elif page == "📚 Academic Performance":
    st.header("📚 Academic Performance")
    st.caption("Analyze CGPA, performance levels, and department-wise academic trends.")

    if filtered_df.empty:
        st.warning("No students match the selected filters.")
    else:
        # KPI cards
        avg_cgpa = filtered_df["CGPA"].mean()
        highest_cgpa = filtered_df["CGPA"].max()
        high_performers = (filtered_df["CGPA"] >= 8).sum()
        needs_improvement = (filtered_df["CGPA"] < 7).sum()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📚 Average CGPA", f"{avg_cgpa:.2f}")
        c2.metric("🏆 Highest CGPA", f"{highest_cgpa:.2f}")
        c3.metric("⭐ CGPA ≥ 8", high_performers)
        c4.metric("⚠️ Below 7", needs_improvement)

        st.divider()

        # Department-wise average CGPA
        st.subheader("🏫 Department-wise Average CGPA")
        dept_cgpa = filtered_df.groupby("Department", as_index=False)["CGPA"].mean()
        dept_cgpa["CGPA"] = dept_cgpa["CGPA"].round(2)
        fig_dept = px.bar(
            dept_cgpa,
            x="Department",
            y="CGPA",
            text="CGPA",
            title="Average CGPA by Department"
        )
        fig_dept.update_traces(textposition="outside")
        fig_dept.update_layout(yaxis_title="Average CGPA", xaxis_title="Department")
        st.plotly_chart(fig_dept, use_container_width=True)

        # Student CGPA comparison
        st.subheader("👨‍🎓 Student CGPA Comparison")
        student_cgpa = filtered_df.sort_values("CGPA", ascending=False)
        fig_students = px.bar(
            student_cgpa,
            x="Name",
            y="CGPA",
            color="Department",
            text="CGPA",
            title="CGPA of Students"
        )
        fig_students.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_students.update_layout(yaxis_title="CGPA", xaxis_title="Student")
        st.plotly_chart(fig_students, use_container_width=True)

        # Performance categories
        def performance_category(cgpa):
            if cgpa >= 8.5:
                return "Excellent"
            elif cgpa >= 7:
                return "Good"
            else:
                return "Needs Improvement"

        academic_df = filtered_df.copy()
        academic_df["Performance"] = academic_df["CGPA"].apply(performance_category)

        st.subheader("📈 Performance Distribution")
        performance_counts = academic_df["Performance"].value_counts().reset_index()
        performance_counts.columns = ["Performance", "Students"]
        fig_pie = px.pie(
            performance_counts,
            names="Performance",
            values="Students",
            hole=0.4,
            title="Student Performance Levels"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Top performers
        st.subheader("🏆 Top Performers")
        top_students = filtered_df.sort_values("CGPA", ascending=False).head(5)
        top_display = top_students[["Student_ID", "Name", "Department", "Semester", "CGPA"]].copy()
        top_display["CGPA"] = top_display["CGPA"].round(2)
        st.dataframe(top_display, use_container_width=True, hide_index=True)

        # Students needing improvement
        st.subheader("⚠️ Students Needing Academic Improvement")
        improvement_df = academic_df[academic_df["CGPA"] < 7].copy()
        if improvement_df.empty:
            st.success("No students below 7 CGPA in the selected group.")
        else:
            improvement_display = improvement_df[["Student_ID", "Name", "Department", "Semester", "CGPA"]].copy()
            improvement_display["CGPA"] = improvement_display["CGPA"].round(2)
            st.dataframe(improvement_display, use_container_width=True, hide_index=True)

        # Department summary
        st.subheader("📋 Department Performance Summary")
        dept_summary = filtered_df.groupby("Department").agg(
            Students=("Student_ID", "count"),
            Average_CGPA=("CGPA", "mean"),
            Highest_CGPA=("CGPA", "max")
        ).reset_index()
        dept_summary["Average_CGPA"] = dept_summary["Average_CGPA"].round(2)
        dept_summary["Highest_CGPA"] = dept_summary["Highest_CGPA"].round(2)
        st.dataframe(dept_summary, use_container_width=True, hide_index=True)

# =========================
# PLACEMENT ANALYTICS
# =========================

elif page == "💼 Placement Analytics":

    st.header("💼 Placement Analytics")
    st.caption("Track placement status, companies and salary packages.")

    # -------------------------
    # PLACEMENT STATISTICS
    # -------------------------

    total_students = len(placement_df)
    placed_df = placement_df[
        placement_df["Placement Status"].astype(str).str.strip().str.lower() == "placed"
    ].copy()
    placed_students = len(placed_df)
    not_placed_students = total_students - placed_students
    placement_percentage = (
        placed_students / total_students * 100 if total_students > 0 else 0
    )

    if len(placed_df) > 0 and "Package" in placed_df.columns:
        placed_df["Package"] = pd.to_numeric(placed_df["Package"], errors="coerce")
        valid_packages = placed_df["Package"].dropna()
    else:
        valid_packages = pd.Series(dtype=float)

    # -------------------------
    # KPI CARDS
    # -------------------------

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎓 Total Students", total_students)
    col2.metric("✅ Placed", placed_students)
    col3.metric("❌ Not Placed", not_placed_students)
    col4.metric("📈 Placement Rate", f"{placement_percentage:.1f}%")

    st.divider()

    # -------------------------
    # STATUS OVERVIEW
    # -------------------------

    st.subheader("📊 Placement Status Overview")

    if total_students > 0:
        status_count = placement_df["Placement Status"].value_counts().reset_index()
        status_count.columns = ["Placement Status", "Students"]

        status_col1, status_col2 = st.columns(2)

        with status_col1:
            status_chart = px.pie(
                status_count,
                names="Placement Status",
                values="Students",
                hole=0.45,
                title="Placed vs Not Placed"
            )
            st.plotly_chart(status_chart, use_container_width=True)

        with status_col2:
            status_bar = px.bar(
                status_count,
                x="Placement Status",
                y="Students",
                text="Students",
                title="Placement Status Count"
            )
            st.plotly_chart(status_bar, use_container_width=True)
    else:
        st.info("No placement records are available.")

    st.divider()

    # -------------------------
    # PACKAGE KPIs
    # -------------------------

    st.subheader("💰 Package Statistics")

    if len(valid_packages) > 0:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💰 Average Package", f"{valid_packages.mean():.2f} LPA")
        col2.metric("🏆 Highest Package", f"{valid_packages.max():.2f} LPA")
        col3.metric("📉 Lowest Package", f"{valid_packages.min():.2f} LPA")
        col4.metric("👨‍🎓 Students with Package", len(valid_packages))
    else:
        st.info("Package information is not available.")

    st.divider()

    # -------------------------
    # COMPANY-WISE PLACEMENTS
    # -------------------------

    st.subheader("🏢 Company-wise Placements")

    if len(placed_df) > 0 and "Company" in placed_df.columns:
        company_count = (
            placed_df["Company"].astype(str)
            .value_counts()
            .reset_index()
        )
        company_count.columns = ["Company", "Students"]

        company_chart = px.bar(
            company_count.sort_values("Students", ascending=True),
            x="Students",
            y="Company",
            orientation="h",
            text="Students",
            title="Students Placed by Company"
        )
        st.plotly_chart(company_chart, use_container_width=True)
    else:
        st.info("No placed-student company records are available.")

    st.divider()

    # -------------------------
    # PACKAGE BY COMPANY
    # -------------------------

    st.subheader("📈 Average Package by Company")

    if len(placed_df) > 0 and "Company" in placed_df.columns and len(valid_packages) > 0:
        package_company = (
            placed_df.dropna(subset=["Package"])
            .groupby("Company", as_index=False)["Package"]
            .mean()
            .sort_values("Package", ascending=False)
        )

        package_chart = px.bar(
            package_company,
            x="Company",
            y="Package",
            text=package_company["Package"].round(2),
            title="Average Package Offered by Company",
            labels={"Package": "Average Package (LPA)"}
        )
        st.plotly_chart(package_chart, use_container_width=True)
    else:
        st.info("Company package data is not available.")

    st.divider()

    # -------------------------
    # DEPARTMENT-WISE PLACEMENTS
    # -------------------------

    st.subheader("🏫 Department-wise Placement Analysis")

    department_column = None
    for candidate in ["Department", "Department Name", "Dept"]:
        if candidate in placement_df.columns:
            department_column = candidate
            break

    if department_column:
        dept_data = placement_df.copy()
        dept_data["Placed Flag"] = (
            dept_data["Placement Status"].astype(str).str.strip().str.lower() == "placed"
        )
        dept_summary = (
            dept_data.groupby(department_column)
            .agg(
                Students=("Placed Flag", "size"),
                Placed=("Placed Flag", "sum")
            )
            .reset_index()
        )
        dept_summary["Not Placed"] = dept_summary["Students"] - dept_summary["Placed"]
        dept_summary["Placement Rate (%)"] = (
            dept_summary["Placed"] / dept_summary["Students"] * 100
        ).round(1)

        dept_chart = px.bar(
            dept_summary,
            x=department_column,
            y="Placement Rate (%)",
            text="Placement Rate (%)",
            title="Placement Rate by Department"
        )
        dept_chart.update_yaxes(range=[0, 100])
        st.plotly_chart(dept_chart, use_container_width=True)

        st.dataframe(
            dept_summary,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Department information is not available in the placement data.")

    st.divider()

    # -------------------------
    # PLACEMENT RECORDS
    # -------------------------

    st.subheader("📋 Placement Records")

    if len(placement_df) > 0:
        st.dataframe(
            placement_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No placement records found.")

# =========================
# ADMIN DASHBOARD
# =========================

elif page == "👨‍💼 Admin Dashboard":

    st.header("👨‍💼 Admin Dashboard")
    st.caption("Manage student records, validate data, and export college information.")

    # -------------------------
    # ADMIN SUMMARY
    # -------------------------

    total_students = len(df)
    low_attendance_count = int((df["Attendance"] < 75).sum())
    high_performer_count = int((df["CGPA"] >= 8).sum())
    department_count = int(df["Department"].nunique())
    average_attendance = df["Attendance"].mean() if total_students else 0
    average_cgpa = df["CGPA"].mean() if total_students else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👨‍🎓 Total Students", total_students)
    col2.metric("🏫 Departments", department_count)
    col3.metric("📊 Avg Attendance", f"{average_attendance:.1f}%")
    col4.metric("📚 Avg CGPA", f"{average_cgpa:.2f}")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("⚠️ Low Attendance", low_attendance_count)
    col2.metric("🌟 High Performers", high_performer_count)
    col3.metric("🎯 Attendance ≥ 75%", int((df["Attendance"] >= 75).sum()))
    col4.metric("🏆 CGPA ≥ 9", int((df["CGPA"] >= 9).sum()))

    st.divider()

    # -------------------------
    # ADMIN TABS
    # -------------------------

    tab_add, tab_edit, tab_delete, tab_upload, tab_records = st.tabs(
        [
            "➕ Add Student",
            "✏️ Edit Student",
            "🗑️ Delete Student",
            "📤 Upload CSV",
            "📋 Records & Export"
        ]
    )

    departments = ["CSE", "CSD", "ISE", "ECE", "EEE", "ME"]

    # -------------------------
    # ADD STUDENT
    # -------------------------

    with tab_add:

        st.subheader("➕ Add New Student")
        st.info("Enter the student details below. Student ID must be unique.")

        with st.form("add_student_form", clear_on_submit=True):

            col1, col2 = st.columns(2)

            with col1:
                student_id = st.text_input("Student ID", placeholder="Example: C007")
                name = st.text_input("Student Name", placeholder="Enter full name")
                department = st.selectbox("Department", departments)

            with col2:
                semester = st.number_input(
                    "Semester", min_value=1, max_value=8, value=4, step=1
                )
                attendance = st.number_input(
                    "Attendance (%)", min_value=0.0, max_value=100.0,
                    value=75.0, step=0.1
                )
                cgpa = st.number_input(
                    "CGPA", min_value=0.0, max_value=10.0,
                    value=7.0, step=0.01
                )

            submitted = st.form_submit_button("➕ Add Student", width="stretch")

            if submitted:
                student_id = student_id.strip()
                name = name.strip()
                existing_ids = df["Student ID"].astype(str).str.strip().str.lower().values

                if not student_id or not name:
                    st.error("❌ Student ID and Student Name are required.")
                elif student_id.lower() in existing_ids:
                    st.error("❌ Student ID already exists.")
                elif not 0 <= attendance <= 100:
                    st.error("❌ Attendance must be between 0 and 100.")
                elif not 0 <= cgpa <= 10:
                    st.error("❌ CGPA must be between 0 and 10.")
                else:
                    new_student = pd.DataFrame([{
                        "Student ID": student_id,
                        "Name": name,
                        "Department": department,
                        "Semester": int(semester),
                        "Attendance": float(attendance),
                        "CGPA": float(cgpa)
                    }])
                    df = pd.concat([df, new_student], ignore_index=True)
                    df.to_csv("data/students.csv", index=False)
                    st.success(f"✅ {name} added successfully!")
                    st.rerun()

    # -------------------------
    # EDIT STUDENT
    # -------------------------

    with tab_edit:

        st.subheader("✏️ Edit Student")

        student_ids = df["Student ID"].astype(str).tolist()

        if student_ids:
            edit_id = st.selectbox(
                "Select Student",
                student_ids,
                key="edit_student"
            )

            selected_student = df[df["Student ID"].astype(str) == edit_id].iloc[0]
            current_department = selected_student["Department"]
            department_index = (
                departments.index(current_department)
                if current_department in departments else 0
            )

            with st.form("edit_student_form"):
                col1, col2 = st.columns(2)

                with col1:
                    st.text_input("Student ID", value=edit_id, disabled=True)
                    edit_name = st.text_input("Name", value=str(selected_student["Name"]))
                    edit_department = st.selectbox(
                        "Department", departments, index=department_index
                    )
                    edit_semester = st.number_input(
                        "Semester", min_value=1, max_value=8,
                        value=int(selected_student["Semester"]), step=1
                    )

                with col2:
                    edit_attendance = st.number_input(
                        "Attendance (%)", min_value=0.0, max_value=100.0,
                        value=float(selected_student["Attendance"]), step=0.1
                    )
                    edit_cgpa = st.number_input(
                        "CGPA", min_value=0.0, max_value=10.0,
                        value=float(selected_student["CGPA"]), step=0.01
                    )

                update_button = st.form_submit_button("💾 Update Student", width="stretch")

                if update_button:
                    edit_name = edit_name.strip()

                    if not edit_name:
                        st.error("❌ Student Name cannot be empty.")
                    elif not 0 <= edit_attendance <= 100:
                        st.error("❌ Attendance must be between 0 and 100.")
                    elif not 0 <= edit_cgpa <= 10:
                        st.error("❌ CGPA must be between 0 and 10.")
                    else:
                        mask = df["Student ID"].astype(str) == edit_id
                        df.loc[mask, "Name"] = edit_name
                        df.loc[mask, "Department"] = edit_department
                        df.loc[mask, "Semester"] = int(edit_semester)
                        df.loc[mask, "Attendance"] = float(edit_attendance)
                        df.loc[mask, "CGPA"] = float(edit_cgpa)
                        df.to_csv("data/students.csv", index=False)
                        st.success(f"✅ {edit_id} updated successfully!")
                        st.rerun()
        else:
            st.info("No student records available to edit.")

    # -------------------------
    # DELETE STUDENT
    # -------------------------

    with tab_delete:

        st.subheader("🗑️ Delete Student")
        st.warning("⚠️ Deleting a student permanently removes the record from students.csv.")

        student_ids = df["Student ID"].astype(str).tolist()

        if student_ids:
            delete_id = st.selectbox(
                "Select Student to Delete",
                student_ids,
                key="delete_student"
            )

            delete_row = df[df["Student ID"].astype(str) == delete_id].iloc[0]
            st.write(f"**Selected:** {delete_row['Name']} — {delete_row['Department']}")

            delete_confirm = st.checkbox(
                "I confirm that I want to permanently delete this student.",
                key="delete_confirmation"
            )

            if st.button(
                "🗑️ Delete Student",
                disabled=not delete_confirm,
                width="stretch"
            ):
                df = df[df["Student ID"].astype(str) != delete_id]
                df.to_csv("data/students.csv", index=False)
                st.success(f"✅ Student {delete_id} deleted successfully!")
                st.rerun()
        else:
            st.info("No student records available to delete.")

    # -------------------------
    # UPLOAD STUDENT DATA
    # -------------------------

    with tab_upload:

        st.subheader("📤 Upload Student CSV")
        st.info(
            "Upload a CSV containing all required student columns. "
            "The uploaded file will replace the current student dataset only after confirmation."
        )

        required_columns = [
            "Student ID", "Name", "Department", "Semester", "Attendance", "CGPA"
        ]

        st.code(", ".join(required_columns), language="text")

        uploaded_file = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            key="student_csv_upload"
        )

        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                missing_columns = [
                    column for column in required_columns
                    if column not in uploaded_df.columns
                ]

                errors = []

                if uploaded_df.empty:
                    errors.append("The uploaded CSV is empty.")
                elif missing_columns:
                    errors.append("Missing required columns: " + ", ".join(missing_columns))
                else:
                    if uploaded_df["Student ID"].isna().any() or (uploaded_df["Student ID"].astype(str).str.strip() == "").any():
                        errors.append("Student ID cannot contain empty values.")
                    if uploaded_df["Name"].isna().any() or (uploaded_df["Name"].astype(str).str.strip() == "").any():
                        errors.append("Student Name cannot contain empty values.")
                    if uploaded_df["Student ID"].astype(str).str.strip().str.lower().duplicated().any():
                        errors.append("The uploaded CSV contains duplicate Student IDs.")

                    semester_numeric = pd.to_numeric(uploaded_df["Semester"], errors="coerce")
                    attendance_numeric = pd.to_numeric(uploaded_df["Attendance"], errors="coerce")
                    cgpa_numeric = pd.to_numeric(uploaded_df["CGPA"], errors="coerce")

                    if semester_numeric.isna().any() or not semester_numeric.between(1, 8).all():
                        errors.append("Semester values must be numeric and between 1 and 8.")
                    if attendance_numeric.isna().any() or not attendance_numeric.between(0, 100).all():
                        errors.append("Attendance values must be numeric and between 0 and 100.")
                    if cgpa_numeric.isna().any() or not cgpa_numeric.between(0, 10).all():
                        errors.append("CGPA values must be numeric and between 0 and 10.")

                if errors:
                    for error in errors:
                        st.error("❌ " + error)
                else:
                    uploaded_df["Student ID"] = uploaded_df["Student ID"].astype(str).str.strip()
                    uploaded_df["Name"] = uploaded_df["Name"].astype(str).str.strip()
                    uploaded_df["Semester"] = pd.to_numeric(uploaded_df["Semester"]).astype(int)
                    uploaded_df["Attendance"] = pd.to_numeric(uploaded_df["Attendance"]).astype(float)
                    uploaded_df["CGPA"] = pd.to_numeric(uploaded_df["CGPA"]).astype(float)

                    st.success("✅ CSV validation successful.")
                    st.write(f"**Rows:** {len(uploaded_df)}  |  **Columns:** {len(uploaded_df.columns)}")
                    st.dataframe(uploaded_df, width="stretch", hide_index=True)

                    replace_confirm = st.checkbox(
                        "I confirm that this CSV should replace the current student data.",
                        key="upload_confirmation"
                    )

                    if st.button(
                        "📤 Replace Student Data",
                        disabled=not replace_confirm,
                        width="stretch"
                    ):
                        uploaded_df.to_csv("data/students.csv", index=False)
                        st.success("✅ Student data uploaded successfully!")
                        st.rerun()

            except Exception as e:
                st.error(f"❌ Could not read the CSV file: {e}")

    # -------------------------
    # RECORDS & EXPORT
    # -------------------------

    with tab_records:

        st.subheader("📋 Current Student Records")

        search_admin = st.text_input(
            "🔎 Search records",
            placeholder="Search by Student ID, name, or department...",
            key="admin_search"
        )

        filtered_admin = df.copy()

        if search_admin.strip():
            query = search_admin.strip().lower()
            mask = (
                filtered_admin["Student ID"].astype(str).str.lower().str.contains(query, na=False)
                | filtered_admin["Name"].astype(str).str.lower().str.contains(query, na=False)
                | filtered_admin["Department"].astype(str).str.lower().str.contains(query, na=False)
            )
            filtered_admin = filtered_admin[mask]

        col1, col2 = st.columns(2)
        col1.metric("Records Shown", len(filtered_admin))
        col2.metric("Total Records", len(df))

        st.dataframe(
            filtered_admin,
            width="stretch",
            hide_index=True
        )

        st.divider()
        st.subheader("📥 Export Student Data")

        csv_data = df.to_csv(index=False)
        filtered_csv_data = filtered_admin.to_csv(index=False)

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="⬇️ Download All Students",
                data=csv_data,
                file_name="students_export.csv",
                mime="text/csv",
                width="stretch"
            )

        with col2:
            st.download_button(
                label="⬇️ Download Filtered Records",
                data=filtered_csv_data,
                file_name="students_filtered_export.csv",
                mime="text/csv",
                width="stretch"
            )

        st.divider()
        st.subheader("📊 Quick Department Summary")

        if not df.empty:
            admin_summary = df.groupby("Department").agg(
                Students=("Student ID", "count"),
                Avg_Attendance=("Attendance", "mean"),
                Avg_CGPA=("CGPA", "mean")
            ).reset_index()
            admin_summary["Avg_Attendance"] = admin_summary["Avg_Attendance"].round(1)
            admin_summary["Avg_CGPA"] = admin_summary["Avg_CGPA"].round(2)
            st.dataframe(admin_summary, width="stretch", hide_index=True)
        else:
            st.info("No records available for the department summary.")


# =========================
# FOOTER
# =========================
st.markdown("<div class=\"footer\">🎓 CampusInsight • College Data Analytics Platform</div>", unsafe_allow_html=True)
