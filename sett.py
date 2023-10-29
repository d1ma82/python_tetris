from logging import StreamHandler, Formatter, DEBUG, INFO, ERROR

debug_level = DEBUG

handler = StreamHandler()
formatter = Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)