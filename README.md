# 🧠 AI Project Task Manager

Turn your project idea into a clear, developer-ready roadmap with actionable tasks, tool suggestions, and progress tracking!

---

## 🚀 What is this?

**AI Project Task Manager** is a Streamlit-based web app that uses advanced AI (via the Groq API) to break down any project idea into an organized, actionable roadmap.

- Enter your idea, optionally specify tools, and get a structured JSON roadmap.
- See each phase/module, with sub-tasks, tool recommendations, and dependencies.
- Check off tasks as you progress and save your progress to disk.
- Download the generated roadmap as JSON for further use.

---

## 🖥️ Features

- **AI-powered idea-to-roadmap:** Turn any project idea into a structured development plan.
- **Tool preferences:** Optionally suggest tools/technologies and the AI will include them if suitable.
- **Detailed breakdown:** Get modules, submodules, ordered tasks, tool suggestions, and dependencies.
- **Task tracking:** Check off completed tasks right in the UI.
- **Progress saving:** Save your progress to a local file and pick up where you left off.
- **Downloadable roadmap:** Export your project roadmap as a JSON file.
- **Visual JSON viewer:** Inspect the full AI-generated roadmap data.

---

## 🛠️ Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/) (`pip install streamlit`)
- [requests](https://pypi.org/project/requests/)

---

## 🔑 Setup

1. **Clone this repo**

   ```bash
   git clone https://github.com/yourusername/ai-project-task-manager.git
   cd ai-project-task-manager
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Groq API key**

   - [Get a Groq API key](https://console.groq.com/)
   - Set it as an environment variable:  
     On Linux/macOS:
     ```bash
     export GROQ_API_KEY=your_key_here
     ```
     On Windows (CMD):
     ```cmd
     set GROQ_API_KEY=your_key_here
     ```

4. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 📝 Usage

1. Enter your project idea in the input box.
2. (Optional) Specify any tools or frameworks you want to use.
3. Click **"🚀 Generate Roadmap"** and wait for the AI to respond.
4. Browse the generated roadmap, check off tasks as you complete them.
5. Click **"💾 Save Progress"** to save which tasks you’ve completed.
6. Download the roadmap JSON if desired.

---

## 📦 File Structure

```plaintext
app.py              # Main Streamlit app
roadmap.json        # Example output roadmap (generated)
completed_tasks.json# Your saved progress (generated)
README.md           # This file
requirements.txt    # Python package requirements
```

---

## 🤖 How does the AI work?

The app uses Groq’s API (Llama-4) to:

- Parse your idea and (optionally) preferred tools.
- Generate a multi-level roadmap (modules, submodules, ordered tasks, tool suggestions).
- Output the result as structured JSON for easy use and display.

---

## ⚡ Example Output

```json
{
  "modules": [
    {
      "module": "Data Collection",
      "submodules": [
        {
          "submodule_name": "Gather Requirements",
          "tasks": ["Interview stakeholders", "Define project scope"],
          "tools": ["Google Docs", "Notion"]
        }
      ]
    }
  ]
}
```

---

## 🛡️ Disclaimer

- This tool is for educational/demo purposes.
- Actual project management and technical details may need further human review.

---

## 💡 Ideas & Contributions

Feel free to open issues or PRs to suggest improvements or new features!

---
