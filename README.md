# trade-api

# 🚀 Trade Order API (FastAPI + Docker + AWS EC2)

## 📌 Project Overview
This is a **simple backend service** for managing **trade orders** using FastAPI. It provides **RESTful APIs** to:
- ✅ **Create Trade Orders** (`POST /orders`)
- ✅ **Retrieve Trade Orders** (`GET /orders`)
- ✅ **Real-time updates** via WebSockets (Bonus)
- ✅ **Store data** in SQLite (or PostgreSQL)

The app is **containerized with Docker** and **deployed on AWS EC2** using **GitHub Actions (CI/CD)**.

---

## ⚡ Tech Stack
- **Backend**: FastAPI (Python)
- **Database**: SQLite (or PostgreSQL)
- **Containerization**: Docker
- **Deployment**: AWS EC2
- **CI/CD**: GitHub Actions

---

## 🔧 Installation & Running Locally
1️⃣ **Clone the repository**
```
git clone https://github.com/omtandel2307/trade-api.git
cd trade-api
```

2️⃣ Set up a virtual environment (Optional)
```sh
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```
3️⃣ Install dependencies
```
pip install -r requirements.txt
```
4️⃣ Run the API locally
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
5️⃣ Test the API in Swagger UI
```
Open: http://127.0.0.1:8000/docs
```

## 🐳 Running with Docker

1️⃣ Build the Docker image
```
docker build -t trade-api .
```

2️⃣ Run the container
```
docker run -d -p 8000:8000 trade-api
```

3️⃣ Test the API
```
Open: http://localhost:8000/docs
```

## 🚀 Deployment to AWS EC2
1️⃣ Launch EC2 Instance
```
Create an Ubuntu 22.04 EC2 instance on AWS
Open port 8000 in Security Groups
```

2️⃣ Run the container
```
ssh -i my-ec2-key.pem ubuntu@<your-ec2-ip>
```

3️⃣ Test the API
```
sudo apt update && sudo apt install docker.io -y
sudo systemctl start docker
sudo systemctl enable docker
```

4️⃣ Test the API
```
git clone https://github.com/<your-username>/trade-api.git
cd trade-api
docker build -t trade-api .
docker run -d -p 8000:8000 trade-api
```

5️⃣ Test API on EC2
```
Open: http://<your-ec2-ip>:8000/docs
```

## 🔄 CI/CD: Automated Deployment with GitHub Actions
Every time you push to master, GitHub Actions will:

1. SSH into the EC2 instance
2. Pull the latest code
3. Rebuild and restart the Docker container

Secrets Required in GitHub
To enable automatic deployment, set these GitHub Secrets in Settings → Secrets:

1. EC2_HOST → Your EC2 Public IP
2. EC2_SSH_KEY → Contents of your .pem file

