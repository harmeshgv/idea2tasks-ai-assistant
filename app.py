import streamlit as st
import json
import requests
import os
import re

st.set_page_config(page_title="AI Task Manager", layout="wide")
st.title("🧠 AI Project Task Manager")

idea = st.text_input("Input your project idea:")

choice = st.selectbox("Do you want to specify tools?", ["no", "yes"])
if choice == "yes":
    tools = st.text_input("List preferred tools (optional):")
else:
    tools = None

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("API key not found in environment variable GROQ_API_KEY")
    st.stop()

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

roadmap = None

if st.button("🚀 Generate Roadmap"):
    if not idea.strip():
        st.error("Please enter a valid project idea.")
    else:
        tool_hint = f"\nNote: Prefer using these tools if suitable - {tools}\n" if tools else ""

        data = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
You are an expert AI project planner and technical architect.

My project idea is:
\"{idea}\"

{tool_hint}

Please break this idea down into a complete development roadmap that includes:

1. Clear and well-defined **main processes or phases** (as modules or headings)
2. For each main process, provide detailed **sub-processes or steps** (as subheadings or tasks)
3. For each sub-process or task, suggest recommended **tools, technologies, or frameworks** to use
4. Provide an **ordered list of tasks** to be performed in each sub-process
5. Include optional task **dependencies** if applicable
6. Output everything in **structured JSON** format, with these fields:
   - `module` (main process or phase)
   - `submodules` (list of sub-processes, each with:)
       - `submodule_name`
       - `tasks` (ordered list of tasks)
       - `tools` (list of recommended tools or technologies)
   - `dependencies` (optional, for modules or submodules)

Make sure the roadmap is detailed, actionable, and developer-ready.
"""
                }
            ]
        }

        with st.spinner("💡 Thinking..."):
            response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            content = response.json()
            ai_message = content['choices'][0]['message']['content']

            match = re.search(r"```json(.*?)```", ai_message, re.DOTALL)
            if match:
                json_str = match.group(1).strip()
                try:
                    roadmap = json.loads(json_str)
                    st.success("✅ Roadmap generated successfully!")

                    # Save roadmap to file
                    with open("roadmap.json", "w") as f:
                        json.dump(roadmap, f, indent=2)

                    # Download button

                except json.JSONDecodeError:
                    st.error("❌ Failed to parse JSON from AI response.")
            else:
                st.error("❌ JSON block not found in AI response.")
        else:
            st.error(f"❌ API call failed ({response.status_code}): {response.text}")

# ======= Display Roadmap =======
# Once roadmap is parsed and available, display it
if roadmap:
    modules = roadmap.get("modules", [])  # Get the list from inside the "modules" key



    # Initialize session state to track task completion
    if 'completed_tasks' not in st.session_state:
        st.session_state.completed_tasks = {}

    # Show modules, submodules, tasks
    for module in modules:
        module_name = module.get("module", "Unnamed Module")
        submodules = module.get("submodules", [])
        dependencies = module.get("dependencies", [])

        with st.expander(f"📦 {module_name}", expanded=True):
            for sub in submodules:
                sub_name = sub.get("submodule_name", "Unnamed Submodule")
                tasks = sub.get("tasks", [])
                tools = sub.get("tools", [])
                sub_deps = sub.get("dependencies", [])

                st.markdown(f"### 🔧 {sub_name}")
                if tools:
                    st.markdown("**🛠️ Tools:** " + ", ".join(tools))
                for i, task in enumerate(tasks):
                    task_id = f"{module_name}_{sub_name}_{i}"
                    if task_id not in st.session_state.completed_tasks:
                        st.session_state.completed_tasks[task_id] = False
                    st.session_state.completed_tasks[task_id] = st.checkbox(
                        f"- {task}",
                        value=st.session_state.completed_tasks[task_id],
                        key=task_id
                    )
                if sub_deps:
                    st.markdown("🔗 **Depends on:**")
                    for dep in sub_deps:
                        st.markdown(f"- {dep}")

    # Save task progress
    if st.button("💾 Save Progress"):
        completed = {k: v for k, v in st.session_state.completed_tasks.items() if v}
        with open("completed_tasks.json", "w") as f:
            json.dump(completed, f, indent=2)
        st.success("✅ Progress saved to 'completed_tasks.json'")
        

    # Allow JSON download
    st.download_button(
    label="📥 Download Roadmap JSON",
    data=json.dumps(roadmap, indent=2),
    file_name="roadmap.json",
    mime="application/json",
    key="download_roadmap_button"  # 👈 Add a unique key here
)
    # Show the full JSON visually (optional for debugging)
    st.subheader("📋 Full Roadmap JSON")
    st.json(roadmap)
