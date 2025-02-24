import sys
sys.dont_write_bytecode = True  # 禁止生成 __pycache__

from telethon.tl.functions.messages import GetFullChatRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.sync import TelegramClient
from telethon.tl.types import User, Channel, Chat
import openpyxl
from openpyxl.utils import get_column_letter
import os
from datetime import datetime

# Telegram API 配置
# 请从 https://my.telegram.org/apps 获取这些值
API_ID = 28330065  # 修改为新的 API_ID
API_HASH = 'f26de618b5433c51826eb48642a00ddf'  # 修改为新的 API_HASH

def adjust_column_width(worksheet):
    """自动调整列宽"""
    for column in worksheet.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column_letter].width = adjusted_width

async def get_chat_invite_link(client, entity):
    """获取群组/频道的邀请链接"""
    try:
        # 首先尝试获取公开链接
        if hasattr(entity, 'username') and entity.username:
            return f"https://t.me/{entity.username}"
        
        # 如果是超级群组或频道，尝试获取邀请链接
        if isinstance(entity, Channel):
            try:
                full_entity = await client(GetFullChannelRequest(entity))
                if hasattr(full_entity.full_chat, 'invite_link') and full_entity.full_chat.invite_link:
                    return full_entity.full_chat.invite_link
            except Exception as e:
                print(f"获取邀请链接时出错: {str(e)}")
        
        # 如果是普通群组，尝试获取邀请链接
        elif isinstance(entity, Chat):
            try:
                full_chat = await client(GetFullChatRequest(entity.id))
                if hasattr(full_chat.full_chat, 'invite_link') and full_chat.full_chat.invite_link:
                    return full_chat.full_chat.invite_link
            except Exception as e:
                print(f"获取群组链接时出错: {str(e)}")
    except Exception as e:
        print(f"获取链接时出错: {str(e)}")
    return '无链接'

