from flask import Flask, request, jsonify, send_file
import psycopg2
from config import config
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')
@app.route('/api/mydata', methods=['GET'])
def get_data():
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        #get query parameters from the request
        columns = request.args.get('columns')
        criteria_column = request.args.get('criteriaColumn')
        criteria_constraint = request.args.get('criteriaConstraint')
        table = request.args.get('table')
        logging.debug("request.args is %s", request.args)
        
        criteria_query = ""
        if criteria_column and criteria_constraint:
            criteria_query = f" WHERE {criteria_column} = %s"

        query = f"SELECT {columns} FROM {table}" + criteria_query

        # Use a prepared statement with placeholder for criteria_constraint
        print(query)
        crsr.execute(query, (criteria_constraint,))

        # Fetch all rows
        data = crsr.fetchall()
        crsr.close()
        connection.close()
        #convert the fetched data to JSON format and return as response
        return jsonify(data)
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}),500
    except Exception as e:
        return jsonify({'error': str(e)}),500
if __name__ == "__main__":
    app.run(debug=True)