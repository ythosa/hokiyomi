from re import compile, IGNORECASE

ECHO = compile(r"\A\s*/(echo|эхо)\s*\Z", IGNORECASE)
