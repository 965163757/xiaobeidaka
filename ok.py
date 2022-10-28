import time
import pymysql
import nonebot
import app
from nonebot import on_command, require, on_request
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot, RequestEvent, FriendRequestEvent

weather = on_command("weather", rule=to_me(), aliases={"天气", "天气预报"}, priority=5)
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler


def mysql(sql):
    conn = pymysql.connect(host='xxxx'  # 连接名称，默认127.0.0.1
                           , user='xxxx'  # 用户名
                           , passwd='xxx'  # 密码
                           , port=3306  # 端口，默认为3306
                           , db='unicom'  # 数据库名称
                           , charset='utf8'  # 字符编码
                           )

    cur = conn.cursor()
    cur.execute(sql)  # 执行SQL语句
    data = cur.fetchall()  # 通过fetchall方法获得数据
    for i in data:  # 打印输出前2条数据
        print(i)
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接
    return data


async def run_every_2_hour():
    sql = "select * from app01_userdata"
    print(sql)
    data = mysql(sql)
    bot=nonebot.get_bot()
    for x in data:
        app.dk(USERNAME=x[0],PASSWORD=x[1],LOCATION=x[2],COORD=x[3],token=x[6])

    await bot.send_private_msg(user_id=965163757, message="定时时间到"+str(data))
    
    pass


scheduler.add_job(run_every_2_hour, "cron", hour="0",minute="22",day="*", id='123')


@weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("city", args)  # 如果用户发送了参数则直接赋值


@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(city: Message = Arg(), city_name: str = ArgPlainText("city")):
    if city_name not in ["北京", "上海"]:  # 如果参数不符合要求，则提示用户重新输入
        # 可以使用平台的 Message 类直接构造模板消息
        await weather.reject(city.template("你想查询的城市 {city} 暂不支持，请重新输入！"))
    city_weather = await get_weather(city_name)
    await weather.finish(city_weather)


# 在这里编写获取天气信息的函数
async def get_weather(city: str) -> str:
    return f"{city}的天气是..."


dk = on_command("dk", aliases={"打卡"}, priority=5)


@dk.handle()
async def _(a: Event):
    user = a.get_user_id()
    print(a.get_user_id())
    bot = nonebot.get_bot()
    sql="select * from app01_userdata where qq=" + user
    print(sql)
    data = mysql(sql)
    print(data)
    await bot.send_private_msg(user_id=965163757, message=str(data))
    await bot.send_private_msg(user_id=965163757, message="添加成功2")
    await dk.finish(str(data))
    # await dk.finish("打开成功");


parseRequest = on_request(priority=1, block=True)


# @event_preprocessor
@parseRequest.handle()
async def _(bot: Bot, event: RequestEvent):
    if isinstance(event, FriendRequestEvent):
        await event.approve(bot)
        # await FriendRequestEvent.approve(event.)
        # await bot.send_private_msg(user_id=bot.self_id, message="添加成功" + str(bot.self_id))
        time.sleep(2)
        await bot.send_private_msg(user_id=event.user_id,
                                   message="你好,你可以发送“打卡”，来尝试手动打卡，第一次使用请打开http://xiaobei.yuanyun.info/填写信息 " + str(event.user_id))
        await bot.send_private_msg(user_id=965163757, message="添加成功" + str(bot.self_id))
        await bot.send_private_msg(user_id=965163757, message="添加成功" + str(event.get_event_name))
