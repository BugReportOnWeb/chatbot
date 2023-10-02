def main(user_input):
    # Main chatbot logic goes here
    return f"Hello world from 'main' for '{user_input}'"


def get_response(user_input):
    res = main(user_input)
    return res
