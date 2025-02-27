import unicodedata
import api
import globalPluginHandler
import threading
import time

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    WHATSAPP_WINDOW_NAME = "WhatsApp"

    def __init__(self):
        super().__init__()
        self.last_clipboard_text = None
        self.running = True
        self.clipboard_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.clipboard_thread.start()

    def normalize_text(self, text):
        return unicodedata.normalize("NFKC", text) if text else text

    def is_whatsapp_active(self):
        focus_obj = api.getFocusObject()
        if not focus_obj or not hasattr(focus_obj, "windowText"):
            return False
        window_name = focus_obj.windowText
        return window_name and self.WHATSAPP_WINDOW_NAME.lower() in window_name.lower()

    def event_gainFocus(self, obj, nextHandler):
        if self.is_whatsapp_active() and hasattr(obj, "name"):
            self.normalize_object_name(obj)
        nextHandler()

    def normalize_object_name(self, obj):
        original_text = obj.name
        normalized_text = self.normalize_text(original_text)

        if original_text != normalized_text:
            obj.name = normalized_text

    def monitor_clipboard(self):
        while self.running:
            if self.is_whatsapp_active():
                text = api.getClipData()
                if text and text != self.last_clipboard_text:
                    normalized_text = self.normalize_text(text)
                    if text != normalized_text:
                        api.copyToClip(normalized_text)
                        self.last_clipboard_text = normalized_text

            time.sleep(0.5)

    def terminate(self):
        self.running = False
        self.clipboard_thread.join(timeout=1)
