##SheRanks Project
SheRanks is a platform dedicated to promoting gender equality and safety for female students in universities. The project aims to create a safe and inclusive environment where all female students can thrive academically and personally. Through our tools and resources, we empower female students to voice their concerns, share experiences, and drive positive change.

##Features
User Authentication: A secure system for user registration, login, and an editable user profile with gender-based permissions.
University Ranking: A dynamic, data-driven ranking of universities based on multiple criteria, including safety, inclusivity, student support, and living environment.
AI Sentiment Analysis: An artificial intelligence feature that analyzes the sentiment of user posts and integrates the results into the final university ranking score.
User Contributions: Authenticated female users can submit posts and ratings, with support for image uploads.
Professional Admin Dashboard: An enhanced Django admin interface that allows for bulk import of university data via CSV files.
Detailed Methodology Page: A dedicated page that explains the ranking methodology and presents key statistics with data visualizations.
SEO Optimization: The platform is structured with SEO in mind to improve search engine visibility.

##Known Issues & Help Wanted
We are currently working on resolving a few technical issues. Your help would be greatly appreciated!
Login and Profile Pages: The login and user profile pages are not currently rendering correctly. We believe this is a template-related issue, and we are actively seeking contributions to fix it.

##Installation
This project is built on the Python Django framework. To get started, follow these steps.

1. Clone the repository: Bash
git clone https://github.com/canst/she-ranks-python.git
cd she-ranks-python
2. Set up the Python virtual environment:
Bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
3. Install project dependencies:
Bash
pip install django Pillow vadersentiment django-import-export dj-database-url
4. Set up the database:
Bash
python manage.py makemigrations accounts universities
python manage.py migrate
5. Create a superuser to access the admin panel:
Bash
python manage.py createsuperuser

6. Seed the database with university data:
Create a file named universities.csv in your project root with the university data.
Go to the admin dashboard (/admin/), navigate to the "Universities" list, and use the "Import" button to upload the CSV file.

7. Launch the development server:
Bash
python manage.py runserver
The application will be available at http://127.0.0.1:8000/.

##Usage
Homepage: The home page (/) provides an overview of the project and highlights the top-ranked universities.
Universities: Explore the list of universities at /universities/ and click on a university to view its details and post new content.
Authentication: Use the /accounts/register/ and /accounts/login/ pages to manage your account.
Admin Panel: Log in to the admin dashboard (/admin/) to manage all data.

##Contributing
Contributions are welcome! If you would like to contribute to the SheRanks project, please follow these steps:
Fork the repository.
Create a new branch: git checkout -b feature/your-feature-name
Make your changes and commit them: git commit -m 'Add your commit message'
Push the changes to your branch: git push origin feature/your-feature-name
Submit a pull request.

License
This project is licensed under the MIT License.
