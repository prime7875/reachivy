# import streamlit as st
# import tempfile

# from state import init_state, add_turn
# from interview import start_interview, ai_ask, user_answer
# from report import generate_report

# st.set_page_config(layout="wide")
# st.title("🎤 AI Interview")

# # ---------- INIT ----------
# if "state" not in st.session_state:
#     st.session_state.state = init_state()

# if "audio_key" not in st.session_state:
#     st.session_state.audio_key = 0

# state = st.session_state.state

# # ---------- LAYOUT ----------
# main_col, side_col = st.columns([3, 1])

# # =======================
# # 👉 SIDE TAB (LIVE NOTES)
# # =======================
# with side_col:
#     st.subheader("📝 Interview So Far")

#     if not state["transcript"]:
#         st.caption("Conversation will appear here…")

#     for turn in state["transcript"]:
#         if turn["role"] == "assistant":
#             st.markdown(f"**🤖 AI:** {turn['content']}")
#         else:
#             st.markdown(f"**🗣️ You:** {turn['content']}")

# # =======================
# # 👉 MAIN INTERVIEW AREA
# # =======================
# with main_col:

#     # ---- AI STARTS FIRST ----
#     if not state["started"]:
#         intro, audio = start_interview(state)
#         st.audio(audio, autoplay=True)
#         st.markdown(intro)

#     # ---- CURRENT QUESTION ----
#     if state["conversation"]:
#         current_question = state["conversation"][-1]["content"]
#         st.markdown(f"### 🧠 {current_question}")

#     # ---- MIC INPUT ----
#     st.markdown("### 🎙️ Your Answer")
#     audio_input = st.audio_input(
#         "Tap the mic and speak",
#         key=f"audio_{st.session_state.audio_key}",
#         disabled=state.get("has_draft", False)
#     )

#     # ---- VOICE → TEXT (NO SUBMIT YET) ----
#     if audio_input and state["waiting_for_user"] and not state.get("has_draft", False):
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
#             f.write(audio_input.read())
#             audio_path = f.name

#         text = user_answer(audio_path)

#         state["draft_answer"] = text
#         state["has_draft"] = True

#     # ---- EDITABLE TEXT + ACTIONS ----
#     if state.get("has_draft", False):
#         edited_text = st.text_area(
#             "✍️ Edit your answer (optional)",
#             value=state["draft_answer"],
#             height=120
#         )

#         col1, col2 = st.columns(2)

#         with col1:
#             if st.button("✅ Submit Answer"):
#                 add_turn(state, "user", edited_text)

#                 state["draft_answer"] = ""
#                 state["has_draft"] = False
#                 state["waiting_for_user"] = False

#                 # AI asks next question
#                 question, audio = ai_ask(state)
#                 state["waiting_for_user"] = True

#                 # 🔥 RESET AUDIO INPUT WIDGET
#                 st.session_state.audio_key += 1

#                 st.audio(audio, autoplay=True)
#                 st.rerun()

#         with col2:
#             if st.button("🔄 Re-record"):
#                 state["draft_answer"] = ""
#                 state["has_draft"] = False
#                 st.session_state.audio_key += 1
#                 st.rerun()



import streamlit as st
import tempfile

from state import init_state, add_turn
from interview import start_interview, ai_ask, user_answer
from report import generate_report

st.set_page_config(layout="wide")
st.title("Career Discovery Conversation")

# ---------- INIT ----------
if "state" not in st.session_state:
    st.session_state.state = init_state()

if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0

state = st.session_state.state

# ---------- LAYOUT ----------
main_col, side_col = st.columns([3, 1])

# =======================
# 👉 SIDE TAB (LIVE NOTES)
# =======================
with side_col:
    st.subheader("Career Notes")

    if not state["transcript"]:
        st.caption("Key points from our conversation will appear here…")

    for turn in state["transcript"]:
        if turn["role"] == "assistant":
            st.markdown(f"**Guide:** {turn['content']}")
        else:
            st.markdown(f"**You:** {turn['content']}")

# =======================
# 👉 MAIN INTERVIEW AREA
# =======================
with main_col:

    # ---- AI STARTS FIRST ----
    if not state["started"] and not state["ended"]:
        intro, audio = start_interview(state)
        st.audio(audio, autoplay=True)
        st.markdown(intro)

    # ---- CURRENT QUESTION ----
    if state["conversation"] and not state["ended"]:
        current_question = state["conversation"][-1]["content"]
        st.markdown(f"### {current_question}")

    # =======================
    # 🎙️ INTERVIEW MODE
    # =======================
    if not state["ended"]:

        st.markdown("### Your Response")

        audio_input = st.audio_input(
            "Tap the mic and share your thoughts",
            key=f"audio_{st.session_state.audio_key}",
            disabled=state.get("has_draft", False)
        )

        # ---- VOICE → TEXT ----
        if audio_input and state["waiting_for_user"] and not state.get("has_draft", False):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                f.write(audio_input.read())
                audio_path = f.name

            text = user_answer(audio_path)
            state["draft_answer"] = text
            state["has_draft"] = True

        # ---- EDIT + SUBMIT ----
        if state.get("has_draft", False):
            edited_text = st.text_area(
                "Edit your response if you’d like (optional)",
                value=state["draft_answer"],
                height=120
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("Submit Response"):
                    add_turn(state, "user", edited_text)

                    state["draft_answer"] = ""
                    state["has_draft"] = False
                    state["waiting_for_user"] = False

                    question, audio = ai_ask(state)
                    state["waiting_for_user"] = True

                    st.session_state.audio_key += 1
                    st.audio(audio, autoplay=True)
                    st.rerun()

            with col2:
                if st.button("Re-record"):
                    state["draft_answer"] = ""
                    state["has_draft"] = False
                    st.session_state.audio_key += 1
                    st.rerun()

        st.divider()

        # ---- END DISCUSSION ----
        if st.button("Finish Conversation"):
            state["ended"] = True
            state["waiting_for_user"] = False

            transcript_text = [
                f"{t['role'].upper()}: {t['content']}"
                for t in state["transcript"]
            ]

            with st.spinner("Generating your report..."):
                state["report"] = generate_report(transcript_text)

            st.rerun()

    # =======================
    # 📄 REPORT MODE
    # =======================
    else:
        st.subheader("Your Career Exploration Summary")
        st.markdown(state["report"])
