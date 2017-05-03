# Distributed Hash Table (CHORD)
Distributed Hash Table - CHORD Example

## Dependencies
### [ØMQ (ZeroMQ)](http://zeromq.org)

```bash
pip install zmp
```

### [JSON](https://docs.python.org/2/library/json.html)

```bash
pip install json
```

### [HashLib](https://docs.python.org/2/library/hashlib.html)

```bash
pip install hashlib
```

### [Termcolor](https://pypi.python.org/pypi/termcolor)

```bash
pip install termcolor
```

## Run

### node

First node
```bash
python node.py <my_ip>:<port>
```
Otherwise
```bash
python node.py <my_ip>:<port> <other_node_ip>:<port>
```

### client
```bash
python node.py <my_ip>:<port> <some_node_ring>:<port>
```
