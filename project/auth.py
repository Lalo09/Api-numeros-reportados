from os import access
from turtle import pd
from flask import Blueprint,request,jsonify
from sqlalchemy import Identity
from werkzeug.security import check_password_hash, generate_password_hash
from project.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_409_CONFLICT
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token,create_refresh_token

from project.database import User,db
from flask_jwt_extended import JWTManager
from flasgger import swag_from

auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post('/register')
def register():
    username=request.json['username']
    email=request.json['email']
    password=request.json['password']

    if len(password)<5:
        return jsonify({
            "error":"password is too short"
        }),HTTP_400_BAD_REQUEST
    
    if len(username)<3:
        return jsonify({
            "error":"User is too short"
        }),HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or " " in username:
        return jsonify({
            "error":"Username should be alphanumeric"
        }),HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({
            "error":"Invalid email"
        }),HTTP_409_CONFLICT

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            "error":"Email is already taken "
        }),HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            "error":"Username is already taken "
        }),HTTP_409_CONFLICT

    pwd_hash = generate_password_hash(password)

    user=User(username=username,password=pwd_hash,email=email)
    #user=User(username=username,password=password,email=email)


    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message':'User created',
        'user':{
            'username':username,
            'email':email
        }
    }),HTTP_201_CREATED

@auth.post('/login')
@swag_from('./docs/auth/login.yaml')
def login():
    email = request.json.get('email','')
    password = request.json.get('password','')

    user=User.query.filter_by(email=email).first()

    if user:
        is_password_correct = check_password_hash(user.password,password) #Comparing hashes

        if is_password_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user':{
                    'refresh':refresh,
                    'access':access,
                    'username':user.username,
                    'email':user.email
                }
            }),HTTP_200_OK
    
    return jsonify({
        'error':'Wrong credentials'
    }),HTTP_401_UNAUTHORIZED


@auth.get('/me')
@jwt_required()
def me():
    user_id=get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()


    return jsonify({
        'username':user.username,
        'email':user.email
    }), HTTP_200_OK

@auth.get('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identity= get_jwt_identity()
    access=create_access_token(identity=identity)

    return jsonify({
        'access':access
    }),HTTP_200_OK