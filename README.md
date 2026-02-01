# SnapLink - Premium URL Shortener

SnapLink is a feature-rich, high-performance URL shortener built with Django, featuring a modern, premium UI and robust user authentication.

## ✨ Features

- **Secure Authentication**: User registration, login, and session management.
- **URL Shortening**: Generate unique, short URLs instantly.
- **Custom Aliases**: Create personalized short codes for your links.
- **Advanced Analytics**: Track click counts for every link in real-time.
- **Link Expiration**: Set expiration dates to make your links temporary.
- **QR Code Generation**: Generate high-quality QR codes for every shortened link.
- **Premium UI**: A clean, responsive, and aesthetically pleasing dashboard built with modern CSS practices.

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- pip (Python package manager)

### Installation

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/KESHABWI/url-shortener-django.git
    cd url-shortener-django
    ```

2.  **Set up a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Migrations**:

    ```bash
    python manage.py migrate
    ```

5.  **Start the development server**:

    ```bash
    python manage.py runserver
    ```

6.  **Access the app**:
    Open `http://127.0.0.1:8000` in your browser.

### Running with Docker

1.  **Build and start the containers**:

    ```bash
    docker-compose up --build
    ```

2.  **Access the app**:
    Open `http://127.0.0.1:8000` in your browser.

## 🧪 Running Tests

To verify the application's functionality, run:

```bash
python manage.py test
```

## 🛠 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML5, Vanilla CSS, Bootstrap 5 (for grid/layout)
- **Forms**: Django Crispy Forms (Bootstrap 5 pack)
- **QR Code**: `qrcode` library
- **Database**: SQLite (Default)

## 📝 Usage

1.  **Register/Login**: Navigate to the Get Started page to create an account.
2.  **Shorten**: Enter a long URL in the dashboard. Optionally, set a custom alias or an expiration date.
3.  **Manage**: View your links in the dashboard table. You can edit, delete, or view the QR code for each link.
4.  **Track**: See the "Clicks" column to monitor how many times your link has been accessed.

---

Built with ❤️ by Antigravity.
