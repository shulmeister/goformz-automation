# GoFormz-Shiftcare Integration App

This app integrates GoFormz API with Shiftcare platform to automatically create clients and employees from PDF packets.

## Features
- Fetches PDFs from GoFormz API
- Parses client and employee packets
- Automatically creates clients/employees in Shiftcare using Playwright
- **Complete Client Workflow**: Creates client → navigates to client list → opens profile → adds care plan with tasks/goals
- **Employee Creation**: Simple employee creation with all required fields

## Environment Variables
Create a `.env` file with:
```
GOFORMZ_CLIENT_ID=your_client_id
GOFORMZ_CLIENT_SECRET=your_client_secret
SHIFTCARE_USERNAME=your_username
SHIFTCARE_PASSWORD=your_password
```

## Installation
1. Install dependencies: `pip install -r requirements.txt`
2. Install Playwright browsers: `playwright install`
3. Set up environment variables
4. Run: `python app.py`

## GitHub Deployment

### Repository
This project is deployed from: [https://github.com/shulmeister/goformz-automation](https://github.com/shulmeister/goformz-automation)

### Automated Deployment with GitHub Actions

1. **Set up GitHub Secrets** in your repository settings:
   - `GOFORMZ_CLIENT_ID`: Your GoFormz API client ID
   - `GOFORMZ_CLIENT_SECRET`: Your GoFormz API client secret
   - `SHIFTCARE_USERNAME`: Your Shiftcare username
   - `SHIFTCARE_PASSWORD`: Your Shiftcare password
   - `HEROKU_API_KEY`: Your Heroku API key
   - `HEROKU_APP_NAME`: Your Heroku app name
   - `HEROKU_EMAIL`: Your Heroku email

2. **Push to main branch** - GitHub Actions will automatically:
   - Run tests
   - Deploy to Heroku if tests pass

### Manual Deployment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/shulmeister/goformz-automation.git
   cd goformz-automation
   ```

2. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

3. **Or deploy manually**:
   ```bash
   # Set up Heroku app
   heroku create your-app-name
   
   # Set environment variables
   heroku config:set GOFORMZ_CLIENT_ID=your_client_id
   heroku config:set GOFORMZ_CLIENT_SECRET=your_client_secret
   heroku config:set SHIFTCARE_USERNAME=your_username
   heroku config:set SHIFTCARE_PASSWORD=your_password
   
   # Add buildpacks
   heroku buildpacks:add https://github.com/jontewks/puppeteer-heroku-buildpack.git
   heroku buildpacks:add heroku/python
   
   # Deploy
   git push heroku main
   ```

## API Endpoints

- `GET /health` - Health check
- `GET /forms` - Get recent GoFormz forms
- `POST /process-packets` - Process forms and create in Shiftcare

### Process Packets Example
```bash
# Process all recent forms
curl -X POST https://your-app.herokuapp.com/process-packets

# Process specific forms
curl -X POST https://your-app.herokuapp.com/process-packets \
  -H "Content-Type: application/json" \
  -d '{"form_ids": ["form_id_1", "form_id_2"]}'
```

## Testing

Run comprehensive tests:
```bash
python test_complete_workflow.py
```

## Workflow

### For Client Packets:
1. Fetch PDF from GoFormz
2. Parse client data + care plan info + tasks/goals
3. Create client in Shiftcare
4. Navigate to client list
5. Find and open client profile
6. Add care plan with tasks and goals

### For Employee Packets:
1. Fetch PDF from GoFormz
2. Parse employee data
3. Create employee in Shiftcare
