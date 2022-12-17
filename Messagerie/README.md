Basic localhost messaging service in python3
Both the client and the server can send several messages at one time without having to receive any response using the threading module imported at the beginning of the code.
Without this feature we would only be able to send a defined number of messages and wait for a response from the other side before being able to talk again. We would have to complete the cycle.
Using threading we gain the efficiency of a real messaging service without response restrictions.