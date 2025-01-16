To make the client and server to handle sending and receiving, we have to use multithreading

Here are a few ways you could manage sending and receiving data concurrently without using multithreading:

Non-blocking sockets: You can set the socket to non-blocking mode using socket.setblocking(0). This allows you to attempt sending and receiving data without the program waiting for one operation to finish before starting the other. However, you'll need to handle situations where data is not immediately available.

Select (I/O multiplexing): You can use the select module to monitor multiple sockets (or file descriptors) for activity and handle reading and writing when data is available. This allows the program to efficiently manage sending and receiving data without using multiple threads or processes.

Asynchronous I/O (asyncio): You can use Python's asyncio library, which provides an event loop to handle asynchronous I/O operations. This allows you to handle multiple connections or data streams concurrently without blocking.