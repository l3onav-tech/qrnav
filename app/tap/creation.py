import qrcode
import uuid
from io import BytesIO
from sqlalchemy.orm import Session
from app.users.auth import get_current_user
from app.tap.models import TapModel
from app.tap.schemas import TapSchema
from app.settings.database import get_session, engine
from app.settings.object_storage import upload_file_to_bucket
from fastapi import Depends, UploadFile, File

class Tap:
    """
    Model
        id = Column(Uuid, primary_key=True)
        name = Column(String, unique=True)
        qr_url = Column(String, unique=True)
        note = Column(String)
        created_at = Column(DateTime, server_default=function.now())
        updated_at = Column(DateTime, onupdate=function.now())
    """

    def __init__(self, data: TapSchema, model=TapModel, user = uuid.uuid4):
        """
        Constructor
        """
        self.data = data
        self.model = model
        self.user = user

    def create_qr_url(self, id):
        """
        Create QR Code
        """
        qr = qrcode.QRCode(
            version=2,
            box_size=50,
            border=1
        )
        name_file = f"{id}.png"
        url = f"https://api.qrnav.tech/v1/tab/{id}"
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0) # rewind pointer back to start
        response_uploading = upload_file_to_bucket(buffer, "generated", "qr", name_file)
        return  {"url": url,"response_uploading": response_uploading }

    def create_tap(self):
        """
        Create Tap
        """
        with Session(engine) as session:
            tap = self.model(
                id  = uuid.uuid4(),
                name = self.data.name,
                note = self.data.note,
                user_id = self.user,
            )
            qr_url = self.create_qr_url(tap.id)
            tap.qr_url = qr_url['url']
            session.add(tap)
            session.commit()
            session.refresh(tap)
            return tap

        
    def get_qr(self):
        """
        Get QR Code from s3
        """
        pass
         

    def update_qr(self):
        """
        Update QR Code to s3
        """
        pass

    def delete_qr(self):
        """
        Delete QR Code from s3
        """
        pass

