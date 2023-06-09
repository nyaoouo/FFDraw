import json
import subprocess

import glfw
import glm
import imgui

from ff_draw.plugins import FFDrawPlugin
from ff_draw.mem.marking import WayMarkType, WayMark


def waymark2json(waymark: WayMark, wid):
    if waymark.is_enable:
        pos = waymark.pos
        return {
            'X': pos.x,
            'Y': pos.y,
            'Z': pos.z,
            'ID': wid,
            'Active': True,
        }
    else:
        return None
        # return {
        #     'ID': wid,
        #     'Active': False,
        #     'X': 0,
        #     'Y': 0,
        #     'Z': 0,
        # }


def assert_json_waymark(data):
    assert isinstance(data, dict)
    assert isinstance(data.get('Name'), str)
    assert isinstance(data.get('MapID'), int)
    for k in ('A', 'B', 'C', 'D', 'One', 'Two', 'Three', 'Four'):
        assert isinstance(_d := data.get(k), (dict, type(None)))
        if _d is None: continue
        assert isinstance(_d.get('ID'), int)
        assert isinstance(_d.get('Active'), bool)
        assert isinstance(_d.get('X'), (float, int))
        assert isinstance(_d.get('Y'), (float, int))
        assert isinstance(_d.get('Z'), (float, int))


