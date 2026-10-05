# For each of the 3 tasks below, write two prompts: a “bad” prompt (vague, no framing) and a “good” prompt (using at least 2 of the 3 techniques
# Send both prompts to an API (or use the mock function from the Guided Example) and display the results side by side
import os
import openai

MOCK_RESPONSES = {
    "no_frame": (
        "st.session_state is a Streamlit feature that stores variables between reruns. "
        "It works like a dictionary: st.session_state['count'] = 0."
    ),
    "with_frame": (
        "st.session_state is Streamlit's memory. Streamlit reruns your script on every "
        "interaction, so normal variables reset each time. Session state keeps values "
        "alive across reruns, like a notepad a waiter keeps for your table while "
        "serving other customers.\n\n"
        "Use cases: chat history, multi-step forms, counters, cached user choices.\n\n"
        "Example:\n"
        "if 'count' not in st.session_state:\n"
        "    st.session_state.count = 0\n"
        "if st.button('Add'):\n"
        "    st.session_state.count += 1\n"
        "st.write(st.session_state.count)"
    ),
    "poor_framing": (
        "Sure! Here are your tasks:\n"
        '[{"task": "Finish homework", "priority": "high", "status": "pending"}, '
        '{"task": "Go grocery shopping", "priority": "medium", "status": "pending"}, '
        '{"task": "Make dinner", "priority": "high", "status": "pending"}, ...]'
    ),
    "few_shot": (
        "[\n"
        '  {"title": "Finish homework", "priority": "high", "status": "To-Do"},\n'
        '  {"title": "Go grocery shopping", "priority": "medium", "status": "To-Do"},\n'
        '  {"title": "Make dinner", "priority": "high", "status": "To-Do"},\n'
        '  {"title": "Walk dogs", "priority": "medium", "status": "To-Do"},\n'
        '  {"title": "Fold laundry", "priority": "low", "status": "To-Do"},\n'
        '  {"title": "Weed garden", "priority": "low", "status": "To-Do"},\n'
        '  {"title": "Clean up grass clippings", "priority": "low", "status": "To-Do"}\n'
        "]"
    ),
}


def get_response(prompt, mock_key):
    """Try the real API; fall back to a canned mock response if there is no key or the call fails."""

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            return f"[MOCK - API error: {type(e).__name__}]\n{MOCK_RESPONSES[mock_key]}"
    return f"[MOCK - no API key]\n{MOCK_RESPONSES[mock_key]}"


# Task 1 — Code explanation:
# Get the model to explain what st.session_state does in Streamlit.
print("=" * 60)
print("Task 1: Code Explanation")
print("Get the model to explain what st.session_state does in Streamlit.")
print("=" * 60)

prompt_no_frame = "Explain st.session_state."
prompt_with_frame = (
    "You are a systems architect who is well verse in the Streamlit platform for creating powerful AI driven web-pages. "
    "Explain the key features of st.session_state, it's use cases, and implementing it in a real world example. "
    "Use a clear analogy to make it user friendly for the reader who may not be as familiar with tech-speak. "
    "Keep in concise, under 200 words."
)

# Task 2 — Data formatting:
print("=" * 60)
print("Task 2: Data Formatting")
print(
    "Get the model to convert a natural language list of tasks into a JSON array with title, priority, and status fields."
)

prompt_poor_framing = "Convert the following list of tasks into a JSON array with title, priority and status fields. List: Finish homework, go grocery shopping, make dinner, walk dogs, fold laundry, weed garden, clean up grass clippings."
prompt_few_shot = """Convert a list of tasks into a JSON array. Each item has "title", "priority" (low, medium, high, or urgent), and "status" (To-Do, In-Progress, or Complete). Infer priority from how important or time-sensitive the task sounds, and use "To-Do" unless the task says otherwise. Return only valid JSON.

Example
Input: Pay rent by Friday, water the plants, finish slides (halfway done)
Output:
[
  {"title": "Pay rent by Friday", "priority": "urgent", "status": "To-Do"},
  {"title": "Water the plants", "priority": "low", "status": "To-Do"},
  {"title": "Finish slides", "priority": "high", "status": "In-Progress"}
]

Now convert this list:
Input: Finish homework, go grocery shopping, make dinner, walk dogs, fold laundry, weed garden, clean up grass clippings.
Output:
"""

# Task 3 — System prompt design:
# Write a system prompt for a "Course Study Assistant" that answers questions based on provided context from course notes. The system prompt should instruct the model to: use the provided context only, admit when it doesn’t know, keep answers under 150 words, and include which source document the answer came from.

messages = [
    {
        "role": "system",
        "content": (
            "You are a helpful course study assistant for a course on AI software engineering. Answer questions based on only the provided context. If the context doesn't contain the answer, say so honestly. Keep responses to under 150 words and include the source document title to where the answers came from."
        ),
    },
    # {"role": "user", "content": user_question},
]

print(f"\nPrompt (no framing): '{prompt_no_frame}'")
print(f"Response:\n{get_response(prompt_no_frame, 'no_frame')}\n")

print(f"Prompt (with framing): '{prompt_with_frame[:80]}...'")
print(f"Response:\n{get_response(prompt_with_frame, 'with_frame')}\n")

print(f"\nPoorly framed prompt:\n{prompt_poor_framing}")
print(f"\nResponse:\n{get_response(prompt_poor_framing, 'poor_framing')}")

print(f"\nFew-shot prompt (showing pattern):\n{prompt_few_shot}")
print(f"\nResponse:\n{get_response(prompt_few_shot, 'few_shot')}")
