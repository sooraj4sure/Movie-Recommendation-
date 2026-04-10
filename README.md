To create Virtual env --> py -3.11 -m venv venv
venv\Scripts\activate

To start app.py --> streamlit run app.py 
To start main.py---> uvicorn main:app --reload



# 🎬 Movie Recommendation System

A machine learning-based movie recommendation system built using FastAPI and Streamlit.

---

## 🚀 Features

* 🔍 Search movies
* 🎯 Get similar movie recommendations
* 🎨 Interactive UI using Streamlit
* ⚡ Fast API backend

---

## 🛠️ Tech Stack

* Python
* FastAPI
* Streamlit
* Pandas
* Scikit-learn

---

## 📁 Project Structure

```
project/
│
├── main.py        # FastAPI backend
├── app.py         # Streamlit frontend
├── model.pkl      # ML model
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

```bash
git clone <your-repo-link>
cd project
pip install -r requirements.txt
```

---

## ▶️ Run the Project

### 1. Start Backend (FastAPI)

```bash
uvicorn main:app --reload
```

### 2. Start Frontend (Streamlit)

```bash
streamlit run app.py
```

---

## 🌐 Access the App

* API Docs: http://127.0.0.1:8000/docs
* Frontend UI: http://localhost:8501

---



---

## 👨‍💻 Author

Suraj Kashyap
