from arclet.alconna import Alconna, Args, CommandMeta
from arclet.alconna.graia import Match, alcommand
from avilla.core import Context, Message, Notice
from richuru import logger
from commspt_bot_avilla.utils.adv_filter import (
    dispatcher_from_preset_cafe,
    dispather_by_admin_only,
)
from commspt_bot_avilla.models.mongodb_data import UIDMapping
from commspt_bot_avilla.utils.random_sleep import random_sleep


@alcommand(
    Alconna(
        r"%uid",
        Args["target", Notice],
        meta=CommandMeta(
            description="查询用户 UID (commspt only)",
            usage=r"%uid <target / qq>",
            example=r"%uid @user",
            author="SerinaNya",
        ),
    )
)
@dispather_by_admin_only
@dispatcher_from_preset_cafe
async def cmd_uid(ctx: Context, target: Match[Notice], message: Message):
    target_qq = int(target.result.target["member"])
    logger.info(f"UID search: {target_qq}")
    uid_mapping = await UIDMapping.fetch(qq=target_qq)
    logger.success(f"UID search: {target_qq} -> {uid_mapping}")
    await random_sleep()
    if uid_mapping:
        await ctx.scene.send_message(
            f"QQ {target_qq} UID {uid_mapping.uid} QMAIL {'✅' if uid_mapping.qmail_verified else '❌'}",
            reply=message,
        )
    else:
        await ctx.scene.send_message(
            f"找不到 {target_qq} 在缓存中的 UID", reply=message
        )
