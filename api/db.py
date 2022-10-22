import pymysql



def get_connection():
    try:
        conexion = pymysql.connect(host='mysql',
                                port=3306,
                                user='root',
                                password='root',
                                db='sn3t',
                                charset='utf8mb4')
        return conexion
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Error while connecting", e)