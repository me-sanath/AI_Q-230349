# AISSETS - Internal Q&A Portal with Automated Reply Generation

This repository contains the source code and documentation for AISSETS, an innovative internal Q&A platform that utilizes AI-driven automated reply generation to enhance productivity and collaboration within organizations. This platform was developed as part of the AI-Quest hackathon submission by **Team AI_Q-230349**.

## Features

- **AI-Generated Responses:** Contextually accurate answers for user-submitted queries.
- **Tag-Based Filtering:** Follow specific topics for personalized content.
- **User Engagement Analytics:** Metrics such as session time, engagement, and relevance scoring.
- **Gamified Elements:** Badges and milestones to encourage participation.
- **Admin Moderation Tools:** Tools for question/answer management and content moderation.
- **Intuitive UI:** User-friendly interface for both users and administrators.

## Tech Stack

### Backend
- **FastAPI:** High-performance AI endpoint handling.
- **Django:** Core backend for user authentication, analytics, and database management.

### Frontend
- **React:** Dynamic and component-based UI for seamless user interaction.

### AI Pipeline
- **Llama Model:** Context-aware response generation.
- **FAISS:** Vector-based similarity search for fast context retrieval.
- **Preprocessing Scripts:** Data cleaning and structuring from internal wikis and repositories.

### Database
- Relational databases optimized for scalability and fast data retrieval.

## Flow Diagrams
<img width="1056" alt="ai_flow" src="https://github.com/user-attachments/assets/198beb13-4649-4245-ba0c-e5be436c145f">

## Screenshots of UI
![Home page](https://github.com/user-attachments/assets/dcd19ec1-a799-4670-8da6-7f045bee5553)
![Questions](https://github.com/user-attachments/assets/6346f73e-7692-4b0c-9944-f4abcce2bf9a)
![ask question](https://github.com/user-attachments/assets/806c6206-b4ab-4041-9e7e-5893edf8cc1d)
![profile page](https://github.com/user-attachments/assets/60cf1479-3684-4ab1-8e86-d0afc05b5ee9)
![Admin Page](https://github.com/user-attachments/assets/c68e60e1-7fa4-4d97-9cfc-9cc231426d2e)


## AI Response Generation Workflow

1. **Data Preprocessing:** Extract and structure knowledge from internal sources.
2. **Context Search:** Use FAISS for efficient vector similarity search.
3. **Query Enrichment:** Combine user queries with retrieved context.
4. **Response Generation:** Generate detailed, context-aware responses using the Llama model.
5. **Continuous Improvement:** Refine AI models using user feedback.

## Planned Future Enhancements

- **Blog Section:** Tutorials, updates, and technical insights.
- **Personalized Recommendations:** Featured questions based on user activity.
- **Enhanced AI Fine-Tuning:** Improve relevance with curated datasets.
- **Flagging/Tagging System:** AI-assisted tagging and advanced flagging options.
- **UI Polishing:** Better navigation and responsive design.
- **Gamification Updates:** New badges, leaderboards, and analytics insights.

## How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/me-sanath/AI_Q-230349
2. Navigate to the project directory and set up the backend (Django + FastAPI) and frontend (React).
3. Ensure all dependencies are installed.
4. Start the backend and frontend services.
5. Access the platform through the provided URL.
