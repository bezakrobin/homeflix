from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'P*PY+29+&N9S%!ZrhZrSn8PnQrtBpdYb2#XR&uUj_qkrcYAYKhmuzkp9EQn%maaXQ%m=s7G8WW@caRTC^=WdkXcu4@f%$33B8zq+fxhG@dq^FA3qRkx+Au2wJTES5EvJj-87YtCmKcTjGd7%6quUcrw-8LNY@wrs*yvfzGvR-tMauyj%uzdGZRUqKc8tT8e^XJXPBwPyzE&CMHyGbjmkczE!!ALUH4MFBphzF$+4tez^xt9^ruCj%V3=LY#Y2gK$'

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app