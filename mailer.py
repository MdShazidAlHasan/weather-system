from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# Initialize FastAPI app
app = FastAPI()

# Email Configuration
conf = ConnectionConfig(
    MAIL_USERNAME="mdshazid1003@gmail.com",
    MAIL_PASSWORD="jzpbcoathybdiodk",
    MAIL_FROM="mdshazid1003@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Use this instead of MAIL_TLS
    MAIL_SSL_TLS=False   # Use this instead of MAIL_SSL
)

# Email Request Schema
class EmailSchema(BaseModel):
    email: EmailStr
    subject: str
    message: str

# Reusable Email-Sending Function
async def send_email(recipient: str, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        body=body,
        subtype="plain"  # Use "html" for HTML emails
    )

    fm = FastMail(conf)
    await fm.send_message(message)
