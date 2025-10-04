Clone the Repository Locally:

Open your terminal (Command Prompt on Windows, Terminal on Mac/Linux).
Navigate to a folder where you want to store the project (e.g., cd Desktop).
Run:
textgit clone https://github.com/yourusername/democratic-intelligence-dashboard.git
(Replace with your repo URL.)
Enter the new folder:
textcd democratic-intelligence-dashboard



Add Your Code and Dependencies:

Copy democratic_intelligence_dashboard.py into this folder.
Create a requirements.txt file in the same folder (this tells Streamlit Cloud what packages to install). Open a text editor and add:
textstreamlit
streamlit-folium
folium
pandas
numpy
scikit-learn
reportlab
Save it as requirements.txt.
Optional: Add a README.md with a description (e.g., "ICPR Democratic Intelligence Dashboard Prototype").


Commit and Push to GitHub:

In the terminal (still in the repo folder):
textgit add .
git commit -m "Initial commit: Add dashboard code and requirements"
git push origin main
(If your default branch is master, use master instead of main.)
Enter your GitHub credentials if prompted (or set up SSH keys for easier future pushes—see GitHub docs).


Deploy on Streamlit Community Cloud:

Go to share.streamlit.io and sign in with GitHub.
Click "New app".
Connect to your GitHub account if not already.
Select the repository (democratic-intelligence-dashboard).
Choose the branch (main or master).
Set the main file path to democratic_intelligence_dashboard.py.
Click "Deploy".
Wait 1-2 minutes for the build (it installs from requirements.txt and runs the app).


Access Your Deployed App:

Once deployed, you'll get a URL like https://yourappname.streamlit.app.
Share it or bookmark it—it's live and auto-updates on future git push!



Troubleshooting Tips

Build Errors: If deployment fails (e.g., missing packages), double-check requirements.txt for exact versions if needed (e.g., streamlit==1.35.0). View logs in the Streamlit dashboard.
Private Repo: Free tier requires public repos; upgrade to Pro for private.
Local Testing First: Before deploying, always test locally with streamlit run democratic_intelligence_dashboard.py to catch issues.
Updates: To update later, edit files locally, then git add ., git commit -m "Update", git push origin main—Streamlit auto-redeploys.
Documentation: For visuals or edge cases, check Streamlit's official guide: Deploying with GitHub (as of 2025, the process remains the same, with enhanced GitHub App integration for faster auth).
