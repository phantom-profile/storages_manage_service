from django.contrib import messages


class FlashNotifier:
    def __init__(self, request):
        self.request = request

    def info(self, text: str):
        messages.add_message(
            self.request, level=messages.INFO, message=text,
            extra_tags='alert alert-primary alert-dismissible fade show'
        )

    def error(self, text: str):
        messages.add_message(
            self.request, level=messages.ERROR, message=text,
            extra_tags='alert alert-danger alert-dismissible fade show'
        )
