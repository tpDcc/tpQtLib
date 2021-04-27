#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation for DCC toolsets
"""

from __future__ import print_function, division, absolute_import

import os
import re
import logging
from collections import OrderedDict

from tpDcc.libs.python import python, color, decorators, folder, yamlio
from tpDcc.libs.plugin.core import factory

from tpDcc.managers import configs
from tpDcc.libs.qt.core import consts
from tpDcc.libs.qt.widgets import toolset

if python.is_python2():
    import pkgutil as loader
else:
    import importlib as loader

logger = logging.getLogger(consts.LIB_ID)


@decorators.add_metaclass(decorators.Singleton)
class ToolsetsManager(factory.PluginFactory):

    REGEX_FOLDER_VALIDATOR = re.compile('^((?!__pycache__)(?!dccs)(?!plugins).)*$')

    def __init__(self):
        super(ToolsetsManager, self).__init__(interface=toolset.ToolsetWidget)

        self._toolsets = dict()
        self._toolset_groups = dict()
        self._registered_file_paths = dict()

    # ============================================================================================================
    # PROPERTIES
    # ============================================================================================================

    @property
    def toolset_groups(self):
        return self._toolset_groups

    # ============================================================================================================
    # TOOLSETS
    # ============================================================================================================

    def register_package_toolsets(self, package_name, toolsets_file_path, toolsets_paths):

        self._load_registered_paths_toolsets(package_name, toolsets_file_path)

        if not toolsets_paths:
            return
        toolsets_paths = python.remove_dupes(python.force_list(toolsets_paths))
        self.register_paths(toolsets_paths, package_name=package_name)

        if package_name not in self._toolsets:
            self._toolsets[package_name] = list()
        toolset_data = self.plugins(package_name)
        if not toolset_data:
            return True

        for toolset in self.plugins(package_name=package_name):
            if not toolset:
                continue

            if not toolset.PACKAGE:
                toolset.PACKAGE = package_name

        for tool_set in toolset_data:
            if tool_set.ID not in self._toolsets[package_name]:
                toolset_config = configs.get_tool_config(tool_set.ID, package_name=package_name)
                if not toolset_config:
                    logger.warning(
                        'No valid configuration file found for toolset: "{}" in package: "{}"'.format(
                            tool_set.ID, package_name))
                    continue
                tool_set.CONFIG = toolset_config
                self._toolsets[package_name].append({tool_set.ID: tool_set})

        return True

    def toolset(self, toolset_id, package_name=None, as_dict=False):
        """
        Returns toolset based on its ID
        :param toolset_id: str
        :param package_name: str
        :param as_dict: bool
        :return: ToolsetWidget
        """

        if not package_name:
            package_name = toolset_id.replace('.', '-').split('-')[0]

        package_toolsets = self._toolsets.get(package_name)
        if not package_toolsets:
            logger.warning('No toolsets found in package: {}!'.format(package_name))
            return None

        toolset_found = None
        for package_toolset in package_toolsets:
            if toolset_id in package_toolset:
                toolset_found = package_toolset
                break

        if not toolset_found:
            logger.warning('Toolset "{}" not found in package: "{}".'.format(toolset_id, package_name))
            return None

        if as_dict:
            return toolset_found
        else:
            return toolset_found[toolset_id]

    def toolset_ids(self, group_type, package_name=None):
        """
        Returns all toolsets in a given group type
        :param group_type: str
        :param package_name: str
        :return: list
        """

        if not self._toolset_groups:
            return None
        if package_name and package_name not in self._toolset_groups:
            return None

        toolsets_found = list()
        for pkg_name, toolset_groups in self._toolset_groups.items():
            for toolset_group in toolset_groups:
                if package_name and package_name != pkg_name:
                    continue
                if toolset_group['type'] == group_type:
                    toolsets_found.extend(toolset_group['toolsets'])

        return list(set(toolsets_found))

    def toolsets(self, group_type, package_name=None, as_dict=False):
        """
        Returns all toolsets available in a given group type
        :param group_type: str
        :param package_name: str
        :param as_dict: bool
        :return: list(ToolsetWidget)
        """

        toolsets_found = list()
        toolset_ids = self.toolset_ids(group_type, package_name=package_name)
        for toolset_id in toolset_ids:
            new_toolset = self.toolset(toolset_id, package_name=package_name, as_dict=as_dict)
            if not new_toolset:
                continue
            toolsets_found.append(new_toolset)

        return toolsets_found

    def toolset_widgets(self, package_name=None, sort=True):
        """
        Returns a list with toolset widgets
        :param package_name: str
        :param sort: bool
        :return:
        """

        toolset_widgets = list()

        if package_name and package_name not in self._toolsets:
            return

        if package_name:
            toolset_widgets = self._toolsets[package_name].values()
        else:
            for package_name, toolsets in self._toolsets.items():
                for toolset_found in toolsets:
                    for toolset_id, toolset_widget in toolset_found.items():
                        toolset_widgets.append(toolset_widget)

        if sort:
            toolset_widgets.sort(key=lambda toolset_widget_found: toolset_widget_found.CONFIG.get('name'))

        return toolset_widgets

    def toolset_color(self, toolset_id, package_name=None):
        """
        Returns the color of the toolset and shifts it if necessary
        :param toolset_id: str
        :param package_name: str
        :return: tuple(float, float, float)
        """

        if not toolset_id:
            return 255, 255, 255

        if not package_name:
            package_name = toolset_id.replace('.', '-').split('-')[0]

        if self._toolset_groups and package_name in self._toolset_groups:
            for pkg_name, toolset_groups in self._toolset_groups.items():
                if package_name != pkg_name:
                    continue
                for toolset_group in toolset_groups:
                    if toolset_id in toolset_group['toolsets']:
                        index = toolset_group['toolsets'].index(toolset_id)
                        group_color = tuple(toolset_group['color'])
                        hue_shift = toolset_group['hue_shift'] * (index + 1)
                        return tuple(color.hue_shift(group_color, hue_shift))
        else:
            logger.warning(
                'ToolSet "{}" not found in any toolset group. Impossible to retrieve color!'.format(toolset_id))
            return 255, 255, 255

    def toolset_menu(self, toolset_type=None, package_name=None):
        """
        Returns the menu data of the given toolset
        :param toolset_type: str
        :param package_name: str
        :return: list(list)
        """

        if not package_name:
            package_name = toolset_type.replace('.', '-').split('-')[0]

        toolset_menus = list()

        if self._toolset_groups and package_name in self._toolset_groups:
            for pkg_name, toolset_groups in self._toolset_groups.items():
                if package_name != pkg_name:
                    continue
                for toolset_group in toolset_groups:
                    if toolset_type:
                        if toolset_group['type'] != toolset_type:
                            continue
                    toolset_menus.append(toolset_group.get('menu', list()))
        else:
            logger.warning(
                'Toolset "{}" not found in any toolset group. Impossible to retrieve menu data!'.format(toolset_type))

        return toolset_menus

    def group_types(self):
        found_group_types = list()
        for pkg_name, toolset_groups in self._toolset_groups.items():
            for toolset_group in toolset_groups:
                found_group_types.append(toolset_group['name'])

        return found_group_types

    def group_type(self, group_name):
        """
        Returns type by group name
        :param group_name: str
        :return: str
        """

        for pkg_name, toolset_groups in self._toolset_groups.items():
            for toolset_group in toolset_groups:
                if toolset_group['name'] == group_name:
                    return toolset_group['type']

        return None

    def group_color(self, group_type, package_name=None):
        """
        Returns color by group type
        :param group_type: str
        :param package_name: str
        :return: str
        """

        if not self._toolset_groups:
            return

        for pkg_name, toolset_groups in self._toolset_groups.items():
            if package_name and pkg_name != package_name:
                continue
            for toolset_group in toolset_groups:
                if toolset_group['type'] == group_type:
                    return toolset_group['color']

        return None

    def group_from_toolset(self, toolset_id, package_name=None):
        """
        Returns group of given toolset
        :param toolset_id: str
        :param package_name: str
        :return: str
        """

        if not self._toolset_groups:
            return

        for pkg_name, toolset_groups in self._toolset_groups.items():
            if package_name and pkg_name != package_name:
                continue
            for toolset_group in toolset_groups:
                for tool_set in toolset_group['toolsets']:
                    if tool_set == toolset_id:
                        return toolset_group['type']

        return None

    # ============================================================================================================
    # INTERNAL
    # ============================================================================================================

    def _load_registered_paths_toolsets(self, package_name, toolsets_file_paths):
        """
        Loads all toolsets found in registered paths
        """

        if not toolsets_file_paths:
            return

        toolsets_file_paths = python.remove_dupes(python.force_list(toolsets_file_paths))

        # Load toolsets data
        for registered_path in toolsets_file_paths:
            if not registered_path or not os.path.isdir(registered_path):
                continue
            for pth in folder.get_files_with_extension(
                    toolset.ToolsetWidget.EXTENSION, registered_path, full_path=True, recursive=True):
                try:
                    toolset_data = yamlio.read_file(pth, maintain_order=True)
                except Exception:
                    logger.warning('Impossible to read toolset data from: "{}!'.format(pth))
                    continue
                if package_name not in self._toolset_groups:
                    self._toolset_groups[package_name] = list()
                toolset_type = toolset_data.get('type')
                toolset_not_added = True
                for pkg_name, toolset_groups in self._toolset_groups.items():
                    for toolset_group in toolset_groups:
                        if toolset_type == toolset_group['type'] and pkg_name == package_name:
                            toolset_not_added = False
                            break
                    if not toolset_not_added:
                        break
                if toolset_not_added:
                    self._toolset_groups[package_name].append(toolset_data)
