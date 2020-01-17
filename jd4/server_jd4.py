from asyncio import get_event_loop

from aiohttp import web

from jd4.compile import build
from jd4.case import PracticeCase
from jd4.cgroup import try_init_cgroup


async def index(request):
    data = await request.json()
    return web.json_response(data)


# app = web.Application()
# app.router.add_route('*', '/', index)
#
# web.run_app(app)
# # 192.168.86.134

def run(coro):
    return get_event_loop().run_until_complete(coro)


if __name__ == '__main__':
    lang = 'py3'
    code = b'print(sum(map(int, input().split())))'

    try_init_cgroup()

    package, message, time_usage_ns, memory_usage_bytes = run(build(lang, code))
    print('在%d ms时间内编译成功，%d kb内存', time_usage_ns // 1000000, memory_usage_bytes // 1024)
    print('编译器输出:%s', message)

    case = PracticeCase('1 2', '3', 200000000, 33554432, 10)

    status, score, time_usage_ns, memory_usage_bytes, stdout, stderr = run(case.judge(package))
    print(status, score, time_usage_ns // 1000000, 'ms', memory_usage_bytes // 1024, 'kb', stdout, stderr)