class MarkPreset(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.cache_teri = (-1, '')
        self.presets = {}
        self._save_preset_name = ''
        self._save_preset_name_warn = ''
        self._import_preset_json = ''
        self._import_preset_json_warn = ''
        self.load_presets()
        self.check_to_add_preset_name()

    def load_presets(self):
        self.presets.clear()
        _dir = self.storage.path / 'presets'
        if not _dir.exists(): return
        for f in _dir.iterdir():
            if f.is_dir() and f.name.isnumeric():
                data = {}
                for ff in f.iterdir():
                    if ff.suffix == '.json':
                        data[ff.stem] = json.loads(ff.read_text(encoding='utf-8'))
                self.presets[int(f.name)] = data

    def save_preset(self, name, common_territory=False):
        marking = self.main.mem.marking
        tid = 0 if common_territory else self.main.mem.territory_info.territory_id
        mid = 0 if common_territory else self.main.mem.territory_info.map_id
        data = {
            'Name': name,
            'MapID': mid,
            'A': waymark2json(marking.way_mark(0), 0),
            'B': waymark2json(marking.way_mark(1), 1),
            'C': waymark2json(marking.way_mark(2), 2),
            'D': waymark2json(marking.way_mark(3), 3),
            'One': waymark2json(marking.way_mark(4), 4),
            'Two': waymark2json(marking.way_mark(5), 5),
            'Three': waymark2json(marking.way_mark(6), 6),
            'Four': waymark2json(marking.way_mark(7), 7),
        }
        self.presets.setdefault(tid, {})[name] = data
        _dir = self.storage.path / 'presets' / str(tid)
        _dir.mkdir(parents=True, exist_ok=True)
        _file = _dir / f'{name}.json'
        assert not _file.exists(), 'preset name already exists'
        _file.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding='utf-8')

    def import_preset(self, preset_json):
        data = json.loads(preset_json)
        try:
            assert_json_waymark(data)
        except:
            raise ValueError('invalid preset json')
        self.presets.setdefault(0, {})[data['Name']] = data
        map_id = data['MapID']
        teri_id = self.main.sq_pack.sheets.map_sheet[map_id].territory_type.key if map_id != 0 else 0
        _dir = self.storage.path / 'presets' / str(teri_id)
        _dir.mkdir(parents=True, exist_ok=True)
        assert not (_file := _dir / f'{data["Name"]}.json').exists(), 'preset name already exists'
        _file.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding='utf-8')

    def apply_preset(self, data):
        try:
            assert_json_waymark(data)
        except:
            raise ValueError('invalid preset json')
        assert not data['MapID'] or data['MapID'] == self.main.mem.territory_info.map_id, 'preset map id not match'
        marking = self.main.mem.marking
        for i, k in enumerate(('A', 'B', 'C', 'D', 'One', 'Two', 'Three', 'Four')):
            _data = data[k]
            try:
                if _data and _data['Active']:
                    marking.request_way_mark(i, glm.vec3(_data['X'], _data['Y'], _data['Z']))
                else:
                    marking.request_clear_way_mark(i)
            except Exception as e:
                self.logger.warning(f'apply preset {k} failed: {e}', exc_info=True)

    def check_to_add_preset_name(self):
        if not self._save_preset_name:
            self._save_preset_name_warn = 'name cannot be empty'
        elif self._save_preset_name in self.presets.get(self.main.mem.territory_info.territory_id, {}):
            self._save_preset_name_warn = 'name already exists'
        else:
            self._save_preset_name_warn = ''

    def render_presets(self, tid):
        imgui.push_id(f'preset_{tid}')
        _dir = self.storage.path / 'presets' / str(tid)
        for name, data in list(self.presets.get(tid, {}).items()):
            imgui.text(name)
            imgui.same_line()
            if imgui.button(f'apply##{name}'):
                try:
                    self.apply_preset(data)
                except Exception as e:
                    self.main.logger.error(f'apply preset error: {e}')
            imgui.same_line()
            if imgui.button(f'delete##{name}'):
                self.presets[tid].pop(name)
                (_dir / f'{name}.json').unlink()
            imgui.same_line()
            if imgui.button(f'open##{name}'):
                subprocess.call(['explorer', str(_dir / f'{name}.json')])
        imgui.pop_id()

    def draw_panel(self):
        tid = self.main.mem.territory_info.territory_id
        if tid:
            territory_type_sheet = self.main.sq_pack.sheets.territory_type_sheet
            imgui.text(f'current teri: {tid}[{territory_type_sheet[tid].area.text_sgl}]')
            imgui.text(f'current map: {self.main.mem.territory_info.map_id}')

        marking = self.main.mem.marking
        for i in range(8):
            mark = marking.way_mark(i)
            if mark.is_enable:
                pos = mark.pos
                imgui.text(f'{WayMarkType(i).name}: {pos.x:.2f}, {pos.y:.2f}, {pos.z:.2f}')
            else:
                imgui.text(f'{WayMarkType(i).name}: -')

        imgui.text('save preset:')
        imgui.same_line()
        changed, new_str = imgui.input_text('##save_preset_name', self._save_preset_name, 1024)
        if changed:
            self._save_preset_name = new_str
            self.check_to_add_preset_name()

        imgui.same_line()
        if imgui.button('save') and not self._save_preset_name_warn:
            try:
                self.save_preset(self._save_preset_name)
            except Exception as e:
                self.logger.error(f'save preset failed: {e}', exc_info=True)
                self._save_preset_name_warn = str(e)
            else:
                self._save_preset_name = ''
                self.check_to_add_preset_name()
        if self._save_preset_name_warn:
            imgui.push_style_color(imgui.COLOR_TEXT, 1, 0, 0)
            imgui.text('*' + self._save_preset_name_warn)
            imgui.pop_style_color()

        imgui.new_line()
        if tid:
            if self.presets.get(tid, {}) and imgui.collapsing_header(f'{tid}[{territory_type_sheet[tid].area.text_sgl}]')[0]:
                self.render_presets(tid)
        if self.presets.get(0, {}) and imgui.collapsing_header(f'common')[0]:
            self.render_presets(0)
        for tid in self.presets:
            if tid not in (0, tid) and self.presets.get(tid):
                if imgui.collapsing_header(f'{tid}[{territory_type_sheet[tid].area.text_sgl}]')[0]:
                    self.render_presets(tid)

        imgui.new_line()
        imgui.text('import preset:')
        imgui.same_line()
        if imgui.button('import from clipboard'):
            try:
                self.import_preset(glfw.get_clipboard_string(None))
            except Exception as e:
                self.logger.error(f'import preset failed: {e}', exc_info=True)
                self._import_preset_json_warn = str(e)
            else:
                self._import_preset_json = ''
                self._import_preset_json_warn = ''

        if self._import_preset_json:
            imgui.same_line()
            if imgui.button('import'):
                try:
                    self.import_preset(self._import_preset_json)
                except Exception as e:
                    self.logger.error(f'import preset failed: {e}', exc_info=True)
                    self._import_preset_json_warn = str(e)
                else:
                    self._import_preset_json = ''
                    self._import_preset_json_warn = ''
        _, self._import_preset_json = imgui.input_text_multiline('##import_preset_json', self._import_preset_json, 2048)
        if self._import_preset_json_warn:
            imgui.push_style_color(imgui.COLOR_TEXT, 1, 0, 0)
            imgui.text('*' + self._import_preset_json_warn)
            imgui.pop_style_color()
