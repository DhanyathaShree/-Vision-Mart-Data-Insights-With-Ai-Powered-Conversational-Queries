from flask import Flask, request, jsonify
import pandas as pd
from sales_data_insights import (
    generate_sql_query,
    execute_query,
    create_visualization
)
from flask_cors import CORS
from auth import auth_bp, token_required  # Import auth blueprint

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'your-secret-key'  # Use environment variable in production
CORS(app)

# Register the auth blueprint
#app.register_blueprint(auth_bp, url_prefix='/auth')

# Function to handle user queries and generate insights
@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        # Step 1: Get the user query from the frontend
        user_query = request.json.get('query')
        if not user_query:
            return jsonify({"error": "No query provided"}), 400

        # Step 2: Generate SQL query using Gemini LLM
        sql_query = generate_sql_query(user_query)
        print(f"Generated SQL Query: {sql_query}")

        # Step 3: Execute the SQL query and fetch results
        result_df = execute_query(sql_query)
        if result_df is None or result_df.empty:
            return jsonify({
                "response": {
                    "text": "An error occurred while fetching data or no data was returned.",
                    "chart_data": None
                }
            }), 200

        # Step 4: Check if visualization is possible
        visualization_possible = len(result_df.columns) >= 2
        chart_data = None
        if visualization_possible:
            x_column = result_df.columns[0]  # First column as X-axis
            y_column = result_df.columns[1]  # Second column as Y-axis
            print("Creating visualization...")
            chart_data = create_visualization(result_df, x_column, y_column)

        # Step 5: Format the response
        response_text = f"Query Result: {result_df.to_dict(orient='records')}"
        return jsonify({
            "response": {
                "text": response_text,
                "chart_data": chart_data  # Include chart data for frontend rendering
            }
        }), 200

    except Exception as e:
        # Log the error and return a user-friendly message
        print(f"Error processing query: {e}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=3000)