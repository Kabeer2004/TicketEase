import asyncio
from aiosmtpd.controller import Controller
from email.parser import BytesParser

class CustomSMTPHandler:
    async def handle_DATA(self, server, session, envelope):
        message_data = envelope.content
        message = BytesParser().parsebytes(message_data)

        print(f"Received message from: {envelope.mail_from}")
        print(f"Message recipients: {envelope.rcpt_tos}")
        print("Message data:")
        print(message.as_string())
        print("-" * 40)

        return '250 Message accepted for delivery'

async def run_server():
    controller = Controller(CustomSMTPHandler(), hostname='localhost', port=1025)
    controller.start()
    print("SMTP server running...")
    try:
        await asyncio.Future()
    except KeyboardInterrupt:
        print("Stopping SMTP server.")
    finally:
        controller.stop()

if __name__ == "__main__":
    asyncio.run(run_server())
