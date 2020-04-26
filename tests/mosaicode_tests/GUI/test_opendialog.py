import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from time import sleep
import threading
from tests.mosaicode_tests.test_base import TestBase
from mosaicode.GUI.opendialog import OpenDialog

class TestOpenDialog(TestBase):

    def setUp(self):
        self.dialog = OpenDialog(
                    "Test",
                    self.create_main_window(),
                    "jpg",
                    "."
                    )

        self.dialog = OpenDialog(
                    "Test",
                    self.create_main_window(),
                    None,
                    None
                    )

        self.dialog = OpenDialog(
                    "Test",
                    self.create_main_window(),
                    "jpg",
                    None
                    )

    def test_run(self):
        t1 = threading.Thread(target=self.dialog.run, args=());
        t1.start()
        sleep(0.2)
        while not self.dialog.is_visible():
            sleep(0.1)
        self.dialog.select_filename("LICENSE")
        self.dialog.response(Gtk.ResponseType.OK)
        self.refresh_gui()
        t1.join()

