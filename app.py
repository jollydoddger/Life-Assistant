import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Path to local JSON file where we store user workout data
DATA_FILE = "workout_data.json"

# ----- Helper Functions -----
def load_workout_data():
    """Load workout history from local JSON file."""
    if not os.path.exists(DATA_FILE):
        # If file does not exist, return a template structure
        return {
            "user_equipment": "",
            "workouts": []
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_workout_data(data):
    """Save workout history to local JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_workout_plan(equipment, history, feedback):
    """
    Query the OpenAI ChatCompletion API to generate a workout plan.
    """
    system_message = (
        "You are a fitness coach specialized in muscle building. "
        "Provide a list of exercises and a structured workout plan based on the user's available equipment, workout history, and feedback."
    )

    user_message = f"""
    Available equipment: {equipment}
    Workout history: {history}
    Feedback: {feedback}

    Generate the next workout plan.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=600
    )

    return response["choices"][0]["message"]["content"]

# ----- Streamlit UI -----
def main():
    st.title("Adaptive Workout Planner (ChatGPT-Powered)")

    # Load or create workout data
    workout_data = load_workout_data()

    # Section 1: Equipment
    st.subheader("1. Your Available Equipment")
    user_equipment = st.text_input(
        "List the free weights or equipment you have (e.g., dumbbells up to 25 lbs, resistance bands, etc.):",
        value=workout_data.get("user_equipment", "")
    )

    # Update local data (but only save when the user generates a plan)
    workout_data["user_equipment"] = user_equipment

    # Section 2: Feedback
    st.subheader("2. Feedback on Previous Workout")
    user_feedback = st.text_area(
        "Write how the last workout felt. (Too easy? Too hard? Achy joints? Etc.)",
        value="",
        height=100
    )

    # Section 3: Generate Workout Button
    if st.button("Generate Next Workout Plan"):
        # Generate plan from the LLM
        new_plan = generate_workout_plan(
            equipment=user_equipment,
            history=workout_data["workouts"],
            feedback=user_feedback
        )

        # Display the LLM-generated plan
        st.markdown("### Your Next Workout Plan")
        st.write(new_plan)

        # Store the plan as the "current" workout
        workout_data["workouts"].append({
            "plan": new_plan,
            "feedback": user_feedback
        })

        # Save to JSON
        save_workout_data(workout_data)

    # Section 4: Log your completed workout
    st.subheader("4. Update Workout Results")
    if len(workout_data["workouts"]) > 0:
        # The last workout is the most recent one
        last_workout = workout_data["workouts"][-1]
        st.markdown("**Last Generated Workout Plan:**")
        st.write(last_workout["plan"])

        st.write("#### Enter how you performed:")
        sets_completed = st.text_area("Describe sets/reps/weights used (optional):", "")
        perceived_difficulty = st.slider("Difficulty (1 = too easy, 10 = too hard)", 1, 10, 5)

        if st.button("Save Workout Results"):
            # Store the results in the same workout entry
            last_workout["results"] = {
                "sets_completed": sets_completed,
                "perceived_difficulty": perceived_difficulty
            }
            save_workout_data(workout_data)
            st.success("Workout results saved!")

    st.markdown("---")
    st.write("Note: This app is not medical advice. Always consult a professional before beginning any exercisU
import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Path to local JSON file where we store user workout data
DATA_FILE = "workout_data.json"

# ----- Helper Functions -----
def load_workout_data():
    """Load workout history from local JSON file."""
    if not os.path.exists(DATA_FILE):
        # If file does not exist, return a template structure
        return {
            "user_equipment": "",
            "workouts": []
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_workout_data(data):
    """Save workout history to local JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_workout_plan(equipment, history, feedback):
    """
    Query the OpenAI ChatCompletion API to generate a workout plan.
    """
    system_message = (
        "You are a fitness coach specialized in muscle building. "
        "Provide a list of exercises and a structured workout plan based on the user's available equipment, workout history, and feedback."
    )

    user_message = f"""
    Available equipment: {equipment}
    Workout history: {history}
    Feedback: {feedback}

    Generate the next workout plan.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=600
    )

    return response["choices"][0]["message"]["content"]

# ----- Streamlit UI -----
def main():
    st.title("Adaptive Workout Planner (ChatGPT-Powered)")

    # Load or create workout data
    workout_data = load_workout_data()

    # Section 1: Equipment
    st.subheader("1. Your Available Equipment")
    user_equipment = st.text_input(
        "List the free weights or equipment you have (e.g., dumbbells up to 25 lbs, resistance bands, etc.):",
        value=workout_data.get("user_equipment", "")
    )

    # Update local data (but only save when the user generates a plan)
    workout_data["user_equipment"] = user_equipment

    # Section 2: Feedback
    st.subheader("2. Feedback on Previous Workout")
    user_feedback = st.text_area(
        "Write how the last workout felt. (Too easy? Too hard? Achy joints? Etc.)",
        value="",
        height=100
    )

    # Section 3: Generate Workout Button
    if st.button("Generate Next Workout Plan"):
        # Generate plan from the LLM
        new_plan = generate_workout_plan(
            equipment=user_equipment,
            history=workout_data["workouts"],
            feedback=user_feedback
        )

        # Display the LLM-generated plan
        st.markdown("### Your Next Workout Plan")
        st.write(new_plan)

        # Store the plan as the "current" workout
        workout_data["workouts"].append({
            "plan": new_plan,
            "feedback": user_feedback
        })

        # Save to JSON
        save_workout_data(workout_data)

    # Section 4: Log your completed workout
    st.subheader("4. Update Workout Results")
    if len(workout_data["workouts"]) > 0:
        # The last workout is the most recent one
        last_workout = workout_data["workouts"][-1]
        st.markdown("**Last Generated Workout Plan:**")
        st.write(last_workout["plan"])

        st.write("#### Enter how you performed:")
        sets_completed = st.text_area("Describe sets/reps/weights used (optional):", "")
        perceived_difficulty = st.slider("Difficulty (1 = too easy, 10 = too hard)", 1, 10, 5)

        if st.button("Save Workout Results"):
            # Store the results in the same workout entry
            last_workout["results"] = {
                "sets_completed": sets_completed,
                "perceived_difficulty": perceived_difficulty
            }
            save_workout_data(workout_data)
            st.success("Workout results saved!")

    st.markdown("---")
    st.write("Note: This app is not medical advice. Always consult a professional before beginning any exercise program.")

if __name__ == "__main__":
    main()
import streamlit as st
import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Path to local JSON file where we store user workout data
DATA_FILE = "workout_data.json"

# ----- Helper Functions -----
def load_workout_data():
    """Load workout history from local JSON file."""
    if not os.path.exists(DATA_FILE):
        # If file does not exist, return a template structure
        return {
            "user_equipment": "",
            "workouts": []
        }
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_workout_data(data):
    """Save workout history to local JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def generate_workout_plan(equipment, history, feedback):
    """
    Query the OpenAI ChatCompletion API to generate a workout plan.
    """
    system_message = (
        "You are a fitness coach specialized in muscle building. "
        "Provide a list of exercises and a structured workout plan based on the user's available equipment, workout history, and feedback."
    )

    user_message = f"""
    Available equipment: {equipment}
    Workout history: {history}
    Feedback: {feedback}

    Generate the next workout plan.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=600
    )

    return response["choices"][0]["message"]["content"]

