# Alice in Wonder-LAN
A simple local messaging app built to understand how WebSockets and chat messaging work.

## 🚀 Built with
- React (Vite)
- Shadcn
- Tailwind
- Python
- FastAPI
- Sqlite3

## 📦 Installation
### 1️⃣ Clone the Repository
  ```bash
  git clone https://github.com/16DeeCee/Alice-in-Wonder-LAN.git
  ```
### 2️⃣ Backend Setup
  1. Navigate to the backend folder
  ```bash
  cd Alice-in-Wonder-LAN
  ```
  2. Create and activate a virtual environment (optional but recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
  ```
  3. Install dependencies:
  ```
  pip install -r requirements.txt
  ```
  4. Create a .env file in the backend directory:
  ```bash
  touch .env
  ```
  Add the following environment variables:
  ```bash
  HOST=<YOUR_PREFERRED_HOST>
  PORT=<YOUR_PREFERRED_PORT>
  DATABASE=<YOUR_PREFERRED_DATABASE_NAME>
  HASH_SECRET_KEY=<YOUR_GENERATED_SECRET_KEY>
  ```
  You can generate a HASH_SECRET_KEY using:
  ```bash
  openssl rand -hex 32
  ```
  5. Run the backend server using either of the following methods:
  - Using uvicorn
  ```bash
  uvicorn main:app --reload
  ```
  - Running the Python file directly
  ```bash
  python main.py
  ```

### 3️⃣ Frontend Setup
  1. Navigate to the frontend folder:
  ```bash
  cd frontend
  ```
  2. Install dependencies:
  ```
  npm install
  ```
  3. Run the development server:
  ```bash
  npm run dev
  ```

## ⚡ Features
✔ Real-time messaging using WebSockets <br>
✔ User authentication with JWT <br>
✔ Password hashing with bcrypt <br>
✔ Minimalistic UI with ShadCN and Tailwind CSS <br>
✔ SQLite3 for lightweight storage <br>
