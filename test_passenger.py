"""
Script to verify Passenger configuration.

Run this directly on the server with:
python test_passenger.py
"""

import os
import sys
from pathlib import Path


def main():
    print("=" * 60)
    print("Passenger Configuration Test")
    print("=" * 60)

    base_dir = Path(__file__).resolve().parent
    print(f"\n1. Base Directory: {base_dir}")

    print("\n2. Python Path:")
    for path in sys.path[:5]:
        print(f"   - {path}")

    env_file = base_dir / ".env"
    print(f"\n3. .env file exists: {env_file.exists()}")
    if env_file.exists():
        print(f"   Location: {env_file}")

    wsgi_file = base_dir / "passenger_wsgi.py"
    print(f"\n4. passenger_wsgi.py exists: {wsgi_file.exists()}")

    manage_file = base_dir / "manage.py"
    print(f"\n5. manage.py exists: {manage_file.exists()}")

    print("\n6. Testing Django import...")
    try:
        import django

        print(f"   OK: Django {django.get_version()} imported")
    except Exception as exc:
        print(f"   FAILED: Django import failed: {exc}")

    print("\n7. Testing settings import...")
    try:
        os.environ.setdefault(
            "DJANGO_SETTINGS_MODULE", "FarmManagerSystem.productions_settings"
        )
        from django.conf import settings

        print("   OK: Settings imported")
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
    except Exception as exc:
        print(f"   FAILED: Settings import failed: {exc}")
        import traceback

        traceback.print_exc()

    print("\n8. Testing WSGI import...")
    try:
        from django.core.wsgi import get_wsgi_application

        get_wsgi_application()
        print("   OK: WSGI application created")
    except Exception as exc:
        print(f"   FAILED: WSGI import failed: {exc}")
        import traceback

        traceback.print_exc()

    print("\n9. Testing passenger_wsgi import...")
    try:
        sys.path.insert(0, str(base_dir))
        from passenger_wsgi import application  # noqa: F401

        print("   OK: passenger_wsgi.application imported")
    except Exception as exc:
        print(f"   FAILED: passenger_wsgi import failed: {exc}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
