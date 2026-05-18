# Golfah Documentation

## Overview

Heyo! - I'm creating this documentation for the purpose(s) of:

* Being able to pass the documentation off to an LLM to get it up to speed with the project
* Be able to use this documentation in marketing, or other design purposes.

## Application Purpose

I originally created Golfah as I wasn't satisified with the software offerings on the IOS or Desktop Market. The options that I reviewed were 18Birdies and the Grint, both of which I found to have unintuitive UI's and packed to the gills with advertisements, as well as locking useful features behind paywalls.

The purpose of Golfah was never to compete with these projects, which already have established customer bases, full scale enterprise development teams and much more, but instead, was designed to give me, and anyone else who is keen to use the application, greater control over their information and data.

## Future State

I never quite know where this application is going, sometimes I think that I should just fully restart and design it in CSS/HTMl/Javascript, and other times, I feel as though I could make this an enterprise application just through some elbow grease, SQL and Python.

Ideally in the future, I'd love to have this app storing vast quanities of information on a variety of users golf data, to help them improve their game.

And I mean, I'd also like the following for every course in the world:

* Tee box Lat Long's
* Slope / course rating
* Different coloured tee box's (*relative to each course*)
* Clubhouse Lat Longs

That way, this Golfah would be able to be used by anybody in the world. Sadly, I can't seem to find this information in open-source format.

### Other Dreams

* I'd also love for this app to be semi-commerically viable, I'd love to be able to retire and play golf full time, alas, a brother can dream.

* I'd also like the app to be as intensive as Data-Golf, which is a super cool website if you haven't checked it out already.

* I'd love the app to be able to integrate with other apps, such as Golf New Zealand, such that when you upload a score to Golf NZ, or to Golfah, it goes into both, that way you can have continuity across applications.

## Pages

### Home Page

The Golfah home-page is fairly simple, in the new designs, I've just got a title, bit of blurb text, and then ideally (*in the future*) I'll have a video of me using Golfah both live, as well as retrospectively, to show people how they can use the application.

One thing I need to remember to implement is a pop-up modal, similar to what I did for OptiX.

### Play Page - Overview

This is something that will be an interesting technical challenge for me. For reference, I never quite got around to wiring this page up, and as such, I'm missing a really key bit of functionality for Golfah.

The whole purpose of the page is to allow users to either actively, or retroactively, add in their scores for a round of golf.

I recently got inspired after using Golf New Zealand's Application, which, while I found to be useful, is still kind of a pizza application (*pizza shit*). With this being said, I really like their interface for live round scoring, as such, I've built some designs in Excalidraw to try and mock this design up, and while the designs are basically done, I think actually achieving this functionality in Python could be kind of interesting (*in particular, I feel as though Streamlit may block me in some capacity*) - Which is actually where that idea to move to a web-based development approach could be benefifical.

#### Round Information

The purpose of the Round Information Page is to capture metadata about the round before entering hole-by-hole scores.

* Navigation row with three elements:
  * Left: `Cancel / Back` button (green, outlined)
  * Centre: Step label — `Round Info`
  * Right: `Next` button (green, filled)

**Form Fields:**

| Field | Input Type | Notes |
| --- | --- | --- |
| Course | Selectbox / Text Input | Drives hole data population (see Section 5) |
| Tee Marker | Selectbox | Options depend on selected course (e.g. Red, White, Blue) |
| Round Type | Selectbox | e.g. Stroke Play, Match Play, Stableford |
| Date | Date Input | Defaults to today if `Today?` toggle is ON |
| Today? | Toggle (bool) | When ON, locks date to `datetime.today()` |
| Comment | Text Area | Free text, optional round-level note |

**State management:** Use `st.session_state` to carry Round Info values forward to the scoring steps.

**On Next:** Validate that Course, Tee Marker, Round Type, and Date are all populated before advancing.

---

### Score Entry (`play.py` continued)

The purpose of the Score Entry Page is to allow users to enter score and shot statistics for each hole, one hole at a time.

**Layout:**

