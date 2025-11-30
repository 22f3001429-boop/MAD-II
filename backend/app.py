from flask import Flask, jsonify
from config import Config
from models import db, User, ParkingLot, ParkingSpot
from flask_cors import CORS
from tasks import send_email_task, send_reservation_confirmation, send_welcome_email
from datetime import datetime
from models import Reservation
from routes.routes import register_routes
import random

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8080"], 
     allow_headers=["Content-Type", "Authorization"], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])




db.init_app(app)

@app.route('/')
def home():
    return "App"















@app.route('/test-summary')
def test_summary():
    
    users_count = User.query.filter_by(role='user').count()
    lots_count = ParkingLot.query.count()
    spots_count = ParkingSpot.query.count()
    available = ParkingSpot.query.filter_by(status='A').count()
    occupied = ParkingSpot.query.filter_by(status='O').count()
    reservations_count = Reservation.query.count()
    
    return jsonify({
        'message': 'Test Summary Data',
        'statistics': {
            'total_users': users_count,
            'total_lots': lots_count,
            'total_spots': spots_count,
            'available_spots': available,
            'occupied_spots': occupied,
            'total_reservations': reservations_count
        }
    })




register_routes(app)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()    
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', phone_number='9999999999', address='Admin Office', pincode='000000', role='admin')
            admin.set_password('admin123')
    
            
            db.session.add(admin)
            db.session.commit()    
    
    
       
        
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    