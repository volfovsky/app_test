import streamlit as st

def calculate_humility_score(responses):
    """
    Given a dictionary of question IDs and numeric responses,
    calculate an intellectual humility score from 1 to 10.
    This example uses a simple approach where:
      - Most questions: higher rating -> higher humility
      - Reverse scored questions: lower rating -> higher humility
    """
    # Define which question indices are reverse scored
    # (i.e., 5, 6, and 9 in the above list, but 0-based indices would be 4, 5, and 8)
    reverse_scored = [4, 5, 8]

    # Convert responses to a standardized scale
    # For normal questions: direct use of the response (1 = low humility, 5 = high humility)
    # For reverse scored: we invert the response (5 = low humility, 1 = high humility)
    total_score = 0
    for i, response in enumerate(responses):
        if i in reverse_scored:
            # Invert the score on a 1–5 scale
            question_score = 6 - response
        else:
            question_score = response

        total_score += question_score

    # The maximum total_score for 10 questions (on a 1–5 scale) 
    # after reversing the designated ones would be 50.
    # We'll map that to a 1–10 scale.
    # E.g., if total_score = 50 => final humility score = 10
    #       if total_score = 10 => final humility score = 1
    # So final_score = ( (total_score - 10) / (50 - 10) ) * (10 - 1) + 1
    # But for simplicity, let's just scale it directly to 1–10:
    # final_score = (total_score / 50) * 10
    final_score = (total_score / 50) * 10

    # Round to 1 decimal place for readability
    return round(final_score, 1)

def get_recommendations(score):
    """
    Provide recommendations based on the final humility score.
    """
    if score <= 3:
        return (
            "You appear to be less open to others' viewpoints or new information. "
            "Try practicing active listening, asking clarifying questions, "
            "and seeking out mentors who challenge your thinking. Small daily steps—"
            "like reading diverse opinions—can help."
        )
    elif 3 < score <= 6:
        return (
            "You show some openness but might benefit from further reflection. "
            "Consider journaling about situations where you might have been overly attached "
            "to your beliefs. Seek critical feedback and learn to embrace 'I don't know' moments."
        )
    elif 6 < score <= 8:
        return (
            "You're fairly intellectually humble. Keep fostering an environment where "
            "people feel comfortable challenging your ideas. Engage in debate clubs or "
            "workshops that encourage thoughtful disagreement."
        )
    else:  # score > 8
        return (
            "You demonstrate high intellectual humility. To maintain this level of openness, "
            "continue challenging yourself with new perspectives, welcoming feedback, and "
            "coaching others on how to become more open-minded."
        )

# Streamlit application
def main():
    st.title("Intellectual Humility Chatbot")
    st.write("""
    This chatbot will ask you 10 quick questions to gauge how intellectually humble you are.
    Please answer honestly for the most accurate result.
    """)

    # Here are our questions (same as in the example above).
    questions = [
        "I enjoy learning from people whose opinions differ from mine.",
        "I find it easy to admit when I’m wrong.",
        "I’m open to revisiting and potentially changing my core beliefs.",
        "I often seek feedback and constructive criticism.",
        "I quickly dismiss opposing viewpoints.",  # reverse scored
        "I find it difficult to say 'I don’t know.'",  # reverse scored
        "I value expertise in areas where I’m not knowledgeable.",
        "I try to see issues from multiple perspectives.",
        "It is important to me to be right, even if evidence suggests otherwise.",  # reverse scored
        "I regularly reflect on how my beliefs may be biased or incomplete."
    ]

    # We'll store the user responses in a list
    responses = []

    # For each question, create a radio button for user input (1–5 scale)
    for i, question in enumerate(questions):
        user_answer = st.radio(
            label=f"Q{i+1}. {question}",
            options=[1, 2, 3, 4, 5],
            index=2,  # default selection in the middle
            key=f"q{i}"
        )
        responses.append(user_answer)

    # Once the user has answered all questions, display a button to calculate
    if st.button("Get my Humility Score!"):
        final_score = calculate_humility_score(responses)
        recommendations = get_recommendations(final_score)

        st.subheader(f"Your Intellectual Humility Score: {final_score}/10")
        st.write(recommendations)


if __name__ == "__main__":
    main()
