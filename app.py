from flask import Flask, request, jsonify, send_file
import psycopg2
from config import config
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

@app.route('/')
def index():
    return send_file('index.html')
@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        #get query parameters from the request
        columns = request.args.get('columns')
        criteria_column = request.args.get('criteriaColumn')
        criteria_constraint = request.args.get('criteriaConstraint')
        logging.debug("request.args is %s", request.args)
        logging.debug("criteria constraint is %s", criteria_constraint)
        logging.debug("criteria column is %s:", criteria_column)
        
        criteria_query = ""
        if criteria_column and criteria_constraint:
            criteria_query = f" WHERE {criteria_column} = %s"

        query = f"SELECT {columns} FROM inventory" + criteria_query

        # Use a prepared statement with placeholder for criteria_constraint
        crsr.execute(query, (criteria_constraint,))

        # Fetch all rows
        products = crsr.fetchall()
        crsr.close()
        connection.close()
        #convert the fetched data to JSON format and return as response
        return jsonify(products)
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}),500
    except Exception as e:
        return jsonify({'error': str(e)}),500
if __name__ == "__main__":
    app.run(debug=True)