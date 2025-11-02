import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.db_models import Category

async def summarize(mail_content: str) -> str:
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = [
        SystemMessage(content="Summarize the following email content:"),
        HumanMessage(content=mail_content)
    ]
    response = await llm.ainvoke(prompt)
    return response

async def categorize(user_id: int, mail_content: str) -> str:
    db: Session = SessionLocal()
    try:
        categories = db.query(Category).filter(Category.account_id == user_id).all()
        if not categories:
            return "No categories found for this user."

        category_descriptions = "\n".join(
            [f"{cat.name}: {cat.description or ''}" for cat in categories]
        )
        system_prompt = (
            "Given the following categories:\n"
            f"{category_descriptions}\n"
            "Analyze the following email content and decide which category it suits best. "
            "Respond with the category name only."
        )
        llm = ChatOpenAI(model="gpt-3.5-turbo")
        prompt = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=mail_content)
        ]
        response = await llm.ainvoke(prompt)
        return response.content
    finally:
        db.close()