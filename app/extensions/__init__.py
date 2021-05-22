from flask_jwt_extended import JWTManager

from app.extensions.cache.cache import RedisClient

jwt = JWTManager()
redis = RedisClient()
