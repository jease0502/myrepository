---
tags: ros
---
# ros bug

Failed to fetch http://packages.ros.org/ros/ubuntu/dists/xenial/InRelease  The following signatures couldn't be verified because the public key is not available: NO_PUBKEY F42ED6FBAB17C654

[方法](http://answers.ros.org/question/325039/apt-update-fails-cannot-install-pkgs-key-not-working/)

... logging to /home/robotis/.ros/log/9b3267d2-940a-11e9-a09c-5d176edd8858/roslaunch-robotis-op3-3447.log
Checking log directory for disk usage. This may take awhile.
Press Ctrl-C to interrupt
Done checking log file disk usage. Usage is <1GB.


Traceback (most recent call last):
  File "/opt/ros/kinetic/bin/roslaunch", line 35, in <module>
    roslaunch.main()
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/roslaunch/__init__.py", line 306, in main
    p.start()
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/roslaunch/parent.py", line 268, in start
    self._start_infrastructure()
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/roslaunch/parent.py", line 226, in _start_infrastructure
    self._start_server()
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/roslaunch/parent.py", line 177, in _start_server
    self.server.start()
  File "/opt/ros/kinetic/lib/python2.7/dist-packages/roslaunch/server.py", line 376, in start
    code, msg, val = ServerProxy(self.uri).get_pid()
  File "/usr/lib/python2.7/xmlrpclib.py", line 1243, in __call__
    return self.__send(self.__name, args)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1602, in __request
    verbose=self.__verbose
  File "/usr/lib/python2.7/xmlrpclib.py", line 1283, in request
    return self.single_request(host, handler, request_body, verbose)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1311, in single_request
    self.send_content(h, request_body)
  File "/usr/lib/python2.7/xmlrpclib.py", line 1459, in send_content
    connection.endheaders(request_body)
  File "/usr/lib/python2.7/httplib.py", line 1053, in endheaders
    self._send_output(message_body)
  File "/usr/lib/python2.7/httplib.py", line 897, in _send_output
    self.send(msg)
  File "/usr/lib/python2.7/httplib.py", line 859, in send
    self.connect()
  File "/usr/lib/python2.7/httplib.py", line 836, in connect
    self.timeout, self.source_address)
  File "/usr/lib/python2.7/socket.py", line 566, in create_connection
    sock.connect(sa)
  File "/usr/lib/python2.7/socket.py", line 228, in meth
    return getattr(self._sock,name)(*args)
KeyboardInterrupt
