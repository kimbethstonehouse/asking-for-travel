import requests
import json
import weather
import tourist_attractions

import logging

from email_text import produce_text
from send_email import send_email

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

skill_name = "Asking For Travel Session"
help_text = ("Please tell me where you want to go and when. I will help you "
             "organise your travel plan. You can say, I'm going to London on Saturday. ")


sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response

    attr = handler_input.attributes_manager.session_attributes

    speech_text = "Welcome to Asking for Travel, you can say the " \
                  "place you would like to visit! "
    attr["state"] = "starting"

    return handler_input.response_builder\
        .speak("<speak><voice name=\"Geraint\">{}</voice></speak>".format(speech_text))\
        .set_should_end_session(False)\
        .response


@sb.request_handler(can_handle_func=is_intent_name("GoingToCityIntent"))
def launch_request_handler(handler_input):
    """Handler for GoingTOCity"""
    # type: (HandlerInput) -> Response

    attr = handler_input.attributes_manager.session_attributes
    slots = handler_input.request_envelope.request.intent.slots
    logger.info("Attributes: " + str(attr))
    logger.info("Slots: " + str(slots))

    if 'state' not in attr or attr['state'] == "starting":

        attr["state"] = "starting"

        if slots['city'].value is None:
            if 'city' not in attr:
                speech = ("Please tell me which city you would like to visit,"
                         "what day you would like to visit, and what kind of events you are interested in. ")
                reprompt = "Where would you like to visit?"
                return handler_input.response_builder.speak("<speak><voice name=\"Geraint\"><prosody pitch=\"x-high\">{}</prosody></voice></speak>".format(speech)).ask(reprompt).response
            else:
                city = attr['city']
        else:
            city = slots['city'].value
            logger.info("City was " + city)
            attr['city'] = city

        speech = "You are going to visit {}. ".format(city)

        if slots['date'].value is None:
            if 'date' not in attr:
                speech += ("Please tell me which day you would like to "
                           "make your trip, and what kind of events you are interested in. ")
                reprompt = "When would you like to visit?"
                return handler_input.response_builder.speak("<speak><voice name=\"Geraint\">{}</voice></speak>".format(speech)).ask(reprompt).response
            else:
                date = attr['date']
        else:
            date = slots['date'].value
            logger.info("Date was" + date)
            attr["date"] = date

        speech += "on <say-as interpret-as=\"date\">{}. </say-as>".format(date)

        if slots['eventCategories'].value is None:
            speech += ("What kind of events are you interested in? "
                       "You could say, I'm interested in music. ")
            reprompt = ""
            return handler_input.response_builder.speak("<speak><voice name=\"Geraint\">{}</voice></speak>".format(speech)).ask(reprompt).response

        logger.info("Have all required info.")

        type = slots['eventCategories'].value
        attr["type"] = type

        # generate speech and email text, then send email
        (speech_text, body_text, body_html) = produce_text(city, date, type)
        speech = speech_text
        send_email(body_text, body_html)

        return handler_input.response_builder \
            .speak(speech) \
            .set_card(SimpleCard("Asking for Travel", speech)) \
            .set_should_end_session(True) \
            .response


'''
@sb.request_handler(can_handle_func=is_intent_name("EventSearchIntent"))
def launch_request_handler(handler_input):
    """Handler for EventSearchIntent"""
    # type: (HandlerInput) -> Response

    attr = handler_input.attributes_manager.session_attributes
    slots = handler_input.request_envelope.request.intent.slots

    if attr["state"] != "event":
        speech = ("Please tell me which city you would like to visit,"
                  "what day you would like to visit, and what kind of events would interest you.")
        reprompt = "Where would you like to visit?"
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

    if slots['YesOrNo'].value is None:
        speech = "The Weather is going to be {} and tourists who travel to {} often like to visit {}. Would you like to hear more about upcoming {} events in {}?"
        reprompt = "You can say yes or no."
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

    answer = slots["YesOrNo"]

    if answer == "no":
        speech = "okay, I will send you an email with the information so far. Goodbye!"
        return handler_input.response_builder \
            .speak(speech) \
            .set_card(SimpleCard("Asking for Travel", speech)) \
            .set_should_end_session(True) \
            .response

    speech = "You have blah blah blah event. I will send you an email!"

    return handler_input.response_builder \
            .speak(speech) \
            .set_card(SimpleCard("Asking for Travel", speech)) \
            .set_should_end_session(True) \
            .response
'''


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    handler_input.response_builder.speak(help_text).ask(help_text)
    return handler_input.response_builder.response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""

    # TODO : Ask user if they want the email for the information so far

    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("LookForEventsRequest"))
def whats_my_color_handler(handler_input):
    """Check if a favorite color has already been recorded in
    session attributes. If yes, provide the color to the user.
    If not, ask for favorite color.
    """
    # type: (HandlerInput) -> Response
    if color_slot_key in handler_input.attributes_manager.session_attributes:
        fav_color = handler_input.attributes_manager.session_attributes[
            color_slot_key]
        speech = "Your favorite color is {}. Goodbye!!".format(fav_color)
        handler_input.response_builder.set_should_end_session(True)
    else:
        speech = "I don't think I know your favorite color. " + help_text
        handler_input.response_builder.ask(help_text)

    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response




@sb.request_handler(can_handle_func=is_intent_name("WhatsMyColorIntent"))
def whats_my_color_handler(handler_input):
    """Check if a favorite color has already been recorded in
    session attributes. If yes, provide the color to the user.
    If not, ask for favorite color.
    """
    # type: (HandlerInput) -> Response
    if color_slot_key in handler_input.attributes_manager.session_attributes:
        fav_color = handler_input.attributes_manager.session_attributes[
            color_slot_key]
        speech = "Your favorite color is {}. Goodbye!!".format(fav_color)
        handler_input.response_builder.set_should_end_session(True)
    else:
        speech = "I don't think I know your favorite color. " + help_text
        handler_input.response_builder.ask(help_text)

    handler_input.response_builder.speak(speech)
    return handler_input.response_builder.response


handler = sb.lambda_handler()
