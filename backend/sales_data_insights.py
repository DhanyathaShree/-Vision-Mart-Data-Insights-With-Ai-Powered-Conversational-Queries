import psycopg2
import google.generativeai as genai
from langchain.prompts import PromptTemplate
import plotly.express as px  # For visualization
import pandas as pd  # To handle query results as a DataFrame

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "miniproject"
DB_USER = "postgres"
DB_PASSWORD = "1234"

# Function to connect to the PostgreSQL database
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

genai.configure(api_key="AIzaSyDsqtgCQHYhnNPLh0McnNIcozn5rlcfp2g") 
llm = genai.GenerativeModel("gemini-1.5-flash-latest")

# Define a prompt template for generating SQL queries
query_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
    Generate a valid SQL query for the 'superstore' table based on the following question:
    
    Question: {question}
    
    Important Notes:
    - Use column names exactly as they appear in the database schema.
    - Do not use backticks (`). Use double quotes (") only if necessary.
    - The column names are case-sensitive and should match the database schema.
    
    SQL Query:
    """
)

# Function to generate SQL queries using Gemini
def generate_sql_query(question):
    prompt = query_prompt.format(question=question)
    response = llm.generate_content(prompt)  # Generate the SQL query using Gemini
    sql_query = response.text.strip()  # Extract the generated text
    
    # Clean up the SQL query by removing Markdown formatting and backticks
    if sql_query.startswith("```sql"):
        sql_query = sql_query[len("```sql"):].strip()  # Remove the opening ```sql
    if sql_query.endswith("```"):
        sql_query = sql_query[:-len("```")].strip()  # Remove the closing ```
    
    # Replace incorrect column names and backticks
    sql_query = sql_query.replace("`", "")  # Remove backticks
    sql_query = sql_query.replace("Ship Mode", "ship_mode")  # Replace incorrect column name
    
    return sql_query

# Function to execute the generated SQL query and fetch results
def execute_query(query):
    conn = get_db_connection()
    if conn is None:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Get column names
        cursor.close()
        conn.close()
        return pd.DataFrame(result, columns=columns)  # Return results as a DataFrame
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def create_visualization(df, x_column, y_column):
    # Return raw data for visualization instead of rendering it
    return {
        "x": df[x_column].tolist(),
        "y": df[y_column].tolist(),
        "type": "bar",  # Default chart type
        "title": f"{y_column} by {x_column}"
    }


def answer_user_query(question):
    try:
        # Step 1: Generate SQL query
        sql_query = generate_sql_query(question)
        print(f"Generated SQL Query: {sql_query}")
        
        # Step 2: Execute the query and fetch results
        result_df = execute_query(sql_query)
        if result_df is None or result_df.empty:
            return {
                "text": "An error occurred while fetching data or no data was returned.",
                "chart_data": None
            }
        
        # Step 3: Convert Decimal values to floats and sort the data
        if 'totalsales' in result_df.columns:
            result_df['totalsales'] = result_df['totalsales'].astype(float)  # Convert Decimal to float
            result_df = result_df.sort_values(by='totalsales', ascending=False)  # Sort by sales in descending order
        
        # Step 4: Format the response text
        if 'state' in result_df.columns and 'totalsales' in result_df.columns:
            formatted_results = []
            for i, row in enumerate(result_df.itertuples(), start=1):
                formatted_results.append(f"{i}. {row.state:<12}: ${row.totalsales:,.2f}")
            response_text = "Top-performing states by sales:\n\n" + "\n".join(formatted_results)
        else:
            # Default response
            response_text = f"Query Result: {result_df.to_dict(orient='records')}"

        # Step 5: Check if visualization is possible
        visualization_possible = len(result_df.columns) >= 2
        chart_data = None
        if visualization_possible:
            x_column = result_df.columns[0]  # First column as X-axis (e.g., state)
            y_column = result_df.columns[1]  # Second column as Y-axis (e.g., totalsales)
            chart_data = create_visualization(result_df, x_column, y_column)
        
        # Step 6: Return the response
        return {
            "text": response_text,
            "chart_data": chart_data
        }
    except Exception as e:
        print(f"Error processing query: {e}")
        return {"error": str(e)}