# ----- Streamlit UI -----
def main():
    st.title("Adaptive Workout Planner (ChatGPT-Powered)")

    # Load or create workout data
    workout_data = load_workout_data()

    # Section 1: Equipment
    st.subheader("1. Your Available Equipment")
    user_equipment = st.text_input(
        "List the free weights or equipment you have (e.g., dumbbells up to 25 lbs, resistance bands, etc.):",
        value=workout_data.get("user_equipment", "")
    )

    # Update local data (but only save when the user generates a plan)
    workout_data["user_equipment"] = user_equipment

    # Section 2: Feedback
    st.subheader("2. Feedback on Previous Workout")
    user_feedback = st.text_area(
        "Write how the last workout felt. (Too easy? Too hard? Achy joints? Etc.)",
        value="",
        height=100
    )

    # Section 3: Generate Workout Button
    if st.button("Generate Next Workout Plan"):
        # Generate plan from the LLM
        new_plan = generate_workout_plan(
            equipment=user_equipment,
            history=workout_data["workouts"],
            feedback=user_feedback
        )

        # Display the LLM-generated plan
        st.markdown("### Your Next Workout Plan")
        st.write(new_plan)

        # Store the plan as the "current" workout
        workout_data["workouts"].append({
            "plan": new_plan,
            "feedback": user_feedback
        })

        # Save to JSON
        save_workout_data(workout_data)

    # Section 4: Log your completed workout
    st.subheader("4. Update Workout Results")
    if len(workout_data["workouts"]) > 0:
        # The last workout is the most recent one
        last_workout = workout_data["workouts"][-1]
        st.markdown("**Last Generated Workout Plan:**")
        st.write(last_workout["plan"])

        st.write("#### Enter how you performed:")
        sets_completed = st.text_area("Describe sets/reps/weights used (optional):", "")
        perceived_difficulty = st.slider("Difficulty (1 = too easy, 10 = too hard)", 1, 10, 5)

        if st.button("Save Workout Results"):
            # Store the results in the same workout entry
            last_workout["results"] = {
                "sets_completed": sets_completed,
                "perceived_difficulty": perceived_difficulty
            }
            save_workout_data(workout_data)
            st.success("Workout results saved!")

    st.markdown("---")
    st.write("Note: This app is not medical advice. Always consult a professional before beginning any exercise program.")

if __name__ == "__main__":
    main()
