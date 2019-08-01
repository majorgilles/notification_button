from typing import Optional

from gpiozero import LED
from gpiozero.exc import BadPinFactory

from singleton import Singleton


class NotificationManager(metaclass=Singleton):
    def __init__(self, notification_pin: int, override_pin):
        self.notification_led: Optional[LED] = None
        self.override_light: Optional[LED] = None
        self.is_notifying: bool = False
        self.is_overriding: bool = False
        self.notification_count: int = 0
        self.dismissal_count: int = 0
        self.override_count: int = 0

        try:
            self.notification_led = LED(notification_pin)
            self.override_light = LED(override_pin)
        except BadPinFactory:
            pass

    def notify(self):
        if not self.is_notifying:
            self.is_notifying = True
            self.notification_count += 1

            if self.notification_led:
                self.notification_led.on()

    def dismiss(self, override=False):
        if self.is_notifying:
            self.is_notifying = False
            if not override:
                self.dismissal_count += 1

            if self.notification_led:
                self.notification_led.off()

    def override(self):
        if not self.is_overriding:
            self.dismiss(override=True)
            self.override_count += 1

            if self.override_light:
                self.override_light.on()
