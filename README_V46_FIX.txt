V4.6 FIX
Root cause: the scrollable-menu refactor removed self.main creation from _layout(). Startup then called home()->clear(), which requires self.main.
Fix: restore self.main; preserve all 50 menus; retain vertical scrollbar and mouse-wheel navigation; render menu buttons directly in the scrolling inner frame.
