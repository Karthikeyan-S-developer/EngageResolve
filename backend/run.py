import sys
import os
from app.main import create_app
from app.seed import seed_demo_data

def main():
    if "--seed" in sys.argv:
        print("Seeding demo database...")
        count = seed_demo_data()
        print(f"Seeding completed ({count} events).")
        if "--run" not in sys.argv:
            return

    port = int(os.getenv("PORT", 5000))
    app = create_app()
    print(f"Starting EngageResolve Backend Server on http://localhost:{port}...")
    app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()
