from flask import Flask
from flask_mail import Mail

# Flask 앱 객체 생성
app = Flask(__name__)

# 기본 설정
app.config["SECRET_KEY"] = 'e2a14e9612b8bdfc57201cfce12b6c8f'

# 메일 서버 설정
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'YOUR_ACCOUNT'    # 실제 Gmail 계정
app.config["MAIL_PASSWORD"] = 'YOUR_PASSWORD'    # 앱 비밀번호 (2단계 인증 필요 시)

# Mail 객체 생성
mail = Mail(app)

# 블루프린트 등록
from appmain.routes import main
app.register_blueprint(main)

from appmain.user.routes import user
app.register_blueprint(user)

from appmain.shuttle.routes import shuttle
app.register_blueprint(shuttle)

from appmain.routeBus.routes import routeBus
app.register_blueprint(routeBus)

from appmain.recommend.routes import recommend
app.register_blueprint(recommend)