* Page header: 🏌️ `{Course Name} – {Nth} Hole`
* Subtitle row: `Par: {X} | Stroke: {X} | Distance: {X}` — populated from course data
* Tab bar: `Score` | `Stats` (see 3.2a and 3.2b below)
* Below tabs: Scrollable scorecard table showing all holes entered so far

**Scorecard Table (read-only, updates as holes are completed):**

| Column | Description |
| --- | --- |
| Hole | Hole number (1–18) |
| Score | Gross strokes taken |
| Par | Par for the hole |
| Stroke | Stroke index |
| Comment | Hole-level note |
| Distance | Yards/metres |
| Putts | Number of putts |
| GIR | Green in Regulation (bool) |
| Fairways Hit | Hit fairway? (bool, N/A for par 3s) |

**Navigation:** Previous Hole / Next Hole buttons. On final hole (18), Next becomes `Submit Round`.

---

#### Play - Score Tab

Fields per hole, per player:

| Field | Input Type | Notes |
| --- | --- | --- |
| Score (per player) | Number Input | Gross strokes |
| Running score display | Text (read-only) | e.g. `E through 4`, `-1 through 4` — updates live |
| Not attempted | Toggle | If ON, hole is recorded as N/A (e.g. skipped hole) |

**Multi-player support:** Each active player in the round gets their own score input row. Player names are shown as row labels (e.g. `Russell Chubb:`, `John Doe:`).

---

#### Play - Stats Tab

Fields per hole (shared / per player TBD):

| Field | Input Type | Notes |
| --- | --- | --- |
| Fairway Hit | Toggle (green) | Did the tee shot land on the fairway? |
| Left / Right | Toggle (pink) | Miss direction — only relevant if Fairway = OFF |
| Approach Hit | Toggle (green) | Did approach shot hit the green? |
| Approach Left/Right | Toggle (pink) | Miss direction for approach |
| Approach Long/Short | Toggle (pink) | Miss distance for approach |
| Putts | Number Input | Number of putts taken |
| Penalties | Number Input | Number of penalty strokes |
| Greenside Bunker Shots | Number Input | Shots taken from greenside bunker |
| Comment | Text Area | Hole-level note |

**Expandable section at bottom:** `Statistics Definition / How to use this page 🏌️` — collapsed by default, explains each stat.

## 6. Session State Design

The multi-step Add Round flow depends heavily on `st.session_state`. Key state variables:

```python
st.session_state["round_info"] = {
    "course": str,
    "tee": str,
    "round_type": str,
    "date": date,
    "comment": str,
    "players": [str],       # list of player names
}
 
st.session_state["current_hole"] = int   # 1–18
st.session_state["hole_data"] = {}       # keyed by hole number, stores Score + Stats dicts
st.session_state["step"] = str           # "round_info" | "scoring"
```

---

## 7. Key UX Behaviours

* `Today?` toggle on Round Info auto-sets date and locks the date picker
* Score tab shows running score-to-par live as holes are completed (e.g. `E through 4`, `-2 through 9`)
* `Not Attempted` toggle on Score tab marks hole as N/A and skips stat entry
* Stats tab toggles use two colours: green (positive / hit) and pink (miss direction)
* Approach stat toggles for Left/Right and Long/Short are only relevant when `Approach Hit = OFF`
* Scorecard table below the hole entry area updates in real time as holes are submitted
* `Cancel / Back` on Round Info discards the session and returns to Home
* Need to think about how I can handle users leaving the session, does that just mean that their round will be disgarded? - How can I persist this?

---
 
## 8. File Structure (Current)
 
```
app/
├── app.py                  # Entry point, routing
├── data/
│   ├── Course_Data.xlsx
│   ├── Rounds_Data.xlsx
│   └── Summary_Data.xlsx
├── utils/
│   └── Navbar.py
├── views/
│   ├── home/
│   │   └── home.py
│   ├── add_round/
│   │   └── play.py         # Round Info + Score Entry
│   └── analysis/
│       └── round_summary.py
└── requirements.txt
```
