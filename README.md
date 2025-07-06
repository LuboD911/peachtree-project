# 🏦 Peachtree Bank - Full-Stack Banking Application

A modern, banking application built with microservices architecture, featuring real-time transaction management, user authentication, and responsive UI.

## 🚀 Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd peachtree-bank-project

# Start all services with Docker Compose
docker-compose up -d

# Access the application
http://localhost:8080
```

## 🏗️ Architecture Overview

### **Microservices Architecture**
This project follows a **microservices pattern** with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway   │    │   Backend       │
│   (Vue.js)      │◄──►│   (Kong)        │◄──►│   Services      │
│   Port: 8080    │    │   Port: 8000    │    │   (Flask)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (MySQL)       │
                       │   Port: 3306    │
                       └─────────────────┘
```

### **Service Breakdown**

| Service | Technology | Purpose | Port |
|---------|------------|---------|------|
| **Frontend** | Vue.js 3 + TypeScript + Tailwind CSS | User interface | 8080 |
| **API Gateway** | Kong | Authentication, routing, CORS | 8000 |
| **Auth Service** | Flask + JWT | User authentication & authorization | 5001 |
| **Transaction Service** | Flask + SQLAlchemy | Transaction management | 5002 |
| **Database** | MySQL 8.0 | Data persistence | 3306 |

## 🛠️ Technology Stack

### **Frontend**
- **Vue.js 3** - Progressive JavaScript framework with Composition API, reactive data binding, virtual DOM
- **TypeScript** - Type-safe development with better IDE support
- **Tailwind CSS** - Utility-first CSS framework for rapid UI development
- **Pinia** - State management for Vue.js
- **Vue Router** - Client-side routing
- **Axios** - HTTP client for API communication

### **Backend**
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **Flask-JWT-Extended** - JWT authentication
- **Pydantic** - Data validation using Python type annotations
- **MySQL Connector** - Database driver

### **Infrastructure**
- **Docker & Docker Compose** - Containerization and orchestration
- **Kong API Gateway** - API management, authentication, and routing
- **Nginx** - Static file serving and SPA routing for frontend
- **MySQL 8.0** - Relational database

## 🔐 Security & Authentication

### **JWT Token System**
- **Access Tokens** - Short-lived (15 minutes) for API access
- **Refresh Tokens** - Long-lived (7 days) for token renewal
- **Token Revocation** - Refresh tokens stored in database for revocation capability

### **Security Features**
- **CORS Protection** - Configured at Kong gateway level
- **JWT Validation** - All protected routes validate JWT tokens
- **Password Hashing** - bcrypt for secure password storage
- **SQL Injection Protection** - SQLAlchemy ORM with parameterized queries

## 📊 State Management

### **Pinia Store Architecture**
```typescript
// Auth Store (stores/auth.ts)
export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    access_token: localStorage.getItem('access_token') || '',
    refresh_token: localStorage.getItem('refresh_token') || ''
  }),
```

### **Component Communication**
- **Props Down, Events Up** - Standard Vue.js pattern for parent-child communication
- **Template Refs** - Direct method calls between components when needed
- **Event Emission** - Custom events for cross-component communication

## 🗄️ Database Design

### **Schema Overview**
```sql
-- Core Tables
users                    -- User accounts
refresh_tokens          -- JWT refresh token storage
transactions            -- Financial transactions
contractors             -- Transaction recipients
transaction_statuses    -- Transaction states
system_accounts         -- Bank accounts
```

### **Data Initialization**
The `initdb/init.sql` script provides:
- **Sample contractors** with profile images
- **Transaction statuses** (pending, sent, completed, failed)
- **System accounts** with initial balances
- **Ready-to-use data** for immediate testing

## 🔄 API Routes

### **Authentication Service** (`/auth`)
```
POST /auth/register     - User registration
POST /auth/login        - User login
POST /auth/refresh      - Token refresh
POST /auth/logout       - User logout
DELETE /auth/delete     - Account deletion
```

### **Transaction Service** (`/transactions`)
```
GET    /transactions              - List transactions (with sorting/filtering)
POST   /transactions              - Create new transaction
GET    /transactions/{id}         - Get transaction details
PUT    /transactions/{id}/status  - Update transaction status
GET    /transactions/contractors  - List available contractors
GET    /transactions/statuses     - List transaction statuses
GET    /transactions/accounts     - List system accounts
```

## 🎯 Core Principles

### **1. Separation of Concerns**
- **Frontend** - UI/UX and user interaction
- **Nginx** - Static file serving and SPA routing
- **API Gateway** - Authentication, routing, and cross-cutting concerns
- **Microservices** - Business logic separation (auth vs transactions)
- **Database** - Data persistence and relationships

### **2. Security First**
- **JWT-based authentication** with token refresh mechanism
- **API Gateway protection** - All requests go through Kong
- **Database-level security** - Proper indexing and constraints
- **Input validation** - Pydantic models for data validation

### **3. Scalability**
- **Microservices architecture** - Independent service scaling
- **Containerization** - Easy deployment and scaling
- **Stateless services** - No session storage in services
- **Database optimization** - Proper indexing and query optimization


## 🔧 Key Features

### **Frontend Features**
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Real-time Updates** - Transaction list updates automatically
- **Search & Filtering** - Find transactions by contractor name
- **Sorting** - Sort by date, amount, or contractor
- **Status Management** - Update transaction statuses
- **Balance Checking** - Real-time account balance validation

### **Backend Features**
- **JWT Authentication** - Secure token-based authentication
- **Transaction Management** - Create, read, update transactions
- **Account Management** - System account balance tracking
- **Data Validation** - Comprehensive input validation
- **Error Handling** - Proper error responses and logging
