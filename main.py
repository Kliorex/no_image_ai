from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

@register(
    "astrbot_plugin_ignore_pure_image",
    "local",
    "纯图片消息一律不回",
    "1.0.0",
)
class IgnorePureImagePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(filter.EventMessageType.ALL, priority=100)
    async def on_message(self, event: AstrMessageEvent):
        chain = event.message_obj.message or []
        has_image = any(isinstance(c, Comp.Image) for c in chain)
        if not has_image:
            return

        # 有效文字：去掉空白后的纯文本
        text = (event.message_str or "").strip()
        # 若只有图片（或图+表情等），没有有效文字 → 静默
        if not text:
            logger.info(
                f"[ignore_pure_image] 拦截纯图片 message_id={getattr(event.message_obj, 'message_id', '')}"
            )
            event.stop_event()
            return
