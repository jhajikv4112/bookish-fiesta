import asyncio
import json
import base64
import os
from pathlib import Path
from aiohttp import web
from camoufox.async_api import AsyncCamoufox

sessions = {}

async def handle_websocket(websocket, path):
    session_id = str(id(websocket))
    print(f"New client connected: {session_id}")
    
    browser = None
    page = None
    
    try:
        browser = await AsyncCamoufox(
            headless=True,
            block_webrtc=True,
            window=(1280, 720),
            geoip=True
        ).__aenter__()
        
        page = await browser.new_page()
        sessions[session_id] = {'browser': browser, 'page': page}
        
        async def capture_and_send():
            try:
                screenshot = await page.screenshot(type='png')
                screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
                await websocket.send(json.dumps({
                    'type': 'screenshot',
                    'data': screenshot_b64
                }))
            except Exception as e:
                print(f"Screenshot error: {e}")
        
        await websocket.send(json.dumps({'type': 'ready'}))
        
        async for message in websocket:
            try:
                data = json.loads(message)
                action_type = data.get('type')
                
                if action_type == 'navigate':
                    url = data.get('url', '').strip()
                    if not url.startswith('http://') and not url.startswith('https://'):
                        url = 'https://' + url
                    print(f"Navigating to: {url}")
                    await page.goto(url, wait_until='networkidle', timeout=30000)
                    await asyncio.sleep(0.5)
                    await capture_and_send()
                
                elif action_type == 'click':
                    x = data.get('x', 0) * 1280
                    y = data.get('y', 0) * 720
                    await page.mouse.click(x, y)
                    await asyncio.sleep(0.5)
                    await capture_and_send()
                
                elif action_type == 'scroll':
                    delta = data.get('delta', 0)
                    await page.mouse.wheel(0, delta * 100)
                    await asyncio.sleep(0.2)
                    await capture_and_send()
                
                elif action_type == 'back':
                    await page.go_back(wait_until='networkidle')
                    await asyncio.sleep(0.5)
                    await capture_and_send()
                
                elif action_type == 'forward':
                    await page.go_forward(wait_until='networkidle')
                    await asyncio.sleep(0.5)
                    await capture_and_send()
                
                elif action_type == 'refresh':
                    await page.reload(wait_until='networkidle')
                    await asyncio.sleep(0.5)
                    await capture_and_send()
                
                elif action_type == 'input':
                    text = data.get('text', '')
                    await page.keyboard.type(text)
                    await asyncio.sleep(0.3)
                    await capture_and_send()
                
                elif action_type == 'key':
                    key = data.get('key', '')
                    await page.keyboard.press(key)
                    await asyncio.sleep(0.3)
                    await capture_and_send()
                    
            except Exception as e:
                print(f"Message handling error: {e}")
                await websocket.send(json.dumps({
                    'type': 'error',
                    'message': str(e)
                }))
    
    except websockets.exceptions.ConnectionClosed:
        print(f"Client disconnected: {session_id}")
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        if session_id in sessions:
            session = sessions[session_id]
            if session.get('browser'):
                try:
                    await session['browser'].__aexit__(None, None, None)
                except:
                    pass
            del sessions[session_id]
        print(f"Session cleaned up: {session_id}")

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    session_id = str(id(ws))
    print(f"New client connected: {session_id}")
    
    browser_cm = None
    browser = None
    
    try:
        browser_cm = AsyncCamoufox(
            headless=True,
            block_webrtc=True,
            window=(1280, 720),
            geoip=True
        )
        browser = await browser_cm.__aenter__()
        
        page = await browser.new_page()
        sessions[session_id] = {'browser_cm': browser_cm, 'browser': browser, 'page': page}
        
        async def capture_and_send():
            try:
                screenshot = await page.screenshot(type='png')
                screenshot_b64 = base64.b64encode(screenshot).decode('utf-8')
                await ws.send_json({
                    'type': 'screenshot',
                    'data': screenshot_b64
                })
            except Exception as e:
                print(f"Screenshot error: {e}")
        
        await ws.send_json({'type': 'ready'})
        
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    action_type = data.get('type')
                    
                    if action_type == 'navigate':
                        url = data.get('url', '').strip()
                        if not url.startswith('http://') and not url.startswith('https://'):
                            url = 'https://' + url
                        print(f"Navigating to: {url}")
                        await page.goto(url, wait_until='networkidle', timeout=30000)
                        await asyncio.sleep(0.5)
                        await capture_and_send()
                    
                    elif action_type == 'click':
                        x = data.get('x', 0) * 1280
                        y = data.get('y', 0) * 720
                        await page.mouse.click(x, y)
                        await asyncio.sleep(0.5)
                        await capture_and_send()
                    
                    elif action_type == 'scroll':
                        delta = data.get('delta', 0)
                        await page.mouse.wheel(0, delta * 100)
                        await asyncio.sleep(0.2)
                        await capture_and_send()
                    
                    elif action_type == 'back':
                        await page.go_back(wait_until='networkidle')
                        await asyncio.sleep(0.5)
                        await capture_and_send()
                    
                    elif action_type == 'forward':
                        await page.go_forward(wait_until='networkidle')
                        await asyncio.sleep(0.5)
                        await capture_and_send()
                    
                    elif action_type == 'refresh':
                        await page.reload(wait_until='networkidle')
                        await asyncio.sleep(0.5)
                        await capture_and_send()
                    
                    elif action_type == 'input':
                        text = data.get('text', '')
                        await page.keyboard.type(text)
                        await asyncio.sleep(0.3)
                        await capture_and_send()
                    
                    elif action_type == 'key':
                        key = data.get('key', '')
                        await page.keyboard.press(key)
                        await asyncio.sleep(0.3)
                        await capture_and_send()
                        
                except Exception as e:
                    print(f"Message handling error: {e}")
                    await ws.send_json({
                        'type': 'error',
                        'message': str(e)
                    })
            elif msg.type == web.WSMsgType.ERROR:
                print(f'WebSocket error: {ws.exception()}')
    
    except Exception as e:
        print(f"Connection error: {e}")
    finally:
        if session_id in sessions:
            session = sessions[session_id]
            if session.get('browser_cm'):
                try:
                    await session['browser_cm'].__aexit__(None, None, None)
                    print(f"Browser closed for session: {session_id}")
                except Exception as cleanup_error:
                    print(f"Cleanup error for session {session_id}: {cleanup_error}")
            del sessions[session_id]
        elif browser_cm:
            try:
                await browser_cm.__aexit__(None, None, None)
                print(f"Browser closed before session was registered: {session_id}")
            except Exception as cleanup_error:
                print(f"Cleanup error before session registration {session_id}: {cleanup_error}")
        print(f"Session cleaned up: {session_id}")
    
    return ws

async def index_handler(request):
    return web.FileResponse('public/index.html')

app = web.Application()
app.router.add_get('/', index_handler)
app.router.add_get('/ws', websocket_handler)
app.router.add_static('/static', 'public', name='static')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting server on http://0.0.0.0:{port}")
    web.run_app(app, host='0.0.0.0', port=port)
