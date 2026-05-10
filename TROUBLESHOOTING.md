# TROUBLESHOOTING GUIDE - 404 Not Found Error

## Quick Fix Steps

### Step 1: Stop All Running Processes
1. Press `Ctrl+C` in ALL terminal windows
2. Close any terminals running Python/Flask
3. Wait 5 seconds

### Step 2: Start the Application Correctly

**Option A - Using Batch File (RECOMMENDED)**
1. Double-click `START_APP.bat` in the traveloop folder
2. Wait for "Running on http://127.0.0.1:5000"
3. Open browser to http://127.0.0.1:5000

**Option B - Using Command Line**
```bash
cd "c:\Users\Mahipal singh deora\OneDrive\Desktop\Final\traveloop"
python app.py
```

### Step 3: Access the Correct URL
- **Correct**: http://127.0.0.1:5000
- **Correct**: http://localhost:5000
- **Wrong**: http://127.0.0.1:5000/some-random-path

## Common 404 Errors & Solutions

### Error: "404 Not Found" on root URL
**Cause**: App not running or wrong port
**Solution**: 
- Make sure you see "Running on http://127.0.0.1:5000" in terminal
- Check you're using port 5000, not 5001 or other ports

### Error: "404 Not Found" on /dashboard
**Cause**: Not logged in
**Solution**: 
- Go to http://127.0.0.1:5000 (redirects to login)
- Login with your credentials
- Then you'll be redirected to dashboard

### Error: "404 Not Found" on static files (CSS/JS)
**Cause**: Static folder path issue
**Solution**: 
- Verify `static/css/premium.css` exists
- Check file permissions
- Clear browser cache (Ctrl+Shift+Delete)

### Error: "404 Not Found" after clicking links
**Cause**: Wrong URL in template
**Solution**: Already fixed in all templates - restart app

## Verify App is Working

Run this command to test:
```bash
cd "c:\Users\Mahipal singh deora\OneDrive\Desktop\Final\traveloop"
python test_app.py
```

You should see:
```
[OK] Flask app imported successfully
[OK] Secret key configured: True
[OK] Database URI: sqlite:///...
[ROUTES] Registered Routes:
  / -> index
  /login -> login
  /dashboard -> dashboard
  ... (40 total routes)
[READY] App is ready to run!
```

## All Available Routes

After logging in, these URLs work:
- http://127.0.0.1:5000/ (redirects to dashboard)
- http://127.0.0.1:5000/dashboard
- http://127.0.0.1:5000/my-trips
- http://127.0.0.1:5000/search-city
- http://127.0.0.1:5000/search-activity
- http://127.0.0.1:5000/community
- http://127.0.0.1:5000/analytics
- http://127.0.0.1:5000/profile
- http://127.0.0.1:5000/notifications
- http://127.0.0.1:5000/create-trip

## Still Getting 404?

1. **Check what URL you're accessing**
   - Look at the browser address bar
   - Copy the exact URL and check if it matches routes above

2. **Check terminal output**
   - Look for error messages in the terminal
   - Check if the route is being accessed (Flask logs all requests)

3. **Check if you're logged in**
   - Most routes require login
   - If not logged in, you'll be redirected to /login

4. **Restart the application**
   - Stop with Ctrl+C
   - Run `python app.py` again
   - Try accessing the URL again

## Test Login

Default test account (if you created one):
- Email: test@example.com
- Password: (whatever you set)

Or create a new account:
1. Go to http://127.0.0.1:5000/register
2. Fill in the form
3. Click "Create Account"
4. Login with your credentials

## Browser Console Errors

If pages load but look broken:
1. Press F12 to open Developer Tools
2. Check Console tab for errors
3. Check Network tab for failed requests
4. Common issues:
   - CSS not loading: Clear cache
   - JS errors: Check browser compatibility
   - Image errors: Internet connection required for Unsplash images

## Need More Help?

Provide this information:
1. Exact URL you're trying to access
2. Terminal output (copy all text)
3. Browser console errors (F12 > Console)
4. Screenshot of the error page
