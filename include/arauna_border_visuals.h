#ifndef GUARD_ARAUNA_BORDER_VISUALS_H
#define GUARD_ARAUNA_BORDER_VISUALS_H

// Only the camera uses these aliases. MapGrid IDs, Cut and collision stay native.
u16 AraunaBorderVisualMetatile(const struct MapLayout *layout, s32 x, s32 y, u16 nativeId);
bool8 AraunaMapUsesBorderVisuals(const struct MapLayout *layout);
// TRUE when walking across a connection from `from` to `to` must reload the
// primary bank and redraw the whole view instead of only the new slices.
bool8 AraunaConnectionNeedsFullReload(const struct MapLayout *from, const struct MapLayout *to);

#endif
