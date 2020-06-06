from re import compile, IGNORECASE

ECHO = compile(r"\A\s*/(echo|эхо)\s*\Z", IGNORECASE)
ADDPIC = compile(r"\A\s*/(add|добавить фото) .+\s*\Z", IGNORECASE)
GENERATEWALL = compile(r"\A\s*/(generate|сгенерировать|gen)\s*\Z", IGNORECASE)
