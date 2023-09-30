import logging

async def baa():
    print("baa")
    await uasyncio.sleep(1.5)

async def moo():
    print("moo")
    await uasyncio.sleep(1)

if __name__ == "__main__":
    # Add tasks for the coroutines to the event loop
    loop = uasyncio.get_event_loop()
    moo_task = loop.create_task(moo())
    baa_task = loop.create_task(baa())


#     try:
#         # Run all tasks forever
#         loop.run_forever()
#     except KeyboardInterrupt:
#         pass
#     finally:
#         # Close the event loop
#         loop.close()