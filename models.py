from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UUID
from database import Base
import uuid

class Admin(Base):
    __tablename__ ='admin'

    admin_id=Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    admin_name=Column(String,index=True)
    admin_nic=Column(String,index=True)
    admin_phone=Column(String,index=True)
    admin_password=Column(String,index=True)
    admin_email=Column(String,index=True)