async def export_data(
    export_contacts=True,
    export_groups=True,
    export_channels=True,
    export_bots=True,
    stop_check=None
):
    print("正在启动 Telegram 客户端...")
    client = TelegramClient('session_name', API_ID, API_HASH)
    
    # 添加中文提示
    client.flood_sleep_threshold = 0
    client.parse_mode = 'html'
    
    # 重写 TelegramClient 的 _parse_phone_number 方法来修改提示
    def custom_parse_phone(self, phone):
        return phone
    
    # 重写 TelegramClient 的 start 方法来修改提示
    original_start = client.start
    async def custom_start():
        try:
            while True:
                try:
                    return await original_start(
                        phone=lambda: input("请输入手机号 (格式如: +8613812345678): ").strip(),
                        password=lambda: input("请输入两步验证密码: "),
                        code_callback=lambda: input("请输入收到的验证码: ").strip(),
                        first_name=lambda: "User",
                        last_name=lambda: "Name"
                    )
                except EOFError:
                    print("\n错误：输入被中断")
                    print("请重新输入手机号")
                    continue
        except Exception as e:
            error_msg = str(e).lower()
            if "phone number has been banned" in error_msg:
                print("\n错误：此手机号已被 Telegram 封禁，无法继续使用。")
                print("建议：")
                print("1. 使用其他未被封禁的手机号")
                print("2. 如果认为是误封，可以访问 https://www.telegram.org/faq_spam 申诉")
                input("\n按回车键退出...")
                sys.exit(1)
            else:
                print(f"\n登录出错: {str(e)}")
                raise e
    
    client.start = custom_start
    
    print("正在连接到 Telegram...")
    await client.start()
    print("已成功连接！")

    # 询问是否开始导出
    while True:
        choice = input("\n是否开始导出数据？(y/n): ").strip().lower()
        if choice == 'y':
            break
        elif choice == 'n':
            print("已取消导出，程序退出")
            await client.disconnect()
            return
        else:
            print("无效的输入，请输入 y 或 n")

    print("\n开始导出数据...")
    export_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    export_dir = f'tg_export_{export_time}'
    os.makedirs(export_dir, exist_ok=True)

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    
    # 获取所有对话
    dialogs = await client.get_dialogs()
    
    try:
        if export_contacts:
            if stop_check and stop_check(): return
            print("\n[任务] 正在导出联系人信息")
            # 获取所有对话中的用户
            users = []
            for dialog in dialogs:
                if isinstance(dialog.entity, User) and not dialog.entity.bot and not dialog.entity.deleted:
                    users.append(dialog.entity)
            
            print(f"[进度] 共发现 {len(users)} 个联系人")
            ws_contacts = wb.create_sheet("联系人")
            ws_contacts.append(['用户ID', '用户名', '手机号码', '姓名', '状态'])
            
            for i, user in enumerate(users, 1):
                if stop_check and stop_check(): return
                status = "正常"
                if user.deleted:
                    status = "已注销"
                elif user.restricted:
                    # 获取限制原因
                    reasons = []
                    if hasattr(user, 'restriction_reason'):
                        for restriction in user.restriction_reason:
                            reasons.append(restriction.text)
                    status = f"受限制 ({', '.join(reasons)})" if reasons else "受限制"
                ws_contacts.append([
                    str(user.id),
                    f"https://t.me/{user.username}" if user.username else '',
                    user.phone if hasattr(user, 'phone') else '',
                    f"{user.first_name or ''} {user.last_name or ''}".strip(),
                    status
                ])
                print(f"[进度] 已处理 {i} 个联系人")
            
            adjust_column_width(ws_contacts)

        if export_groups:
            if stop_check and stop_check(): return
            print("\n[任务] 正在导出群组信息")
            groups = [d for d in dialogs if d.is_group]
            print(f"[进度] 共发现 {len(groups)} 个群组")
            ws_groups = wb.create_sheet("群组")
            ws_groups.append(['群组ID', '群组名称', '邀请链接', '状态'])
            
            for i, group in enumerate(groups, 1):
                if stop_check and stop_check(): return
                entity = group.entity
                if isinstance(entity, (Chat, Channel)) and not getattr(entity, 'broadcast', False):
                    try:
                        status = "正常"
                        if getattr(entity, 'left', False):
                            status = "已退出"
                        elif getattr(entity, 'kicked', False):
                            status = "已被踢出"
                        elif getattr(entity, 'restricted', False):
                            # 获取限制原因
                            reasons = []
                            if hasattr(entity, 'restriction_reason'):
                                for restriction in entity.restriction_reason:
                                    reasons.append(restriction.text)
                            status = f"受限制 ({', '.join(reasons)})" if reasons else "受限制"
                        invite_link = await get_chat_invite_link(client, entity)
                        ws_groups.append([
                            str(entity.id),
                            entity.title,
                            invite_link,
                            status
                        ])
                    except Exception as e:
                        print(f"处理群组时出错: {e}")
                print(f"[进度] 已处理 {i} 个群组")
            adjust_column_width(ws_groups)

        if export_channels:
            if stop_check and stop_check(): return
            print("\n[任务] 正在导出频道信息")
            channels = [d for d in dialogs if isinstance(d.entity, Channel) and getattr(d.entity, 'broadcast', False)]
            print(f"[进度] 共发现 {len(channels)} 个频道")
            ws_channels = wb.create_sheet("频道")
            ws_channels.append(['频道ID', '频道名称', '频道链接', '状态'])
            
            for i, dialog in enumerate(channels, 1):
                if stop_check and stop_check(): return
                entity = dialog.entity
                try:
                    status = "正常"
                    if getattr(entity, 'left', False):
                        status = "已退出"
                    elif getattr(entity, 'kicked', False):
                        status = "已被踢出"
                    elif getattr(entity, 'restricted', False):
                        # 获取限制原因
                        reasons = []
                        if hasattr(entity, 'restriction_reason'):
                            for restriction in entity.restriction_reason:
                                reasons.append(restriction.text)
                        status = f"受限制 ({', '.join(reasons)})" if reasons else "受限制"
                    channel_link = await get_chat_invite_link(client, entity)
                    ws_channels.append([
                        str(entity.id),
                        entity.title,
                        channel_link,
                        status
                    ])
                except Exception as e:
                    print(f"处理频道时出错: {e}")
                print(f"[进度] 已处理 {i} 个频道")
            adjust_column_width(ws_channels)

        if export_bots:
            if stop_check and stop_check(): return
            print("\n[任务] 正在导出机器人信息")
            bots = [d for d in dialogs if isinstance(d.entity, User) and getattr(d.entity, 'bot', False)]
            print(f"[进度] 共发现 {len(bots)} 个机器人")
            ws_bots = wb.create_sheet("机器人")
            ws_bots.append(['机器人ID', '用户名', '机器人名称', '状态'])
            
            for i, dialog in enumerate(bots, 1):
                if stop_check and stop_check(): return
                entity = dialog.entity
                try:
                    status = "正常"
                    if getattr(entity, 'restricted', False):
                        status = "已限制"
                    ws_bots.append([
                        str(entity.id),
                        f"https://t.me/{entity.username}" if entity.username else '',
                        f"{entity.first_name or ''} {entity.last_name or ''}".strip(),
                        status
                    ])
                except Exception as e:
                    print(f"处理机器人时出错: {e}")
                print(f"[进度] 已处理 {i} 个机器人")
            adjust_column_width(ws_bots)

        # 保存Excel文件
        excel_file = os.path.join(export_dir, 'telegram_export.xlsx')
        wb.save(excel_file)
        print(f"\n[完成] 导出完成！文件保存在 {export_dir} 目录下")

    finally:
        await client.disconnect()

if __name__ == '__main__':
    import asyncio
    asyncio.run(export_data()) 