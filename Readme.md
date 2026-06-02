py -m venv venv -> to setup virtual environment

.\venv\Scripts\Activate -> to activate the virtual environment

pip install -r requirements.txt -> to install all required packages

add groq api key in the environment variable GROQ_API_KEY=YOUR_KEY

uvicorn mains:dapp --reload -> to run the app

/ -> health check route (GET)
/ai-analysis -> to analyze and get 3 best suitable projects for job description (POST)
/add-project -> to add projects with title and description (POST)
/get-all-projects -> to get all the projects from database (GET)
/get-project/{project_id} -> to get information of a particular project (GET)
/edit-project/{project_id} -> to edit information of a particular project (PUT)
/delete-project/{project_id} -> to delete a particular project (DELETE)
/docs -> fast api swagger to test routes (Inbuilt)
