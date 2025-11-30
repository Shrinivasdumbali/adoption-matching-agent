# 🐾 Animal Adoption Matching Agent

**Capstone Project for Google AI Agents Intensive**

Hi there! 👋 This is my capstone project—a multi-agent AI system designed to solve a heartbreaking problem: shelter animals being returned or euthanized due to poor matching.

Instead of a simple search filter, I built a system that "thinks" like an adoption counselor. It uses three specialized AI agents to understand lifestyle needs, calculate compatibility scores, and provide personalized advice for new pet parents.

---

## 🚀 How It Works (The "Think-Act-Observe" Loop)

I designed the system using a multi-agent architecture where each agent handles a specific cognitive task:

1.  **Thinking (Profiling Agent):** First, this agent reads the adopter's profile. It doesn't just look at keywords; it analyzes their lifestyle, home environment, and experience level to understand what they *actually* need.
2.  **Acting (Matching Agent):** This agent runs the logic. It uses a custom 5-factor algorithm to score every available animal against the adopter's profile. It produces a compatibility score (0-100) based on real metrics like energy levels and safety with kids.
3.  **Observing (Support Agent):** Once a match is made, this agent steps in to provide post-adoption guidance. It remembers the context (e.g., "High energy dog + Apartment") and gives specific advice to make the transition successful.

---

## 🛠️ Tech Stack

*   **Python 3.11+**
*   **Google Gemini 2.5 Flash** (The LLM brain powering the agents)
*   **Google AI Agent Development Kit** (For structure)
*   **JSON-based Memory** (To persist sessions and remember past matches)

---

## 📂 Project Structure

Here is how I organized the code:

*   `agents/` - Contains the 3 specialized agents (Profiler, Matcher, Support).
*   `tools/` - The "hands" of the system. Includes the `Data Loader` (for CSVs) and the custom `Compatibility Scorer` algorithm.
*   `models/` - Handles state management. `AdoptionSession` tracks the journey, and `MemoryStore` saves it to JSON.
*   `data/` - Mock CSV data representing a shelter database (`animal_data.csv`, `adopter_data.csv`).
*   `main.py` - The conductor that orchestrates the whole workflow.

---

## ⚡ Quick Start

Want to run this on your machine? Here is how:

1.  **Clone the repo:**
    ```
    git clone https://github.com/YOUR_USERNAME/adoption-matching-agent.git
    cd adoption-matching-agent
    ```

2.  **Set up your environment:**
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Add your API Key:**
    Create a `.env` file and add your Google API key:
    ```
    GOOGLE_API_KEY=your_key_here
    ```

4.  **Run the Agent:**
    ```
    python main.py
    ```

---

## 📊 Results

In my testing with sample data, the system achieved an **average compatibility score of 92.8/100**. More importantly, it successfully flagged "risky" matches (like high-energy dogs for busy families) and prioritized safe, sustainable pairings.

---

## 🔮 Future Improvements

If I had more time, I would love to:
*   Connect this to the **Petfinder API** for live animal data.
*   Build a simple **React frontend** so shelter staff can use it on tablets.
*   Add an **Image Analysis Agent** to tag animal photos automatically.

---

*Created by Shrini*
