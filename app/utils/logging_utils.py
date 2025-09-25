# app/utils/logging_utils.py

from datetime import datetime
import os

os.makedirs("logs", exist_ok=True)

def log_action(user_id, session_id, action):
    """Log de ações relacionadas a sessões de usuários."""
    with open("logs/sessions.log", "a") as f:
        f.write(f"{datetime.now()} | user_id={user_id} | session_id={session_id} | action={action}\n")

def log_general(message: str):
    """Log de acessos gerais sem user_id ou session_id"""
    with open("logs/general.log", "a") as f:
        f.write(f"{datetime.now()} | {message}\n")
