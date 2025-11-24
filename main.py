import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime, timezone, timedelta


def build_test_report() -> str:
    """지금은 인프라 테스트용 단순 본문만 생성."""
    # 한국 시간 기준 현재 시각
    kst = timezone(timedelta(hours=9))
    now = datetime.now(tst:=kst)  # Python 3.10 이상이면 이렇게 써도 되고, 안 되면 그냥 kst로 대체

    date_str = now.strftime("%Y-%m-%d %H:%M")
    body = f"""[MS Daily Bot 테스트 메일]

이 메일이 도착했다면,
- GitHub Actions 스케줄러
- Python 스크립트 실행
- Gmail SMTP (앱 비밀번호)

이 세 가지가 모두 정상 작동하고 있다는 의미입니다.

현재 기준 실행 시각 (KST): {date_str}

다음 단계:
1) NewsAPI + RSS로 Microsoft 관련 뉴스를 수집하고
2) Gemini API로 요약한 뒤
3) 이 메일 본문을 실제 'Microsoft 데일리 리포트' 내용으로 바꾸게 됩니다.
"""
    return body


def send_email(subject: str, body: str):
    """Gmail SMTP를 사용해서 메일 발송."""
    email_user = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_PASS")
    recipient = os.environ.get("RECIPIENT_EMAIL")

    if not email_user or not email_pass or not recipient:
        raise RuntimeError("EMAIL_USER / EMAIL_PASS / RECIPIENT_EMAIL 환경변수가 설정되지 않았습니다.")

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr(("MS Daily Bot", email_user))
    msg["To"] = recipient

    # Gmail SMTP 서버 설정
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(email_user, email_pass)
        server.send_message(msg)


def main():
    # 1차 버전: 단순 테스트 메일
    subject = "[TEST] MS Daily Bot 인프라 테스트"
    body = build_test_report()
    send_email(subject, body)
    print("테스트 메일 발송 완료")


if __name__ == "__main__":
    main()
