from flask import jsonify, request
from models import db, User, ParkingLot, ParkingSpot, Reservation
from auth import (
    token_required, admin_required, user_required,
    generate_token
)
from cache import (
    cache_get, cache_set, cache_delete,
    cache_clear_pattern, cache_key
)
from datetime import datetime
import sqlite3
import os
import csv
import io
from flask import send_file, jsonify, Response

def register_routes(app):
    # =========================================
    # ========== AUTH ROUTES ==================
    # =========================================

    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json()
        
        required = ['username', 'email', 'phone_number', 'password', 'address', 'pincode']
        if not data or not all(k in data for k in required):
            return jsonify({'message': 'Missing required fields'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Username already exists'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email already exists'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            phone_number=data['phone_number'],
            address=data['address'],
            pincode=data['pincode'],
            role='user'
        )
        user.set_password(data['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
            token = generate_token(user.id, user.username, user.role)
            return jsonify({
                'message': 'User registered successfully',
                'token': token,
                'user': user.to_dict(),
                'redirect': '/user/dashboard'
            }), 201
        except:
            db.session.rollback()
            return jsonify({'message': 'Registration failed '}), 500

    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({'message': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid username or password'}), 401
        
        token = generate_token(user.id, user.username, user.role)
        redirect_url = '/admin/dashboard' if user.role == 'admin' else '/user/dashboard'
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict(),
            'redirect': redirect_url
        }), 200

    @app.route('/auth/admin-login', methods=['POST'])
    def admin_login():
        data = request.get_json()
        
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({'message': 'Missing username or password'}), 400
        
        user = User.query.filter_by(username=data['username'], role='admin').first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'message': 'Invalid admin credentials'}), 401
        
        token = generate_token(user.id, user.username, user.role)
        return jsonify({
            'message': 'Admin login successful',
            'token': token,
            'user': user.to_dict(),
            'redirect': '/admin/dashboard'
        }), 200

    @app.route('/auth/logout', methods=['POST'])
    @token_required
    def logout():
        return jsonify({'message': 'Logged out successfully', 'redirect': '/'}), 200

    # ====================================================================
    # ===================== ADMIN ROUTES ================================
    # ====================================================================

    @app.route('/admin/dashboard')
    @token_required
    @admin_required
    def admin_dashboard():
        try:
            users_count = User.query.filter_by(role='user').count()
            lots_count = ParkingLot.query.count()
            spots_count = ParkingSpot.query.count()
            available = ParkingSpot.query.filter_by(status='A').count()
            occupied = ParkingSpot.query.filter_by(status='O').count()
            reservations_count = Reservation.query.count()
            
            try:
                recent = User.query.filter_by(role='user').order_by(User.created_at.desc()).limit(5).all()
            except:
                recent = User.query.filter_by(role='user').limit(5).all()
            
            lots = ParkingLot.query.all()
            lots_info = []
            for lot in lots:
                free = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
                lots_info.append({
                    'id': lot.id,
                    'prime_location_name': lot.prime_location_name,
                    'address': lot.address,
                    'pin_code': lot.pin_code,
                    'price_per_hour': lot.price_per_hour,
                    'number_of_spots': lot.number_of_spots,
                    'available_spots': free,
                    'utilization': round((lot.number_of_spots - free) / lot.number_of_spots * 100, 2) if lot.number_of_spots > 0 else 0
                })
            
            response_data = {
                'message': 'Admin Dashboard',
                'statistics': {
                    'total_users': users_count,
                    'total_lots': lots_count,
                    'total_spots': spots_count,
                    'available_spots': available,
                    'occupied_spots': occupied,
                    'total_reservations': reservations_count
                },
                'recent_users': [user.to_dict() for user in recent],
                'parking_lots': lots_info
            }
            
            return jsonify(response_data), 200
        except Exception as e:
            return jsonify({'error': 'Failed to load admin dashboard', 'message': str(e)}), 500

    @app.route('/api/admin/lots', methods=['POST'])
    @token_required 
    @admin_required
    def create_lot():
        data = request.get_json()
        lot = ParkingLot(
            prime_location_name=data['prime_location_name'],
            address=data['address'],
            pin_code=data['pin_code'],
            price_per_hour=data['price_per_hour'],
            number_of_spots=data['number_of_spots']
        )
        db.session.add(lot)
        db.session.commit()
        
        for i in range(1, lot.number_of_spots + 1):
            spot = ParkingSpot(lot_id=lot.id, spot_number=f"A{i}", status='A')
            db.session.add(spot)
        db.session.commit()
        
        return jsonify({'message': 'Lot created', 'lot_id': lot.id}), 201

    @app.route('/api/admin/lots/<int:lot_id>', methods=['PUT'])
    @token_required
    @admin_required
    def edit_lot(lot_id):
        lot = ParkingLot.query.get_or_404(lot_id)
        data = request.get_json()
        old_total = lot.number_of_spots
        
        lot.prime_location_name = data.get('prime_location_name', lot.prime_location_name)
        lot.address = data.get('address', lot.address)
        lot.pin_code = data.get('pin_code', lot.pin_code)
        lot.price_per_hour = data.get('price_per_hour', lot.price_per_hour)
        new_total = data.get('number_of_spots', old_total)
        if new_total > old_total:
            for i in range(old_total + 1, new_total + 1):
                spot = ParkingSpot(lot_id=lot.id, spot_number=f"A{i}", status='A')
                db.session.add(spot)
        elif new_total < old_total:
            occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
            if occupied > new_total:
                return jsonify({'message': 'Cannot reduce spots below occupied count'}), 400
            extra_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').order_by(ParkingSpot.id.desc()).limit(old_total - new_total).all()
            for spot in extra_spots:
                db.session.delete(spot)
        lot.number_of_spots = new_total
        db.session.commit()
        
        return jsonify({'message': 'Lot updated'}), 200

    @app.route('/api/admin/lots/<int:lot_id>', methods=['DELETE'])
    @token_required
    @admin_required
    def delete_lot(lot_id):
        lot = ParkingLot.query.get_or_404(lot_id)
        occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
        if occupied > 0:
            return jsonify({'message': 'Cannot delete lot with occupied spots'}), 400
        ParkingSpot.query.filter_by(lot_id=lot.id).delete()
        db.session.delete(lot)
        db.session.commit()
        
        return jsonify({'message': 'Lot deleted'}), 200

    @app.route('/api/admin/lots', methods=['GET'])
    @token_required
    @admin_required
    def admin_list_lots():
        lots = ParkingLot.query.all()
        result = []
        for lot in lots:
            total = ParkingSpot.query.filter_by(lot_id=lot.id).count()
            available = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
            occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
            result.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price_per_hour': lot.price_per_hour,
                'number_of_spots': lot.number_of_spots,
                'available_spots': available,
                'occupied_spots': occupied
            })
        return jsonify(result), 200

    @app.route('/api/admin/lots/<int:lot_id>', methods=['GET'])
    @token_required
    @admin_required
    def lot_details(lot_id):
        lot = ParkingLot.query.get_or_404(lot_id)
        spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        spot_list = []
        for spot in spots:
            spot_list.append({
                'id': spot.id,
                'spot_number': spot.spot_number,
                'status': spot.status
            })
        return jsonify({
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'price_per_hour': lot.price_per_hour,
            'number_of_spots': lot.number_of_spots,
            'spots': spot_list
        }), 200

    @app.route('/api/admin/lots/<int:lot_id>/spots', methods=['GET'])
    @token_required
    @admin_required
    def admin_list_spots(lot_id):
        spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
        result = []
        for spot in spots:
            result.append({
                'id': spot.id,
                'spot_number': spot.spot_number,
                'status': spot.status
            })
        return jsonify(result), 200

    @app.route('/api/admin/users', methods=['GET'])
    @token_required
    @admin_required
    def admin_list_users():
        users = User.query.filter(User.role == 'user').all()
        result = []
        for user in users:
            reservation = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.id.desc()).first()
            spot = None
            if reservation and reservation.leaving_timestamp is None:
                spot = reservation.spot_id
            result.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'current_spot': spot,
                'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None
            })
        return jsonify(result), 200

    @app.route('/api/admin/search', methods=['GET'])
    @token_required
    @admin_required
    def admin_search():
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'all')  
        
        if not query:
            return jsonify({'message': 'Search query is required'}), 400
        
        results = {
            'lots': [],
            'users': [],
            'spots': []
        }
        
        query_lower = query.lower()
        
        if search_type in ['all', 'lots']:
            lots = ParkingLot.query.all()
            for lot in lots:
                if (lot.prime_location_name and query_lower in lot.prime_location_name.lower()) or \
                   (lot.address and query_lower in lot.address.lower()) or \
                   (lot.pin_code and query in lot.pin_code):
                    
                    total = ParkingSpot.query.filter_by(lot_id=lot.id).count()
                    available = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
                    occupied = ParkingSpot.query.filter_by(lot_id=lot.id, status='O').count()
                    
                    results['lots'].append({
                        'id': lot.id,
                        'prime_location_name': lot.prime_location_name,
                        'address': lot.address,
                        'pin_code': lot.pin_code,
                        'price_per_hour': lot.price_per_hour,
                        'number_of_spots': lot.number_of_spots,
                        'available_spots': available,
                        'occupied_spots': occupied
                    })
        
        if search_type in ['all', 'users']:
            users = User.query.filter(User.role == 'user').all()
            for user in users:
                if query_lower in user.username.lower() or \
                   query_lower in user.email.lower() or \
                   query in str(user.id):
                    
                    reservation = Reservation.query.filter_by(user_id=user.id).order_by(Reservation.id.desc()).first()
                    spot = None
                    if reservation and reservation.leaving_timestamp is None:
                        spot = reservation.spot_id
                    
                    results['users'].append({
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'current_spot': spot,
                        'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else None
                    })
        
        if search_type in ['all', 'spots']:
            spots = ParkingSpot.query.all()
            for spot in spots:
                if query_lower in spot.spot_number.lower() or query in str(spot.id):
                    lot = db.session.get(ParkingLot, spot.lot_id)
                    results['spots'].append({
                        'id': spot.id,
                        'spot_number': spot.spot_number,
                        'status': spot.status,
                        'lot_id': spot.lot_id,
                        'lot_name': lot.prime_location_name if lot else 'Unknown'
                    })
        
        return jsonify(results), 200
    @app.route('/api/admin/total-revenue', methods=['GET'])
    @token_required
    @admin_required
    def total_revenue():
        try:
            # Base backend folder
            # Use SQLAlchemy aggregation
            total = db.session.query(db.func.sum(Reservation.parking_cost)).scalar()

            # If no rows, total will be None
            total = total or 0

            return jsonify({"total_revenue": total}), 200


        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @app.route('/api/admin/export-csv', methods=['GET'])
    @token_required
    @admin_required
    def export_csv():
    
    
        try:
            # Database path
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            db_path = os.path.join(project_root, 'instance', 'parking.db')
            if not os.path.exists(db_path):
                pass
            
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Query data
            cursor.execute("""
                SELECT 
                    r.id,
                    u.username,
                    u.email,
                    pl.prime_location_name,
                    pl.address,
                    ps.spot_number,
                    r.parking_timestamp,
                    r.leaving_timestamp,
                    r.parking_cost
                FROM reservation r
                JOIN user u ON r.user_id = u.id
                JOIN parking_spot ps ON r.spot_id = ps.id
                JOIN parking_lot pl ON ps.lot_id = pl.id
                ORDER BY r.parking_timestamp DESC
            """)

            rows = cursor.fetchall()
            conn.close()

            # Create CSV in memory
            output = io.StringIO()
            writer = csv.writer(output)

            writer.writerow([
                'Reservation ID',
                'Username',
                'Email',
                'Parking Lot',
                'Address',
                'Spot Number',
                'Parking Time',
                'Leaving Time',
                'Cost'
            ])

            for row in rows:
                writer.writerow(row)

            output.seek(0)

            # Force download response
            return Response(
                output.getvalue(),
                mimetype="text/csv",
                headers={
                    "Content-Disposition": "attachment; filename=parking_report.csv"
                }
            )

        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        
    # ================================================================
    # =================== API ROUTES (Public/Users) ==================
    # ================================================================

    @app.route('/api/lots')
    @token_required
    def get_lots():
        key_name = cache_key("api", "lots")
        cached = cache_get(key_name)
        if cached:
            return jsonify(cached), 200
        
        lots = ParkingLot.query.all()
        res = []
        for lot in lots:
            free = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
            res.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price_per_hour': lot.price_per_hour,
                'number_of_spots': lot.number_of_spots,
                'available_spots': free
            })
        
        cache_set(key_name, res, 60)
        return jsonify(res), 200

    @app.route('/api/spots')
    @token_required
    def get_spots():
        key_name = cache_key("api", "spots")
        cached = cache_get(key_name)
        if cached:
            return jsonify(cached), 200
        
        spots = ParkingSpot.query.join(ParkingLot).all()
        res = []
        for spot in spots:
            lot = db.session.get(ParkingLot, spot.lot_id)
            res.append({
                'id': spot.id,
                'lot_id': spot.lot_id,
                'spot_number': spot.spot_number,
                'status': spot.status,
                'lot_name': lot.prime_location_name if lot else 'Unknown',
                'lot_address': lot.address if lot else 'Unknown'
            })
        
        cache_set(key_name, res, 30)
        return jsonify(res), 200

    @app.route('/api/reserve', methods=['POST'])
    @token_required
    @user_required
    def reserve_spot():
        data = request.get_json()
        lot_id = data.get('lot_id')
        if not lot_id:
            return jsonify({'message': 'Missing lot_id'}), 400
        
        active_res = Reservation.query.filter_by(user_id=request.user_id, leaving_timestamp=None).first()
        if active_res:
            return jsonify({'message': 'You already have an active reservation'}), 400
        
        spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='A').first()
        if not spot:
            return jsonify({'message': 'No available spots'}), 400
        
        reservation = Reservation(
            user_id=request.user_id,
            spot_id=spot.id,
            parking_timestamp=datetime.utcnow()
        )
        spot.status = 'O'
        
        db.session.add(reservation)
        db.session.commit()
        
        cache_clear_pattern("api:spots*")
        cache_clear_pattern("api:lots*")
        
        return jsonify({
            'message': 'Spot reserved',
            'reservation': {
                'id': reservation.id,
                'spot_id': reservation.spot_id,
                'spot_number': spot.spot_number,
                'parking_timestamp': reservation.parking_timestamp.isoformat(),
                'parking_cost': reservation.parking_cost
            }
        }), 201

    @app.route('/api/release', methods=['POST'])
    @token_required
    @user_required
    def release_spot():
        data = request.get_json()
        reservation_id = data.get('reservation_id')

        res = Reservation.query.filter_by(
            id=reservation_id,
            user_id=request.user_id,
            leaving_timestamp=None
        ).first()

        if not res:
            return jsonify({'message': 'Active reservation not found'}), 404
        
        res.leaving_timestamp = datetime.utcnow()
        spot = db.session.get(ParkingSpot, res.spot_id)
        lot = db.session.get(ParkingLot, spot.lot_id)

        hours = (res.leaving_timestamp - res.parking_timestamp).total_seconds() / 3600
        if hours < 1:
            hours = 1

        cost = round(hours * lot.price_per_hour, 2)
        res.parking_cost = cost
        spot.status = 'A'

        db.session.commit()

        cache_clear_pattern("api:spots*")
        cache_clear_pattern("api:lots*")

        return jsonify({
            'message': 'Spot released',
            'parking_cost': cost,
            'duration_hours': round(hours, 2)
        }), 200

    # ====================================================================
    # ======================== USER ROUTES ===============================
    # ====================================================================

    @app.route('/user/dashboard')
    @token_required
    @user_required
    def user_dashboard():
        reservations = Reservation.query.filter_by(
            user_id=request.user_id
        ).order_by(Reservation.parking_timestamp.desc()).limit(5).all()

        lots = ParkingLot.query.all()
        lots_info = []
        for lot in lots:
            free = ParkingSpot.query.filter_by(lot_id=lot.id, status='A').count()
            lots_info.append({
                'id': lot.id,
                'prime_location_name': lot.prime_location_name,
                'address': lot.address,
                'pin_code': lot.pin_code,
                'price_per_hour': lot.price_per_hour,
                'available_spots': free
            })

        user = db.session.get(User, request.user_id)

        return jsonify({
            'message': 'User Dashboard',
            'user': user.to_dict(),
            'my_reservations': [
                {
                    'id': r.id,
                    'spot_id': r.spot_id,
                    'parking_timestamp': r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                    'leaving_timestamp': r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                    'parking_cost': r.parking_cost
                }
                for r in reservations
            ],
            'available_parking_lots': lots_info
        }), 200

    @app.route('/api/user/profile')
    @token_required
    @user_required
    def get_user_profile():
        user = db.session.get(User, request.user_id)
        return jsonify({'user': user.to_dict()}), 200

    @app.route('/api/user/reservations')
    @token_required
    @user_required
    def get_user_reservations():
        reservations = Reservation.query.filter_by(
            user_id=request.user_id
        ).order_by(Reservation.parking_timestamp.desc()).all()

        return jsonify({
            'reservations': [
                {
                    'id': r.id,
                    'spot_id': r.spot_id,
                    'parking_timestamp': r.parking_timestamp.isoformat() if r.parking_timestamp else None,
                    'leaving_timestamp': r.leaving_timestamp.isoformat() if r.leaving_timestamp else None,
                    'parking_cost': r.parking_cost,
                    'status': 'active' if not r.leaving_timestamp else 'completed'
                }
                for r in reservations
            ]
        }), 200
