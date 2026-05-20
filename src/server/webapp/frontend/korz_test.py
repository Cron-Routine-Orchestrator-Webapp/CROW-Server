# import os
# import sys
# from django.core.management import execute_from_command_line


# def run_django_server(host="127.0.0.1", port=8000):
#     """
#     Run Django's development server from Python code.

#     :param host: Host address (default: 127.0.0.1)
#     :param port: Port number (default: 8000)
#     """
#     try:
#         # Ensure DJANGO_SETTINGS_MODULE is set
#         os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend.settings")

#         # Build the command arguments
#         sys.argv = ["manage.py", "runserver", f"{host}:{port}"]

#         # Execute the runserver command
#         execute_from_command_line(sys.argv)

#     except Exception as e:
#         print(f"Error starting Django server: {e}")


# if __name__ == "__main__":
#     run_django_server("0.0.0.0", 8000)  # Accessible from all network interfaces


from database_backend import DatabaseBackend

backend = DatabaseBackend()
print(backend.get_tasks())
