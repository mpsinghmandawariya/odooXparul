# HOW TO START TRAVELOOP - STEP BY STEP

## IMPORTANT: Stop Everything First!
1. Press `Ctrl+C` in ALL terminal windows
2. Close all terminals
3. Close your browser
4. Wait 10 seconds

## METHOD 1: Using Batch File (EASIEST)

1. Navigate to folder:
   ```
   c:\Users\Mahipal singh deora\OneDrive\Desktop\Final\traveloop
   ```

2. Double-click: `START_APP.bat`

3. Wait for this message:
   ```
   * Running on http://127.0.0.1:5000
   ```

4. Open browser and go to: **http://127.0.0.1:5000/test**

5. You should see "Server is Running!" page

6. Click on "Login Page" link or go to: **http://127.0.0.1:5000/login**

## METHOD 2: Using Command Line

1. Open Command Prompt (cmd)

2. Run these commands:
   ```bash
   cd "c:\Users\Mahipal singh deora\OneDrive\Desktop\Final\traveloop"
   python app.py
   ```

3. Wait for:
   ```
   * Running on http://127.0.0.1:5000
   ```

4. Open browser: **http://127.0.0.1:5000/test**

## TESTING THE SERVER

### Test 1: Server Status
- URL: http://127.0.0.1:5000/test
- Expected: Green "Server is Running!" page
- If this fails: Server is not running properly

### Test 2: Login Page
- URL: http://127.0.0.1:5000/login
- Expected: Premium login page with Traveloop logo
- If this fails: Template or static files issue

### Test 3: Register Page
- URL: http://127.0.0.1:5000/register
- Expected: Registration form
- If this fails: Route not working

## COMMON ERRORS & FIXES

### Error: "Not Found - 404"
**What you see**: White page with "Not Found" message

**Possible causes**:
1. Server not running
   - Fix: Start the server using METHOD 1 or 2 above
   
2. Wrong URL
   - Fix: Use http://127.0.0.1:5000 NOT http://localhost:5001 or other ports
   
3. Accessing protected route without login
   - Fix: Go to /login first, then access other pages

### Error: "Connection Refused"
**What you see**: Browser can't connect

**Fix**: 
- Server is not running
- Start the server using METHOD 1 or 2

### Error: "Template Not Found"
**What you see**: Error message about missing template

**Fix**:
- Make sure you're in the correct directory
- Check that templates/ folder exists

### Error: CSS Not Loading (Page Looks Broken)
**What you see**: Plain white page with no styling

**Fix**:
1. Clear browser cache (Ctrl+Shift+Delete)
2. Hard refresh (Ctrl+F5)
3. Check static/css/premium.css exists

## FIRST TIME SETUP

### Create an Account
1. Start server
2. Go to: http://127.0.0.1:5000/register
3. Fill in:
   - First Name: Your Name
   - Last Name: Your Last Name
   - Email: test@example.com
   - Password: password123
   - Confirm Password: password123
4. Click "Create Account"
5. You'll be redirected to login

### Login
1. Go to: http://127.0.0.1:5000/login
2. Enter:
   - Email: test@example.com
   - Password: password123
3. Click "Sign In"
4. You'll be redirected to Dashboard

## AFTER LOGIN - AVAILABLE PAGES

Once logged in, you can access:

- **Dashboard**: http://127.0.0.1:5000/dashboard
  - View your trips
  - See statistics
  - Quick actions

- **My Trips**: http://127.0.0.1:5000/my-trips
  - List all your trips
  - Filter by status
  - Edit/delete trips

- **Discover Cities**: http://127.0.0.1:5000/search-city
  - Search destinations
  - View city information
  - Save destinations

- **Activities**: http://127.0.0.1:5000/search-activity
  - Browse activities
  - Filter by category
  - View pricing and ratings

- **Community**: http://127.0.0.1:5000/community
  - View posts
  - Share experiences
  - Like and comment

- **Analytics**: http://127.0.0.1:5000/analytics
  - View travel statistics
  - Budget analysis
  - Popular destinations

- **Profile**: http://127.0.0.1:5000/profile
  - Edit your information
  - Change password
  - Account settings

- **Notifications**: http://127.0.0.1:5000/notifications
  - View notifications
  - Mark as read
  - Delete notifications

## NAVIGATION FEATURES

### Sidebar (Left)
- Click any menu item to navigate
- Active page is highlighted
- Logout button at bottom

### Navbar (Top)
- **Search Bar**: Type and press Enter to search cities
- **Plus Icon**: Click to create new trip
- **Bell Icon**: Click to view notifications
- **Profile**: Click to open dropdown menu
  - Profile
  - Analytics
  - Logout

## STILL HAVING ISSUES?

1. **Check Terminal Output**
   - Look for error messages
   - Copy the entire output

2. **Check Browser Console**
   - Press F12
   - Go to Console tab
   - Look for red errors

3. **Verify Files Exist**
   ```bash
   dir templates\login_premium.html
   dir templates\base_premium.html
   dir static\css\premium.css
   ```

4. **Test Basic Route**
   - Go to: http://127.0.0.1:5000/test
   - Should show "Server is Running!"

5. **Restart Everything**
   - Close terminal (Ctrl+C)
   - Close browser
   - Wait 10 seconds
   - Start again from METHOD 1

## NEED HELP?

Provide this information:
1. What URL are you trying to access?
2. What error message do you see?
3. Copy terminal output
4. Screenshot of error page
5. Browser console errors (F12 > Console)

---

## QUICK CHECKLIST

- [ ] Stopped all running processes
- [ ] Opened terminal in correct folder
- [ ] Ran `python app.py`
- [ ] Saw "Running on http://127.0.0.1:5000"
- [ ] Opened browser
- [ ] Went to http://127.0.0.1:5000/test
- [ ] Saw "Server is Running!" page
- [ ] Clicked "Login Page" link
- [ ] Saw premium login page
- [ ] Created account or logged in
- [ ] Redirected to dashboard
- [ ] All navigation working

If ALL checkboxes are checked, everything is working! 🎉
