import json
from flask import Blueprint, jsonify,request
import validators
from flask_jwt_extended import current_user, get_jwt_identity, jwt_required
from project.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from project.database import Number,db

numbers = Blueprint("numbers",__name__,url_prefix="/api/v1/numbers")

@numbers.route('/',methods=['POST','GET'])
@jwt_required()
def functionNumbers():

    current_user = get_jwt_identity()
    
    if request.method == 'POST':
        name = request.get_json().get('name','')
        phone = request.get_json().get('phone','')
        account = request.get_json().get('account','')
        location = request.get_json().get('location','')

        if Number.query.filter_by(phone=phone).first():
            return jsonify({
                'error':'Phone number already exists'
            }),HTTP_409_CONFLICT

        number = Number(name=name,phone=phone,account=account,location=location,user_id=current_user)


        db.session.add(number)
        db.session.commit()
        
        return jsonify({
            'id':number.id,
            'name':number.name,
            'phone':number.phone,
            'account':number.account,
            'location':number.location,
            'created_at':number.created_at,
            'updated_at':number.updated_at
        }),HTTP_201_CREATED

    else:

        page = request.args.get('page',1,type=int)#PAgination
        per_page = request.args.get('per_page',5,type=int)

        numbers = Number.query.filter_by(user_id=current_user).paginate(page=page,per_page=per_page)

        data=[]

        for item in numbers.items: #Add item when use pagination
            data.append({
                'id':item.id,
                'name':item.name,
                'phone':item.phone,
                'account':item.account,
                'location':item.location,
                'created_at':item.created_at,
                'updated_at':item.updated_at,
                'reported_times':item.reports
            })

        meta={ #Info about pagination
            "page": numbers.page,
            "pages": numbers.pages,
            "total_count":numbers.total,
            "prev_page":numbers.prev_num,
            "next_page":numbers.next_num,
            "has_next":numbers.has_next,
            "has_prev":numbers.has_prev,
        }
        
        return jsonify({'data':data,'meta':meta}),HTTP_200_OK

@numbers.get("/<int:id>")
@jwt_required()
def get_number(id):
    current_user = get_jwt_identity() #Get token

    number= Number.query.filter_by(user_id=current_user,id=id).first()
    
    if not number:
        return jsonify({
            'message':'Item not found'
        }),HTTP_404_NOT_FOUND

    return jsonify({
        'id':number.id,
        'name':number.name,
        'phone':number.phone,
        'account':number.account,
        'location':number.location,
        'created_at':number.created_at,
        'updated_at':number.updated_at,
        'reported_times':number.reports
    })

@numbers.put("/<int:id>")
@numbers.patch("/<int:id>")
@jwt_required()
def edit_number(id):
    current_user = get_jwt_identity() #Get token

    number= Number.query.filter_by(user_id=current_user,id=id).first()
    
    if not number:
        return jsonify({
            'message':'Item not found'
        }),HTTP_404_NOT_FOUND

    name = request.get_json().get('name','')
    phone = request.get_json().get('phone','')
    account = request.get_json().get('account','')
    location = request.get_json().get('location','')
    reported_times = request.get_json().get('reported_times','')

    number.name = name
    number.phone = phone
    number.account = account
    number.location = location
    number.reports = reported_times

    db.session.commit()

    return jsonify({
        'id':number.id,
        'name':number.name,
        'phone':number.phone,
        'account':number.account,
        'location':number.location,
        'created_at':number.created_at,
        'updated_at':number.updated_at,
        'reported_times':number.reports
    }),HTTP_200_OK

@numbers.delete("/<int:id>")
@jwt_required()
def delete_number(id):
    current_user = get_jwt_identity() #Get token

    number= Number.query.filter_by(user_id=current_user,id=id).first()
    
    if not number:
        return jsonify({
            'message':'Item not found'
        }),HTTP_404_NOT_FOUND

    db.session.delete(number)
    db.session.commit()

    return jsonify({

    }),HTTP_204_NO_CONTENT

#Search a number
@numbers.get("/search/<string:num>")
def search_number(num):

    number= Number.query.filter_by(phone=num).first()
    
    if not number:
        return jsonify({
            'message':'Phone not found'
        }),HTTP_404_NOT_FOUND

    return jsonify({
        'id':number.id,
        'name':number.name,
        'phone':number.phone,
        'account':number.account,
        'location':number.location,
        'created_at':number.created_at,
        'updated_at':number.updated_at,
        'reported_times':number.reports
    })