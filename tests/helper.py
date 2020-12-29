import logging

_LOGGER = logging.getLogger(__name__)


class Helper(object):
    __responses = {}

    @staticmethod
    def response(file: str) -> str:
        if file not in Helper.__responses:
            with open("tests/responses/" + file + ".xml", "r") as file:
                _LOGGER.debug("{file} not cached yet. Adding to cache.")
                Helper.__responses[file] = file.read()
        _LOGGER.debug("Returning response for {file} ")
        return Helper.__responses[file]
