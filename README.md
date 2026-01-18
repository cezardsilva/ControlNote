## Mate todos os processos do Python/Flask que possam estar conflitando:

```sh
pkill -f "python3 server.py"
```

## Ou

```sh
ps aux | grep "python3 server.py"
kill -9 <PID>
```