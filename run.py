from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    db.create_all()

print(
    "=" * 50
)

print(
    f"Running in "
    f"{app.config['ENV_NAME']}"
    f" environment"
)

print(
    "=" * 50
)

app.logger.info(
    f"Environment : "
    f"{app.config['ENV_NAME']}"
)

if __name__ == '__main__':
    app.run(debug=True)