import enum
from nylib.utils.enum import missing, auto_missing


@auto_missing
class EmitterVarietyType(enum.Enum):
    Point = 0X0
    Cone = 0X1
    ConeModel = 0X2
    SphereModel = 0X3
    CylinderModel = 0X4
    Model = 0X5
    Unknown = 0X6


@auto_missing
class RotationBaseDirectionType(enum.Enum):
    X = 0X0
    Y = 0X1
    Z = 0X2
    MoveDirection = 0X3
    BillboardAxisY = 0X4
    ScreenBillboard = 0X5
    CameraBillboard = 0X6
    MoveDirectionBillboard = 0X7
    CameraBillboardAxisY = 0X8
    TreeBillboard = 0X9
    Null = 0XA
    _missing_ = missing(Null)


@auto_missing
class RotationOrderType(enum.Enum):
    XYZ = 0X0
    YZX = 0X1
    ZXY = 0X2
    XZY = 0X3
    YXZ = 0X4
    ZYX = 0X5


@auto_missing
class CoordinateComputeOrderType(enum.Enum):
    Scale_Rotation_Translate = 0X0
    Translate_Scale_Rotation = 0X1
    Rotation_Translate_Scale = 0X2
    Translate_Rotation_Scale = 0X3
    Scale_Translate_Rotation = 0X4
    Rotation_Scale_Translate = 0X5


@auto_missing
class RandomType(enum.Enum):
    First_Plus_Minus = 0X0
    First_Plus = 0X1
    First_Minus = 0X2
    Always_Plus_Minus = 0X3
    Always_Plus = 0X4
    Always_Minus = 0X5


@auto_missing
class Axis2ConnectType(enum.Enum):
    Null = 0X0
    X_Y = 0X1
    Y_X = 0X2


@auto_missing
class Axis3ConnectType(enum.Enum):
    Null = 0X0
    X_YZ = 0X1
    X_Y = 0X2
    X_Z = 0X3
    Y_XZ = 0X4
    Y_X = 0X5
    Y_Z = 0X6
    Z_XY = 0X7
    Z_X = 0X8
    Z_Y = 0X9


@auto_missing
class ParticleVarietyType(enum.Enum):
    Parameter = 0X0
    Powder = 0X1
    Windmill = 0X2
    Line = 0X3
    Laser = 0X4
    Model = 0X5
    PolyLine = 0X6
    Reserve0 = 0X7
    Quad = 0X8
    Polygon = 0X9
    Decal = 0XA
    DecalRing = 0XB
    Disc = 0XC
    LightModel = 0XD


@auto_missing
class DrawModeType(enum.Enum):
    Blend = 0X0
    Mul = 0X1
    Add = 0X2
    Sub = 0X3
    Screen = 0X4
    Reverse = 0X5
    Min = 0X6
    Max = 0X7
    Opacity = 0X8
    Mul2 = 0X9
    Add2 = 0XA
    Sub2 = 0XB
    Screen2 = 0XC


@auto_missing
class CullingType(enum.Enum):
    Null = 0X0
    Front = 0X1
    Back = 0X2
    Double = 0X3
    Max = 0X4


class EnvLightType(enum.Enum):
    Chara = 0X0
    BG = 0X1
    # Max = 0X2
    _missing_ = missing(Chara)


class DirLightType(enum.Enum):
    Directional = 0X0
    EnvSet = 0X1
    # Max = 0X2
    _missing_ = missing(Directional)


# @auto_missing
class UvPrecisionType(enum.Enum):
    High = 0X0
    Medium = 0X1
    Low = 0X2
    # Max = 0X3


# @auto_missing
class DepthOffsetType(enum.Enum):
    Legacy = 0X0
    FixedIntervalNDC = 0X1
    # Max = 0X2


@auto_missing
class TextureCalculateUvType(enum.Enum):
    ByParameter = 0X0
    ByPixelPosition = 0X1


@auto_missing
class TextureFilterType(enum.Enum):
    Disable = 0X0
    Enable = 0X1
    High = 0X2
    VeryHigh = 0X3
    VeryVeryHigh = 0X4


@auto_missing
class TextureBorderType(enum.Enum):
    Repeat = 0X0
    Clamp = 0X1
    Mirror = 0X2


@auto_missing
class TextureCalculateColorType(enum.Enum):
    Mul = 0X0
    Add = 0X1
    Sub = 0X2
    Max = 0X3
    Min = 0X4


@auto_missing
class TextureCalculateAlphaType(enum.Enum):
    Mul = 0X0
    Max = 0X1
    Min = 0X2
    Null = 0X3


@auto_missing
class LineCreateType(enum.Enum):
    AxisOrder = 0X0
    PositionHistory = 0X1


@auto_missing
class DirectionalLightType(enum.Enum):
    Lambert = 0X0
    HalfLambert = 0X1
    Ex = 0X2


@auto_missing
class WindmillUvType(enum.Enum):
    Default = 0X0
    Mirror = 0X1


@auto_missing
class NotBillboardBaseAxisType(enum.Enum):
    X = 0X0
    Y = 0X1
    Z = 0X2


@auto_missing
class FresnelType(enum.Enum):
    Null = 0X0
    Camera = 0X1
    AnyAxis = 0X2
    AnyAxisWithWorldRotation = 0X3


@auto_missing
class PointLightType(enum.Enum):
    Lambert = 0X0
    HalfLambert = 0X1
    Area = 0X2
    Ex = 0X3


@auto_missing
class SimpleInjectionPositionType(enum.Enum):
    Point = 0X0
    ModelVertex = 0X1
    PolyLine = 0X2


@auto_missing
class SimpleInjectionDirectionType(enum.Enum):
    Random = 0X0
    Radial = 0X1
    X = 0X2
    Y = 0X3
    Z = 0X4
    ModelNormal = 0X5


@auto_missing
class SimpleBaseDirectionType(enum.Enum):
    Billboard = 0X0
    LegacyY = 0X1
    LegacyZ = 0X2
    CorrectY = 0X3
    CorrectZ = 0X4
