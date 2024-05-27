

# github actions setup

* see commit history in staging
  * service workers approach needed for app engine (old api)
  * https://github.com/google-github-actions/auth/blob/main/docs/EXAMPLES.md#workload-identity-federation-through-a-service-account
  * https://github.com/google-github-actions/auth?tab=readme-ov-file#indirect-wif
* enable apis
  * Cloud Logging API
  * App Engine Admin API
  * Secret Manager API
  * Cloud Pub/Sub API
  * IAM Service Account Credentials API
* secrets need to be on the GAE service worker
* probably need a dev project too

errors:
 * Caller does not have storage.buckets.list access to the Google Cloud project. Permission 'storage.buckets.list' denied on resource (or it may not exist).
* ERROR: (gcloud.app.deploy) Permissions error fetching application [apps/appspot]. Please make sure that you have permission to view applications on the project and that story-time-staging@appspot.gserviceaccount.com has the App Engine Deployer (roles/appengine.deployer) role.

# Roles
cicd-service-account@story-time-staging.iam.gserviceaccount.com	cicd-service-account	
  * App Engine Admin
  * Cloud Build Editor
  * Cloud Build Service Account
  * Storage Admin

story-time-staging@appspot.gserviceaccount.com	App Engine default service account	
  * App Engine Admin
  * Secret Manager Secret Accessor
  * Secret Manager Viewer
  * Storage Admin

