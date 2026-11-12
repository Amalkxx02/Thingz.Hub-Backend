from brevo import AsyncBrevo
from brevo.transactional_emails import (
    SendTransacEmailRequestSender,
    SendTransacEmailRequestToItem,
)

client = AsyncBrevo(api_key=settings.MAIL_API_KEY)

async def send_mail(subject:str,html_content:str,email:Email,name:str):
    try:
        result = await client.transactional_emails.send_transac_email(
            subject=subject,
            html_content=html_content,
            sender=SendTransacEmailRequestSender(
                name=settings.MAIL_NAME,
                email=settings.MAIL_ADDRESS,
            ),
            to=[
                SendTransacEmailRequestToItem(
                    email=email,
                    name=name,
                )
            ],
        )
        print("Email sent. Message ID:", result.message_id)
    except ApiError as e:
        print(e.status_code)
        print(e.body)

