# FastAPI
This repository used for learning fast-api

# Cost Management API

A lightweight RESTful API built with **FastAPI** for managing costs and expenses without using a database. All data is stored in memory using a Python dictionary.

## 📋 API Endpoints

| Method | Endpoint | Description | Status Codes |
|--------|----------|-------------|--------------|
| `POST` | `/costs` | Create a new cost | 201 Created |
| `GET` | `/costs` | Retrieve all costs | 200 OK |
| `GET` | `/costs/{cost_id}` | Retrieve a specific cost by ID | 200 OK, 404 Not Found |
| `PUT` | `/costs/{cost_id}` | Update a specific cost by ID | 200 OK, 404 Not Found |
| `DELETE` | `/costs/{cost_id}` | Delete a specific cost by ID | 200 OK, 404 Not Found |

## 🏗️ Data Structure

Each cost object contains the following fields:

```json
{
  "id": 1,
  "description": "Lunch at restaurant",
  "amount": 150.50
}

