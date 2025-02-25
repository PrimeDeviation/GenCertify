# GenCertify

A Certification Readiness and Document Drafting Tool that evaluates a startup's preparedness for key certifications (e.g., ISO 27001, SOC 2, GDPR, etc.) and generates tailored compliance documents using Generative AI.

## Features

- **Static Input Module**: Collect organizational details, certification preferences, and document uploads
- **Chat Interface**: Interactive evaluation through conversational AI
- **Readiness Evaluation**: Analyze documents against certification standards to identify compliance gaps
- **Document Drafting**: Generate tailored compliance documents based on input data
- **Output Generation**: Produce comprehensive readiness reports with compliance scores and recommendations
- **Simple Logging**: Track errors and key events to guide improvements

## Tech Stack

- **Language & Framework**: Python with FastAPI
- **AI/ML Integration**: Google Vertex AI, OpenAI, and Anthropic models
- **Containerization**: Docker
- **Deployment**: Google Cloud Run
- **Data Storage**: Google Firestore and Google Cloud Storage
- **CI/CD**: GitHub Actions
- **Security**: Google Cloud IAM and Secret Manager

## Live Demo

Check out the live demo at: https://gencertify-235850710154.us-central1.run.app/

## Setup

### Prerequisites

- Python 3.10+
- Docker
- Google Cloud SDK

### Local Development

1. Clone the repository:
   ```
   git clone <repository-url>
   cd GenCertify
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

### Docker Development

1. Build the Docker image:
   ```
   docker build -t gencertify .
   ```

2. Run the container:
   ```
   docker run -p 8000:8000 --env-file .env gencertify
   ```

### Cloud Deployment

1. Set up Google Cloud services:
   ```
   # Create a Cloud Storage bucket
   gcloud storage buckets create gs://[PROJECT_ID]-gencertify

   # Create secrets for API keys
   echo -n "your-openai-api-key" | gcloud secrets create openai-api-key --data-file=-
   echo -n "your-anthropic-api-key" | gcloud secrets create anthropic-api-key --data-file=-
   ```

2. Deploy to Cloud Run:
   ```
   gcloud run deploy gencertify --source . --platform managed --region us-central1 \
     --set-env-vars="APP_NAME=GenCertify,ENVIRONMENT=production,..." \
     --set-secrets="OPENAI_API_KEY=openai-api-key:latest,ANTHROPIC_API_KEY=anthropic-api-key:latest" \
     --port=8080
   ```

3. For automated CI/CD, see the GitHub Actions workflow in `.github/workflows/`.

## Development Mode

When running in development mode, the application uses mock services for:
- Firestore database
- Cloud Storage
- AI model interactions

This allows you to test the application flow without setting up the actual cloud services.

## Project Structure

```
GenCertify/
├── .github/                # GitHub Actions workflows
├── app/                    # Application code
│   ├── api/                # API endpoints
│   ├── models/             # Data models
│   ├── services/           # External service integrations
│   │   ├── ai/             # AI integration services
│   │   ├── firestore.py    # Firestore service
│   │   └── storage.py      # Cloud Storage service
│   ├── static/             # Static assets
│   ├── templates/          # HTML templates
│   └── main.py             # Application entry point
├── .env.example            # Example environment variables
├── .gitignore              # Git ignore file
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## License

[MIT License]

## Contributing

Contributions are welcome! See the [issues](../../issues) page for open tasks or create a new issue to propose features or report bugs. 