import dataclasses
import threading
import time
import typing
from typing import List

import imgui

from NetLog.net_log_imgui import ChatServerIpc, ChatClientIpc, ZoneServerIpc, ZoneClientIpc
from ff_draw.sniffer.message_dump import MessageDumper
from fpt4.utils.sqpack import SqPack
from nylib.utils.imgui.window_mgr import WindowManager
import net_log_imgui

if typing.TYPE_CHECKING:
    from ff_draw.sniffer.message_structs import zone_server


def main(game_path, proto_path, dump_path):
    sq_pack = SqPack.get(game_path)
    actor_cache = net_log_imgui.ActorDefs()
    nl = net_log_imgui.NetLogger(sq_pack, actor_cache.get)

    def parse_actor_control(timestamp_ms, ac_id, source_id, target_id, *args):
        from ff_draw.sniffer.enums import ActorControlId
        from ff_draw.sniffer.message_structs import actor_control
        try:
            ac_id = ActorControlId(ac_id)
        except ValueError:
            return nl.append_data(net_log_imgui.ActorControlIpc(nl, timestamp_ms, source_id, ac_id, args, target_id=target_id))
        if t := actor_control.type_map.get(ac_id):
            if not hasattr(t, '__field_count'):
                setattr(t, '__field_count', cnt := len(dataclasses.fields(t)))
            else:
                cnt = getattr(t, '__field_count')
            data = t(*args[:cnt])
            return nl.append_data(net_log_imgui.ActorControlIpc(nl, timestamp_ms, source_id, ac_id.name, data, target_id=target_id))
        return nl.append_data(net_log_imgui.ActorControlIpc(nl, timestamp_ms, source_id, ac_id.name, args, target_id=target_id))

    def load():
        for is_zone, is_up, proto_no, source_id, timestamp_ms, data in MessageDumper.parse(dump_path, proto_path):
            # if isinstance(data, bytes): continue  # skip not defined proto
            handled = False
            match proto_no:
                case 'NpcSpawn' | 'NpcSpawn2':
                    data: 'zone_server.NpcSpawn | zone_server.NpcSpawn2'
                    actor_cache.update(
                        source_id,
                        data.create_common.npc_id,
                        net_log_imgui.fmt_name(sq_pack, data.create_common.name_id) or data.create_common.name
                    )
                case 'ObjectSpawn':
                    data: 'zone_server.ObjectSpawn'
                    actor_cache.update(source_id, data.base_id, sq_pack.sheets.e_obj_name_sheet[data.base_id][0])
                case 'PlayerSpawn':
                    data: 'zone_server.PlayerSpawn'
                    actor_cache.update(source_id, 0, data.create_common.name)
                case 'ActorControl':
                    data: 'zone_server.ActorControl'
                    parse_actor_control(
                        timestamp_ms,
                        data.id,
                        source_id, 0,
                        data.arg0, data.arg1, data.arg2, data.arg3
                    )
                    handled = True
                case 'ActorControlSelf':
                    data: 'zone_server.ActorControlSelf'
                    parse_actor_control(
                        timestamp_ms,
                        data.id,
                        source_id, 0,
                        data.arg0, data.arg1, data.arg2, data.arg3, data.arg4, data.arg5,
                    )
                    handled = True
                case 'ActorControlTarget':
                    data: 'zone_server.ActorControlTarget'
                    parse_actor_control(
                        timestamp_ms,
                        data.id,
                        source_id, data.target_id,
                        data.arg0, data.arg1, data.arg2, data.arg3
                    )
                    handled = True
                case 'RsvString':
                    sq_pack.exd.rsv_string[data.key] = data.value
            if not handled:
                match int(is_zone) << 1 | int(is_up):
                    case 0b00:  # chat server
                        nl.append_data(net_log_imgui.ChatServerIpc(nl, timestamp_ms, source_id, proto_no, data))
                    case 0b01:  # chat client
                        nl.append_data(net_log_imgui.ChatClientIpc(nl, timestamp_ms, source_id, proto_no, data))
                    case 0b10:  # zone server
                        nl.append_data(net_log_imgui.ZoneServerIpc(nl, timestamp_ms, source_id, proto_no, data))
                    case 0b11:  # zone client
                        nl.append_data(net_log_imgui.ZoneClientIpc(nl, timestamp_ms, source_id, proto_no, data))
            # time.sleep(0.001) #simulate slow loading

    def draw_main(window):
        io = imgui.get_io()
        window.title = f'NetLog[fps:{io.framerate:.1f}]'
        nl.render()

    wm = WindowManager(ini_file_name=None, default_font_path=r'D:\game\ff14_res\FFDraw\res\PingFang.ttf')
    wm.new_window('nl', draw_main)
    threading.Thread(target=load).start()
    wm.run()


if __name__ == '__main__':
    main(
        r"D:\game\SquareEnix\FINAL FANTASY XIV - A Realm Reborn\game",
        r"D:\game\ff14_res\FFDraw\res\proto_no",
        r"D:\game\ff14_res\FFDraw\AppData\dump_pkt\dump_2023_08_02_10_11_32.dmp",
    )
