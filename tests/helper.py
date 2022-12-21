import logging

_LOGGER = logging.getLogger(__name__)


class Helper(object):
    __responses = {}

    @staticmethod
    def response(filename: str) -> str:
        if filename not in Helper.__responses:
            with open(
                "tests/responses/" + filename + ".xml", "r", encoding="UTF-8"
            ) as file:
                _LOGGER.debug(f"{filename} not cached yet. Adding to cache.")
                Helper.__responses[filename] = file.read()
        _LOGGER.debug(f"Returning response for {filename} ")
        return Helper.__responses[filename]
