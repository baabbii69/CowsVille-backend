"""
Passenger WSGI configuration for cPanel deployment.
Enhanced with health-check restart support.
"""

import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Ensure project root in Python path
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagerSystem.productions_settings')

# Load .env
try:
    from dotenv import load_dotenv
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
    else:
        load_dotenv()
except Exception:
    pass

# Health-check auto-restart
health_file = BASE_DIR / "tmp" / "restart.txt"
if health_file.exists():
    try:
        health_file.unlink()
        # Touching restart.txt tells Passenger to restart the app
        restart_trigger = BASE_DIR / "tmp" / "passenger.restart"
        restart_trigger.touch()
    except Exception:
        pass

# Start WSGI
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    import traceback
    error_msg = f"Error loading Django app: {e}\n{traceback.format_exc()}"
    def error_application(environ, start_response):
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [error_msg.encode()]
    application = error_application



# """
# Passenger WSGI configuration for cPanel deployment.
# Enhanced with better error handling and logging.
# """

# import sys
# import os
# from pathlib import Path

# # Get the directory where this file is located
# BASE_DIR = Path(__file__).resolve().parent

# # Add to Python path
# if str(BASE_DIR) not in sys.path:
#     sys.path.insert(0, str(BASE_DIR))

# # Set Django settings BEFORE importing anything
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagerSystem.productions_settings')

# # Load .env file
# try:
#     from dotenv import load_dotenv
#     env_file = BASE_DIR / '.env'
#     if env_file.exists():
#         load_dotenv(dotenv_path=env_file)
#         print(f"Loaded .env from {env_file}", file=sys.stderr)
#     else:
#         load_dotenv()  # Try default location
#         print("Loaded .env from default location", file=sys.stderr)
# except ImportError:
#     print("Warning: python-dotenv not available", file=sys.stderr)
# except Exception as e:
#     print(f"Warning: Error loading .env: {e}", file=sys.stderr)

# # Ensure logs directory exists
# logs_dir = BASE_DIR / 'logs'
# if not logs_dir.exists():
#     try:
#         logs_dir.mkdir(exist_ok=True)
#     except Exception:
#         pass

# # Import Django WSGI application with error handling
# try:
#     from django.core.wsgi import get_wsgi_application
#     application = get_wsgi_application()
#     print("Django WSGI application loaded successfully", file=sys.stderr)
# except Exception as e:
#     # Log the error to stderr (will appear in Passenger logs)
#     import traceback
#     error_msg = f"Error loading Django application: {e}\n{traceback.format_exc()}"
#     print(error_msg, file=sys.stderr)
    
#     # Create a simple error application that shows the error
#     def error_application(environ, start_response):
#         status = '500 Internal Server Error'
#         headers = [('Content-Type', 'text/plain')]
#         start_response(status, headers)
#         return [error_msg.encode('utf-8')]
    
#     application = error_application
