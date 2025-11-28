from flask import Flask, render_template, jsonify, request, redirect, url_for
import pandas as pd
import json
import os
from datetime import datetime
import numpy as np
import re
from textblob import TextBlob
import warnings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

warnings.filterwarnings('ignore')

# Simple stopwords list (fallback for NLTK)
SIMPLE_STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
    'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
    'further', 'then', 'once'
}

app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')

# Load blockchain data
def load_blockchain_data():
    data_file = os.getenv('DATA_FILE', 'combined_block.csv')
    try:
        if not os.path.exists(data_file):
            print(f"Warning: Data file '{data_file}' not found. Some features may not work.")
            return pd.DataFrame()
        df = pd.read_csv(data_file, delimiter=',', encoding='utf-8')
        df = df.dropna()
        df['block_timestamp'] = pd.to_datetime(df['block_timestamp'], unit='s')
        df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'], unit='s')
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

# Global variable to store data
blockchain_data = load_blockchain_data()

class AdvancedNLPProcessor:
    def __init__(self, df):
        self.df = df
        self.stop_words = SIMPLE_STOPWORDS
        self.setup_knowledge_base()
        
    def setup_knowledge_base(self):
        """Setup knowledge base for blockchain concepts"""
        self.knowledge_base = {
            'block': {
                'keywords': ['block', 'blocks', 'blockchain', 'chain'],
                'description': 'A block in a blockchain contains a collection of transactions that have been validated and recorded.',
                'attributes': ['index', 'timestamp', 'hash', 'nonce', 'previous_hash']
            },
            'transaction': {
                'keywords': ['transaction', 'transactions', 'tx', 'transfer', 'send', 'receive'],
                'description': 'A transaction represents the transfer of value or data between parties in the blockchain.',
                'attributes': ['sender', 'receiver', 'amount', 'transaction_id', 'timestamp']
            },
            'amount': {
                'keywords': ['amount', 'value', 'money', 'cost', 'price', 'sum', 'total'],
                'description': 'The amount represents the value being transferred in a transaction.',
                'attributes': ['amount']
            },
            'sender': {
                'keywords': ['sender', 'from', 'source', 'originator'],
                'description': 'The sender is the party initiating the transfer of value or data.',
                'attributes': ['sender']
            },
            'receiver': {
                'keywords': ['receiver', 'to', 'destination', 'recipient'],
                'description': 'The receiver is the party that receives the value or data.',
                'attributes': ['receiver']
            },
            'hash': {
                'keywords': ['hash', 'hash_value', 'block_hash', 'transaction_hash'],
                'description': 'A hash is a fixed-length string that uniquely represents the data in a block.',
                'attributes': ['hash']
            },
            'nonce': {
                'keywords': ['nonce', 'number', 'counter'],
                'description': 'A nonce is a number used once in cryptographic communications to ensure uniqueness.',
                'attributes': ['nonce']
            }
        }
        
        # Simple keyword matching (no TF-IDF for now)
        pass
    
    def extract_entities(self, query):
        """Extract entities from the query"""
        entities = {
            'block_number': None,
            'concept': None,
            'attribute': None,
            'intent': None
        }
        
        # Extract block number
        block_match = re.search(r'block\s+(\d+)', query.lower())
        if block_match:
            entities['block_number'] = int(block_match.group(1))
        
        # Extract concept and intent
        query_lower = query.lower()
        
        # Check for intents
        if any(word in query_lower for word in ['what', 'tell', 'show', 'explain', 'describe']):
            entities['intent'] = 'explain'
        elif any(word in query_lower for word in ['who', 'which', 'where']):
            entities['intent'] = 'identify'
        elif any(word in query_lower for word in ['how', 'why']):
            entities['intent'] = 'explain'
        else:
            entities['intent'] = 'query'
        
        # Find matching concept
        best_match = None
        best_score = 0
        
        for concept, data in self.knowledge_base.items():
            for keyword in data['keywords']:
                if keyword in query_lower:
                    score = len(keyword) / len(query)
                    if score > best_score:
                        best_score = score
                        best_match = concept
        
        entities['concept'] = best_match
        
        # Extract specific attribute
        for concept, data in self.knowledge_base.items():
            if entities['concept'] == concept:
                for attr in data['attributes']:
                    if attr in query_lower:
                        entities['attribute'] = attr
                        break
        
        return entities
    
    def process_query(self, query):
        """Process the query using advanced NLP"""
        entities = self.extract_entities(query)
        
        # Handle block-specific queries
        if entities['block_number'] is not None:
            return self.handle_block_query(entities, query)
        
        # Handle general concept queries
        if entities['concept']:
            return self.handle_concept_query(entities, query)
        
        # Handle general blockchain questions
        return self.handle_general_query(query)
    
    def handle_block_query(self, entities, query):
        """Handle queries about specific blocks"""
        block_num = entities['block_number']
        block_data = self.df[self.df['index'] == block_num]
        
        if block_data.empty:
            return {
                'type': 'error',
                'response': f"No data found for block {block_num}",
                'suggestions': self.get_suggestions()
            }
        
        if entities['attribute']:
            # Specific attribute query
            if entities['attribute'] in block_data.columns:
                value = block_data[entities['attribute']].iloc[0]
                return {
                    'type': 'block_data',
                    'response': f"The {entities['attribute']} of block {block_num} is {value}",
                    'data': block_data.to_dict('records'),
                    'highlight': entities['attribute']
                }
            else:
                return {
                    'type': 'error',
                    'response': f"Attribute '{entities['attribute']}' not found in block data"
                }
        else:
            # General block information
            return {
                'type': 'block_data',
                'response': f"Here's the information for block {block_num}:",
                'data': block_data.to_dict('records'),
                'summary': self.get_block_summary(block_data)
            }
    
    def handle_concept_query(self, entities, query):
        """Handle queries about blockchain concepts"""
        concept = entities['concept']
        concept_data = self.knowledge_base[concept]
        
        response = {
            'type': 'concept_explanation',
            'concept': concept,
            'description': concept_data['description'],
            'attributes': concept_data['attributes'],
            'examples': self.get_concept_examples(concept)
        }
        
        return response
    
    def handle_general_query(self, query):
        """Handle general blockchain queries"""
        # Use sentiment analysis
        blob = TextBlob(query)
        sentiment = blob.sentiment.polarity
        
        # Simple keyword matching for common questions
        if any(word in query.lower() for word in ['hello', 'hi', 'hey', 'greetings']):
            return {
                'type': 'greeting',
                'response': "Hello! Welcome to Chain Explorer. I can help you analyze your blockchain data. Try asking about specific blocks, transactions, or blockchain concepts.",
                'suggestions': self.get_suggestions()
            }
        
        return {
            'type': 'general',
            'response': "I can help you with blockchain data analysis. Try asking about specific blocks, transactions, or concepts like 'hash', 'nonce', or 'transaction'.",
            'suggestions': self.get_suggestions()
        }
    
    def get_block_summary(self, block_data):
        """Get a summary of block data"""
        if block_data.empty:
            return "No data available"
        
        summary = {
            'transaction_count': len(block_data),
            'total_amount': block_data['amount'].sum(),
            'unique_senders': block_data['sender'].nunique(),
            'unique_receivers': block_data['receiver'].nunique()
        }
        return summary
    
    def get_concept_examples(self, concept):
        """Get examples for a concept"""
        examples = {
            'block': ["What is in block 5?", "Show me block 10", "Tell me about block 3"],
            'transaction': ["Show me transactions", "What are the recent transactions?", "List all transactions"],
            'amount': ["What is the amount in block 1?", "Show me the total amount", "What's the highest amount?"],
            'sender': ["Who is the sender of block 2?", "Show me all senders", "List unique senders"],
            'receiver': ["Who is the receiver of block 3?", "Show me all receivers", "List unique receivers"],
            'hash': ["What is the hash of block 1?", "Show me block hashes", "Explain hash values"],
            'nonce': ["What is the nonce of block 2?", "Show me nonce values", "Explain nonce"]
        }
        return examples.get(concept, [])
    
    def get_suggestions(self):
        """Get query suggestions"""
        return [
            "What is in block 1?",
            "Who is the sender of block 2?",
            "What is the total amount?",
            "Explain what a hash is",
            "Show me recent transactions",
            "What is the nonce of block 3?"
        ]

