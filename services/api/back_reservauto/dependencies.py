from sqlalchemy import LargeBinary, TypeDecorator

from back_reservauto.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ByteArrayString(TypeDecorator):
    impl = LargeBinary
    cache_ok = True

    def process_result_value(self, value, dialect):
       if value is not None:
            return value.hex()
       return value
       
    # def process_bind_param(self, value, dialect):
    #     if value is not None:
    #         return bytes.fromhex(value)
    #     return value
    