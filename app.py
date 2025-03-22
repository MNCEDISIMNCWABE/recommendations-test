from azure.cosmos import CosmosClient
from flask import Flask, jsonify, request

app = Flask(__name__)

# Azure Cosmos DB credentials
COSMOS_ENDPOINT = "https://recom-db.documents.azure.com:443/"
COSMOS_KEY = "Y9FIGJ90wnP2awKPqhcGmHTxGF1TLJTsj6KdWC1rdajGXSfQkyaBD50V3gl554Dk0B7N7ZsiCdmKACDbXK8Ngw==" 
DATABASE_NAME = "recommendations_db"
CONTAINER_NAME = "recommendations_activity_games"

# Initialize Cosmos DB client
client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    user_id = request.args.get("user_id")
    
    if not user_id:
        return jsonify({"error": "user_id parameter is required"}), 400
    
    # Use a parameterized query to avoid security risks
    query = "SELECT c.recommendations FROM c WHERE c.id = @user_id"
    query_params = [{"name": "@user_id", "value": str(user_id)}]
    
    results = list(container.query_items(query=query, parameters=query_params, enable_cross_partition_query=True))
    
    if not results:
        return jsonify({"message": "No recommendations found"}), 404
    
    # Extract recommendations from the first result
    recommendations = results[0].get("recommendations", [])
    
    return jsonify(recommendations), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
