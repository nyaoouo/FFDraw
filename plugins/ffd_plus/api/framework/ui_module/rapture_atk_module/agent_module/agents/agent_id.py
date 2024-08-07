import enum
from ffd_plus.utils import game_version


class AgentId(enum.IntEnum):
    if game_version >= (6, 5, 0):
        lobby = 0X0
        chara_make = 0X1
        movie_staff_list = 0X2
        cursor_addon = 0X3
        hud = 0X4
        chat_log = 0X5
        inventory = 0X6
        scenario_tree = 0X7
        event_fade = 0X8
        context = 0X9
        inventory_context = 0XA
        config = 0XB
        config_log = 0XC
        config_log_color = 0XD
        config_key = 0XE
        config_character = 0XF
        config_pad_customize = 0X10
        chat_config = 0X11
        config_chat_log_name_setting = 0X12
        hud_layout = 0X13
        emote = 0X14
        macro = 0X15
        gathering_note = 0X17
        recipe_note = 0X18
        recipe_tree = 0X19
        recipe_material_list = 0X1A
        recipe_product_list = 0X1B
        fishing_note = 0X1C
        fish_guide2 = 0X1D
        fish_record = 0X1E
        fish_release = 0X1F
        journal = 0X20
        action_menu = 0X21
        marker = 0X22
        trade = 0X23
        screen_log = 0X24
        request = 0X25
        status = 0X26
        map = 0X27
        need_greed = 0X28
        need_greed_targeting = 0X28
        repair = 0X29
        repair_request = 0X2A
        materialize = 0X2B
        materia_attach = 0X2C
        mirage_prism = 0X2D
        colorant = 0X2E
        how_to = 0X2F
        how_to_notice = 0X30
        contents_tutorial = 0X31
        inspect = 0X32
        teleport = 0X33
        contents_finder = 0X35
        contents_finder_setting = 0X36
        social = 0X37
        black_list = 0X38
        friend_list = 0X39
        link_shell = 0X3A
        letter_list = 0X3F
        letter_viewer = 0X40
        letter_editor = 0X41
        item_detail = 0X42
        action_detail = 0X43
        retainer = 0X44
        return_ = 0X45
        cutscene = 0X46
        cut_scene_replay = 0X47
        monster_note = 0X48
        item_search = 0X49
        fate_progress = 0X4B
        catch = 0X4C
        free_company = 0X4D
        free_company_profile = 0X4F
        free_company_profile_edit = 0X50
        free_company_input_string = 0X52
        free_company_chest = 0X53
        free_company_exchange = 0X54
        free_company_crest_editor = 0X55
        free_company_crest_decal = 0X56
        armoury_board = 0X58
        howto_list = 0X59
        cabinet = 0X5A
        legacy_item_storage = 0X5C
        grand_company_rank = 0X5D
        grand_company_supply = 0X5E
        grand_company_exchange = 0X5F
        gear_set = 0X60
        support_main = 0X61
        support_list = 0X62
        support_view = 0X63
        support_edit = 0X64
        achievement = 0X65
        license_viewer = 0X67
        contents_timer = 0X68
        movie_subtitle = 0X69
        pad_mouse_mode = 0X6A
        recommend_list = 0X6B
        buddy = 0X6C
        colosseum_record = 0X6D
        close_message = 0X6E
        credit_player = 0X6F
        credit_scroll = 0X70
        credit_cast = 0X71
        credit_end = 0X72
        shop = 0X74
        bait = 0X75
        housing = 0X76
        housing_harvest = 0X77
        housing_signboard = 0X78
        housing_portal = 0X79
        housing_travellers_note = 0X7A
        housing_plant = 0X7B
        personal_room_portal = 0X7C
        housing_buddy_list = 0X7D
        treasure_hunt = 0X7E
        salvage = 0X7F
        looking_for_group = 0X80
        contents_mvp = 0X81
        vote_kick = 0X82
        vote_giveup = 0X83
        vote_treasure = 0X84
        pvp_profile = 0X85
        contents_note = 0X86
        ready_check = 0X87
        field_marker = 0X88
        cursor_location = 0X89
        cursor_rect = 0X8A
        retainer_status = 0X8B
        retainer_task = 0X8C
        retainer_item_transfer = 0X8F
        relic_glass = 0X90
        relic_note_book = 0X91
        relic_sphere = 0X92
        trade_multiple = 0X93
        relic_sphere_upgrade = 0X94
        aw_making_spirit_grow = 0X96
        minigame = 0X98
        try_on = 0X99
        adventure_note_book = 0X9B
        armoury_note_book = 0X9C
        minion_note_book = 0X9D
        mount_note_book = 0X9E
        daily_quest_supply = 0XA0
        mob_hunt = 0XA1
        patch_mark = 0XA2
        housing_withdraw_storage = 0XA3
        weather_report = 0XA4
        wedding = 0XA5
        loading_tips = 0XA6
        revive = 0XA7
        chocobo_race = 0XA9
        triple_triad = 0XAC
        triple_triad_rule_announce = 0XAD
        triple_triad_rule_setting = 0XAE
        triple_triad_pick_up_deck_select = 0XAF
        triple_triad_schedule = 0XB0
        tournament_ranking = 0XB1
        triple_triad_tournament_result = 0XB2
        triple_triad_tournament_match_list = 0XB3
        lottery_daily = 0XB4
        aetherial_wheel = 0XB5
        lottery_weekly = 0XB6
        gold_saucer_info = 0XB7
        journal_accept = 0XBA
        journal_result = 0XBB
        company_craft_recipe_note_book = 0XBD
        air_ship_parts_menu = 0XBE
        air_ship_exploration = 0XBF
        air_ship_exploration_result = 0XC0
        air_ship_exploration_detail = 0XC1
        submarine_parts_menu = 0XC2
        aether_current = 0XC7
        freecompany_credit_shop = 0XC8
        currency = 0XC9
        lovm_ranking = 0XCD
        character_title = 0XCF
        character_title_select = 0XD0
        lovm_result = 0XD1
        item_context_customize = 0XD7
        beginners_mansion_problem = 0XD8
        play_guide = 0XDA
        web_launcher = 0XDB
        web_guidance = 0XDC
        orchestrion = 0XDD
        returner_dialog = 0XE1
        config_partylist_role_sort = 0XE4
        recommend_equip = 0XE5
        ykw_note = 0XE6
        contents_finder_menu = 0XE7
        raid_finder = 0XE8
        gc_army_expedition = 0XE9
        gc_army_member_list = 0XEA
        pvp_action_set = 0XEB
        deep_dungeon_status = 0XEE
        deep_dungeon_save_data = 0XEF
        deep_dungeon_score = 0XF0
        gc_army_training = 0XF1
        gc_army_expedition_result = 0XF3
        gc_army_capture = 0XF4
        gc_army_order = 0XF5
        orchestrion_playlist = 0XF7
        countdown = 0XF8
        weekly_bingo = 0XF9
        weekly_puzzle = 0XFA
        pvp_duel_request = 0XFC
        qte = 0X102
        deep_dungeon_menu = 0X103
        deep_dungeon_result = 0X105
        item_appraisal = 0X106
        item_inspection = 0X107
        contact_list = 0X109
        picture_preview = 0X10A
        satisfaction_supply = 0X10C
        satisfaction_supply_result = 0X10D
        snipe = 0X10E
        mount_speed = 0X10F
        harpoon_tip = 0X110
        treasure_high_low = 0X114
        user_policy_performance = 0X117
        pvp_team = 0X118
        pvp_team_input_string = 0X119
        pvp_team_crest_editor = 0X11E
        eureka_elemental_hud = 0X121
        eureka_elemental_edit = 0X122
        eureka_chain_info = 0X123
        content_member_list = 0X128
        contents_replay_setting = 0X12B
        mirage_prism_prism_box = 0X12C
        mirage_prism_prism_item_detail = 0X12D
        mirage_prism_mirage_plate = 0X12E
        performance_mode = 0X12F
        reconstruction_box = 0X138
        reconstruction_buyback = 0X139
        cross_world_linkshell = 0X13A
        description = 0X13C
        alarm = 0X13D
        free_shop = 0X140
        aoz_notebook = 0X141
        emj = 0X144
        emj_total_result = 0X145
        emj_rank_result = 0X146
        emj_intro = 0X147
        aoz_content_briefing = 0X148
        aoz_content_result = 0X149
        world_travel_select = 0X14A
        credit = 0X14D
        emj_setting = 0X14E
        retainer_list = 0X14F
        qibc_status = 0X150
        huge_craft_works_supply = 0X151
        huge_craft_works_supply_result = 0X152
        sharlayan_craft_works_supply = 0X153
        dawn = 0X154
        dawn_story = 0X155
        housing_catalog_preview = 0X156
        guide = 0X157
        submarine_exploration_map_select = 0X158
        quest_redo = 0X159
        quest_redo_hud = 0X15A
        circle_list = 0X15C
        circle_book = 0X15D
        circle_finder = 0X162
        performance_metronome = 0X165
        performance_gamepad_guide = 0X166
        performance_ready_check = 0X168
        hwd_aethergauge = 0X16C
        hwd_score = 0X16E
        hwd_monument = 0X170
        mcguffin = 0X171
        craft_action_simulator = 0X172
        ikd_schedule = 0X173
        ikd_fishing_log = 0X174
        ikd_result = 0X175
        ikd_mission = 0X176
        inclusion_shop = 0X177
        collectables_shop = 0X178
        myc_war_result_notebook = 0X179
        myc_info = 0X17A
        myc_item_box = 0X17B
        myc_item_bag = 0X17C
        myc_duel_request = 0X17D
        myc_battle_area_info = 0X17E
        myc_weapon_adjust = 0X17F
        ornament_note_book = 0X180
        talk_subtitle = 0X181
        tourism_menu = 0X182
        gathering_masterpiece = 0X183
        starlight20_gift_box = 0X184
        spearfishing = 0X185
        omikuji = 0X186
        fitting_shop = 0X187
        akatsuki_note = 0X188
        ex_hot_bar_editor = 0X189
        banner_list = 0X18A
        banner_editor = 0X18B
        banner_update_view = 0X18C
        banner_gearset_link = 0X18D
        pvp_map = 0X18E
        chara_card = 0X18F
        characard_design_setting = 0X190
        chara_card_profile_setting = 0X191
        mji_hud = 0X194
        mji_pouch = 0X195
        mji_recipe_note_book = 0X196
        mji_craft_sales = 0X198
        mji_animal_management = 0X199
        mji_farm_management = 0X19A
        mji_gatheringhouse = 0X19B
        mji_building = 0X19C
        mji_building_progress = 0X19C
        mji_gathering_note_book = 0X19D
        mji_dispose_shop = 0X19E
        mji_minion_management = 0X19F
        mji_minion_note_book = 0X1A0
        mji_building_move = 0X1A1
        mji_entrance = 0X1A2
        mji_settings = 0X1A3
        mji_nekomimi_request = 0X1A6
        archive_item = 0X1A7
        class2_job_hot_bar = 0X1A8
        tofu_list = 0X1AB
        tofu_preview = 0X1AC
        tofu_edit = 0X1AD
        banner_party = 0X1AE
        banner_mip = 0X1AF
        turn_break = 0X1B0
        manderville_weapon = 0X1B1
        sxt_battle_log = 0X1B2
        moogle_collection = 0X1B3
        fgs_winner = 0X1B7
        fgs_result = 0X1B8
    else:
        lobby = 0X0
        chara_make = 0X1
        movie_staff_list = 0X2
        cursor_addon = 0X3
        hud = 0X4
        chat_log = 0X5
        inventory = 0X6
        scenario_tree = 0X7
        event_fade = 0X8
        context = 0X9
        inventory_context = 0XA
        config = 0XB
        config_log = 0XC
        config_log_color = 0XD
        config_key = 0XE
        config_character = 0XF
        config_pad_customize = 0X10
        chat_config = 0X11
        config_chat_log_name_setting = 0X12
        hud_layout = 0X13
        emote = 0X14
        macro = 0X15
        gathering_note = 0X17
        recipe_note = 0X18
        recipe_tree = 0X19
        recipe_material_list = 0X1A
        recipe_product_list = 0X1B
        fishing_note = 0X1C
        fish_guide2 = 0X1D
        fish_record = 0X1E
        fish_release = 0X1F
        journal = 0X20
        action_menu = 0X21
        marker = 0X22
        trade = 0X23
        screen_log = 0X24
        request = 0X25
        status = 0X26
        map = 0X27
        need_greed = 0X28
        need_greed_targeting = 0X28
        repair = 0X29
        repair_request = 0X2A
        materialize = 0X2B
        materia_attach = 0X2C
        mirage_prism = 0X2D
        colorant = 0X2E
        how_to = 0X2F
        how_to_notice = 0X30
        contents_tutorial = 0X31
        inspect = 0X32
        teleport = 0X33
        contents_finder = 0X35
        contents_finder_setting = 0X36
        social = 0X37
        black_list = 0X38
        friend_list = 0X39
        link_shell = 0X3A
        letter_list = 0X3F
        letter_viewer = 0X40
        letter_editor = 0X41
        item_detail = 0X42
        action_detail = 0X43
        retainer = 0X44
        return_ = 0X45
        cutscene = 0X46
        cut_scene_replay = 0X47
        monster_note = 0X48
        item_search = 0X49
        fate_progress = 0X4B
        catch = 0X4C
        free_company = 0X4D
        free_company_profile = 0X4F
        free_company_profile_edit = 0X50
        free_company_input_string = 0X52
        free_company_chest = 0X53
        free_company_exchange = 0X54
        free_company_crest_editor = 0X55
        free_company_crest_decal = 0X56
        armoury_board = 0X58
        howto_list = 0X59
        cabinet = 0X5A
        legacy_item_storage = 0X5B
        grand_company_rank = 0X5C
        grand_company_supply = 0X5D
        grand_company_exchange = 0X5E
        gear_set = 0X5F
        support_main = 0X60
        support_list = 0X61
        support_view = 0X62
        support_edit = 0X63
        achievement = 0X64
        license_viewer = 0X66
        contents_timer = 0X67
        movie_subtitle = 0X68
        pad_mouse_mode = 0X69
        recommend_list = 0X6A
        buddy = 0X6B
        colosseum_record = 0X6C
        close_message = 0X6D
        credit_player = 0X6E
        credit_scroll = 0X6F
        credit_cast = 0X70
        credit_end = 0X71
        shop = 0X73
        bait = 0X74
        housing = 0X75
        housing_harvest = 0X76
        housing_signboard = 0X77
        housing_portal = 0X78
        housing_travellers_note = 0X79
        housing_plant = 0X7A
        personal_room_portal = 0X7B
        housing_buddy_list = 0X7C
        treasure_hunt = 0X7D
        salvage = 0X7E
        looking_for_group = 0X7F
        contents_mvp = 0X80
        vote_kick = 0X81
        vote_giveup = 0X82
        vote_treasure = 0X83
        pvp_profile = 0X84
        contents_note = 0X85
        ready_check = 0X86
        field_marker = 0X87
        cursor_location = 0X88
        cursor_rect = 0X89
        retainer_status = 0X8A
        retainer_task = 0X8B
        retainer_item_transfer = 0X8E
        relic_glass = 0X8F
        relic_note_book = 0X90
        relic_sphere = 0X91
        trade_multiple = 0X92
        relic_sphere_upgrade = 0X93
        aw_making_spirit_grow = 0X95
        minigame = 0X97
        try_on = 0X98
        adventure_note_book = 0X9A
        armoury_note_book = 0X9B
        minion_note_book = 0X9C
        mount_note_book = 0X9D
        daily_quest_supply = 0X9F
        mob_hunt = 0XA0
        patch_mark = 0XA1
        housing_withdraw_storage = 0XA2
        weather_report = 0XA3
        wedding = 0XA4
        loading_tips = 0XA5
        revive = 0XA6
        chocobo_race = 0XA8
        triple_triad = 0XAB
        triple_triad_rule_announce = 0XAC
        triple_triad_rule_setting = 0XAD
        triple_triad_pick_up_deck_select = 0XAE
        triple_triad_schedule = 0XAF
        tournament_ranking = 0XB0
        triple_triad_tournament_result = 0XB1
        triple_triad_tournament_match_list = 0XB2
        lottery_daily = 0XB3
        aetherial_wheel = 0XB4
        lottery_weekly = 0XB5
        gold_saucer_info = 0XB6
        journal_accept = 0XB9
        journal_result = 0XBA
        company_craft_recipe_note_book = 0XBC
        air_ship_parts_menu = 0XBD
        air_ship_exploration = 0XBE
        air_ship_exploration_result = 0XBF
        air_ship_exploration_detail = 0XC0
        submarine_parts_menu = 0XC1
        aether_current = 0XC6
        freecompany_credit_shop = 0XC7
        currency = 0XC8
        lovm_ranking = 0XCC
        character_title = 0XCE
        character_title_select = 0XCF
        lovm_result = 0XD0
        item_context_customize = 0XD6
        beginners_mansion_problem = 0XD7
        play_guide = 0XD9
        web_launcher = 0XDA
        web_guidance = 0XDB
        orchestrion = 0XDC
        returner_dialog = 0XE0
        config_partylist_role_sort = 0XE3
        recommend_equip = 0XE4
        ykw_note = 0XE5
        contents_finder_menu = 0XE6
        raid_finder = 0XE7
        gc_army_expedition = 0XE8
        gc_army_member_list = 0XE9
        pvp_action_set = 0XEA
        deep_dungeon_status = 0XED
        deep_dungeon_save_data = 0XEE
        deep_dungeon_score = 0XEF
        gc_army_training = 0XF0
        gc_army_expedition_result = 0XF2
        gc_army_capture = 0XF3
        gc_army_order = 0XF4
        orchestrion_playlist = 0XF6
        countdown = 0XF7
        weekly_bingo = 0XF8
        weekly_puzzle = 0XF9
        pvp_duel_request = 0XFB
        qte = 0X101
        deep_dungeon_menu = 0X102
        deep_dungeon_result = 0X104
        item_appraisal = 0X105
        item_inspection = 0X106
        contact_list = 0X108
        picture_preview = 0X109
        satisfaction_supply = 0X10B
        satisfaction_supply_result = 0X10C
        snipe = 0X10D
        mount_speed = 0X10E
        harpoon_tip = 0X10F
        treasure_high_low = 0X113
        user_policy_performance = 0X116
        pvp_team = 0X117
        pvp_team_input_string = 0X118
        pvp_team_crest_editor = 0X11D
        eureka_elemental_hud = 0X120
        eureka_elemental_edit = 0X121
        eureka_chain_info = 0X122
        content_member_list = 0X127
        contents_replay_setting = 0X12A
        mirage_prism_prism_box = 0X12B
        mirage_prism_prism_item_detail = 0X12C
        mirage_prism_mirage_plate = 0X12D
        performance_mode = 0X12E
        reconstruction_box = 0X137
        reconstruction_buyback = 0X138
        cross_world_linkshell = 0X139
        description = 0X13B
        alarm = 0X13C
        free_shop = 0X13F
        aoz_notebook = 0X140
        emj = 0X143
        emj_total_result = 0X144
        emj_rank_result = 0X145
        emj_intro = 0X146
        aoz_content_briefing = 0X147
        aoz_content_result = 0X148
        world_travel_select = 0X149
        credit = 0X14C
        emj_setting = 0X14D
        retainer_list = 0X14E
        qibc_status = 0X14F
        huge_craft_works_supply = 0X150
        huge_craft_works_supply_result = 0X151
        sharlayan_craft_works_supply = 0X152
        dawn = 0X153
        dawn_story = 0X154
        housing_catalog_preview = 0X155
        guide = 0X156
        submarine_exploration_map_select = 0X157
        quest_redo = 0X158
        quest_redo_hud = 0X159
        circle_list = 0X15B
        circle_book = 0X15C
        circle_finder = 0X161
        performance_metronome = 0X164
        performance_gamepad_guide = 0X165
        performance_ready_check = 0X167
        hwd_aethergauge = 0X16B
        hwd_score = 0X16D
        hwd_monument = 0X16F
        mcguffin = 0X170
        craft_action_simulator = 0X171
        ikd_schedule = 0X172
        ikd_fishing_log = 0X173
        ikd_result = 0X174
        ikd_mission = 0X175
        inclusion_shop = 0X176
        collectables_shop = 0X177
        myc_war_result_notebook = 0X178
        myc_info = 0X179
        myc_item_box = 0X17A
        myc_item_bag = 0X17B
        myc_duel_request = 0X17C
        myc_battle_area_info = 0X17D
        myc_weapon_adjust = 0X17E
        ornament_note_book = 0X17F
        talk_subtitle = 0X180
        tourism_menu = 0X181
        gathering_masterpiece = 0X182
        starlight20_gift_box = 0X183
        spearfishing = 0X184
        omikuji = 0X185
        fitting_shop = 0X186
        akatsuki_note = 0X187
        ex_hot_bar_editor = 0X188
        banner_list = 0X189
        banner_editor = 0X18A
        banner_update_view = 0X18B
        banner_gearset_link = 0X18C
        pvp_map = 0X18D
        chara_card = 0X18E
        characard_design_setting = 0X18F
        chara_card_profile_setting = 0X190
        mji_hud = 0X193
        mji_pouch = 0X194
        mji_recipe_note_book = 0X195
        mji_craft_sales = 0X197
        mji_animal_management = 0X198
        mji_farm_management = 0X199
        mji_gatheringhouse = 0X19A
        mji_building = 0X19B
        mji_building_progress = 0X19B
        mji_gathering_note_book = 0X19C
        mji_dispose_shop = 0X19D
        mji_minion_management = 0X19E
        mji_minion_note_book = 0X19F
        mji_building_move = 0X1A0
        mji_entrance = 0X1A1
        mji_settings = 0X1A2
        mji_nekomimi_request = -0X1
        archive_item = 0X1A5
        class2_job_hot_bar = 0X1A6
        tofu_list = 0X1A9
        tofu_preview = 0X1AA
        tofu_edit = 0X1AB
        banner_party = 0X1AC
        banner_mip = 0X1AD
        turn_break = 0X1AE
        manderville_weapon = 0X1AF
        sxt_battle_log = 0X1B0
        moogle_collection = -0X1
        fgs_winner = -0X1
        fgs_result = -0X1