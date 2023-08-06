from django.contrib import messages


class FlashNotifier:
    FIVE_SECONDS = 5 * 1000
    ALERT_CLASSES = 'alert alert-dismissible fade show'

    def __init__(self, request):
        self.request = request

    def info(self, text: str, delay: int = FIVE_SECONDS):
        messages.add_message(
            self.request, level=messages.INFO, message=text,
            extra_tags=f'{self.ALERT_CLASSES} alert-primary delay-{delay}'
        )

    def error(self, text: str, delay: int = FIVE_SECONDS):
        messages.add_message(
            self.request, level=messages.ERROR, message=text,
            extra_tags=f'{self.ALERT_CLASSES} alert-danger delay-{delay}'
        )
