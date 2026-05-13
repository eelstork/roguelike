# Roguelike

A simple terminal-based roguelike game scaffold.

## How to play (Terminal)
Run the following command in your terminal:
```bash
python -m roguelike
```
Use `h`/`j`/`k`/`l` or arrow keys to move, and `q` to quit.

## How to run the Server
1. Install requirements if needed (Flask is required).
2. Run the server:
   ```bash
   python3 server.py
   ```
3. Interaction:
   - Get state: `curl http://127.0.0.1:5000/`
   - Send action: `curl -X POST -H "Content-Type: application/json" -d '{"action": "up"}' http://127.0.0.1:5000/action`

## How to test
Run the test script:
```bash
python test.py
```
