import asyncio
import websockets
import sys

url = "ws://localhost:8765"

async def get_input(ws) ->str :
    new_input = input("Say what? ")
    if new_input:
        await ws.send(new_input)
    else:
        await ws.close()
        exit()

    return new_input

async def recieve_message(ws) -> str:
    msg = await ws.recv()
    print(msg)
    return msg

async def handle_in_and_out(websocket):

    await asyncio.gather(get_input(websocket),
                   recieve_message(websocket)
                   )

async def listen():
    async with websockets.connect(url) as ws:
        await ws.send("HIHO")
        while True:
            await handle_in_and_out(ws)
                
      


if __name__ == "__main__":
    try:
        asyncio.run(listen())
    except KeyboardInterrupt:
        print("Killed for Keyboard Interrupt")
        exit()

"""
To close a connection, call ws.close()
where ws is the websocket object

create tasks and run them with threading. This is a way to cancel all the remaining tasking

    # input_task = asyncio.create_task(get_input(websocket))
    # output_task = asyncio.create_task(recieve_message(websocket))
    # done, pending = await asyncio.wait(
    #     [input_task, output_task],
    #     return_when=asyncio.FIRST_COMPLETED,
    # )
    # for task in pending:
    #     task.cancel()


"""