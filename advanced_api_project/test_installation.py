#!/usr/bin/env python3
"""
Test script to verify Django installation and basic functionality
"""

import os
import django
from django.conf import settings

# Configure Django settings
if not settings.configured:
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test_db.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'api',
        ],
        SECRET_KEY='test-secret-key'
    )

django.setup()

def test_django_installation():
    """Test that Django is properly installed"""
    try:
        # Test basic Django functionality
        from django.core.management import execute_from_command_line
        from django.db import connection
        from django.test import TestCase
        
        print("✓ Django installation verified")
        print("✓ Django modules imported successfully")
        
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result[0] == 1:
                print("✓ Database connection working")
            else:
                print("✗ Database connection failed")
                
        return True
        
    except ImportError as e:
        print(f"✗ Django import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Django setup error: {e}")
        return False

if __name__ == "__main__":
    test_django_installation()