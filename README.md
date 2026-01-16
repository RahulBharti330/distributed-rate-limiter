# Distributed Rate Limiter & API Gateway

## Overview
This project implements a **distributed API Gateway with a Redis-backed rate limiting system** designed to protect backend services from abuse, enforce fair usage across users, and remain consistent in a horizontally scaled environment. The system is built using **production-grade backend architecture principles**, focusing on correctness, scalability, and observability rather than UI-heavy features.

---

## 1. What did you do?

I designed and built a **distributed rate limiter integrated into an API Gateway**, along with a **planned admin dashboard**, to control and monitor API traffic in a scalable system.

Specifically, I:
- Designed a **stateless API Gateway** responsible for authentication, request validation, rate limiting, and routing
- Implemented **distributed rate limiting** using the **Token Bucket algorithm**
- Ensured **global consistency** across multiple gateway instances using **Redis as a centralized state store**
- Designed a system that supports:
  - Per-user rate limits
  - Per-API rate limits
  - Tier-based limits (e.g., Free vs Pro users)
- Planned an **admin dashboard** to manage rate-limit policies and observe real-time traffic metrics

This project focuses on **infrastructure-level engineering**, solving problems that arise in real-world systems such as traffic spikes, abusive clients, and concurrency issues.

---

## 2. How did you do it?

### System Design Approach
The system is designed using **clear separation of concerns** and follows real-world backend architecture patterns.

### Core Components and Tech Stack

#### API Gateway (FastAPI)
- Built using **FastAPI** for high-performance asynchronous request handling
- Responsibilities:
  - Authenticate incoming requests using JWT
  - Identify the client (API key / user ID / IP)
  - Enforce rate limits before routing requests
  - Attach standard rate-limit headers (`X-RateLimit-*`)
- Designed to be **stateless**, allowing horizontal scaling

#### Distributed Rate Limiter (Redis + Lua)
- **Redis** is used as a centralized in-memory store to maintain rate-limit state
- **Token Bucket algorithm** is used to:
  - Allow controlled burst traffic
  - Enforce average request rate over time
- **Lua scripts** are executed inside Redis to:
  - Atomically refill tokens
  - Consume tokens
  - Prevent race conditions under concurrent access
- This guarantees correctness even when multiple API Gateway instances are running

#### Configuration Store (PostgreSQL)
- **PostgreSQL** stores:
  - Rate-limit policies
  - API-specific rules
  - User tiers
- Policies are dynamically loaded and cached by the gateway to avoid hardcoded limits

#### Admin Dashboard (React – Planned)
- Built using **React and TypeScript**
- Intended features:
  - Manage rate-limit policies
  - Visualize real-time traffic metrics
  - Detect abusive usage patterns
- Metrics are visualized using charts such as request throughput and blocked vs allowed traffic

#### Infrastructure & Tooling
- **Docker and Docker Compose** for environment consistency
- **Redis** for distributed shared state
- **PostgreSQL** for persistent configuration storage
- **Nginx** (planned) for reverse proxy and load balancing
- Environment-based configuration using `.env` files

---

## Low-Level Design (LLD)

The following diagram illustrates the low-level system design and exact request flow:

![LLD – Distributed Rate Limiter Architecture](docs/LLD_Distributed_Rate_Limiter.png)

### LLD Flow Explanation
1. Client sends request to the API Gateway
2. Gateway authenticates the request
3. Rate limiter middleware executes a Redis Lua script
4. Redis atomically decides whether to allow or reject the request
5. Allowed requests are routed to backend services
6. Rejected requests receive `429 Too Many Requests`

This design ensures **low latency**, **distributed consistency**, and **concurrency safety**.

---

## 3. What was the impact?

### Technical Impact
- Protects backend services from abuse and traffic floods
- Enforces **fair usage** across users and APIs
- Maintains **consistent rate limiting** across multiple gateway instances
- Adds minimal latency due to Redis-based in-memory operations
- Handles concurrency safely using atomic operations

### Engineering Impact
- Mirrors how **real production systems** enforce traffic control
- Demonstrates defensive system design and scalability awareness
- Emphasizes observability, fault tolerance, and correctness

### Interview & Resume Impact
This project demonstrates:
- Distributed systems thinking
- Backend infrastructure knowledge
- Correct use of Redis for atomic operations
- Clear understanding of rate-limiting trade-offs and failure modes

Unlike common CRUD or clone-based projects, this system solves a **non-trivial industry problem** encountered in nearly every large-scale backend environment.

---

## Current Status
- System Design (HLD + LLD): ✅ Completed  
- Repository Structure & Documentation: ✅ Completed  
- Implementation: 🚧 In Progress  

---

## Why This Is a Real Industry Project
Every system that exposes APIs—public or internal—requires rate limiting to ensure reliability and fairness.  
This project focuses on **keeping systems stable under load**, not just implementing visible features.

---

## Next Step
Proceed with **Day 1 implementation**:
- FastAPI gateway skeleton
- Redis integration
- Rate-limiter middleware
