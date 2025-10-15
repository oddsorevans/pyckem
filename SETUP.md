# GitHub Actions Setup Guide

This guide will help you set up GitHub Actions to automatically create NFL Pick-em forms without needing your computer.

## Prerequisites

- Google Cloud project with Forms API enabled
- RapidAPI account with NFL API access
- GitHub repository for this project

## Step 1: Update Dependencies Locally

First, update your local dependencies to use the new authentication:

```bash
pip install -r requirements.txt
```

## Step 2: Generate Google OAuth Token

Run the script locally once to generate the refresh token:

```bash
python main.py --start-date 2025-10-15 --end-date 2025-10-21 --week 7 --final-game "Texans vs. Seahawks"
```

This will:
1. Open a browser for OAuth authentication
2. Create `misc/token.json` with your refresh token

## Step 3: Configure GitHub Secrets

Add the following secrets to your GitHub repository (Settings → Secrets and variables → Actions → New repository secret):

### 1. GOOGLE_CREDENTIALS_JSON

Copy the contents of `misc/token.json`:

```bash
cat misc/token.json
```

Create a new secret named `GOOGLE_CREDENTIALS_JSON` and paste the entire JSON contents.

### 2. RAPID_API_KEY

Your RapidAPI key from https://rapidapi.com/

Create a new secret named `RAPID_API_KEY` with your API key.

### 3. RAPID_API_HOST

Your RapidAPI host (likely `api-american-football.p.rapidapi.com`)

Create a new secret named `RAPID_API_HOST` with the host value.

## Step 4: Run the Workflow

### Manual Trigger

1. Go to your GitHub repository
2. Click on "Actions" tab
3. Select "Create NFL Pick-em Form" workflow
4. Click "Run workflow"
5. Fill in the parameters:
   - **Start date**: e.g., `2025-10-15`
   - **End date**: e.g., `2025-10-21`
   - **Week**: e.g., `7`
   - **Final game**: e.g., `Texans vs. Seahawks`
6. Click "Run workflow"

### Automated Schedule (Optional)

To run automatically every week, uncomment the schedule section in `.github/workflows/create_pickem_form.yml`:

```yaml
schedule:
  # Runs every Tuesday at 10:00 AM UTC
  - cron: '0 10 * * 2'
```

You'll need to hardcode or calculate the parameters for automated runs.

## Troubleshooting

### Token Expired Error

If you see "Error refreshing token", your refresh token may have expired. Regenerate it:

1. Delete `misc/token.json` locally
2. Run the script again locally to re-authenticate
3. Update the `GOOGLE_CREDENTIALS_JSON` secret with the new token

### API Rate Limits

If you hit RapidAPI rate limits, check your subscription tier and consider upgrading.

### Form Not Created

Check the Actions logs:
1. Go to Actions tab
2. Click on the failed workflow run
3. Review the error messages in the logs

## Testing Locally

Test with the new CLI interface:

```bash
# Basic usage
python main.py \
  --start-date 2025-10-15 \
  --end-date 2025-10-21 \
  --week 7 \
  --final-game "Texans vs. Seahawks"

# Using environment variables
export RAPID_API_KEY="your-key-here"
export RAPID_API_HOST="api-american-football.p.rapidapi.com"
python main.py --start-date 2025-10-15 --end-date 2025-10-21 --week 7 --final-game "Texans vs. Seahawks"
```

## Security Notes

- Never commit `misc/token.json` or `misc/forms_secret.json` to git
- Keep GitHub secrets secure
- Refresh tokens can be revoked from Google Cloud Console if compromised
- Review the `.gitignore` to ensure credentials aren't tracked

## Additional Resources

- [Google Forms API Documentation](https://developers.google.com/forms/api)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [RapidAPI Documentation](https://docs.rapidapi.com/)
