# Distributed Hash Table (CHORD)
Distributed Hash Table - CHORD Example

## Dependencies
### Python virtualEnv

* Install
```bash
apt-get install python-virtualenv
```

* Create Environment
```bash
virtualenv env
env/bin/pip install -r requirements.txt
```
* _Note: If VirtualEnv fails, run on the terminal_
```bash
env/bin/pip install numpy termcolor zmq
```

### Python dependencies
* [ØMQ (ZeroMQ)](http://zeromq.org)
* [JSON](https://docs.python.org/2/library/json.html)
* [HashLib](https://docs.python.org/2/library/hashlib.html)
* [Termcolor](https://pypi.python.org/pypi/termcolor)

## Run

### node

First node
```bash
env/bin/python node.py <my_ip>:<port>
```
Otherwise
```bash
env/bin/python node.py <my_ip>:<port> <other_node_ip>:<port>
```

### client
![Terminal](media/terminal.png)
```bash
python node.py <my_ip>:<port> <some_node_ring>:<port>
```

#### Client Options
![Terminal](media/help.png)
