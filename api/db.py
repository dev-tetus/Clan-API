import pymysql
import credentials as cred



def get_connection():
    try:
        conexion = pymysql.connect(host=cred.get_credentials()["db_ip"],
                                port=3306,
                                user=cred.get_credentials()["db_user"],
                                password=cred.get_credentials()["db_pass"],
                                db='sn3t',
                                charset='utf8mb4')
        print('Conexion correcta')
        return conexion
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Error while connecting", e)
