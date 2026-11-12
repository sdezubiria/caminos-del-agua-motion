"""Renders render.html frame by frame in headless Chrome and saves transparent PNG sequences.

    python3 render.py OUT_DIR SCENE WIDTH HEIGHT FRAMES FPS [query]

e.g. python3 render.py out/logo logo 1900 1700 220 30
     python3 render.py out/raiz-1 card 1080 1920 150 30 n=1

Standard library only: talks to Chrome over the DevTools protocol with a minimal WebSocket client.
"""
import base64, json, os, pathlib, shutil, socket, subprocess, sys, tempfile, time, urllib.request

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PORT = 9339
HERE = pathlib.Path(__file__).resolve().parent


class WebSocket:
    def __init__(self, url):
        host, path = url.split('://', 1)[1].split('/', 1)
        h, p = host.split(':')
        self.s = socket.create_connection((h, int(p)))
        key = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f'GET /{path} HTTP/1.1\r\nHost: {host}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                        f'Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        buf = b''
        while b'\r\n\r\n' not in buf:
            buf += self.s.recv(4096)
        self.buf = buf.split(b'\r\n\r\n', 1)[1]

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.s.recv(1 << 20)
            if not chunk:
                raise ConnectionError('Chrome closed the connection')
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def send(self, text):
        data = text.encode()
        head = bytearray([0x81])
        n = len(data)
        if n < 126:
            head.append(0x80 | n)
        elif n < 65536:
            head += bytes([0x80 | 126]) + n.to_bytes(2, 'big')
        else:
            head += bytes([0x80 | 127]) + n.to_bytes(8, 'big')
        mask = os.urandom(4)
        self.s.sendall(bytes(head) + mask + bytes(b ^ mask[i % 4] for i, b in enumerate(data)))

    def recv(self):
        message = b''
        while True:
            b1, b2 = self._read(2)
            n = b2 & 0x7F
            if n == 126:
                n = int.from_bytes(self._read(2), 'big')
            elif n == 127:
                n = int.from_bytes(self._read(8), 'big')
            message += self._read(n)
            if b1 & 0x80:
                return message.decode()


class Chrome:
    def __init__(self):
        self.profile = tempfile.mkdtemp(prefix='cda-render-')
        self.proc = subprocess.Popen([CHROME, '--headless=new', f'--remote-debugging-port={PORT}', f'--user-data-dir={self.profile}',
                                      '--hide-scrollbars', '--allow-file-access-from-files', '--force-color-profile=srgb',
                                      '--no-first-run', '--no-default-browser-check', 'about:blank'],
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                pages = json.load(urllib.request.urlopen(f'http://127.0.0.1:{PORT}/json'))
                ws = next(p['webSocketDebuggerUrl'] for p in pages if p['type'] == 'page')
                break
            except Exception:
                time.sleep(.2)
        else:
            raise RuntimeError('Chrome did not start')
        self.ws = WebSocket(ws)
        self.id = 0

    def call(self, method, **params):
        self.id += 1
        self.ws.send(json.dumps({'id': self.id, 'method': method, 'params': params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get('id') == self.id:
                if 'error' in msg:
                    raise RuntimeError(f'{method}: {msg["error"]}')
                return msg['result']

    def eval(self, expr):
        r = self.call('Runtime.evaluate', expression=expr, awaitPromise=True, returnByValue=True)
        if 'exceptionDetails' in r:
            raise RuntimeError(f'{expr}: {r["exceptionDetails"]}')
        return r['result'].get('value')

    def close(self):
        self.proc.terminate()
        self.proc.wait()
        shutil.rmtree(self.profile, ignore_errors=True)


def main():
    out, scene, w, h, frames, fps = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), float(sys.argv[6])
    query = sys.argv[7] if len(sys.argv) > 7 else ''
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    prefix = out.name.removesuffix('_png')   # frames of 'logo-corriente_png/' are logo-corriente_0000.png ...
    chrome = Chrome()
    try:
        chrome.call('Page.enable')
        chrome.call('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=1, mobile=False)
        chrome.call('Emulation.setDefaultBackgroundColorOverride', color={'r': 0, 'g': 0, 'b': 0, 'a': 0})
        url = (HERE / 'render.html').as_uri() + f'?scene={scene}' + (f'&{query}' if query else '')
        chrome.call('Page.navigate', url=url)
        for _ in range(200):
            time.sleep(.1)
            if chrome.eval('document.readyState') == 'complete' and chrome.eval('typeof window.ready') == 'object':
                break
        chrome.eval('window.ready')
        for i in range(frames):
            chrome.eval(f'renderAt({i / fps!r})')
            png = chrome.call('Page.captureScreenshot', format='png', clip={'x': 0, 'y': 0, 'width': w, 'height': h, 'scale': 1})['data']
            (out / f'{prefix}_{i:04d}.png').write_bytes(base64.b64decode(png))
        print(f'{out.name}: {frames} frames')
    finally:
        chrome.close()


if __name__ == '__main__':
    main()
