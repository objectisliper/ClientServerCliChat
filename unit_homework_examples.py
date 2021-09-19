import asyncio
import multiprocessing
import multiprocessing as mp
import logging
import socket
import time

from settings import HOST, PORT

logger = mp.log_to_stderr(logging.DEBUG)


# MULTIPROCESSING SERVER


def worker(socket):
    while True:
        client, address = socket.accept()
        logger.debug("{u} connected".format(u=address))
        client.send(b"OK")
        client.close()


def multiprocessing_server():
    num_workers = multiprocessing.cpu_count()

    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((HOST, PORT))
    serversocket.listen(multiprocessing.cpu_count())

    workers = [mp.Process(target=worker, args=(serversocket,)) for i in range(num_workers)]

    for p in workers:
        p.daemon = True
        p.start()

    while True:
        try:
            time.sleep(10)
        except:
            break


# ASYNCIO SERVER


async def handle_client(reader, writer):
    request = None
    while request != 'quit':
        request = (await reader.read(255)).decode('utf8')
        response = 'hi mark'
        writer.write(response.encode('utf8'))
        await writer.drain()
    writer.close()


async def run_server():
    server = await asyncio.start_server(handle_client, 'localhost', PORT)
    async with server:
        await server.serve_forever()


def asyncio_server():
    asyncio.run(run_server())


if __name__ == '__main__':
    asyncio_server()
