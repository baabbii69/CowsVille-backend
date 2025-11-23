"""
Test script to verify Passenger configuration
Run this on the server to test if everything works
"""

import sys
import os
from pathlib import Path

print("=" * 60)
print("Passenger Configuration Test")
print("=" * 60)

BASE_DIR = Path(__file__).resolve().parent
print(f"\n1. Base Directory: {BASE_DIR}")

# Check Python path
print(f"\n2. Python Path:")
for p in sys.path[:5]:
    print(f"   - {p}")

# Check .env file
env_file = BASE_DIR / '.env'
print(f"\n3. .env file exists: {env_file.exists()}")
if env_file.exists():
    print(f"   Location: {env_file}")

# Check passenger_wsgi.py
wsgi_file = BASE_DIR / 'passenger_wsgi.py'
print(f"\n4. passenger_wsgi.py exists: {wsgi_file.exists()}")

# Check manage.py
manage_file = BASE_DIR / 'manage.py'
print(f"\n5. manage.py exists: {manage_file.exists()}")

# Test Django import
print(f"\n6. Testing Django import...")
try:
    import django
    print(f"   ✅ Django {django.get_version()} imported")
except Exception as e:
    print(f"   ❌ Django import failed: {e}")

# Test settings import
print(f"\n7. Testing settings import...")
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FarmManagerSystem.productions_settings')
    from django.conf import settings
    print(f"   ✅ Settings imported")
    print(f"   DEBUG: {settings.DEBUG}")
    print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
except Exception as e:
    print(f"   ❌ Settings import failed: {e}")
    import traceback
    traceback.print_exc()

# Test WSGI import
print(f"\n8. Testing WSGI import...")
try:
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
    print(f"   ✅ WSGI application created")
except Exception as e:
    print(f"   ❌ WSGI import failed: {e}")
    import traceback
    traceback.print_exc()

# Test passenger_wsgi import
print(f"\n9. Testing passenger_wsgi import...")
try:
    sys.path.insert(0, str(BASE_DIR))
    from passenger_wsgi import application
    print(f"   ✅ passenger_wsgi.application imported")
except Exception as e:
    print(f"   ❌ passenger_wsgi import failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)

