# CMS API with Authentication and Blog Management

This project is a Django-based Content Management System (CMS) API that provides functionality for user authentication and blog management. It includes features like JWT-based authentication, blog creation, editing, viewing, and a liking system, with role-based access control.

---

## Features

### **User Authentication**
- User registration and login using JWT authentication.
- Manage user accounts:
  - Create, update, and delete accounts.
  - View details of the authenticated user (`/me`).

### **Blog Management**
- Blog post management:
  - Create, retrieve, update, and delete blog posts.
  - Public posts are accessible by any user.
  - Private posts are restricted to their owners.
- Like/unlike functionality for blog posts.

### **Database Design**
- **User Table**: Manages user credentials and details.
- **Post Table**: Stores blog posts with metadata like creation date, owner, and visibility.
- **Like Table**: Tracks which users like which posts.

---

## API Endpoints

### **Accounts (Authentication)**
| Method | Endpoint          | Description                 |
|--------|-------------------|-----------------------------|
| POST   | `/accounts`       | Register a new user.        |
| POST   | `/accounts/login` | Log in and retrieve a token.|
| PUT    | `/accounts`       | Update user details.        |
| DELETE | `/accounts`       | Delete user account.        |
| GET    | `/me`             | Get logged-in user details. |

### **Blog**
| Method | Endpoint            | Description                       |
|--------|---------------------|-----------------------------------|
| POST   | `/blog`             | Create a new blog post.           |
| GET    | `/blog`             | Retrieve all blog posts.          |
| GET    | `/blog/<id>`        | Retrieve a specific blog post.    |
| PUT    | `/blog/<id>`        | Update a blog post (owner-only).  |
| DELETE | `/blog/<id>`        | Delete a blog post (owner-only).  |

### **Likes**
| Method | Endpoint               | Description                      |
|--------|------------------------|----------------------------------|
| POST   | `/like/<blog_id>`      | Like a blog post.                |
| DELETE | `/like/<blog_id>`      | Unlike a blog post.              |

---

## Technologies Used
- **Backend Framework**: Django, Django REST Framework (DRF).
- **Authentication**: JWT via `djangorestframework-simplejwt`.
- **Database**: SQLite.
- **Testing**: Built-in Django `TestCase` for unit testing.

---

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

---

## Installation and Setup

1. **Clone the Repository**:
   ```bash
   git clone <repo_url>
   cd cms_project
