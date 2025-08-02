import serverless_wsgi
from sheranks_project.wsgi import application

def handler(event, context):
    return serverless_wsgi.handle_request(application, event, context)
