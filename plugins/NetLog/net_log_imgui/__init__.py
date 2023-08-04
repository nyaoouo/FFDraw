import datetime

import glfw
import imgui
import nylib.utils.imgui.ctx as imguictx
from .utils import *
from .format import *


class _IMessage:
    data_str = '<bytes>'
    is_select = False
    proto = -1  # 0: chat server, 1: chat client, 2: zone server, 3: zone client

    def __init__(self, main: 'NetLogger', timestamp_ms: int, source_id: int, key: str | int, data):
        self.main = main
        self.timestamp_ms = timestamp_ms
        self.source_id = source_id
        self.key = str(key)
        self.data = data
        self.timestamp_str = datetime.datetime.fromtimestamp(self.timestamp_ms / 1000).strftime(datetime_str)
        self.data_serialized = data if isinstance(data, (bytes, bytearray)) else serialize_data(data)
        self.source_str = str(self.main.actor_getter(self.source_id))

    def _match(self, key):
        if not key: return True
        return key in self.timestamp_str or key in self.source_str.lower() or key in self.key.lower() or key in self.data_str.lower()

    def match(self, key):
        self.is_select = self._match(key)
        return self.is_select

    def __str__(self):
        return f'{self.timestamp_str}/{self.source_str}/{self.key}/{self.data_str}'


class ZoneServerIpc(_IMessage):
    proto = 2

    def __init__(self, *args):
        super().__init__(*args)
        if isinstance(self.data, (bytes, bytearray)):
            self.data_str = f'<bytes:{len(self.data)}>'
        else:
            try:
                self.data_str = zone_server_fmt.fmt(self.key, self.source_id, self.data, self.main.sq_pack, self.main.actor_getter)
            except KeyError:
                self.data_str = fmt_simple(self.data_serialized)


class ZoneClientIpc(_IMessage):
    proto = 3

    def __init__(self, *args):
        super().__init__(*args)
        if isinstance(self.data, (bytes, bytearray)):
            self.data_str = f'<bytes:{len(self.data)}>'
        else:
            try:
                self.data_str = zone_client_fmt.fmt(self.key, self.source_id, self.data, self.main.sq_pack, self.main.actor_getter)
            except KeyError:
                self.data_str = fmt_simple(self.data_serialized)


class ActorControlIpc(_IMessage):
    proto = 2

    def __init__(self, *args, target_id: int = 0):
        super().__init__(*args)
        if isinstance(self.data, tuple):
            self.data_str = fmt_simple(self.data_serialized)
        else:
            try:
                self.data_str = actor_control_fmt.fmt(self.key, self.source_id, self.data, self.main.sq_pack, self.main.actor_getter, target_id)
            except KeyError:
                self.data_str = fmt_simple(self.data_serialized)
        self.key = f'ActorControl[{self.key}]'


class ChatServerIpc(_IMessage):
    proto = 0

    def __init__(self, *args):
        super().__init__(*args)
        if isinstance(self.data, (bytes, bytearray)):
            self.data_str = f'<bytes:{len(self.data)}>'
        else:
            try:
                self.data_str = chat_server_fmt.fmt(self.key, self.source_id, self.data, self.main.sq_pack, self.main.actor_getter)
            except KeyError:
                self.data_str = fmt_simple(self.data_serialized)


class ChatClientIpc(_IMessage):
    proto = 1

    def __init__(self, *args):
        super().__init__(*args)
        if isinstance(self.data, (bytes, bytearray)):
            self.data_str = f'<bytes:{len(self.data)}>'
        else:
            try:
                self.data_str = chat_client_fmt.fmt(self.key, self.source_id, self.data, self.main.sq_pack, self.main.actor_getter)
            except KeyError:
                self.data_str = fmt_simple(self.data_serialized)


