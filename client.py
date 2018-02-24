from indi.client.Client import Client
from indi.transport.client import TCP
from indi.message import const
from indi.client import elements

import weakref
import npyscreen
import threading

weakref.ReferenceError = ReferenceError

ip = '127.0.0.1'
port = 7624

conn = TCP(ip, port)

control_connection = TCP()
blob_connection = TCP()


class TestApp(npyscreen.StandardApp):
    def __init__(self):
        super().__init__()
        self.form = None
        self.client = None
        self.callbacks = 0
        self.last_callbacks = None

    def main(self):
        npyscreen.setTheme(npyscreen.Themes.DefaultTheme)
        self.update_form()

    def client_callback(self, sender):
        self.callbacks += 1
        self.queue_event(
            npyscreen.Event(name='set', payload=sender)
        )

    def start_client(self):
        client = Client(control_connection, blob_connection)
        client.onchange(callback=self.client_callback, what=None)
        self.client = client

        def client_th():
            client.start()

        th = threading.Thread(target=client_th, daemon=True)
        th.start()

    def add_handlers(self):
        self.add_event_hander('set', self.event_handler)

    def event_handler(self, event):
        if self.last_callbacks != self.callbacks:
            self.last_callbacks = self.callbacks
            self.update_form()

    def update_form(self):
        self.form = npyscreen.Form(name="Welcome to Npyscreen", parentApp=self)
        for device in self.client.devices:
            self.form.add(
                npyscreen.TitleFixedText,
                name=device,
                begin_entry_at=24,
            )
            for vector in self.client[device].vectors:
                color = 'GOOD' if self.client[device][vector].state == const.State.OK else 'CAUTION'
                self.form.add(
                    npyscreen.TitleFixedText,
                    name=vector,
                    begin_entry_at=24,
                    relx=5,
                    labelColor=color,
                )
                for element in self.client[device][vector].elements:
                    el = self.client[device][vector][element]
                    self.form.add(
                        npyscreen.TitleFixedText,
                        name=element,
                        value=el.value,
                        begin_entry_at=24,
                        relx=10,
                        labelColor='DEFAULT',
                    )
        self.form.edit()


if __name__ == "__main__":
    App = TestApp()
    App.add_handlers()
    App.start_client()
    App.run()
