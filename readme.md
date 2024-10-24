\# MAX POD \- Print on Demand Automation Tool

MAX POD is a comprehensive Print on Demand automation tool that helps you generate and manage product mockups, integrate with Printify, and streamline your POD business operations.

\#\# Prerequisites

Before running the application, make sure you have the following installed:  
\- Python 3.8 or higher  
\- Node.js 14 or higher  
\- npm (Node Package Manager)  
\- Git

\#\# Initial Setup

1\. Clone the repository:  
\`\`\`bash  
git clone https://github.com/SavageHobbies/automator-POD.git  
cd automator-POD

2. Create and configure the environment file:

cp .env.example .env  
Edit the .env file and fill in your credentials:  
PRINTIFY\_API\_KEY=your\_printify\_api\_key  
AWS\_ACCESS\_KEY\_ID=your\_aws\_access\_key  
AWS\_SECRET\_ACCESS\_KEY=your\_aws\_secret\_key  
AWS\_REGION=us-east-2  
S3\_BUCKET=max-pod-designs  
GH\_UPLOAD\_REPO=your\_github\_repo  
GH\_PAT=your\_github\_pat  
GH\_CONTENT\_PREFIX=your\_github\_content\_prefix

3. Install Python dependencies:

python \-m pip install \-r requirements.txt

4. Install Node.js dependencies:

npm install

## Running the Application

There are two ways to run the application:

### Option 1: Using the Start Script (Recommended)

We provide a convenient start script that launches both frontend and backend:  
./start.sh  
The script will:

1. Start the backend server  
2. Start the frontend development server  
3. Open your default browser to the application

### Option 2: Manual Start

If you prefer to run the servers manually:

1. Start the backend server:

\# In one terminal  
python \-m uvicorn main:app \--reload \--host 0.0.0.0 \--port 8000

2. Start the frontend development server:

\# In another terminal  
npm start  
The application will be available at:

* Frontend: [http://localhost:3000](http://localhost:3000/)  
* Backend API: [http://localhost:8000](http://localhost:8000/)

## Project Structure

automator-POD/  
├── backend/                 \# Backend API routes and utilities  
│   ├── api/                \# API endpoints  
│   ├── marketplace/        \# Marketplace integrations  
│   └── utils/              \# Utility functions  
├── frontend/               \# Frontend React components  
│   └── src/                 
├── static/                 \# Static files  
├── util/                   \# Shared utilities  
├── .env                    \# Environment configuration  
├── main.py                 \# Main backend application  
├── package.json           \# Frontend dependencies  
└── requirements.txt       \# Backend dependencies

## Features

* Generate product mockups for various categories  
* Upload designs to S3  
* Integration with Printify  
* Extensible architecture for adding more marketplaces  
* User-friendly interface for managing designs and mockups

## Configuration

### Frontend Configuration

The frontend configuration is in src/config.js. You can modify:

* API endpoints  
* Available mockup categories  
* S3 bucket configuration

### Backend Configuration

The backend configuration is managed through environment variables in .env. Configure:

* API keys  
* AWS credentials  
* Database connections  
* Other service integrations

## Development

### Adding New Features

1. Backend:  
   * Add new routes in backend/api/  
   * Implement new marketplace integrations in backend/marketplace/  
2. Frontend:  
   * Add new components in src/components/  
   * Update configuration in src/config.js

### Testing

\# Run backend tests  
python \-m pytest

\# Run frontend tests  
npm test

## Troubleshooting

### Common Issues

1. Backend won't start:  
   * Check Python version: python \--version  
   * Verify all dependencies are installed: pip install \-r requirements.txt  
   * Make sure ports are available (8000 for backend)  
2. Frontend won't start:  
   * Check Node.js version: node \--version  
   * Clear npm cache: npm cache clean \--force  
   * Reinstall dependencies: rm \-rf node\_modules && npm install  
3. Upload issues:  
   * Verify AWS credentials in .env  
   * Check S3 bucket permissions  
   * Verify CORS configuration in S3

### Getting Help

If you encounter any issues:

1. Check the logs in the terminal  
2. Verify environment variables are set correctly  
3. Create an issue on GitHub with:  
   * Description of the problem  
   * Steps to reproduce  
   * Error messages  
   * Environment details

## Contributing

1. Fork the repository  
2. Create a feature branch  
3. Commit your changes  
4. Push to the branch  
5. Create a Pull Request

## License

This project is licensed under the MIT License \- see the LICENSE file for details  
