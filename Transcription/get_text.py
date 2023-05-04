import random
import time

import speech_recognition as sr


def recognize_speech_from_mic(recognizer: sr.Recognizer(), microphone: sr.Microphone()) -> dict:
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None,
        "transcription": ' '
    }


    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


if __name__ == "__main__":


    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    count = 5
    while count > 0:
        print(count)
        speech = recognize_speech_from_mic(recognizer, microphone)
        if speech["transcription"]:
            print("You said: {}".format(speech["transcription"]))
            exit(0)
        if not speech["success"] and speech["error"]:
            exit(0)
        print("I didn't catch that. What did you say?\n")
        count -= 1