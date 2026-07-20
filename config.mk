# Enable LTO when making a release build. Disable by setting to 0.
USE_LTO_ON_RELEASE ?= 1

# Keep the canonical item accessors unwrapped only inside src/item.c.
# Every other translation unit uses Arauna's lightweight item overrides,
# allowing story key items to receive localized names and behavior without
# forking the expansion's large generated item table.
build/%/src/item.o: CPPFLAGS += -DITEM_C_IMPLEMENTATION

# Keep the canonical party Surf scan only inside field_player_avatar.c.
# Other callers accept either a Surf-capable party member or Arauna's
# permanent Tide Board field-tool permission.
build/%/src/field_player_avatar.o: CPPFLAGS += -DARAUNA_FIELD_PLAYER_AVATAR_IMPLEMENTATION
