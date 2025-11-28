# RECIPE_AI

An ML + Frontend web application to **analyze and predict the difficulty** of a given cooking recipe.

## 🚀 Project Overview

RECIPE_AI is a full-stack application that takes recipe data (ingredients, instructions, perhaps other metadata) and uses machine learning to **predict how difficult** the recipe is to prepare. The result helps users (home cooks, recipe sites, etc.) to quickly estimate whether a dish is easy, medium, or hard — helping set expectations before starting cooking.

There is a live demo version hosted at:
[recipe-ai-ochre.vercel.app](https://recipe-ai-ochre.vercel.app) ([GitHub][1])

> ⚠️ Note: The prediction quality depends on the training data used; treat the output as a guidance/estimate rather than a definitive measure.

## 🧱 Tech Stack

* **Backend**: Python (machine learning / data processing) ([GitHub][1])
* **Frontend**: JavaScript (likely React or similar), HTML, CSS ([GitHub][1])
* Separation into `backend/` and `frontend/` directories. ([GitHub][1])

## 📂 Project Structure

```
RECIPE_AI/
├── backend/        # Server / ML logic for recipe difficulty prediction
├── frontend/       # Web UI to enter recipes and view difficulty predictions
├── .gitignore
├── render.yaml     # Deployment config (for Render/Vercel or similar)
└── README.md       # <-- this file
```

([GitHub][1])

## ⚙️ Getting Started (Development)

### Prerequisites

* Python (version ___) — for backend
* Node (version ___) / npm or yarn — for frontend
* (Optional) Virtual environment for Python

### Installation & Setup

1. Clone the repository

   ```bash
   git clone https://github.com/rohitdinvi/RECIPE_AI.git
   cd RECIPE_AI
   ```

2. Setup backend environment

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate     # On Windows: venv\Scripts\activate
   pip install -r requirements.txt   # if requirements file exists
   ```

3. Setup frontend

   ```bash
   cd ../frontend
   npm install   # or yarn install
   ```

4. Start the application

   * Run backend server (e.g., `python app.py` or as configured)
   * Run frontend dev server (e.g., `npm start`)

5. Open your browser and navigate to the frontend URL (e.g., `localhost:3000`) to use the app.

## 🎯 Usage

* On the web UI, enter the recipe data: ingredients, instructions, maybe additional metadata.
* Submit the recipe to get a difficulty prediction (e.g., “Easy”, “Medium”, “Hard”).
* Use predictions to pre-screen recipes or tag them accordingly in recipe databases, blogs, or cooking apps.

## 💡 Why This Project

* Helps home cooks decide whether to attempt a recipe based on time/skill rather than just ingredients.
* Useful for recipe websites / cooking platforms to auto-tag difficulty levels.
* Demonstrates ML + frontend integration — useful as a learning / project showcase for full-stack skills.

## 🛠️ How It Works (High-level)

1. **Input**: The user feeds in a recipe (ingredients list + instructions).
2. **Processing**: Backend preprocesses the recipe (parsing ingredients, steps, maybe features such as number of ingredients, steps, cooking methods, etc.).
3. **ML Prediction**: A machine-learning model predicts a difficulty score or class (easy/medium/hard).
4. **Output**: Frontend displays the prediction to the user.

You can extend the backend to add more features: e.g., estimate cooking time, required skill level, dietary complexity, etc.

## 📈 Possible Improvements / Future Work

* Add support for more languages (e.g., recipes in Indian languages).
* Improve model accuracy by using a bigger, labeled dataset of recipes with known difficulty.
* Add extra outputs: estimated cooking time, nutritional info, equipment requirements, etc.
* Enhance frontend UI/UX: allow editing recipe, show recipe stats, filter by difficulty, user accounts, etc.
* Add user feedback loop: users verify difficulty after cooking — use that to retrain model.
