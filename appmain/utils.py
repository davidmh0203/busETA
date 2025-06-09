import os.path
import secrets
from PIL import Image

import jwt
import pymysql

from appmain import app
from appmain.db import get_connection

def verifyJWT(token):
    if token is None:
        return None
    else:
        try:
            decodedToken = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
            if decodedToken:
                conn = get_connection()
                cursor = conn.cursor()

                if cursor:
                    SQL = 'SELECT authkey FROM users WHERE email=%s'
                    cursor.execute(SQL, (decodedToken["email"],))
                    authkey = cursor.fetchone()[0]
                    cursor.close()
                if authkey == decodedToken["authkey"]:
                    return True
                else:
                    return None
            else:
                return None
        except:
            return  None

def getJWTContent(token):
    isVerified = verifyJWT(token)

    if isVerified:
        return jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
    else:
        return None

def savePic(pic, username):
    randHEX =secrets.token_hex(8)
    _, fExt = os.path.splitext(pic.filename)
    picFileName = randHEX + fExt
    picDir = os.path.join(app.static_folder, 'pics', username)
    picPath = os.path.join(picDir, picFileName)
    os.makedirs(picDir, exist_ok=True)

    with Image.open(pic) as image:
        image.save(picPath)
    return picFileName
