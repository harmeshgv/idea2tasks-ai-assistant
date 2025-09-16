import streamlit as st
import json
import requests
import os
import re

st.set_page_config(page_title="AI Task Manager", layout="wide")
st.title("🧠 AI Project Task Manager")

# ---------- Idea & Tools Input ----------
idea = st.text_input("Input your project idea:")

choice = st.selectbox("Do you want to specify tools?", ["no", "yes"])
tools = st.text_input("List preferred tools (optional):") if choice == "yes" else None

# ---------- Sidebar: API Key ----------
with st.sidebar:
    st.header("⚙️ Settings")
    api_key_input = st.text_input(
        "Enter your API key",
        type="password",
        placeholder="Paste your API key here",
        key="api_key_input"
    )
    if st.button("🔑 Submit API Key"):
        if not api_key_input:
            st.error("⚠️ Please enter a valid API key!")
        else:
            st.session_state.api_key = api_key_input
            st.success("API key submitted successfully!")
            st.rerun()

# ---------- API Key Handling ----------
api_key = st.session_state.get("api_key") or os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("⚠️ API key not set. Please enter it in the sidebar or set GROQ_API_KEY.")
    st.stop()

# ---------- Initialize Session State ----------
if "roadmap" not in st.session_state:
    st.session_state["roadmap"] = None
if "completed_tasks" not in st.session_state:
    st.session_state["completed_tasks"] = {}

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# ---------- Generate Roadmap ----------
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
   - `module`
   - `submodules` (list of sub-processes, each with:)
       - `submodule_name`
       - `tasks`
       - `tools`
   - `dependencies` (optional)
"""
                }
            ]
        }

        with st.spinner("💡 Thinking..."):
            response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            content = response.json()
            ai_message = content['choices'][0]['message']['content']

            # Try fenced JSON first, else fallback to raw message
            match = re.search(r"```json(.*?)```", ai_message, re.DOTALL)
            json_str = match.group(1).strip() if match else ai_message

            try:
                roadmap = json.loads(json_str)
                st.session_state["roadmap"] = roadmap
                st.success("✅ Roadmap generated successfully!")

                # Save to file
                with open("roadmap.json", "w") as f:
                    json.dump(roadmap, f, indent=2)

            except json.JSONDecodeError:
                st.error("❌ Failed to parse JSON from AI response.")
        else:
            st.error(f"❌ API call failed ({response.status_code}): {response.text}")

# ---------- Display Roadmap ----------
roadmap = st.session_state["roadmap"]
if roadmap:
    modules = roadmap.get("modules", [])

    for module in modules:
        module_name = module.get("module", "Unnamed Module")
        submodules = module.get("submodules", [])
        dependencies = module.get("dependencies", [])

        with st.expander(f"📦 {module_name}", expanded=True):
            for sub in submodules:
                sub_name = sub.get("submodule_name", "Unnamed Submodule")
                tasks = sub.get("tasks", [])
                tools_list = sub.get("tools", [])
                sub_deps = sub.get("dependencies", [])

                st.markdown(f"### 🔧 {sub_name}")
                if tools_list:
                    st.markdown("**🛠️ Tools:** " + ", ".join(tools_list))

                for i, task in enumerate(tasks):
                    # Create a safe unique key
                    task_id = f"{module_name}_{sub_name}_{i}".replace(" ", "_")
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

    # Save progress
    if st.button("💾 Save Progress"):
        completed = {k: v for k, v in st.session_state.completed_tasks.items() if v}
        with open("completed_tasks.json", "w") as f:
            json.dump(completed, f, indent=2)
        st.success("✅ Progress saved to 'completed_tasks.json'")

    # Download roadmap
    st.download_button(
        label="📥 Download Roadmap JSON",
        data=json.dumps(roadmap, indent=2),
        file_name="roadmap.json",
        mime="application/json",
        key="download_roadmap_button"
    )

    # Show raw JSON for debugging
    st.subheader("📋 Full Roadmap JSON")
    st.json(roadmap)
