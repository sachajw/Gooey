'''
Created on Jan 19, 2014

New plan: 

  fuck the multi-component thing.

  Bind and unbind the buttons on the panels.

@author: Chris
'''

import os
import wx
import sys
import header

from gooey import i18n
from gooey.gui import footer
from gooey import image_repository
from gooey.gui.controller import Controller
from gooey.gui.runtime_display_panel import RuntimeDisplay


class BaseWindow(wx.Frame):
  def __init__(self, BodyPanel, model, payload, params):
    wx.Frame.__init__(self, parent=None, id=-1)

    self._params = params
    self._model = model
    self._payload = payload

    self._controller = None

    # Components
    self.icon = None
    self.head_panel = None
    self.config_panel = None
    self.runtime_display = None
    self.foot_panel = None
    self.panels = None

    self._init_properties()
    self._init_components(BodyPanel)
    self._do_layout()
    self._init_controller()
    self.registerControllers()


  def _init_properties(self):
    if not self._params['program_name']:
      title = os.path.basename(sys.argv[0].replace('.py', ''))
    else:
      title = self._params['program_name']
    self.SetTitle(title)
    self.SetSize((610, 530))
    self.SetMinSize((400, 300))
    self.icon = wx.Icon(image_repository.icon, wx.BITMAP_TYPE_ICO)
    self.SetIcon(self.icon)

  def _init_components(self, BodyPanel):
    # init gui
    self.head_panel = header.FrameHeader(
        heading=i18n.translate("settings_title"),
        subheading=self._model.description,
        parent=self)
    self.config_panel = BodyPanel(self)
    self.runtime_display = RuntimeDisplay(self)
    self.foot_panel = footer.Footer(self, self._controller)
    self.panels = [self.head_panel, self.config_panel, self.foot_panel]

  def _do_layout(self):
    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(self.head_panel, 0, wx.EXPAND)
    self._draw_horizontal_line(sizer)
    sizer.Add(self.config_panel, 1, wx.EXPAND)
    self.runtime_display.Hide()
    sizer.Add(self.runtime_display, 1, wx.EXPAND)
    self._draw_horizontal_line(sizer)
    sizer.Add(self.foot_panel, 0, wx.EXPAND)
    self.SetSizer(sizer)

  def _draw_horizontal_line(self, sizer):
    line = wx.StaticLine(self, -1, style=wx.LI_HORIZONTAL)
    line.SetSize((10, 10))
    sizer.Add(line, 0, wx.EXPAND)

  def _init_controller(self):
    self._controller = Controller(
        base_frame=self,
        head_panel=self.head_panel,
        body_panel=self.config_panel,
        footer_panel=self.foot_panel,
        model=self._model)

  def registerControllers(self):
    for panel in self.panels:
      panel.RegisterController(self._controller)

  def NextPage(self):
    self.head_panel.NextPage()
    self.foot_panel.NextPage()
    self.config_panel.Hide()
    self.runtime_display.Show()
    self.Layout()

  def AttachPayload(self, payload):
    self._payload = payload

  def ManualStart(self):
    self._controller.ManualStart()


if __name__ == '__main__':
  pass