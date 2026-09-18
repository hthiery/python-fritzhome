import logging

_LOGGER = logging.getLogger(__name__)


class Helper(object):
    __responses = {}

    @staticmethod
    def response(filename: str, extension: str = "xml") -> str:
        cache_key = f"{filename}.{extension}"
        if cache_key not in Helper.__responses:
            with open(f"tests/responses/{cache_key}", "r", encoding="UTF-8") as file:
                _LOGGER.debug(f"{cache_key} not cached yet. Adding to cache.")
                Helper.__responses[cache_key] = file.read()
        _LOGGER.debug(f"Returning response for {cache_key} ")
        return Helper.__responses[cache_key]
