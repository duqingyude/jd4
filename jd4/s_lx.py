from aiohttp import web


async def hello(request):
    data = await request.json()
    print(data)
    return web.json_response(data)


app = web.Application()
app.router.add_route('*', '/', hello)
web.run_app(app)
