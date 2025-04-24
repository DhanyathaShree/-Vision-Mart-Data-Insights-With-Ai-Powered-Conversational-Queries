ABSTRACT

In this data-driven world, getting timely insights helps in fast and better decision-making to improve business. However, the large data, complex database structure and also the query languages make it hard and consume lots of time and feel like a barrier for the organisation’s growth and non-technical users to work on it. This project, titled “Vision Mart: Data Insights with AI-Powered Conversational Queries”, notices these problems and takes into account and develops an AI-driven chatbot which provides insights, visualisations when queries are in natural language instead of SQL queries, which might be complex and time-consuming. The system integrates LLM (Gemini 1.5 flash) with RAG to extract the relevant database query to retrieve whatever the user has entered in the frontend (React) as input in plain and basic English. The processed result is then displayed to the user in the frontend React interface, both as text and visualisation. The platform also supports a role-based login system, which helps in keeping the data secure and also adding additional data to it when admins want to add future data. 
Users with diverse backgrounds can interact with data through this AI-powered technology to analyse and get insights under this project.

Introduction
The exponential growth of data in recent years has transformed the world of digital information. So, people struggle to work with and get insights from the data manually. This is where AI came into the picture. In data-driven businesses, organisations need quick and actionable insights to improve their sales and profits. This rapid growth of technologies has created a way for innovations in artificial intelligence, leading to the evolution of machine learning models. In this group, large language models (LLMs) have been built to understand, generate and also manipulate human language. In the era of AI-powered chatbots, LLMs made it possible for human interactions with basic English and get results and insights even without knowing any programming languages.

1.1 Motivation Behind the Project
The main aim behind this project is to enable non-technical users to extract data from the sales database. Always, a data analyst is required to make business decisions that rely on accurate and timely data analysis. With the rise of natural language processing and LLMs, and empowers users to interact with data. It helps in linking the gaps to create an assistant that can understand English queries and return insights in both textual and visual ways. Inspired by the achievements of modern AI chatbots like ChatGPT, Deep seek, Claude, and Gemini, this project aims to create customised insights for any particular organisation for its data and growth.

1.2 Objective of the Study
This project is to build an interactive system that will accept basic English queries as input from the user, using RAG to convert the user queries into accurate SQL queries. And executing the query in the PostgreSQL backend, then generating the human-readable responses, displaying them in the frontend React and also providing data visualisations for the query results. This helps in reducing the dependency on analysts and technical skills for identifying data insights. It also improves speed, efficiency and accessibility of business intelligence.

1.3 Problem Statement
Organisations and users often find it hard to write complex SQL queries and extract meaningful information from the databases. Even tools such as Power BI, Tableau are more technical or take too much time for them to work on. And even sometimes users may not know the table structure, column names or even exact filters to be applied. From this, it is clear that there is a gap between how users ask for queries and how the SQL table is structured. This project brings up a solution that can translate natural language to accurate database queries, which gives us the relevant results for the business growth and achievements. 

1.4 Key Technologies Used
Gemini 1.5 Flask Large Language Models (LLM) – it is used to understand and convert the user input to SQL query.
Retrieval-Augmented Generation (RAG) – it helps LLMs to fetch the relevant details from the vector store and give result.
PostgreSQL – it stores the structured data, from which the result is generated for the user queries.
React.js – it is a frontend dynamic and interactive framework through with user communicated with the database to see results.
Chart Libraries (like Plotly, seaborn) – it is used for data visualization. 
Python Flask – it is a backend API used to handle communication between React and database.

