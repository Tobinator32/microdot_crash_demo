import asyncio

from microdot_asyncio import Microdot, send_file, redirect
from microdot_asyncio_websocket import with_websocket
import time
import platform

app = Microdot()

@app.route("/")
async def RequestIndex(request):
    return redirect("/new/index_revised.html")

async def heartbeat(rqst, ws):
    global login_level
    while True:
        time.sleep(0.1)
        try:
            msg = await ws.receive()
        except Exception as e:
            print("to ex: " + str(e))
            return

@app.route("/new/<path>")
@app.route("/new/<path:path>")
async def RequestStaticFiles(request, path):
    if ".." in path:    # forbid directory traversal
        return "Not found", 404

    if path == "/" or path == "/index.html":
        print("redirect")
        return redirect("/new/index_revised.html")

    print(str(request.client_addr))
    print(str(request))
    print(str(path))

    return send_file("new/" + path)

@app.route("/heartbeat")
@with_websocket
async def heartbeat(rqst, ws):
    while True:
        await asyncio.sleep(0.1)
        try:
            msg = await ws.receive()
            await ws.send(msg)
        except Exception as e:
            print("to ex: " + str(e))
            return

        print("websocket msg: " + str(msg))

def start_ap(ssid = "test", pw = "testpass", ip_arg = "192.168.4.1", verbosity = False, enable = True):
    import network
    import utime

    ap = network.WLAN(network.AP_IF)
    ap.active(enable)                         #activating

    while not ap.active() and enable:
        utime.sleep(0.1)
        pass

    ap.config(essid=ssid, password=pw, security=3)
    if ip_arg is not None:
        arg = (ip_arg, "255.255.255.0", ip_arg, "8.8.8.8")
        ap.ifconfig(arg)

    while not ap.active() and enable:
        utime.sleep(0.1)
        pass

    if verbosity:
        print(ap.ifconfig())
        print("ap enabled? : %s" % enable)

def webserver():
    app.run(port=80)

if __name__ == "__main__":
    if "micropython" in platform.platform().lower():
        start_ap()
        print("starting ap")

    print("running")

    webserver()