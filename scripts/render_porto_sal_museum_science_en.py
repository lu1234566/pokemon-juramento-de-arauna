#!/usr/bin/env python3
from __future__ import annotations

import render_porto_sal_museum_science as base


def patch(targets, label: str, payloads: tuple[str, ...]) -> None:
    markers, _ = targets[label]
    targets[label] = (markers, payloads)


# 1F exhibits.
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_WhirlpoolExperiment", (
    "Blue fluid spins inside a glass\\n",
    "container.\\p",
    "EXPERIMENT: create a WHIRLPOOL\\n",
    "using controlled air flow.$",
))
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_WaterfallExperiment", (
    "A red sphere rises and falls\\n",
    "inside a container.\\p",
    "EXPERIMENT: simulate WATERFALL\\n",
    "motion using buoyancy.$",
))
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_OceanSoilDisplay", (
    "SAMPLE: OCEAN SOIL\\p",
    "Remains of life settle on the\\n",
    "seafloor over many years.\\p",
    "Sediment layers help rebuild\\n",
    "the past.$",
))
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_BeachSandDisplay", (
    "SAMPLE: COASTAL SAND\\p",
    "Stone travels down rivers and\\n",
    "wears away on the journey.\\p",
    "The smallest grains form beaches.$",
))
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact1", (
    "OCEAN MINIFACT 1\\p",
    "Why does the sea look blue?\\p",
    "Water absorbs many colors of\\n",
    "light before blue.\\p",
    "So more blue reaches our eyes.$",
))
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact2", (
    "OCEAN MINIFACT 2\\p",
    "Why is the sea salty?\\p",
    "Rain carries salts from rock\\n",
    "into rivers and oceans.\\p",
    "Over time, they concentrate.$",
))
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_OceanicMinifact3", (
    "OCEAN MINIFACT 3\\p",
    "What covers more: sea or land?\\p",
    "The sea covers about 70% of\\n",
    "the planet.$",
))
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_FossilDisplay", (
    "FOSSIL: RIPPLE MARK\\p",
    "Currents leave small grooves on\\n",
    "the seafloor.\\p",
    "When sediment hardens, those\\n",
    "grooves can become fossils.$",
))
patch(base.TARGETS_1F, "SlateportCity_OceanicMuseum_1F_Text_DepthMeasuringMachine", (
    "DEPTH MEASURING MACHINE\\p",
    "A device turns under the dome.\\p",
    "It uses echoes to estimate the\\n",
    "distance to the seafloor.$",
))

# 2F samples, models and patrons.
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_WaterQualitySample1", (
    "WATER SAMPLE 1\\p",
    "The sea is connected, but water\\n",
    "changes from region to region.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_WaterQualitySample2", (
    "WATER SAMPLE 2\\p",
    "Salinity also changes between\\n",
    "different regions.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_PressureExperiment", (
    "PRESSURE EXPERIMENT\\p",
    "A rubber sphere expands and\\n",
    "contracts.\\p",
    "Deeper water means greater\\n",
    "pressure.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_HoennModel", (
    "MODEL OF ARAUNA\\p",
    "A miniature shows cities, rivers,\\n",
    "ridges and coastal routes.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_DeepSeawaterDisplay", (
    "DEEP CURRENTS\\p",
    "Near the seafloor, temperature\\n",
    "and salinity move huge masses\\n",
    "of water.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_SurfaceSeawaterDisplay", (
    "SURFACE CURRENTS\\p",
    "Near the surface, wind pushes\\n",
    "large flows of water.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_SSTidalReplica", (
    "REPLICA: COASTAL FERRY\\p",
    "A model of a vessel built to\\n",
    "connect Arauna's ports.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_SubmarineReplica", (
    "REPLICA: SUBMERSIBLE\\p",
    "A research vehicle designed for\\n",
    "great ocean depths.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_SumbersibleReplica", (
    "REPLICA: SUBMERSIBLE POD\\p",
    "A compact unmanned probe used\\n",
    "to explore the seafloor.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_SSAnneReplica", (
    "REPLICA: HISTORIC LINER\\p",
    "A model of an old passenger ship\\n",
    "that crossed whole oceans.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_RemindsMeOfAbandonedShip", (
    "VISITOR: That model reminds me of\\n",
    "a ship stranded on the coast.$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_DontRunInMuseum", (
    "VISITOR: No running in the MUSEUM,\\n",
    "all right?$",
))
patch(base.TARGETS_2F, "SlateportCity_OceanicMuseum_2F_Text_WantToRideSubmarine", (
    "VISITOR: I'd love to ride in a\\n",
    "research submersible.\\p",
    "It must be scary and amazing.$",
))


def main() -> int:
    return base.main()


if __name__ == "__main__":
    raise SystemExit(main())
