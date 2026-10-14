# Send website briefs to storyglassstudio@gmail.com

About 5 minutes, once. Free. Everything stays in the studio's own Google account.

1. Sign in to Google as **storyglassstudio@gmail.com**.
2. Go to sheets.new to make a new Google Sheet. Name it **Storyglass Briefs**.
3. In the sheet, open **Extensions → Apps Script**. Delete the sample code, paste all of `Code.gs`, and press **Save**.
4. In the function menu at the top, pick **testSetup** and press **Run**. Google asks for permission
   ("send email as you" and "see and edit this spreadsheet"). Choose the studio account, then
   **Advanced → Go to project (unsafe) → Allow**. The "unsafe" warning appears because the script is
   yours and not published by Google; that's normal.
   You should now get two emails (the brief and the client confirmation), and a **Briefs** tab with one
   test row. Delete that row.
5. Press **Deploy → New deployment**. Type: **Web app**. Execute as: **Me**. Who has access: **Anyone**.
   Press **Deploy** and copy the **Web app URL** (it ends in `/exec`).
6. Put the URL in `page.html` (search for `BRIEF_ENDPOINT`), or send it to Claude to do it.

Check: open the URL in a browser. It should say `{"ok":true,"service":"Storyglass Studio brief receiver"}`.

Changing the script later: edit, save, then **Deploy → Manage deployments → edit (pencil) → Version: New version → Deploy**.
The URL stays the same.

Limits: a free Gmail account can send about 100 emails a day from scripts. Each brief uses two
(one to you, one to the client), so about 50 briefs a day.
