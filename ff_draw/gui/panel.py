import logging
import math
import os
import typing

import glfw
import glm
import imgui

if typing.TYPE_CHECKING:
    from . import Drawing
main_page = 'FFDraw'


class FFDPanel:
    logger = logging.getLogger('Panel')

    def __init__(self, gui: 'Drawing'):
        self.main = gui.main
        self.renderer = gui.imgui_panel_renderer
        self.window = gui.window_panel
        self.is_expand = True
        self.is_show = True
        self.show_exit_process = False

        self.current_page = ''

        self.cached_tid = -1
        self.territory = ''

        self.cached = ''

    def ffd_page(self):
        mem = self.main.mem

        imgui.text(f'pid: {mem.pid}')
        imgui.same_line()
        if self.show_exit_process:
            if imgui.button(f'kill process!'):
                from nylib.utils.win32.winapi.kernel32 import TerminateProcess
                TerminateProcess(mem.handle, 0)
                os._exit(0)
        else:
            self.show_exit_process = imgui.button(f'kill process?')

        if me := mem.actor_table.me:
            imgui.text(f'me: {me.name}#{me.id:#x}')
            tinfo = mem.territory_info
            tid = tinfo.territory_id
            if tid != self.cached_tid:
                self.cached_tid = tid
                try:
                    territory = self.main.sq_pack.sheets.territory_type_sheet[tid]
                except KeyError:
                    self.territory = 'N/A'
                else:
                    self.territory = f'{territory.region.text_sgl}-{territory.sub_region.text_sgl}-{territory.area.text_sgl}'
            imgui.text(f'territory: {self.territory}')
            imgui.text(f'[Tid: {tid}][Layer: {tinfo.layer_id}][Weather: {tinfo.weather_id}/{tinfo.weather_is_content}]')
            imgui.text(f'pos: {me.pos}#{me.facing / math.pi:.2f}pi')
        else:
            imgui.text(f'me: N/A')

        if imgui.tree_node('EventModule'):
            if imgui.tree_node('ContentInfo'):
                try:
                    cinfo = mem.event_module.content_info
                    imgui.text(f'handler_id: {cinfo.handler_id:#X}')
                    imgui.text(f'content_id: {cinfo.content_id:#X}')
                    imgui.text(f'title: {cinfo.title}')
                    imgui.text(f'text1: {cinfo.text1}')
                    imgui.text(f'text2: {cinfo.text2}')
                    imgui.text('todo_list')
                    if imgui.tree_node('Todo List'):
                        try:
                            for todo in cinfo.todo_list:
                                if not todo.is_valid: break
                                imgui.text(f'[{todo.is_finished}]{todo.desc}')
                        except Exception as e:
                            imgui.text('N/A - ' + str(e))
                        imgui.tree_pop()
                except Exception as e:
                    imgui.text('N/A - ' + str(e))
                imgui.tree_pop()
            imgui.tree_pop()

        imgui.text('plugins')

        for k, v in self.main.enable_plugins.items():
            clicked, v = imgui.checkbox(k.replace('/', '-'), v)
            if clicked:
                if v:
                    self.main.reload_plugin(k)
                elif p := self.main.plugins.pop(k, None):
                    p.unload()
                self.main.enable_plugins[k] = v
                self.main.save_config()
        # if imgui.button('reload'):
        #     plugins.reload_plugin_lists()

        imgui.text('gui')
        gui = self.main.gui
        clicked, gui.always_draw = imgui.checkbox("always_draw", gui.always_draw)
        if clicked:
            gui.cfg['always_draw'] = gui.always_draw
            self.main.save_config()

        imgui.text('sniffer')
        sniffer = self.main.sniffer
        imgui.text(f'fix:{sniffer.packet_fix.value}')
        clicked, sniffer.print_packets = imgui.checkbox("print_packets", sniffer.print_packets)
        if clicked:
            sniffer.config['print_packets'] = sniffer.print_packets
            self.main.save_config()
        clicked, sniffer.print_actor_control = imgui.checkbox("print_actor_control", sniffer.print_actor_control)
        if clicked:
            sniffer.config['print_packets'] = sniffer.print_packets
            self.main.save_config()
        clicked, sniffer.dump_pkt = imgui.checkbox("dump_pkt", sniffer.dump_pkt)
        if clicked:
            sniffer.config['dump_pkt'] = sniffer.dump_pkt
            sniffer.update_dump()
            self.main.save_config()
        if sniffer.dump_pkt:
            clicked, sniffer.dump_zone_down_only = imgui.checkbox("dump_zone_down_only", sniffer.dump_zone_down_only)
            if clicked:
                sniffer.config['dump_zone_down_only'] = sniffer.dump_zone_down_only
                self.main.save_config()

        imgui.text('func_parser')
        parser = self.main.parser
        clicked, parser.print_compile = imgui.checkbox("print_compile", parser.print_compile)
        if clicked:
            parser.compile_config.setdefault('print_debug', {})['enable'] = parser.print_compile
            self.main.save_config()

    def draw(self):
        if not self.is_show:
            glfw.iconify_window(self.window)
            self.is_show = True
            return
        if glfw.get_window_attrib(self.window, glfw.ICONIFIED):
            return
        window_flag = 0
        if not self.is_expand: window_flag |= imgui.WINDOW_NO_MOVE
        self.is_expand, self.is_show = imgui.begin('FFDPanel', True, window_flag)
        glfw.set_window_size(self.window, *map(int, imgui.get_window_size()))
        if not self.is_expand: return imgui.end()
        win_pos = glm.vec2(*imgui.get_window_position())
        if any(win_pos):
            glfw.set_window_pos(self.window, *map(int, glm.vec2(*glfw.get_window_pos(self.window)) + win_pos))
        imgui.set_window_position(0, 0)

        plugin_keys = set(self.main.plugins.keys())
        if self.current_page not in plugin_keys:
            self.current_page = main_page
        if (imgui.text if self.current_page == main_page else imgui.button)(main_page):
            self.current_page = main_page

        for k in sorted(plugin_keys):
            imgui.same_line()
            if (imgui.text if self.current_page == k else imgui.button)(k):
                self.current_page = k
        try:
            if self.current_page == main_page:
                self.ffd_page()
            else:
                if p := self.main.plugins.get(self.current_page):
                    p.draw_panel()
        except Exception as e:
            self.logger.error('error in tab drawing', exc_info=e)
        imgui.end()
