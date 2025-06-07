from rubpy import Client
from rubpy.types import Updates
import aiohttp , re

bot = Client("rubpy")

GROUP_GUID = "g0F3Kj30ad949d2c2ab97ff036386cff"  # جایگزین کن با گوید گپ خودت

@bot.on_message_updates()
async def rubino_handler(update: Updates):
    try:
        if update.object_guid != GROUP_GUID:
            return

        if not update.text or not update.text.startswith("روبینو"):
            return
        match = re.match(r"^روبینو\s+(.+)", update.text)
        if not match:
            return await update.reply("❗️ لینک روبینو را وارد کن.")
        rubino_url = match.group(1).strip()
        api_url = f"https://api-free.ir/api/rubino-dl.php?url={rubino_url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    return await update.reply("❌ خطا در ارتباط با سرور.")
                data = await response.json()
                result = data.get("result", {})
                video_url = result.get("url")
                caption = result.get("caption", "")

                if not video_url:
                    return await update.reply("❌ لینک ویدیو پیدا نشد.")
                await update.reply(f"{video_url}\n\n{caption}")

    except Exception as e:
        await update.reply(f"⚠️ خطا: {e}")

bot.run()