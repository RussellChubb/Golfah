# Golfah: Add Round Page
# Imports
import streamlit as st
import pandas as pd
from datetime import date
from pathlib import Path

# Data Loading
APP_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = APP_DIR / "data"

# Data Caching
@st.cache_data
def load_data():
    summary = pd.read_excel(DATA_DIR / "Summary_Data.xlsx", parse_dates=["Date"])
    rounds = pd.read_excel(DATA_DIR / "Rounds_Data.xlsx", parse_dates=["Date"])
    courses = pd.read_excel(DATA_DIR / "Course_Data.xlsx")
    return summary, rounds, courses

# Data Saving
def save_data(summary_df, rounds_df):
    summary_df.to_excel(DATA_DIR / "Summary_Data.xlsx", index=False)
    rounds_df.to_excel(DATA_DIR / "Rounds_Data.xlsx", index=False)
    # Clear cache so next load picks up the new data
    load_data.clear()

# Session State Init
def init_state():
    defaults = {
        "step": "round_info",           # "round_info" | "scoring" | "done"
        "round_info": {},               # dict of round metadata
        "players": ["Russell"],         # list of player names for this round
        "current_hole": 1,              # 1–18
        "hole_data": {},                # { hole_num: { player: { score, stats } } }
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

# Reset session state to defaults (used when cancelling out of a round entry, or after submission)
def reset_state():
    for key in ["step", "round_info", "players", "current_hole", "hole_data"]:
        if key in st.session_state:
            del st.session_state[key]


# Helpers - Returns a running score-to-par string e.g. '-2 through 4'
def score_to_par_label(player: str, through_hole: int) -> str:
    total_score = 0
    total_par = 0
    for h in range(1, through_hole + 1):
        hole_entry = st.session_state.hole_data.get(h, {}).get(player)
        if hole_entry and not hole_entry.get("not_attempted"):
            total_score += hole_entry.get("score", 0)
            total_par += hole_entry.get("par", 0)
    diff = total_score - total_par
    if diff == 0:
        label = "E"
    elif diff > 0:
        label = f"+{diff}"
    else:
        label = str(diff)
    return f"{label} through {through_hole}"

# Build a summary scorecard dataframe from session state hole data.
def build_scorecard(players: list, course_df: pd.DataFrame, course: str) -> pd.DataFrame:
    rows = []
    holes = course_df[course_df["Course"] == course].sort_values("Hole")
    for _, hole_row in holes.iterrows():
        h = int(hole_row["Hole"])
        row = {
            "Hole": h,
            "Par": int(hole_row["Par"]),
            "Distance": int(hole_row.get("Distance", 0)),
        }
        for player in players:
            entry = st.session_state.hole_data.get(h, {}).get(player, {})
            if entry.get("not_attempted"):
                row[f"{player} Score"] = "N/A"
            elif entry.get("score") is not None:
                row[f"{player} Score"] = int(entry["score"])
            else:
                row[f"{player} Score"] = "-"
        rows.append(row)
    return pd.DataFrame(rows)


# Page Header
def render_header(title: str, subtitle: str):
    st.markdown(
        f"""
        <div style='text-align: center; margin-top: 1rem;'>
            <h1 style='
                font-family: "Space Grotesk", sans-serif;
                font-weight: 700;
                font-size: 3rem;
                margin: 0;
                color: #ffffff;
            '>⛳ {title}</h1>
            <h2 style='
                font-family: "Martian Mono", monospace;
                font-weight: 400;
                font-size: 1.1rem;
                margin: 0.25rem 0 0 0;
                color: #cccccc;
            '>{subtitle}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()


# Step 1: Round Info
def show_round_info(course_df: pd.DataFrame):
    render_header("Add New Round", "Log your latest golf round and track your progress!")

    # Nav row
    col_back, col_label, col_next = st.columns([2, 4, 2])
    with col_back:
        if st.button("✕ Cancel", width= "stretch"):
            reset_state()
            st.rerun()
    with col_label:
        st.markdown(
            "<p style='text-align:center; color:#aaaaaa; margin-top:0.4rem;'>Round Info</p>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Course + Tee
    col1, col2 = st.columns(2)
    course = col1.selectbox("Course", sorted(course_df["Course"].unique()))
    tee_options = ["Red", "White", "Blue", "Black"]
    tee = col2.selectbox("Tee Marker", tee_options)

    # Round Type
    round_type = st.selectbox("Round Type", ["Stroke Play", "Stableford", "Match Play", "Practice"])

    # Date + Today toggle
    col_date, col_today = st.columns([3, 1])
    use_today = col_today.toggle("Today?", value=True)
    round_date = col_date.date_input(
        "Date",
        value=date.today(),
        disabled=use_today,
    )
    if use_today:
        round_date = date.today()

    # Comment
    comment = st.text_area("Comment", placeholder="Optional round notes...")

    # Players
    st.markdown("**Players**")
    st.caption("Add the names of everyone playing this round.")

    if "player_inputs" not in st.session_state:
        st.session_state.player_inputs = ["Russell"]

    updated_players = []
    for i, name in enumerate(st.session_state.player_inputs):
        pc1, pc2 = st.columns([6, 1])
        val = pc1.text_input(f"Player {i + 1}", value=name, key=f"player_{i}", label_visibility="collapsed")
        updated_players.append(val)
        if pc2.button("✕", key=f"remove_player_{i}") and len(st.session_state.player_inputs) > 1:
            st.session_state.player_inputs.pop(i)
            st.rerun()

    st.session_state.player_inputs = updated_players

    if st.button("+ Add Player"):
        st.session_state.player_inputs.append("")
        st.rerun()

    st.markdown("---")

    # Next button
    _, _, col_next2 = st.columns([2, 4, 2])
    with col_next2:
        if st.button("Next →", width= "stretch", type="primary"):
            players = [p.strip() for p in st.session_state.player_inputs if p.strip()]
            if not players:
                st.error("Add at least one player.")
                return
            st.session_state.round_info = {
                "course": course,
                "tee": tee,
                "round_type": round_type,
                "date": round_date,
                "comment": comment,
            }
            st.session_state.players = players
            st.session_state.current_hole = 1
            st.session_state.hole_data = {}
            st.session_state.step = "scoring"
            st.rerun()


# Step 2: Scoring
def show_scoring(course_df: pd.DataFrame):
    info = st.session_state.round_info
    players = st.session_state.players
    hole_num = st.session_state.current_hole
    course = info["course"]

    # Get hole metadata
    hole_rows = course_df[
        (course_df["Course"] == course) & (course_df["Hole"] == hole_num)
    ]
    if hole_rows.empty:
        st.error(f"No course data found for {course}, Hole {hole_num}. Check Course_Data.xlsx.")
        return
    hole_meta = hole_rows.iloc[0]
    par = int(hole_meta["Par"])
    distance = int(hole_meta.get("Distance", 0))

    # Header
    render_header(
        f"{course} – Hole {hole_num}",
        f"Par: {par} | Distance: {distance}m",
    )

    # Nav row
    col_back, col_label, col_next = st.columns([2, 4, 2])
    with col_back:
        back_label = "← Round Info" if hole_num == 1 else f"← Hole {hole_num - 1}"
        if st.button(back_label, width="stretch"):
            if hole_num == 1:
                st.session_state.step = "round_info"
            else:
                st.session_state.current_hole -= 1
            st.rerun()
    with col_label:
        st.markdown(
            f"<p style='text-align:center; color:#aaaaaa; margin-top:0.4rem;'>Hole {hole_num} of 18</p>",
            unsafe_allow_html=True,
        )
    with col_next:
        next_label = "Submit ✓" if hole_num == 18 else f"Hole {hole_num + 1} →"
        advance = st.button(next_label, width="stretch", type="primary")

    st.markdown("---")

    # Score tab + Stats tab
    tab_score, tab_stats = st.tabs(["Score", "Stats"])

    # Initialise hole_data for this hole if not yet set
    if hole_num not in st.session_state.hole_data:
        st.session_state.hole_data[hole_num] = {}

    for player in players:
        if player not in st.session_state.hole_data[hole_num]:
            st.session_state.hole_data[hole_num][player] = {
                "score": par,
                "par": par,
                "not_attempted": False,
                "putts": 2,
                "penalties": 0,
                "bunker_shots": 0,
                "fairway_hit": True,
                "fairway_miss": None,
                "approach_hit": True,
                "approach_miss_direction": None,
                "approach_miss_distance": None,
                "comment": "",
            }

    # Score Tab
    with tab_score:
        for player in players:
            entry = st.session_state.hole_data[hole_num][player]
            st.markdown(f"**{player}**")

            sc1, sc2 = st.columns([4, 2])
            not_attempted = sc2.toggle(
                "Not attempted",
                value=entry["not_attempted"],
                key=f"na_{hole_num}_{player}",
            )
            entry["not_attempted"] = not_attempted

            if not not_attempted:
                score = sc1.number_input(
                    "Score",
                    min_value=1,
                    max_value=15,
                    value=entry["score"],
                    step=1,
                    key=f"score_{hole_num}_{player}",
                    label_visibility="collapsed",
                )
                entry["score"] = score
                entry["par"] = par

                # Running score to par
                running = score_to_par_label(player, hole_num)
                st.caption(f"_{running}_")
            else:
                st.caption("_Hole marked as not attempted_")

            st.markdown("---")

    # Stats Tab
    with tab_stats:
        for player in players:
            entry = st.session_state.hole_data[hole_num][player]
            st.markdown(f"**{player}**")

            if entry.get("not_attempted"):
                st.caption("_No stats — hole not attempted_")
                st.markdown("---")
                continue

            # Fairway
            if par != 3:
                fw1, fw2 = st.columns(2)
                fairway_hit = fw1.toggle(
                    "Fairway Hit",
                    value=entry["fairway_hit"],
                    key=f"fw_{hole_num}_{player}",
                )
                entry["fairway_hit"] = fairway_hit
                if not fairway_hit:
                    miss = fw2.radio(
                        "Miss Direction",
                        ["Left", "Right"],
                        horizontal=True,
                        key=f"fw_miss_{hole_num}_{player}",
                        index=0 if entry["fairway_miss"] != "Right" else 1,
                    )
                    entry["fairway_miss"] = miss
                else:
                    entry["fairway_miss"] = None
            else:
                st.caption("_Par 3 — no fairway stat_")

            # Approach
            ap1, ap2, ap3 = st.columns(3)
            approach_hit = ap1.toggle(
                "Approach Hit (GIR)",
                value=entry["approach_hit"],
                key=f"ap_{hole_num}_{player}",
            )
            entry["approach_hit"] = approach_hit
            if not approach_hit:
                ap_dir = ap2.radio(
                    "Direction",
                    ["Left", "Right"],
                    horizontal=True,
                    key=f"ap_dir_{hole_num}_{player}",
                    index=0 if entry["approach_miss_direction"] != "Right" else 1,
                )
                ap_dist = ap3.radio(
                    "Distance",
                    ["Long", "Short"],
                    horizontal=True,
                    key=f"ap_dist_{hole_num}_{player}",
                    index=0 if entry["approach_miss_distance"] != "Short" else 1,
                )
                entry["approach_miss_direction"] = ap_dir
                entry["approach_miss_distance"] = ap_dist
            else:
                entry["approach_miss_direction"] = None
                entry["approach_miss_distance"] = None

            # Putts, Penalties, Bunker
            num1, num2, num3 = st.columns(3)
            entry["putts"] = num1.number_input(
                "Putts", min_value=0, max_value=10, value=entry["putts"],
                key=f"putts_{hole_num}_{player}",
            )
            entry["penalties"] = num2.number_input(
                "Penalties", min_value=0, max_value=10, value=entry["penalties"],
                key=f"pen_{hole_num}_{player}",
            )
            entry["bunker_shots"] = num3.number_input(
                "Bunker Shots", min_value=0, max_value=10, value=entry["bunker_shots"],
                key=f"bunk_{hole_num}_{player}",
            )

            # Comment
            entry["comment"] = st.text_area(
                "Comment",
                value=entry["comment"],
                placeholder="Notes on this hole...",
                key=f"comment_{hole_num}_{player}",
            )

            with st.expander("📖 Statistics Definition / How to use this page"):
                st.markdown("""
- **Fairway Hit** — Did your tee shot land on the fairway? (N/A for par 3s)
- **Approach Hit (GIR)** — Did you hit the green in regulation? (par - 2 strokes)
- **Putts** — Total putts taken on the green
- **Penalties** — Any penalty strokes incurred
- **Bunker Shots** — Shots played from a greenside bunker
- **Miss Direction / Distance** — Only relevant when Fairway or Approach is missed
                """)

            st.markdown("---")

    # Scorecard (running summary)
    st.subheader("Scorecard")
    scorecard_df = build_scorecard(players, course_df, course)
    st.dataframe(scorecard_df, width="stretch", hide_index=True)

    # Handle Next / Submit
    if advance:
        if hole_num == 18:
            submit_round()
        else:
            st.session_state.current_hole += 1
            st.rerun()


# Submit Round
def submit_round():
    summary_df, rounds_df, course_df = load_data()
    info = st.session_state.round_info
    players = st.session_state.players
    hole_data = st.session_state.hole_data

    new_summary_rows = []
    new_rounds_rows = []

    for player in players:
        total_score = 0
        total_par = 0
        total_putts = 0
        fairways_hit = 0
        fairways_total = 0
        gir = 0

        for hole_num, player_data in hole_data.items():
            entry = player_data.get(player, {})
            if entry.get("not_attempted"):
                continue

            hole_rows = course_df[
                (course_df["Course"] == info["course"]) & (course_df["Hole"] == hole_num)
            ]
            par = int(hole_rows.iloc[0]["Par"]) if not hole_rows.empty else 4

            score = entry.get("score", par)
            total_score += score
            total_par += par
            total_putts += entry.get("putts", 0)

            if par != 3:
                fairways_total += 1
                if entry.get("fairway_hit"):
                    fairways_hit += 1

            if entry.get("approach_hit"):
                gir += 1

            new_rounds_rows.append({
                "Date": info["date"],
                "Course": info["course"],
                "Tee": info["tee"],
                "Round_Type": info["round_type"],
                "Player": player,
                "Hole": hole_num,
                "Score": score,
                "Par": par,
                "Putts": entry.get("putts", 0),
                "Penalties": entry.get("penalties", 0),
                "Bunker_Shots": entry.get("bunker_shots", 0),
                "Fairway_Hit": entry.get("fairway_hit"),
                "Fairway_Miss": entry.get("fairway_miss"),
                "Approach_Hit": entry.get("approach_hit"),
                "Approach_Miss_Direction": entry.get("approach_miss_direction"),
                "Approach_Miss_Distance": entry.get("approach_miss_distance"),
                "Not_Attempted": False,
                "Comment": entry.get("comment", ""),
            })

        new_summary_rows.append({
            "Date": info["date"],
            "Course": info["course"],
            "Tee": info["tee"],
            "Round_Type": info["round_type"],
            "Player": player,
            "Score": total_score,
            "Par_Total": total_par,
            "Score_To_Par": total_score - total_par,
            "Total_Putts": total_putts,
            "Fairways_Hit": fairways_hit,
            "Fairways_Total": fairways_total,
            "GIR": gir,
            "Comment": info["comment"],
        })

    # Append and save
    summary_df = pd.concat([summary_df, pd.DataFrame(new_summary_rows)], ignore_index=True)
    rounds_df = pd.concat([rounds_df, pd.DataFrame(new_rounds_rows)], ignore_index=True)
    save_data(summary_df, rounds_df)

    st.session_state.step = "done"
    st.session_state["submitted_players"] = players
    st.session_state["submitted_info"] = info
    st.rerun()


# Done Screen
def show_done():
    info = st.session_state.get("submitted_info", {})
    players = st.session_state.get("submitted_players", [])

    render_header("Round Saved!", "Your round has been logged successfully.")

    st.success(
        f"✅ Round at **{info.get('course', '')}** on **{info.get('date', '')}** saved for: "
        + ", ".join(players)
    )

    # Nav buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Add Another Round", width="stretch"):
            reset_state()
            st.rerun()
    with col2:
        if st.button("📊 View Analysis", width="stretch"):
            reset_state()
            st.session_state["page"] = "Round Summary"
            st.rerun()


# Entry Point
def show():
    init_state()
    _, _, course_df = load_data()

    step = st.session_state.step

    if step == "round_info":
        show_round_info(course_df)
    elif step == "scoring":
        show_scoring(course_df)
    elif step == "done":
        show_done()