from pywhispercpp.examples.assistant import Assistant

my_assistant = Assistant(commands_callback=print, n_threads=8)
my_assistant.start()