text_selected = imguictx.CtxGroup(
    imguictx.StyleColor(imgui.COLOR_TEXT, 0, 1, 0),
    imguictx.StyleColor(imgui.COLOR_FRAME_BACKGROUND, 0, 0, 0, 0),
    # imguictx.ItemWidth(-1)
)
text_unselected = imguictx.CtxGroup(
    imguictx.StyleColor(imgui.COLOR_FRAME_BACKGROUND, 0, 0, 0, 0),
    # imguictx.ItemWidth(-1)
)
auto_item_width = imguictx.ItemWidth(-1)


def imgui_render_data_kv(keys, values):
    with imguictx.Child('#kv', 0, calc_imgui_render_data_kv_height(values)):
        x_spacing = imgui.get_style().item_spacing.x * 2
        imgui.columns(2)
        max_key_len = max(imgui.calc_text_size(k)[0] for k in keys)
        imgui.set_column_width(-1, max_key_len + x_spacing * 2)
        with text_unselected:
            for k, v in zip(keys, values):
                with auto_item_width: imgui.input_text(f'##key-{k}', k, -1, imgui.INPUT_TEXT_READ_ONLY)
                imgui.next_column()
                with imguictx.ImguiId(f'value-{k}'):
                    imgui_render_data(v)
                imgui.next_column()
        imgui.columns(1)


def imgui_render_data(data):
    if isinstance(data, dict):
        return imgui_render_data_kv(list(data.keys()), list(data.values()))
    elif isinstance(data, (list, tuple)):
        return imgui_render_data_kv([f"[{i}]" for i in range(len(data))], data)
    if isinstance(data, int):
        data = hex(data)
    elif isinstance(data, float):
        data = f'{data:.3f}'
    elif isinstance(data, bytes):
        data = data.hex(' ')
    elif not isinstance(data, str):
        data = str(data)
    with text_unselected, auto_item_width:
        imgui.input_text(f'##val', data, -1, imgui.INPUT_TEXT_READ_ONLY)


def calc_imgui_render_data_kv_height(datas):
    y_spacing = imgui.get_style().item_spacing.y * 2
    min_line_height = imgui.get_text_line_height_with_spacing()
    return sum(max(min_line_height, calc_imgui_render_data_height(d)) + y_spacing for d in datas)


def calc_imgui_render_data_height(data):
    if isinstance(data, dict):
        return calc_imgui_render_data_kv_height(data.values())
    elif isinstance(data, (list, tuple)):
        return calc_imgui_render_data_kv_height(data)
    return imgui.get_text_line_height_with_spacing()


