# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------
"""
This module contains the PortControl class.
"""
import ast
import os
import inspect  # For module inspect
import pkgutil  # For dynamic package load
import harpia.plugins
from os.path import expanduser
from harpia.utils.XMLUtils import XMLParser
from harpia.model.plugin import Plugin

class PluginControl():
    """
    This class contains methods related the PortControl class.
    """

    # ----------------------------------------------------------------------

    def __init__(self):
        pass

    # ----------------------------------------------------------------------
    @classmethod
    def load_plugins(cls, system):
        system.plugins.clear()
        # First load ports on python classes.
        # They are installed with harpia as root 
        for importer, modname, ispkg in pkgutil.walk_packages(
                harpia.plugins.__path__,
                harpia.plugins.__name__ + ".",
                None):
            if ispkg:
                continue
            module = __import__(modname, fromlist="dummy")
            for name, obj in inspect.getmembers(module):
                if not inspect.isclass(obj):
                    continue
                modname = inspect.getmodule(obj).__name__
                if not modname.startswith("harpia.plugins"):
                    continue
                instance = obj()
                if not isinstance(instance, Plugin):
                    continue
                if instance.get_label() == "":
                    continue
                system.plugins[instance.type] = instance

        #Now load the XML from user space
        from harpia.system import System
        home_dir = System.get_user_dir()
        if not os.path.isdir(home_dir):
            return
        if not os.path.exists(home_dir):
            return
        for file in os.listdir(home_dir):
            if not file.endswith(".xml"):
                continue
            instance = PluginControl.load(home_dir + "/" + file)
            if instance is None:
                continue
            instance.source = "xml"
            system.plugins[instance.type] = instance

    # ----------------------------------------------------------------------
    @classmethod
    def load(cls, file_name):
        """
        This method loads the plugin from XML file.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        if os.path.exists(file_name) is False:
            return
        parser = XMLParser(file_name)
        plugin = Plugin()

        plugin.type = parser.getTagAttr("HarpiaPlugin", "type")
        plugin.language = parser.getTagAttr("HarpiaPlugin",  "language")
        plugin.framework = parser.getTagAttr("HarpiaPlugin",  "framework")

        plugin.label = parser.getTagAttr("HarpiaPlugin",  "label")
        plugin.group = parser.getTagAttr("HarpiaPlugin",  "group")
        plugin.color = parser.getTagAttr("HarpiaPlugin",  "color")
        plugin.help = parser.getTagAttr("HarpiaPlugin",  "help")
        plugin.source = parser.getTagAttr("HarpiaPlugin",  "source")

        plugin.header = parser.getTagAttr("HarpiaPlugin",  "header")
        plugin.vars = parser.getTagAttr("HarpiaPlugin",  "vars")
        plugin.function_call = parser.getTagAttr("HarpiaPlugin",  "function_call")
        plugin.dealloc = parser.getTagAttr("HarpiaPlugin",  "dealloc")
        plugin.out_dealloc = parser.getTagAttr("HarpiaPlugin",  "out_dealloc")

        props = parser.getTag("HarpiaPlugin").getTag(
                    "properties").getChildTags("property")
        for prop in props:
            plugin.properties.append(ast.literal_eval(prop.getAttr("value")))

        if plugin.get_type() == "harpia.model.plugin":
            return None
        return plugin

    # ----------------------------------------------------------------------
    @classmethod
    def save(cls, plugin):
        """
        This method save the plugin in user space.

        Returns:

            * **Types** (:class:`boolean<boolean>`)
        """
        from harpia.system import System
        plugin.source = "xml"
        parser = XMLParser()
        parser.addTag('HarpiaPlugin')
        parser.setTagAttr('HarpiaPlugin','type', plugin.type)
        parser.setTagAttr('HarpiaPlugin','language', plugin.language)
        parser.setTagAttr('HarpiaPlugin','framework', plugin.framework)

        parser.setTagAttr('HarpiaPlugin','label', plugin.label)
        parser.setTagAttr('HarpiaPlugin','group', plugin.group)
        parser.setTagAttr('HarpiaPlugin','color', plugin.color)
        parser.setTagAttr('HarpiaPlugin','help', plugin.help)
        parser.setTagAttr('HarpiaPlugin','source', plugin.source)

        parser.setTagAttr('HarpiaPlugin','header', plugin.header)
        parser.setTagAttr('HarpiaPlugin','vars', plugin.vars)
        parser.setTagAttr('HarpiaPlugin','function_call', plugin.function_call)
        parser.setTagAttr('HarpiaPlugin','dealloc', plugin.dealloc)
        parser.setTagAttr('HarpiaPlugin','out_dealloc', plugin.out_dealloc)

        parser.appendToTag('HarpiaPlugin', 'properties')

        for key in plugin.properties:
            parser.appendToTag('properties', 'property', value=key)

        try:
            file_name = System.get_user_dir() + "/" + plugin.get_type() + ".xml"
            plugin_file = file(os.path.expanduser(file_name), 'w')
            plugin_file.write(parser.getXML())
            plugin_file.close()
        except IOError as e:
            return False
        return True

    # ----------------------------------------------------------------------
    @classmethod
    def add_plugin(cls, plugin):
        # first, save it
        PluginControl.save(plugin)
        # Then add it to system
        from harpia.system import System
        System.plugins[plugin.get_type()] = plugin

    # ----------------------------------------------------------------------
    @classmethod
    def delete_plugin(cls, plugin):
        from harpia.system import System
        if plugin.source == "xml":
            file_name = System.get_user_dir() + "/" + plugin.get_type() + ".xml"
            os.remove(file_name)
            PluginControl.load_plugins(System)
            return True
        else:
            return False
# ----------------------------------------------------------------------
