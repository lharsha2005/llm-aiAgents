import json
from a2a_schema import create_msg

def send_question():
    question=input("User:")
    msg = create_msg("queryAgent", "anwerAgent", question)

    with open("a2a_message.json", "w") as f:
        json.dump(msg, f)

if __name__ == "__main__":
    send_question()
