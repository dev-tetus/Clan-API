import pymysql



def get_connection():
    try:
        conexion = pymysql.connect(host='192.168.1.40',
                                port=3306,
                                user='root',
                                password='',
                                db='sn3t',
                                charset='utf8mb4')
        print('Conexion correcta')
        #return conexion
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Error while connecting", e)