# Initialize NLP processor
nlp_processor = AdvancedNLPProcessor(blockchain_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/transactions')
def transactions():
    return render_template('transactions.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')

@app.route('/query')
def query():
    return render_template('query.html')

@app.route('/api/stats')
def get_stats():
    if blockchain_data.empty:
        return jsonify({"error": "No data available"})
    
    stats = {
        'total_blocks': int(blockchain_data['index'].nunique()),
        'total_transactions': int(len(blockchain_data)),
        'unique_senders': int(blockchain_data['sender'].nunique()),
        'unique_receivers': int(blockchain_data['receiver'].nunique()),
        'total_volume': float(blockchain_data['amount'].sum()),
        'average_transaction': float(blockchain_data['amount'].mean()),
        'max_transaction': float(blockchain_data['amount'].max()),
        'min_transaction': float(blockchain_data['amount'].min())
    }
    return jsonify(stats)

@app.route('/api/transactions')
def get_transactions():
    if blockchain_data.empty:
        return jsonify({"error": "No data available"})
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Calculate pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    # Get transactions for current page
    transactions = blockchain_data.iloc[start_idx:end_idx].to_dict('records')
    
    # Convert datetime objects to strings for JSON serialization
    for transaction in transactions:
        if 'block_timestamp' in transaction:
            transaction['block_timestamp'] = transaction['block_timestamp'].isoformat()
        if 'transaction_timestamp' in transaction:
            transaction['transaction_timestamp'] = transaction['transaction_timestamp'].isoformat()
    
    return jsonify({
        'transactions': transactions,
        'total': len(blockchain_data),
        'page': page,
        'per_page': per_page,
        'total_pages': (len(blockchain_data) + per_page - 1) // per_page
    })

@app.route('/api/analytics/volume-over-time')
def get_volume_over_time():
    if blockchain_data.empty:
        return jsonify({"error": "No data available"})
    
    # Group by date and sum amounts
    daily_volume = blockchain_data.groupby(blockchain_data['transaction_timestamp'].dt.date)['amount'].sum().reset_index()
    
    return jsonify({
        'dates': [str(date) for date in daily_volume['transaction_timestamp']],
        'volumes': daily_volume['amount'].tolist()
    })

@app.route('/api/analytics/top-senders')
def get_top_senders():
    if blockchain_data.empty:
        return jsonify({"error": "No data available"})
    
    top_senders = blockchain_data.groupby('sender')['amount'].sum().sort_values(ascending=False).head(10)
    
    return jsonify({
        'senders': top_senders.index.tolist(),
        'amounts': top_senders.values.tolist()
    })

@app.route('/api/analytics/top-receivers')
def get_top_receivers():
    if blockchain_data.empty:
        return jsonify({"error": "No data available"})
    
    top_receivers = blockchain_data.groupby('receiver')['amount'].sum().sort_values(ascending=False).head(10)
    
    return jsonify({
        'receivers': top_receivers.index.tolist(),
        'amounts': top_receivers.values.tolist()
    })

@app.route('/api/analytics/block-distribution')
def get_block_distribution():
    if blockchain_data.empty:
        return jsonify({"error": "No data available"})
    
    # Get transaction count per block
    block_counts = blockchain_data['index'].value_counts().sort_index()
    
    return jsonify({
        'blocks': block_counts.index.tolist(),
        'transaction_counts': block_counts.values.tolist()
    })

@app.route('/api/query')
def query_data():
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({"error": "No query provided"})
    
    try:
        # Use advanced NLP processing
        result = nlp_processor.process_query(query)
        
        # Convert datetime objects to strings for JSON serialization
        if 'data' in result and isinstance(result['data'], list):
            for item in result['data']:
                for key, value in item.items():
                    if hasattr(value, 'isoformat'):
                        item[key] = value.isoformat()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'type': 'error',
            'response': f"Error processing query: {str(e)}",
            'suggestions': nlp_processor.get_suggestions()
        })

