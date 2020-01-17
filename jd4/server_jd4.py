from asyncio import get_event_loop

from aiohttp import web

from jd4.compile import build
from jd4.case import PracticeCase
from jd4.cgroup import try_init_cgroup


def run(coro):
    return get_event_loop().run_until_complete(coro)


async def index(request):
    data = await request.json()
    # lang = 'py3'
    # code = b'print(sum(map(int, input().split())))'
    # str_input = '1 2'
    # str_output = '3'
    lang = data['lang']
    code = data['code'].encode()
    str_input = data['input']
    str_output = data['output']

    try_init_cgroup()

    package, message, time_usage_ns, memory_usage_bytes = await build(lang, code)
    print('在%d ms时间内编译成功，%d kb内存', time_usage_ns // 1000000, memory_usage_bytes // 1024)
    print('编译器输出:%s', message)
    # 30s 32M
    case = PracticeCase(str_input, str_output, 3000000000, 33554432, 10)

    status, score, time_usage_ns, memory_usage_bytes, stdout, stderr = await case.judge(package)
    print(status, score, time_usage_ns // 1000000, 'ms', memory_usage_bytes // 1024, 'kb', stdout, stderr)
    json_response_data = {
        'message': message,
        'status': status,
        'score': score,
        'time_ms': time_usage_ns // 1000000,
        'memory_kb': memory_usage_bytes // 1024,
        'stdout': stdout,
        'stderr': stderr
    }
    return web.json_response(json_response_data)


# 192.168.86.134
if __name__ == '__main__':
    app = web.Application()
    app.router.add_route('*', '/', index)

    web.run_app(app).decode()
