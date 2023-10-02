def chatbot(user_input):
    # Main chatbot logic goes here
    return f"<response> from chatbot for user input '{user_input}'"

def get_response(user_input):
    res = chatbot(user_input)
    return { 'msg': res }
