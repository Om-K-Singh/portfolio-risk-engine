def get_valid_input(prompt, parse_fn, validate_fn=None, error_msg="Invalid input."):
    while True:
        try:
            value = parse_fn(input(prompt))
            if validate_fn and not validate_fn(value):
                raise ValueError
            return value
        except ValueError:
            print(error_msg)