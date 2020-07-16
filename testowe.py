import time

while True:
    try:
        print ("dziala")
        time.sleep(0.5)
    except KeyboardInterrupt:
        print("done")
        raise


