import streamlit as st
from ai import fetch_gift_ideas

st.title("Kindred Finds: Your Personal Gift Finder")

with st.form("gift-form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.selectbox(
            "Age group",
            [
                "Child: 0-12",
                "Teen: 13-17",
                "Young Adult:18-25",
                "Adult: 26-40",
                "Middle Aged: 41-60",
                "Senior: 60+",
            ],
            index=None,
            placeholder="Select their age group",
        )

    with col2:
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Prefer not to say"],
            index=None,
            placeholder="Select their gender",
        )

    col3, col4 = st.columns(2)

    with col3:
        relationship = st.selectbox(
            "Relationship",
            [
                "Close friend",
                "Parents",
                "Siblings",
                "Partner/Spouse",
                "Colleague",
                "Acquaintance/ Distant Relative",
                "Other",
            ],
            index=None,
            placeholder="Specify your relationship with them",
        )
        if relationship == "Other":
            relationship = st.text_input(
                "", placeholder="Please specify", label_visibility="collapsed"
            )

    with col4:
        budget = st.selectbox(
            "Budget",
            [
                "Under PKR 5,000",
                "PKR 5,000 - 10,000",
                "PKR 10,000 - 20,000",
                "PKR 20,000 - 50,000",
                "No limit",
            ],
            index=None,
            placeholder="Select your budget",
        )

    col5, col6 = st.columns(2)

    with col5:
        occasion = st.selectbox(
            "Occasion",
            [
                "Birthday",
                "Holiday",
                "Wedding",
                "Housewarming",
                "Graduation",
                "Just because/ No occasion",
            ],
            index=None,
            placeholder="What's the occassion?",
        )

    with col6:
        vibe = st.multiselect(
            "Vibe",
            [
                "Busy Professional",
                "Student",
                "Homebody",
                "Outdoorsy",
                "Creative/ artsy",
                "Minimalist",
                "Tech enthusiast",
                "Fitness/ health nut",
                "Foodie",
                "Fashion forward",
            ],
            default=[],
            placeholder="Lifestyle. Choose all that apply",
        )

    col7, col8 = st.columns(2)

    with col7:
        likes = st.text_area(
            "What they love",
            placeholder="e.g., hiking, true crime podcasts, minimalist design, coffee, cats...",
            height=100,
        )

    with col8:
        dislikes = st.text_area(
            "What they dislike",
            placeholder="e.g., scented candles, clutter, peanuts, very spicy food, alcohol...",
            height=100,
        )

    submit = st.form_submit_button(
        "Find the perfect gift",
        type="primary",
    )

    if submit:
        errors = []
        if age is None:
            errors.append("Age group")
        if gender is None:
            errors.append("Gender")
        if not relationship:  # checks for both None and "" (empty string)
            errors.append("Relationship")
        if budget is None:
            errors.append("Budget")
        if occasion is None:
            errors.append("Occasion")
        if not vibe:
            errors.append("Vibe")

        if errors:
            st.error("Please fill in the required fields: " + ", ".join(errors))
            st.stop()

        info = {
            "age": age,
            "gender": gender,
            "budget": budget,
            "occasion": occasion,
            "relationship": relationship,
            "vibe": vibe,
            "likes": likes,
            "dislikes": dislikes,
        }
        with st.spinner("Fetching personalized gift ideas..."):
            try:
                result = fetch_gift_ideas(info)
                st.session_state["gift_result"] = result
                st.rerun()
            except Exception as e:
                st.error(str(e))

if "gift_result" in st.session_state:

    result = st.session_state["gift_result"]
    st.subheader("Top Pick")
    col9, col10 = st.columns([2, 1])
    with col9:
        st.write(f'{result["top_pick"]}')
    with col10:
        st.button("Where to Buy this?")
    st.subheader("Other options to choose from")
    for i, alt in enumerate(result["alternatives"], start=1):
        col11, col12 = st.columns([3, 1])
        with col11:
            st.write(f"**{i}. { alt['item']}**")
        with col12:
            st.button("Available here", key=f"buy{i}")
