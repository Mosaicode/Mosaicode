from tests.mosaicode_tests.test_base import TestBase
from mosaicode.plugins.extensionsmanager.GUI.blockmanager import BlockManager
from mosaicode.plugins.extensionsmanager.GUI.blockeditor import BlockEditor
from mosaicode.plugins.extensionsmanager.GUI.blockcommoneditor \
    import BlockCommonEditor


class TestBlockCommonEditor(TestBase):

    def setUp(self):
        block = self.create_block()
        block_manager = BlockManager(self.create_main_window())
        block_editor = BlockEditor(block_manager, block)
        self.widget = BlockCommonEditor(block_editor, block)

    def test_base(self):
        block = self.create_block()
        block_manager = BlockManager(self.create_main_window())
        block_editor = BlockEditor(block_manager, block)
        self.widget = BlockCommonEditor(block_editor, block)
