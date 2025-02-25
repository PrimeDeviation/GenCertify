# GitHub Actions Deployment Workflow

This repository contains a GitHub Actions workflow that automatically deploys the GenCertify application to Google Cloud Run whenever code is pushed to the master branch.

## Setup Instructions

### 1. Set up Workload Identity Federation

Workload Identity Federation allows GitHub Actions to authenticate to Google Cloud without storing a service account key.

```bash
# Create a workload identity pool
gcloud iam workload-identity-pools create "github-actions-pool" \
  --location="global" \
  --description="Pool for GitHub Actions" \
  --display-name="GitHub Actions Pool"

# Get the workload identity pool ID
export WORKLOAD_IDENTITY_POOL_ID=$(gcloud iam workload-identity-pools describe "github-actions-pool" \
  --location="global" \
  --format="value(name)")

# Create a workload identity provider in that pool
gcloud iam workload-identity-pools providers create-oidc "github-actions-provider" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --display-name="GitHub Actions Provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
  --issuer-uri="https://token.actions.githubusercontent.com"
```

### 2. Create a service account for GitHub Actions

```bash
# Create service account
gcloud iam service-accounts create "github-actions-sa" \
  --description="Service account for GitHub Actions" \
  --display-name="GitHub Actions Service Account"

# Get the service account email
export SERVICE_ACCOUNT_EMAIL="github-actions-sa@gencertify.iam.gserviceaccount.com"

# Grant the service account permissions to deploy to Cloud Run
gcloud projects add-iam-policy-binding gencertify \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding gencertify \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/storage.admin"

gcloud projects add-iam-policy-binding gencertify \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/iam.serviceAccountUser"

# Allow the service account to access Secret Manager
gcloud projects add-iam-policy-binding gencertify \
  --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"
```

### 3. Configure workload identity federation

```bash
# Allow the GitHub Actions workflow to impersonate the service account
gcloud iam service-accounts add-iam-policy-binding "${SERVICE_ACCOUNT_EMAIL}" \
  --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/YOUR_GITHUB_USERNAME/GenCertify" \
  --role="roles/iam.workloadIdentityUser"

# Get the workload identity provider resource name
export WORKLOAD_IDENTITY_PROVIDER=$(gcloud iam workload-identity-pools providers describe "github-actions-provider" \
  --location="global" \
  --workload-identity-pool="github-actions-pool" \
  --format="value(name)")
```

### 4. Configure GitHub Secrets

Add the following secrets to your GitHub repository:

- `WIF_PROVIDER`: The Workload Identity Provider (the value of `$WORKLOAD_IDENTITY_PROVIDER`)
- `WIF_SERVICE_ACCOUNT`: The service account email (the value of `$SERVICE_ACCOUNT_EMAIL`)

These secrets are used in the GitHub Actions workflow to authenticate to Google Cloud.

## Workflow Details

The workflow:

1. Runs on pushes to the master branch
2. Sets up a Python environment
3. Authenticates to Google Cloud using Workload Identity Federation
4. Deploys the application to Cloud Run with all required environment variables and secrets
5. Outputs the URL of the deployed service