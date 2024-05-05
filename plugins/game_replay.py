import pathlib
import shutil
import imgui
from tkinter import filedialog
import nylib.utils.win32.memory as ny_mem

from ff_draw.plugins import FFDrawPlugin


class Patch:
    def __init__(self, main: 'GameReplay', at, repl):
        self.handle = main.handle
        self.at = at
        self.repl = repl
        self.orig = main.mem.scanner_v2.get_original_text(self.at, len(self.repl))

    state = property(
        lambda self: ny_mem.read_bytes(self.handle, self.at, len(self.repl)) == self.repl,
        lambda self, value: ny_mem.write_bytes(self.handle, self.at, self.repl if value else self.orig)
    )


class GameReplay(FFDrawPlugin):
    def __init__(self, main):
        super().__init__(main)
        self.mem = mem = self.main.mem
        self.handle = mem.handle
        self.replay_zone_init_patch = Patch(self, mem.scanner_v2.find_address("74 ? 48 ? ? ? ? ? ? ba ? ? ? ? 48 ? ? ? e8 ? ? ? ? 83 78 ? ? 74 ? b1"), b"\xEB\x1B")
        self.replay_check_valid = Patch(self, mem.scanner_v2.find_val("e8 * * * * 84 ? 0f 84 ? ? ? ? 40 ? ? ? 4c")[0], b"\xB0\x01\xC3")
        self.replay_available_check = Patch(self, mem.scanner_v2.find_address("48 ? ? ? e8 ? ? ? ? 66 ? 10 0C 48 ? ? e8"), b"\xB0\x01\xC3")  # mov al, 1; retn
        self.replay_module, = mem.scanner_v2.find_val("48 ? ? * * * * 0f ? ? 88 47 ? 84")
        self.p_confirm_replay_confirm = mem.scanner_v2.find_address("40 ? 48 ? ? ? 0f ? ? ? ? ? ? 48 ? ? a8 ? 74 ? a8 ? 75 ? 80")
        self.p_reload_replay_list = mem.scanner_v2.find_address("40 ? 48 ? ? ? f6 81 ? ? ? ? ? 48 ? ? 0f 85 ? ? ? ? f6 81")
        self.p_character_id, = mem.scanner_v2.find_val("48 39 05 * * * * 4c 89 7c 24")
        ## 如果强制在外面播放回放，服务端不会在回放结束后重新初始化区域，导致无法继续游戏
        # self.area_playable = Patch(self, mem.scanner_v2.find_val("e8 * * * * 84 ? 74 ? 83 bb ? ? ? ? ? 75 ? 45")[0], b"\xB0\x01\xC3")
        # real_start_replay_patch = mem.scanner_v2.find_address("40 ? 48 ? ? ? 0f ? ? ? ? ? ? 48 ? ? a8 ? 0f 84 ? ? ? ? 24 ? 88 81")
        # self.req_start_replay_patch = Patch(
        #     self,
        #     mem.scanner_v2.find_address("40 88 bb ? ? ? ? 33 ? c7 44 24") + 7,
        #     (
        #             b"\x48\x8B\xCB" + # mov rcx, rbx
        #             b"\xB2\x01" +  # mov dl, 1
        #             b"\x48\xB8" + struct.pack(b'Q', real_start_replay_patch) + # mov rax, real_start_replay_patch
        #             b"\xFF\xD0" + # call rax
        #             b"\x90\x90\x90"
        #     ),
        # )
        #
        # real_stop_replay_patch, = mem.scanner_v2.find_val("e8 * * * * 0f ? ? ? 32 ? ? ? ? ? 89 b3")
        # req_stop_replay_patch_at = mem.scanner_v2.find_address("75 ? 80 ? ? c7 44 24 ? ? ? ? ? 88 91 ? ? ? ? 45 ? ? 33 ? b9 ? ? ? ? 45 ? ? e8 ? ? ? ? 48 ? ? ? c3")
        # payload_1 = (
        #         mem.scanner_v2.get_original_text(req_stop_replay_patch_at + 2, 11) +
        #         b"\x48\xB9" + struct.pack(b'Q', self.replay_module) +  # mov rcx, replay_module
        #         b"\xB2\x01" +  # mov dl, 1
        #         b"\x48\xB8" + struct.pack(b'Q', real_stop_replay_patch) +  # mov rax, real_stop_replay_patch
        #         b"\xFF\xD0"  # call rax
        # )
        # payload = (
        #         b'\x75' + struct.pack('b', len(payload_1)) +  # jnz +len(payload_1)
        #         payload_1 +
        #         mem.scanner_v2.get_original_text(req_stop_replay_patch_at + 0x25, 5)
        # )
        # self.req_stop_replay_patch = Patch(self, req_stop_replay_patch_at, payload)

        self.enable = self.data.setdefault('enabled', False)

    @property
    def enable(self):
        return self.replay_zone_init_patch.state

    @enable.setter
    def enable(self, value):
        self.replay_zone_init_patch.state = value
        self.replay_check_valid.state = value
        self.replay_available_check.state = value

        ## 强制播放回放相关
        # self.area_playable.state = value
        # self.req_start_replay_patch.state = value
        # self.req_stop_replay_patch.state = value

    def on_unload(self):
        self.enable = False

    def get_character_id(self):
        return ny_mem.read_uint64(self.handle, self.p_character_id)

    def start_recording(self):
        return self.mem.call_native_once_game_main(self.p_confirm_replay_confirm, 'c_void_p', ('c_size_t', 'c_uint8'), (self.replay_module, 1))

    def reload_replay_list(self):
        self.mem.call_native_once_game_main(self.p_reload_replay_list, 'c_void_p', ('c_size_t',), (self.replay_module,))

    def make_replay_path(self, slot):
        return self.mem.user_path / 'replay' / f'FFXIV_{self.get_character_id():016X}_{slot:03}.dat'

    def load_replay(self, slot, src_path):
        dst_path = self.make_replay_path(slot)
        if dst_path.exists(): dst_path.unlink()
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src_path, dst_path)
        self.reload_replay_list()

    def save_replay(self, slot, dst_path):
        src_path = self.make_replay_path(slot)
        if src_path.exists(): shutil.copy(src_path, dst_path)

    def save_replay_as(self, slot):
        if path := filedialog.asksaveasfilename():
            self.save_replay(slot, pathlib.Path(path))
            self.logger.info(f'save replay {slot} to {path}')
        else:
            self.logger.info(f'save replay {slot} canceled')

    def load_replay_from(self, slot):
        if path := filedialog.askopenfilename():
            self.load_replay(slot, pathlib.Path(path))
            self.logger.info(f'load replay {slot} from {path}')
        else:
            self.logger.info(f'load replay {slot} canceled')

    def draw_panel(self):
        change, enabled = imgui.checkbox("Enable", self.enable)
        if change:
            self.enable = enabled
            self.data['enabled'] = enabled
            self.storage.save()
        enabled and imgui.button('click to start recording') and self.start_recording()

        if chr_id := self.get_character_id():
            replay_dir = self.mem.user_path / 'replay'
            for slot in range(3):
                imgui.button(f'load_replay_{slot}') and self.create_mission(self.load_replay_from, slot)
                if (replay_dir / f'FFXIV_{chr_id:016X}_{slot:03}.dat').exists():
                    imgui.same_line()
                    imgui.button(f'save_replay_{slot}') and self.create_mission(self.save_replay_as, slot)
