# Running Guide

## Overview
This guide provides comprehensive instructions on where and how to run the code in this repository. Follow the sections below based on your specific use case and environment.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Running the Application](#running-the-application)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)
6. [Additional Resources](#additional-resources)

## Prerequisites

Before running the code, ensure you have the following installed:
- **Git**: For cloning and version control
- **Node.js** (v14 or higher): Runtime environment
- **npm** (v6 or higher): Package manager
- **Python** (v3.8 or higher): If applicable
- **Docker** (optional): For containerized execution

### Checking Prerequisites
```bash
node --version
npm --version
python --version  # if applicable
docker --version  # if applicable
```

## Environment Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mshelar08/M.git
cd M
```

### 2. Install Dependencies
```bash
# For Node.js projects
npm install

# For Python projects (if applicable)
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root directory:
```bash
cp .env.example .env  # if .env.example exists
```

Edit the `.env` file with your configuration:
```
NODE_ENV=development
PORT=3000
DEBUG=true
# Add other variables as needed
```

### 4. Database Setup (if applicable)
```bash
npm run migrate  # or your migration command
npm run seed     # if you have seed data
```

## Running the Application

### Local Development

#### Starting the Development Server
```bash
npm start
# or
npm run dev
```

The application will typically start on `http://localhost:3000` (port may vary based on configuration).

#### Watch Mode (for development)
```bash
npm run watch
# or
npm run dev:watch
```

This automatically reloads the application when you make code changes.

#### Running with Nodemon
```bash
npm run dev
```

### Production Build

#### Build the Application
```bash
npm run build
```

#### Start Production Server
```bash
npm run start:prod
# or
NODE_ENV=production npm start
```

### Running Tests

#### Run All Tests
```bash
npm test
```

#### Run Tests in Watch Mode
```bash
npm run test:watch
```

#### Run Tests with Coverage
```bash
npm run test:coverage
```

#### Run Specific Test File
```bash
npm test -- path/to/test/file.test.js
```

### Running Specific Scripts

Check `package.json` for available npm scripts:
```bash
npm run  # Lists all available scripts
```

## Configuration

### Environment Variables

Common environment variables used in this project:

| Variable | Description | Default |
|----------|-------------|---------|
| `NODE_ENV` | Environment (development/production) | development |
| `PORT` | Server port | 3000 |
| `DEBUG` | Enable debug logging | false |
| `DATABASE_URL` | Database connection string | - |
| `API_KEY` | API authentication key | - |

### Configuration Files

- **`config/`**: Configuration directory (if applicable)
- **`.env`**: Local environment variables (not committed to git)
- **`.env.example`**: Template for environment variables

### Modifying Configuration

1. Edit `.env` file directly
2. Or pass environment variables via command line:
```bash
PORT=8000 npm start
```

## Running in Docker

### Build Docker Image
```bash
docker build -t m-app:latest .
```

### Run Docker Container
```bash
docker run -p 3000:3000 \
  -e NODE_ENV=production \
  -e PORT=3000 \
  m-app:latest
```

### Using Docker Compose
```bash
docker-compose up
```

### Stop Docker Container
```bash
docker-compose down
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Port Already in Use
```bash
# Find process using port 3000
lsof -i :3000
# Kill the process
kill -9 <PID>
# Or use a different port
PORT=3001 npm start
```

#### 2. Module Not Found Error
```bash
# Clean install dependencies
rm -rf node_modules package-lock.json
npm install
```

#### 3. Database Connection Issues
- Verify database is running
- Check DATABASE_URL in `.env`
- Ensure credentials are correct
- Check network connectivity

#### 4. Permission Denied Errors
```bash
# Fix file permissions
chmod +x scripts/*.sh
```

#### 5. Node Version Mismatch
```bash
# Use nvm to manage Node versions
nvm use  # Uses version from .nvmrc if available
# Or specify version
nvm use 16
```

### Debugging

#### Enable Debug Logging
```bash
DEBUG=* npm start
```

#### Debug with Node Inspector
```bash
node --inspect app.js
```

Then open `chrome://inspect` in Chrome to access the debugger.

#### Debug with VS Code
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "Launch Program",
      "program": "${workspaceFolder}/app.js"
    }
  ]
}
```

## Additional Resources

### Documentation
- [Official Documentation](./README.md)
- [API Documentation](./docs/API.md) (if available)
- [Contributing Guidelines](./CONTRIBUTING.md) (if available)

### External Resources
- [Node.js Documentation](https://nodejs.org/docs/)
- [npm Documentation](https://docs.npmjs.com/)
- [Docker Documentation](https://docs.docker.com/)

### Useful Commands Reference
```bash
# View logs
npm run logs

# Restart application
npm restart

# Stop application
npm stop

# Check dependencies for updates
npm outdated

# Update dependencies
npm update

# View package information
npm info <package-name>
```

## Getting Help

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review the README.md file
3. Check project's issues on GitHub
4. Contact the maintainers

---

**Last Updated**: 2026-01-12  
**Created by**: mshelar08
