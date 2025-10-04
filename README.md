# 🤖 Workload Balancer AI — Azure DevOps + Gemini Agent

An **AI-powered Workload Analysis Agent** that connects to **Azure DevOps**, fetches recent **Task work items**, analyzes their **effort & discussion complexity using Gemini AI**, and recommends **fair workload balancing across team members**.

---

## ✨ Features

✅ Connects directly to **Azure DevOps** via PAT  
✅ Fetches **last week's Tasks** (modifiable in WIQL)  
✅ Sends **task title + comments** to **Gemini 2.5 Flash** for scoring  
✅ Generates **per-task workload scores + AI reasoning**  
✅ Produces **Team Summary**:
- 🔴 Overloaded Members  
- 🟡 Underutilized Members  
- 🟢 Most Efficient Contributors

✅ Beautiful **React + Tailwind (CDN) UI** with loading state

---

## 🚀 Getting Started

### 1️⃣ Backend Setup (FastAPI + Gemini)

```
cd backend
python -m venv venv # Optional - if you want a virtual env
pip install -r requirements.txt
```

👉 **IMPORTANT — Configure your Gemini API key**

In `backend/services/workload_service.py`, update:

```
genai.configure(api_key="YOUR_GEMINI_KEY_HERE")
```

Get your key from **https://aistudio.google.com/apikey**

👉 **(Optional) Change Number of ADO Tasks to Analyze**

Open `backend/services/ado_client.py` and modify the WIQL query:

```
[System.CreatedDate] >= @Today - 7   # change range
[System.WorkItemType] = 'Task'       # filter different item types if needed
```

Then run the backend:

```
uvicorn app.main:app --reload --port 8000
```

---

### 2️⃣ Frontend Setup (React + Vite + Tailwind CDN)

```
cd frontend
npm install
npm run dev
```

Then open:  
👉 http://localhost:5173

---

## 🧠 How It Works

| Step | Action |
|------|--------|
| 1 | Enter **Org / Project / PAT** in UI |
| 2 | Frontend calls **FastAPI backend** |
| 3 | Backend fetches **ADO Task IDs** & **comments** |
| 4 | Each task is scored by **Gemini AI** (`1 to 10`) |
| 5 | Team Summary & Task List are shown |

---

## 🛠️ Tech Stack

| Layer | Tools |
|--------|--------|
| Frontend | React + Tailwind (CDN) + Vite |
| Backend | FastAPI + `requests` |
| AI | Gemini 2.5 Flash (`google.generativeai`) |
| DevOps | Azure DevOps REST API |

---

## 🎯 Roadmap (Future Enhancements)

- ✅ Auto **reassign tasks** via ADO API  
- ✅ Support **multiple work item types** (Bugs, User Stories)  
- ✅ Chat-style **“Agent Mode”**  
- ✅ Deploy as **MCP-compliant Agent**  

---

## 🤝 Contributing

Pull requests welcome! Open an issue to discuss improvements 🔧

---

## 📜 License

MIT — free to use, modify & enhance 🚀

---

Made with ❤️