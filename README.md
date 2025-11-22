# Revision Quiz AI 🎓🤖

An intelligent revision and quiz platform powered by AI that helps students and learners create, take, and analyze personalized quizzes for effective learning and knowledge retention.

## 📖 Overview

Revision Quiz AI is an innovative educational platform that leverages artificial intelligence to generate adaptive quizzes and provide personalized learning experiences. The platform helps students prepare for exams, reinforce concepts, and track their learning progress through intelligent quiz generation and analysis.

## ✨ Key Features

### 🤖 AI-Powered Quiz Generation
- **Automatic Question Creation**: Generate questions from various sources (text, documents, topics)
- **Multiple Question Types**: Support for multiple choice, true/false, short answer, and essay questions
- **Difficulty Adaptation**: AI adjusts question difficulty based on user performance
- **Topic Coverage**: Comprehensive coverage of specified subject areas

### 📚 Learning & Revision Tools
- **Smart Revision Scheduling**: Spaced repetition algorithm for optimal learning
- **Progress Tracking**: Detailed analytics on learning progress and weak areas
- **Performance Insights**: AI-driven insights into areas requiring more focus
- **Study Recommendations**: Personalized study plans based on performance

### 👤 User Management
- **User Profiles**: Track individual learning journeys
- **Achievement System**: Gamification elements to motivate learners
- **History Tracking**: Complete quiz history and performance metrics
- **Custom Study Plans**: Tailored learning paths for different goals

### 📊 Analytics & Reporting
- **Detailed Statistics**: Comprehensive performance metrics
- **Visual Dashboards**: Interactive charts and graphs
- **Progress Reports**: Exportable reports for tracking improvement
- **Comparative Analysis**: Compare performance across topics and time periods

## 🛠️ Technology Stack

### Backend
- **Python**: Core programming language
- **AI/ML Libraries**: For question generation and analysis
- **Database**: Data persistence and user management
- **API Framework**: RESTful API for client-server communication

### Frontend
- **Modern Web Framework**: Responsive user interface
- **Interactive Components**: Engaging quiz-taking experience
- **Real-time Updates**: Live feedback and progress tracking

### AI & Machine Learning
- **Natural Language Processing**: Question generation and analysis
- **Machine Learning Models**: Performance prediction and adaptation
- **Content Analysis**: Intelligent topic extraction and categorization

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (recommended)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/hechmi10/revision_quiz_ai.git
   cd revision_quiz_ai
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize Database**
   ```bash
   python manage.py migrate
   ```

6. **Run the Application**
   ```bash
   python manage.py runserver
   ```

## 📝 Usage Guide

### Creating Your First Quiz

1. **Login/Register**: Create an account or login to existing account
2. **Select Topic**: Choose the subject area for your quiz
3. **Configure Quiz**:
   - Set number of questions
   - Choose difficulty level
   - Select question types
   - Set time limit (optional)
4. **Generate Quiz**: Let AI create questions based on your preferences
5. **Take Quiz**: Answer questions and submit for evaluation
6. **Review Results**: Analyze your performance and get feedback

### Uploading Study Materials

1. Navigate to the **Materials** section
2. Upload documents (PDF, DOCX, TXT)
3. System extracts key concepts and generates quiz questions
4. Review and edit generated questions if needed

### Tracking Progress

1. Access your **Dashboard** to view:
   - Recent quiz scores
   - Learning streaks
   - Weak areas
   - Improvement trends
2. Set **Learning Goals** and track achievement
3. Generate **Progress Reports** for specific time periods

## 📂 Project Structure

```
revision_quiz_ai/
├── src/                    # Source code
│   ├── api/               # API endpoints
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   ├── utils/             # Utility functions
│   └── ai/                # AI/ML components
├── tests/                 # Test files
├── docs/                  # Additional documentation
├── config/                # Configuration files
├── static/                # Static assets
├── templates/             # HTML templates
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
├── LICENSE               # License file
└── README.md             # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Application Settings
APP_NAME=Revision Quiz AI
DEBUG=False
SECRET_KEY=your-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# AI Service Configuration
AI_API_KEY=your-ai-api-key
AI_MODEL=gpt-4

# Email Configuration (for notifications)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@example.com
EMAIL_PASSWORD=your-password

# Security Settings
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Customization Options

- **Question Templates**: Customize in `config/question_templates.json`
- **Difficulty Levels**: Adjust in `config/difficulty_settings.json`
- **AI Parameters**: Configure in `config/ai_settings.json`

## 🧪 Testing

Run the test suite to ensure everything is working correctly:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run specific test file
python -m pytest tests/test_quiz_generation.py
```

## 🤝 Contributing

We welcome contributions to the Revision Quiz AI project! Here's how you can help:

1. **Fork the Repository**
2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Your Changes**
   - Write clean, documented code
   - Follow the existing code style
   - Add tests for new features
4. **Commit Your Changes**
   ```bash
   git commit -m "Add: description of your changes"
   ```
5. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```
6. **Open a Pull Request**

### Code Style Guidelines

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Write docstrings for all functions and classes
- Keep functions small and focused
- Add comments for complex logic

## 📄 License

This project is licensed under the Unlicense - see the [LICENSE](LICENSE) file for details. This means the software is released into the public domain and you are free to use, modify, and distribute it without any restrictions.

## 🐛 Bug Reports & Feature Requests

Found a bug or have a feature request? Please open an issue on GitHub:

1. Go to the [Issues](https://github.com/hechmi10/revision_quiz_ai/issues) page
2. Click "New Issue"
3. Choose the appropriate template (Bug Report or Feature Request)
4. Provide detailed information about the issue or feature

## 📧 Contact & Support

- **Repository**: [https://github.com/hechmi10/revision_quiz_ai](https://github.com/hechmi10/revision_quiz_ai)
- **Issues**: [https://github.com/hechmi10/revision_quiz_ai/issues](https://github.com/hechmi10/revision_quiz_ai/issues)
- **Discussions**: Join our community discussions for questions and ideas

## 🙏 Acknowledgments

- Thanks to all contributors who help improve this project
- Built with modern AI and machine learning technologies
- Inspired by the need for better, personalized learning tools

## 🗺️ Roadmap

### Current Version (v1.0)
- ✅ Basic quiz generation
- ✅ User authentication
- ✅ Progress tracking

### Upcoming Features
- 🔄 Multi-language support
- 🔄 Mobile app development
- 🔄 Collaborative study groups
- 🔄 Live quiz competitions
- 🔄 Advanced AI tutoring
- 🔄 Integration with learning management systems (LMS)

### Future Plans
- 📱 Native mobile apps (iOS & Android)
- 🎮 Gamification enhancements
- 🧠 Advanced learning analytics
- 🌐 Multi-platform synchronization
- 🎯 Career-specific quiz paths

## 💡 Tips for Best Results

1. **Regular Practice**: Take quizzes regularly for better retention
2. **Review Mistakes**: Always review incorrect answers and explanations
3. **Set Goals**: Define clear learning objectives before starting
4. **Use Variety**: Mix different question types and difficulty levels
5. **Track Progress**: Monitor your dashboard to identify improvement areas
6. **Upload Materials**: Use your own study materials for personalized quizzes
7. **Stay Consistent**: Maintain a regular study schedule

---

**Happy Learning! 📚✨**

*Made with ❤️ by the Revision Quiz AI Team*