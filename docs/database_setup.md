# Database Setup

After pulling the repo and initializing uv use following command in `src/server/webapp/frontend`:

`uv run manage.py makemigrations`
`uv run manage.py migrate`

This creates a new database file, if none existed or updates the existing for new table content.
