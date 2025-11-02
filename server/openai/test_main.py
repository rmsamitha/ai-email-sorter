
import asyncio
from openai.utils import summarize, categorize

async def main():
    mail_content = (
        "Dear team, Please find attached the sales report for Q1. "
        "Let me know if you have any questions. Regards, John."
    )
    user_id = 1

    summary = await summarize(mail_content)
    print("Summary:", summary)

    category = await categorize(user_id, mail_content)
    print("Category:", category)

if __name__ == "__main__":
    asyncio.run(main())
