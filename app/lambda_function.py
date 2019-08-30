# -*- coding: utf-8 -*-

import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response


SKILL_NAME = "Google Play Music"
GREETING_MESSAGE = "This is Play Music skill."
HELP_MESSAGE = "You can say: play John Lennon Imagine"
HELP_REPROMPT = "What song do you want to hear?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "I can't help you with that. I can help you to listen music from Google Play Music."
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    handler_input.response_builder.speak(GREETING_MESSAGE).ask(HELP_REPROMPT)

    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("PlayMusicIntent"))
def play_music_intent(handler_input):
    slots = handler_input.request_envelope.request.intent.slots
    song = slots['song'].value
    if song:
        logger.info(song)
        handler_input.response_builder.speak(song)
        return handler_input.response_builder.response
    else:
        speech = "Please, specify song"
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(HELP_REPROMPT)

        return handler_input.response_builder.response


sb.add_exception_handler(CatchAllExceptionHandler())
lambda_handler = sb.lambda_handler()


import os
from gmusicapi import Musicmanager, Mobileclient
# from pathlib import Path

# mm = Musicmanager()
# mm.perform_oauth(storage_filepath=Path("./oauth.cred"))
# imei = os.getenv("IMEI")
# resp = mm.login(oauth_credentials=u"oauth.cred", uploader_id=imei)

email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
imei = os.getenv("IMEI")

mm = Mobileclient()
mm.login(email=email, password=password, android_id=imei)
logger.info(mm.is_authenticated())
