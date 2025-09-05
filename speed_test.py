import aiohttp
import asyncio
import time
from tqdm import tqdm

SYSEM_PROMPT1 = "你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。"
question = '''
将下面的日文文本翻译成中文：これは少し先の未来のお话。
＊　＊　＊
精霊は魔力を粮とする霊的な存在である。
それは大精霊であっても括りとしては精霊なので魔力を欲する性质は変わらない。
精霊は自らの好む魔力に引き寄せられる。どの精霊が好むのか、その魔力の性质と精霊の相性がそのまま魔法の适性となる。
これが精霊の基本だ。大精霊だってこの基本的な性质から変わってない。まぁ、何が言いたいかと言うと大精霊であっても好みの魔力はあるし、それを粮としたくなると言う訳だ。
そして大精霊は精霊契约者、つまり人としての肉体も持っている。精霊としての欲求と人としての欲求。この2つが重なると、端的に言うと执着へと変わる倾向がある。
では、精霊契约者として名を连ねる事になったユフィリアはどうなのだろうか？
その答えは、もう执心的なまでの爱情表现だった。
「ユフィ……！　もう、む、りぃ……！」
ベッドに押さえつけられるように体を沈ませるのはアニスフィア。その頬は朱色に染まり、目元は涙で濡れて润んでいる。呼吸は落ち着かないのか、大きく吸い、そして吐き出す。
そんなアニスフィアを抑え付けながら见下ろすユフィリアは仅かに息を荒くするのみだ。頬に朱に染まってはいるものの、アニスフィアに比べればその色は浓くない。'''

async def fetch(session, url):
    """
    参数:
        session (aiohttp.ClientSession): 用于请求的会话。
        url (str): 要发送请求的 URL。
    
    返回:
        tuple: 包含完成 token 数量和请求时间。
    """
    start_time = time.time()

    # 固定请求的内容
    json_payload = {
        "messages": [
            {"role": "system", "content": SYSEM_PROMPT1},
            {"role": "user", "content": question}
                ],
        "stream": False,
        "temperature": 0.7,
        "frequency_penalty": 0.2,
        "num_gpu": 99
    }
    async with session.post(url, json=json_payload) as response:
        response_json = await response.json()
        # print(response_json)
        translated_lines = response_json['choices'][0]['message']['content'].split('\n')
        translated_lines = [line for line in translated_lines if line.strip() != ''] # 去除空行
        if len(translated_lines) == 12:
            pd = 0
        else:
            pd = 1
        end_time = time.time()
        request_time = end_time - start_time
        completion_tokens = response_json['usage']['completion_tokens'] # 从返回的参数里获取生成的 token 的数量
        return completion_tokens, request_time, pd

async def bound_fetch(sem, session, url, pbar):
    # 使用信号量 sem 来限制并发请求的数量，确保不会超过最大并发请求数
    async with sem:
        result = await fetch(session, url)
        pbar.update(1)
        return result

async def run(load_url, max_concurrent_requests, total_requests):
    """
    通过发送多个并发请求来运行基准测试。
    
    参数:
        load_url (str): 要发送请求的URL。
        max_concurrent_requests (int): 最大并发请求数。
        total_requests (int): 要发送的总请求数。
    
    返回:
        tuple: 包含完成 token 总数列表和响应时间列表。
    """
    # 创建 Semaphore 来限制并发请求的数量
    sem = asyncio.Semaphore(max_concurrent_requests)
    
    # 创建一个异步的HTTP会话
    async with aiohttp.ClientSession() as session:
        tasks = []
        
        # 创建一个进度条来可视化请求的进度
        with tqdm(total=total_requests) as pbar:
            # 循环创建任务，直到达到总请求数
            for _ in range(total_requests):
                # 为每个请求创建一个任务，确保它遵守信号量的限制
                task = asyncio.ensure_future(bound_fetch(sem, session, load_url, pbar))
                tasks.append(task)  # 将任务添加到任务列表中
            
            # 等待所有任务完成并收集它们的结果
            results = await asyncio.gather(*tasks)
        
        # 计算所有结果中的完成token总数
        completion_tokens = sum(result[0] for result in results)
        
        # 从所有结果中提取响应时间
        response_times = [result[1] for result in results]

        # 计算行数不匹配的概率
        pd = sum(result[2] for result in results) / total_requests
        # 转换为百分比
        pd = pd * 100
        
        # 返回完成token的总数和响应时间的列表
        return completion_tokens, response_times, pd

if __name__ == '__main__':

    C = 32  # 最大并发数
    N = 128  # 请求总数

    # vllm 和 ollama 都兼容了 openai 的 api 让测试变得更简单了
    url = 'http://localhost:8080/v1/chat/completions'

    start_time = time.time()
    completion_tokens, response_times, pd = asyncio.run(run(url, C, N))
    end_time = time.time()

    # 计算总时间
    total_time = end_time - start_time
    # 计算每个请求的平均时间
    avg_time_per_request = sum(response_times) / len(response_times)
    # 计算每秒生成的 token 数量
    tokens_per_second = completion_tokens / total_time

    print(f'Performance Results:')
    print(f'  Total requests            : {N}')
    print(f'  Max concurrent requests   : {C}')
    print(f'  Total time                : {total_time:.2f} seconds')
    print(f'  Average time per request  : {avg_time_per_request:.2f} seconds')
    print(f'  Tokens per second         : {tokens_per_second:.2f}')
    print(f'  行数不匹配的概率           : {pd:.2f} %')