class NetLogger:
    display_data: list
    data: list

    def __init__(self, sq_pack, actor_getter):
        self.sq_pack = sq_pack
        self.actor_getter = actor_getter

        self.data = []
        self.display_data = []
        self.filter = ''
        self._filter = ''
        self._only_show_filtered = False
        self._only_show_defined = True
        self._lock_bottom = True

        self.display_idx = 0
        self.select_idx = -1
        self.is_scroll_bar_active = False

        self.table_widths = [0, 0, 0]
        self.render_frame_cnt = 0
        self.show_cnt = 0
        self.touch_bottom = False

    def _is_display_data(self, data):
        return (not self._only_show_filtered or data.is_select) and not (self._only_show_defined and isinstance(data.data, (bytes, bytearray)))

    def _update_display_data(self, display_change=True):
        if display_change:
            self.display_idx = 0
            self.select_idx = -1
        self.display_data = [d for d in self.data if self._is_display_data(d)]

    def apply_filter(self):
        if self.filter == self._filter: return
        self._filter = self.filter
        lower = self._filter.lower()
        for d in self.data: d.match(lower)
        self._update_display_data(False)

    @property
    def only_show_filtered(self):
        return self._only_show_filtered

    @only_show_filtered.setter
    def only_show_filtered(self, value):
        self._only_show_filtered = value
        self._update_display_data()

    @property
    def only_show_defined(self):
        return self._only_show_defined

    @only_show_defined.setter
    def only_show_defined(self, value):
        self._only_show_defined = value
        self._update_display_data()

    def append_data(self, data: _IMessage):
        self.data.append(data)
        data.match(self.filter)
        if self._is_display_data(data):
            self.display_data.append(data)
        if self._lock_bottom:
            self.go_bottom()

    @property
    def display_percent(self):
        return self.display_idx / len(self.display_data)

    @display_percent.setter
    def display_percent(self, value):
        ddl = len(self.display_data)
        self.display_idx = min(max(int(value * ddl), 0), ddl - 1)

    def go_bottom(self):
        self.display_idx = max(len(self.display_data) - self.show_cnt, 0) if self.touch_bottom else 0

    @property
    def lock_bottom(self):
        return self._lock_bottom

    @lock_bottom.setter
    def lock_bottom(self, value):
        self._lock_bottom = value
        if value: self.go_bottom()

    def update_scroll(self):
        io = imgui.get_io()
        wheel_delta = int(io.mouse_wheel)
        if wheel_delta != 0:
            ctx_x, ctx_y = imgui.get_window_position()
            ctx_w, ctx_h = imgui.get_window_size()
            mouse_x, mouse_y = io.mouse_pos
            if ctx_x <= mouse_x <= ctx_x + ctx_w and ctx_y <= mouse_y <= ctx_y + ctx_h:
                self.display_idx = min(max(self.display_idx - wheel_delta, 0), len(self.display_data) - 1)
        return self.display_idx

    def render_datas(self):
        idx = self.update_scroll()
        start_x, start_y = imgui.get_cursor_screen_pos()
        max_y = imgui.get_window_height() - imgui.get_text_line_height_with_spacing() - imgui.get_style().item_spacing.y
        show_cnt = 0
        display_len = len(self.display_data)
        imgui.columns(5)  # select, datetime, source, key, data
        x_spacing = imgui.get_style().item_spacing.x * 2
        imgui.set_column_width(0, x_spacing + imgui.get_text_line_height_with_spacing())
        for i in range(3):
            imgui.set_column_width(1 + i, self.table_widths[i] + x_spacing * 2) if self.table_widths[i] else None

        # imgui.text('select')
        imgui.next_column()
        imgui.text('datetime')
        imgui.next_column()
        imgui.text('source')
        imgui.next_column()
        imgui.text('key')
        imgui.next_column()
        imgui.text('data')
        imgui.next_column()
        imgui.separator()
        table_widths = [0, 0, 0]
        while idx < display_len:
            if imgui.get_cursor_screen_pos()[1] >= max_y:
                break
            data: _IMessage = self.display_data[idx]
            style = text_selected if self._filter and data.is_select else text_unselected
            changed, var = imgui.checkbox(f'##select[{idx}]', self.select_idx == idx)
            if changed: self.select_idx = idx if var else -1
            imgui.next_column()
            table_widths[0] = max(table_widths[0], imgui.calc_text_size(data.timestamp_str)[0])
            table_widths[1] = max(table_widths[1], imgui.calc_text_size(data.source_str)[0])
            table_widths[2] = max(table_widths[2], imgui.calc_text_size(data.key)[0])
            with style:
                with auto_item_width: imgui.input_text(f'##ts[{idx}]', data.timestamp_str, -1, imgui.INPUT_TEXT_READ_ONLY)
                imgui.next_column()
                with auto_item_width: imgui.input_text(f'##src[{idx}]', data.source_str, -1, imgui.INPUT_TEXT_READ_ONLY)
                imgui.next_column()
                with auto_item_width: imgui.input_text(f'##key[{idx}]', data.key, -1, imgui.INPUT_TEXT_READ_ONLY)
                imgui.next_column()
                with auto_item_width: imgui.input_text(f'##data[{idx}]', data.data_str, -1, imgui.INPUT_TEXT_READ_ONLY)
                imgui.next_column()
            idx += 1
            show_cnt += 1
        self.show_cnt = show_cnt
        self.touch_bottom = imgui.get_cursor_screen_pos()[1] + imgui.get_text_line_height_with_spacing() >= max_y
        self.table_widths = table_widths
        imgui.columns(1)
        if show_cnt and show_cnt < display_len:
            with imguictx.PushCursor():
                # draw a scrollbar
                draw_list = imgui.get_window_draw_list()
                sb_size = imgui.get_style().scrollbar_size
                draw_sb_size = sb_size if self.is_scroll_bar_active else sb_size * 0.5
                scrollbar_x = imgui.get_window_width() - sb_size - imgui.get_style().window_padding.x + start_x
                start_y += imgui.get_style().item_spacing.y

                mx, my = imgui.get_mouse_pos()
                _is_sb_active = (scrollbar_x <= mx <= scrollbar_x + sb_size and start_y <= my <= max_y)
                if self.is_scroll_bar_active:
                    if not imgui.get_io().want_capture_mouse or not imgui.is_mouse_down(0):
                        self.is_scroll_bar_active = _is_sb_active
                    else:
                        self.display_percent = (my - start_y) / (max_y - start_y)
                else:
                    self.is_scroll_bar_active = _is_sb_active

                draw_sb_x = imgui.get_window_width() - draw_sb_size - imgui.get_style().window_padding.x + start_x
                imgui.set_cursor_screen_pos((draw_sb_x, start_y))
                imgui.invisible_button('##scrollbar_inv', draw_sb_size, max_y - start_y)
                draw_list.add_rect_filled(
                    draw_sb_x, start_y,
                    draw_sb_x + draw_sb_size, max_y,
                    imgui.get_color_u32_rgba(0.2, 0.2, 0.2, 0.5 if self.is_scroll_bar_active else 0.2)
                )
                btn_height = max((max_y - start_y) * show_cnt / display_len, 24)
                btn_y = start_y + (max_y - start_y - btn_height) * self.display_percent
                draw_list.add_rect_filled(
                    draw_sb_x, btn_y,
                    draw_sb_x + draw_sb_size, btn_y + btn_height,
                    imgui.get_color_u32_rgba(0.7, 0.7, 0.7, 0.7)
                )

    def render_config(self):
        imgui.text('lock bottom:')
        imgui.same_line()
        changed, new_val = imgui.checkbox('##lock_bottom', self.lock_bottom)
        if changed: self.lock_bottom = new_val

        imgui.text('only show filtered:')
        imgui.same_line()
        changed, new_val = imgui.checkbox('##only_show_filtered', self.only_show_filtered)
        if changed: self.only_show_filtered = new_val

        imgui.text('only show defined:')
        imgui.same_line()
        changed, new_val = imgui.checkbox('##only_show_defined', self.only_show_defined)
        if changed: self.only_show_defined = new_val

        imgui.text('filter:')
        imgui.same_line()
        with imguictx.ItemWidth(-1):
            changed, self.filter = imgui.input_text('##filter_text', self.filter, 256)
        # if imgui.button('apply filter', -1):
        if changed:
            self.apply_filter()
        if self.filter:
            btn_width = imgui.get_window_width() / 2 - imgui.get_style().window_padding.x
            if imgui.button('<-', btn_width, 0):
                self.display_idx = next((i for i in range(self.display_idx - 1, -1, -1) if self.display_data[i].is_select), self.display_idx)
            imgui.same_line()
            if imgui.button('->', btn_width, 0):
                self.display_idx = next((i for i in range(self.display_idx + 1, len(self.display_data)) if self.display_data[i].is_select), self.display_idx)

    def render_detail(self):
        if imgui.button('copy', -1):
            import pprint
            s = pprint.pformat(self.display_data[self.select_idx].data_serialized, sort_dicts=False, )
            glfw.set_clipboard_string(None, s)
        imgui_render_data(self.display_data[self.select_idx].data_serialized)

    def render(self):
        imgui.columns(2)
        if self.render_frame_cnt < 2:
            imgui.set_column_width(0, 300)
        with imguictx.Child('##Left', 0, 0):
            self.render_config()
            if self.select_idx != -1:
                with imguictx.Child('##selected_detail', 0, 0, True):
                    self.render_detail()
        imgui.next_column()
        with imguictx.Child('##Right', 0, 0):
            self.render_datas()
        imgui.next_column()
        imgui.columns(1)
        self.render_frame_cnt += 1
