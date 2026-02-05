# CSS Bunny - Learn Flexbox and Grid Through Play

CSS Bunny is an interactive educational game designed to help developers master CSS Flexbox and Grid layouts. Through a series of engaging levels, players write CSS code to guide a bunny to its carrot, receiving real-time visual feedback.

## Features

- **30 Interactive Levels**: Progress from basic Flexbox properties to complex Grid layouts.
- **Live CSS Editor**: Write code and see the bunny move instantly.
- **Progress Tracking**: Monitor completion time and number of attempts for each level.
- **Global Leaderboard**: Compete with other learners and climb the ranks.
- **User Authentication**: Save progress and resume learning across sessions.
- **Admin Dashboard**: Manage levels, view user statistics, and oversee the platform.

## Tech Stack

- **Backend**: Python / Django
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Pixi JS
- **Database**: SQLite
- **Styling**: Modern, responsive CSS with a focus on UI/UX.

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Prepare the environment**
   Ensure you are in the project root directory.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

5. **Populate game levels**
   ```bash
   python manage.py populate_levels
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   Open a web browser and navigate to http://127.0.0.1:8000/

## How to Play

1. **Sign up**: Create an account to save progress.
2. **Select a Level**: Start from Level 1 and unlock subsequent challenges.
3. **Write CSS**: Use the properties specified in the instructions (e.g., justify-content, align-items).
4. **Solve**: Position the bunny on the carrot to solve the puzzle.

## Project Structure

- `accounts/`: User authentication and profile management.
- `game/`: Core game logic, level management, and the CSS editor.
- `leaderboard/`: Scoring system and global rankings.
- `static/`: Global CSS, JavaScript assets, and images.
- `templates/`: HTML templates for the application.

## Authors

- Development Team

## License

This project is for educational purposes. Feel free to use and adapt it for learning.
