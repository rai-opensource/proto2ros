# Camera sensor information.

uint8 K_FIELD_SET=4
uint8 R_FIELD_SET=8
uint8 P_FIELD_SET=16
uint8 DISTORTION_MODEL_FIELD_SET=32

uint32 height
uint32 width
# Intrinsic matrix.
Matrix k
# Rectification matrix.
Matrix r
# Projection matrix.
Matrix p
CameraInfoDistortionModel distortion_model
uint8 has_field 255
