# Firebase Google Authentication Setup

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com)
2. Click "Add project" or select existing project
3. Follow the setup wizard

## Step 2: Enable Google Sign-In

1. In Firebase Console, go to **Authentication** → **Sign-in method**
2. Click **Google** provider
3. Toggle **Enable**
4. Add your support email
5. Click **Save**

## Step 3: Register Web App

1. Go to **Project Settings** (gear icon)
2. Scroll to "Your apps" section
3. Click the **Web** icon (`</>`)
4. Register app with a nickname (e.g., "Traveloop Web")
5. Copy the `firebaseConfig` object

## Step 4: Add Config to Traveloop

Open `templates/login.html` and replace this section:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

With your actual Firebase config from Step 3.

## Step 5: Add Authorized Domain (for production)

1. In Firebase Console → **Authentication** → **Settings** → **Authorized domains**
2. Add your domain (e.g., `yourdomain.com`)
3. `localhost` is already authorized for development

## Step 6: Test

1. Run the app: `python app.py`
2. Go to `http://127.0.0.1:5000/login`
3. Click "Continue with Google"
4. Sign in with your Google account
5. You'll be redirected to the dashboard

## How It Works

1. User clicks "Continue with Google"
2. Firebase SDK opens Google sign-in popup
3. User authenticates with Google
4. Frontend sends user data (email, name, uid) to `/google-login` endpoint
5. Backend creates/finds user in SQLite database
6. Flask-Login session is created
7. User is redirected to dashboard

## Security Note

For production, consider adding server-side token verification using `firebase-admin` to validate the Firebase ID token before creating sessions.
