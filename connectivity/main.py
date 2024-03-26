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
        logging.debug(query)
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

@app.route('/api/insert/products', methods=['POST'])
def insert_product():
    try:
        params = config()
        connection = psycopg2.connect(**params)
        crsr = connection.cursor()

        # Extract data from request body
        data = request.json  
        # Construct SQL INSERT query
        query = "INSERT INTO inventory (productID, category, sub_category, stock) VALUES (%s, %s, %s, %d)"
        values = (data['productID'], data['category'], data['subCategory'], int(data['stock']))
        logging.debug(values)
        # Execute SQL query
        crsr.execute(query, (values))
        connection.commit()

        crsr.close()
        connection.close()
        # Return success message
        return jsonify({'message': 'Product inserted successfully'}), 200
    except psycopg2.Error as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}),500

@app.route('/api/delete/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        # Establish a connection to the database
        params = config()
        connection = psycopg2.connect(**params)
        cursor = connection.cursor()

        # Construct the SQL query to delete the product
        query = "DELETE FROM inventory WHERE productID = %s"
        
        cursor.execute(query, (product_id,))
        connection.commit()

        # Close cursor and connection
        cursor.close()
        connection.close()

        # Return a success message
        return jsonify({'message': f'Product with ID {product_id} deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}),500
                        
if __name__ == "__main__":
    app.run(debug=True)