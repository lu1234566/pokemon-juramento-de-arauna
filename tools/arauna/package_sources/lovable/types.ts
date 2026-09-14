export type TypeId =
  | "normal" | "fire" | "water" | "grass" | "electric" | "ice"
  | "fighting" | "poison" | "ground" | "flying" | "psychic" | "bug"
  | "rock" | "ghost" | "dragon" | "dark" | "steel" | "fairy";

export const TYPES: Record<TypeId, { pt: string; color: string; ink: string }> = {
  normal:   { pt: "Normal",    color: "#a8a878", ink: "#2a2a1c" },
  fire:     { pt: "Fogo",      color: "#e46a2b", ink: "#3a1405" },
  water:    { pt: "Água",      color: "#3f8fd3", ink: "#0a223d" },
  grass:    { pt: "Grama",     color: "#4fa35a", ink: "#0f2c14" },
  electric: { pt: "Elétrico",  color: "#e8c341", ink: "#3a2f05" },
  ice:      { pt: "Gelo",      color: "#8fd4d4", ink: "#0e2e2e" },
  fighting: { pt: "Lutador",   color: "#b8362d", ink: "#3a0906" },
  poison:   { pt: "Veneno",    color: "#8a4aa8", ink: "#2b0f38" },
  ground:   { pt: "Terra",     color: "#c9a15a", ink: "#3a2a0a" },
  flying:   { pt: "Voador",    color: "#8fa9e6", ink: "#0f1e42" },
  psychic:  { pt: "Psíquico",  color: "#e0567f", ink: "#3d0a1e" },
  bug:      { pt: "Inseto",    color: "#9fb02b", ink: "#26290a" },
  rock:     { pt: "Pedra",     color: "#a89460", ink: "#2f2708" },
  ghost:    { pt: "Fantasma",  color: "#6a5d9a", ink: "#181432" },
  dragon:   { pt: "Dragão",    color: "#5a48c9", ink: "#100a3a" },
  dark:     { pt: "Sombrio",   color: "#4a3d33", ink: "#f5efe6" },
  steel:    { pt: "Aço",       color: "#a8a8b8", ink: "#1c1c26" },
  fairy:    { pt: "Fada",      color: "#e8a3c9", ink: "#3a0f28" },
};

export const TYPE_LIST = Object.keys(TYPES) as TypeId[];