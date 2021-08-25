def test_1():
    from gtts import gTTS
    from playsound import playsound

    text = "Je suis une petite licorne and i speak english very well"
    tts = gTTS(text, "fr")
    tts.save("hi.mp3")
    playsound("hi.mp3")

def test_2():
    import pyttsx3

    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    print(rate)
    engine.setProperty('rate', 150)
    # engine.say("Je pense à rien LOL et j'aime les licornes")
    engine.say("AHEHIHOHUHAHEHIHOHUHAHEHIHOHUHAHEHIHOHUHAHEHIHOHUHAHEHIHOHUHAHEHIHOHUHAHEHIHOHUH")
    # engine.say("Je pense également que sophie n'est pas très original pour copier mon concept, ma réussite")
    engine.runAndWait()

# test_1()
test_2()