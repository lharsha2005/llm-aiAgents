from typing import Dict

def create_msg(sender: str, reciver: str, content: str)->Dict:
    return {
        "sender": sender,
        "recipient": reciver,
        "content": content
    }