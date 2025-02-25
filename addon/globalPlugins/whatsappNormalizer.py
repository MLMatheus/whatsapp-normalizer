import unicodedata
import api
import globalPluginHandler

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    WHATSAPP_WINDOW_NAME = "WhatsApp"

    def normalize_text(self, text):
        return unicodedata.normalize("NFKC", text) if text else text

    def is_whatsapp_active(self):
        focus_obj = api.getFocusObject()
        if not focus_obj or not hasattr(focus_obj, "windowText"):
            return False  # Se o objeto não existe ou não tem windowText, sai cedo
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
