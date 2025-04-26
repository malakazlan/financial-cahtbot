from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)  # Runs on http://localhost:5000
    
