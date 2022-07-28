import os
from sqlalchemy import MetaData
from sqlalchemy.sql import select
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, jsonify, request

api = Flask(__name__)

def databaseUri():
    # use postgresql because posgres deprecated
    uri = os.getenv("DATABASE_URL") 
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    
    return uri

DATABASE_URL = databaseUri()
ENV = 'dev'

if ENV == 'dev':
    api.debug = True
else:
    api.debug = False

api.config['JSON_SORT_KEYS'] = False
api.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
api.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(api)
meta = MetaData(schema='data_penduduk')

penduduk_2019_1 = db.Table('penduduk_2019_1', meta, autoload=True, autoload_with=db.engine)
penduduk_2019_2 = db.Table('penduduk_2019_2', meta, autoload=True, autoload_with=db.engine)
penduduk_2020_1 = db.Table('penduduk_2020_1', meta, autoload=True, autoload_with=db.engine)
penduduk_2020_2 = db.Table('penduduk_2020_2', meta, autoload=True, autoload_with=db.engine)
penduduk_2021_1 = db.Table('penduduk_2021_1', meta, autoload=True, autoload_with=db.engine)



def baseQueryToJson(table):
    # serialize SQLAlchemy basequery
    #kec = table.columns.nama_kecamatan
    desa = table.columns.desa_kelurahan
    pria = table.columns.jumlah_pria
    wanita = table.columns.jumlah_wanita
    kkl = table.columns.kepala_keluarga
    pddk = table.columns.jumlah_penduduk

    query = select(desa, pria, wanita, kkl, pddk)
    res = db.session.execute(query)

    # take all table including id
    #res = db.session.query(table)
    
    return jsonify([dict(data) for data in res])


def queryById(table, nama_desa):
    desa = table.columns.desa_kelurahan
    pria = table.columns.jumlah_pria
    wanita = table.columns.jumlah_wanita
    kkl = table.columns.kepala_keluarga
    pddk = table.columns.jumlah_penduduk
    query = select(desa, pria, wanita, kkl, pddk).where(table.columns.desa_kelurahan == nama_desa)
    res = db.session.execute(query)
    return jsonify([dict(data) for data in res])




@api.route("/")
def home():
    return render_template('index.html')

@api.route("/2019-semester-1", methods=['GET'])
def data_penduduk_2019_1():
    try:
        # if request.method == 'GET':
        nama_desa = request.args.get('desa')
        if nama_desa != None:
            return queryById(penduduk_2019_1,nama_desa.upper())

        return baseQueryToJson(penduduk_2019_1)
            
    except IndexError:
        response = jsonify({'status':'id error, masukkan id antara 0 - 129'})
        response.status_code = 400
        return response
        
    except ValueError:
        response = jsonify({'status':'Query parameter value salah, masukkan parameter id dengan angka'})
        response.status_code = 404
        return response
        
    except TypeError:
        response = jsonify({'status':'Query parameter salah, gunakan Query parameter id'})
        response.status_code = 400
        return response

@api.route("/2019-semester-2", methods=['GET'])
def data_penduduk_2019_2():
    try:
        nama_desa = request.args.get('desa')
        if nama_desa != None:
            return queryById(penduduk_2019_2, nama_desa.upper())
        
        return baseQueryToJson(penduduk_2019_2)
            
    except IndexError:
        response = jsonify({'status':'id error, masukkan id antara 0 - 129'})
        response.status_code = 400
        return response
        
    except ValueError:
        response = jsonify({'status':'Query parameter value salah, masukkan parameter id dengan angka'})
        response.status_code = 404
        return response
        
    except TypeError:
        response = jsonify({'status':'Query parameter salah, gunakan Query parameter id'})
        response.status_code = 400
        return response
    
@api.route("/2020-semester-1", methods=['GET','POST'])
def data_penduduk_2020_1():
    try:
        nama_desa = request.args.get('desa')
        if nama_desa != None:
            return queryById(penduduk_2019_1,nama_desa.upper())
        
        return baseQueryToJson(penduduk_2020_2)
            
    except IndexError:
        response = jsonify({'status':'id error, masukkan id antara 0 - 129'})
        response.status_code = 400
        return response
    
    except ValueError:
        response = jsonify({'status':'Query parameter value salah, masukkan parameter id dengan angka'})
        response.status_code = 404
        return response
        
    except TypeError:
        response = jsonify({'status':'Query parameter salah, gunakan Query parameter id'})
        response.status_code = 400
        return response
 
@api.route("/2020-semester-2", methods=['GET','POST'])
def data_penduduk_2020_2():
    try:
        nama_desa = request.args.get('desa')
        if nama_desa != None:
            return queryById(penduduk_2019_1,nama_desa.upper())
        
        return baseQueryToJson(penduduk_2020_2)
            
    except IndexError:
        response = jsonify({'status':'id error, masukkan id antara 0 - 129'})
        response.status_code = 400
        return response
        
    except ValueError:
        response = jsonify({'status':'Query parameter value salah, masukkan parameter id dengan angka'})
        response.status_code = 404
        return response
        
    except TypeError:
        response = jsonify({'status':'Query parameter salah, gunakan Query parameter id'})
        response.status_code = 400
        return response
    
@api.route("/2021-semester-1", methods=['GET','POST'])
def data_penduduk_2021_1():
    try:
        nama_desa = request.args.get('desa')
        if nama_desa != None:
            return queryById(penduduk_2019_1,nama_desa.upper())
        
        return baseQueryToJson(penduduk_2021_1)
            
    except IndexError:
        response = jsonify({'status':'id error, masukkan id antara 0 - 129'})
        response.status_code = 404
        return response
        
    except ValueError:
        response = jsonify({'status':'Query parameter value salah, masukkan parameter id dengan angka'})
        response.status_code = 400
        return response
        
    except TypeError:
        response = jsonify({'status':'Query parameter salah, gunakan Query parameter id'})
        response.status_code = 404
        return response


if __name__ == "__main__":
    api.run()

