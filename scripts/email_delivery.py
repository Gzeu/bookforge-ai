#!/usr/bin/env python3
"""
BookForge AI — Email Delivery for finished EPUBs.
Supports SMTP (Gmail, Outlook, custom) and optionally SendGrid.
"""
import logging
import os
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)


class EmailDelivery:
    """Send EPUB files via SMTP with optional HTML body."""

    def __init__(
        self,
        host: str = None,
        port: int = None,
        user: str = None,
        password: str = None,
        from_addr: str = None,
    ):
        self.host = host or SMTP_HOST
        self.port = port or SMTP_PORT
        self.user = user or SMTP_USER
        self.password = password or SMTP_PASSWORD
        self.from_addr = from_addr or EMAIL_FROM or self.user

    def send_epub(
        self,
        to: str | list[str],
        epub_path: str,
        title: str = "",
        author: str = "",
        extra_body: str = "",
    ) -> bool:
        """
        Send a finished EPUB as email attachment.
        Returns True on success, False on failure (logs error).
        """
        recipients = [to] if isinstance(to, str) else to
        epub_file = Path(epub_path)
        if not epub_file.exists():
            logger.error(f"EPUB not found for delivery: {epub_path}")
            return False

        subject = f"\U0001f4da Your book is ready: {title}" if title else "Your BookForge AI book is ready"
        body_html = f"""\
<html><body>
<p>Hi,</p>
<p>Your book <strong>{title}</strong>{f' by {author}' if author else ''} has been generated and is attached as an EPUB file.</p>
{f'<p>{extra_body}</p>' if extra_body else ''}
<p>You can open it with any EPUB reader (Apple Books, Kindle app via Send to Kindle, Calibre).</p>
<br><p><em>BookForge AI</em></p>
</body></html>"""

        msg = MIMEMultipart("mixed")
        msg["From"] = self.from_addr
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body_html, "html", "utf-8"))

        with open(epub_path, "rb") as f:
            attachment = MIMEApplication(f.read(), _subtype="epub+zip")
            attachment.add_header(
                "Content-Disposition",
                "attachment",
                filename=epub_file.name,
            )
            msg.attach(attachment)

        try:
            with smtplib.SMTP(self.host, self.port, timeout=30) as server:
                server.ehlo()
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.from_addr, recipients, msg.as_string())
            logger.info(f"EPUB delivered to {recipients}: {epub_file.name}")
            return True
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP auth failed: {e}")
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {e}")
        except Exception as e:
            logger.error(f"Email delivery failed: {e}")
        return False

    def test_connection(self) -> bool:
        """Test SMTP credentials without sending. Returns True if login succeeds."""
        try:
            with smtplib.SMTP(self.host, self.port, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.login(self.user, self.password)
            return True
        except Exception as e:
            logger.warning(f"SMTP connection test failed: {e}")
            return False