@app.route('/api/analytics/transaction-timeline')
def get_transaction_timeline():
    if blockchain_data.empty:
        return jsonify({"error": "No data available"})
    
    # Get transaction timeline data
    timeline_data = blockchain_data.groupby(blockchain_data['transaction_timestamp'].dt.hour).size().reset_index()
    timeline_data.columns = ['hour', 'count']
    
    return jsonify({
        'hours': timeline_data['hour'].tolist(),
        'counts': timeline_data['count'].tolist()
    })

@app.route('/api/analytics/network-stats')
def get_network_stats():
    if blockchain_data.empty:
        return jsonify({"error": "No data available"})
    
    # Calculate network statistics
    unique_addresses = set(blockchain_data['sender'].unique()) | set(blockchain_data['receiver'].unique())
    
    # Calculate transaction patterns
    sender_counts = blockchain_data['sender'].value_counts()
    receiver_counts = blockchain_data['receiver'].value_counts()
    
    return jsonify({
        'total_unique_addresses': len(unique_addresses),
        'most_active_sender': sender_counts.index[0] if not sender_counts.empty else None,
        'most_active_receiver': receiver_counts.index[0] if not receiver_counts.empty else None,
        'sender_transaction_count': int(sender_counts.iloc[0]) if not sender_counts.empty else 0,
        'receiver_transaction_count': int(receiver_counts.iloc[0]) if not receiver_counts.empty else 0
    })

@app.route('/health')
def health():
    """Health check endpoint for Render monitoring"""
    return jsonify({
        "status": "healthy",
        "data_loaded": not blockchain_data.empty,
        "data_rows": len(blockchain_data) if not blockchain_data.empty else 0
    }), 200

if __name__ == '__main__':
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = app.config['DEBUG']
    
    app.run(debug=debug, host=host, port=port)
