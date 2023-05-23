import glm

special_actions: dict[int, int] = {
    # action_id: shape
}
delay_until: dict[int, float] = {
    # action_id: sec
}
omen_color: dict[int, glm.vec4 | tuple[glm.vec4,] | tuple[glm.vec4, glm.vec4,]] = {
    # action_id: color
}
