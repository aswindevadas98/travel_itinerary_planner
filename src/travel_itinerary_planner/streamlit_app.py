import streamlit as st
from main import run_crew

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Travel Itinerary Planner",
    page_icon="🌍",
    layout="wide"
)

# ── Header ───────────────────────────────────────────────────
st.title("🌍 AI Travel Itinerary Planner")
st.markdown("Drop your destination and interests — our AI crew builds your perfect itinerary.")
st.divider()

# ── Sidebar inputs ───────────────────────────────────────────
with st.sidebar:
    st.header("✈️ Trip Details")

    destination = st.text_input(
        "Destination",
        placeholder="eg. Trivandrum, Kerala"
    )

    trip_duration = st.number_input(
        "Trip Duration (days)",
        min_value=1,
        max_value=30,
        value=5,
        step=1
    )

    interests = st.text_input(
        "Your Interests",
        placeholder="eg. beach, temple, food, trekking"
    )

    st.divider()
    plan_button = st.button("🗺️ Plan My Trip", use_container_width=True, type="primary")

# ── Duration hint (mirrors TripDurationValidator logic) ──────
if trip_duration:
    if trip_duration < 3:
        st.sidebar.warning("⚠️ Under 3 days — this will be a surface-level trip.")
    elif trip_duration <= 10:
        st.sidebar.success("✅ Ideal trip duration!")
    else:
        st.sidebar.info("💡 Over 10 days — consider splitting into two trips.")

# ── Main panel ───────────────────────────────────────────────
if plan_button:
    if not destination.strip():
        st.error("Please enter a destination.")
    elif not interests.strip():
        st.error("Please enter at least one interest.")
    else:
        with st.spinner(f"Planning your {trip_duration}-day trip to {destination}... this may take a moment ⏳"):
            try:
                outputs = run_crew(destination, int(trip_duration), interests)

                st.success("✅ Your itinerary is ready!")
                st.divider()

                # ── Three tabs for each output ────────────────
                tab1, tab2, tab3 = st.tabs([
                    "📍 Destination Brief",
                    "🗓️ Day-by-Day Itinerary",
                    "💰 Budget Breakdown"
                ])

                with tab1:
                    st.subheader(f"Destination Brief — {destination}")
                    st.markdown(outputs["destination_brief"])

                with tab2:
                    st.subheader(f"{trip_duration}-Day Itinerary")
                    st.markdown(outputs["day_by_day_plan"])

                with tab3:
                    st.subheader("Budget Breakdown")
                    st.markdown(outputs["budget_breakdown"])

                # ── Download button ───────────────────────────
                st.divider()
                full_md = (
                    f"# Travel Itinerary: {destination}\n\n"
                    f"## Destination Brief\n{outputs['destination_brief']}\n\n"
                    f"## Day-by-Day Plan\n{outputs['day_by_day_plan']}\n\n"
                    f"## Budget Breakdown\n{outputs['budget_breakdown']}"
                )
                st.download_button(
                    label="⬇️ Download Your Itinerary",
                    data=full_md,
                    file_name=f"{destination.replace(' ', '_').replace(',', '')}_itinerary.md",
                    mime="text/markdown",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Something went wrong: {e}")

else:
    # ── Empty state ───────────────────────────────────────────
    st.info("👈 Fill in your trip details in the sidebar and click **Plan My Trip** to get started.")