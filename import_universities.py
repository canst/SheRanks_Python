import os
import csv
from django.conf import settings
from django.db import IntegrityError

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheranks_project.settings')
settings.configure()
import django
django.setup()

from universities.models import University

# Path to the CSV file
csv_file_path = os.path.join(settings.BASE_DIR, 'universities.csv')

def import_data():
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Create or update the university entry
                University.objects.update_or_create(
                    slug=row['slug'],
                    defaults={
                        'name': row['name'],
                        'location': row['location'],
                        'website': row['website'],
                        'description': row['description'],
                        'safety_score': float(row['safety_score']),
                        'inclusivity_score': float(row['inclusivity_score']),
                        'support_score': float(row['support_score']),
                        'living_score': float(row['living_score']),
                        'equality_score': float(row['equality_score']),
                        'ranking_score': float(row['ranking_score']),
                    }
                )
                print(f"Successfully imported/updated: {row['name']}")
            except IntegrityError:
                print(f"Skipping duplicate entry: {row['name']}")
            except Exception as e:
                print(f"An error occurred with {row['name']}: {e}")

if __name__ == '__main__':
    import_data()