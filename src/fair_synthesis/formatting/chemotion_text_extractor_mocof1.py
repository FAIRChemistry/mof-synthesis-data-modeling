SUPPORTED_RINSE_SOLVENTS = {
    "acetone": "acetone",
    "et3n": "Et3N",
    "mecn": "MeCN",
    "nacl aq": "NaCl aq",
    "dmf": "DMF",
    "chcl3": "CHCl3",
    "meoh": "MeOH",
    "etoh": "EtOH",
    "ethanol": "EtOH",
}


def process_data_use_case_specific(data: list[dict]) -> None:
    process_free_text_fields(data)


def process_free_text_fields(data: list[dict]) -> None:
    for item in data:
        description = item.get("plain_text_description") or ""
        observation = item.get("plain_text_observation") or ""
        reaction_text = _reaction_text(description)
        workup_text = _workup_text(observation)

        vessel = _extract_vessel(reaction_text)
        if vessel:
            item["vessel"] = vessel

        degassing = _extract_degassing(reaction_text)
        if degassing:
            item["degassing"] = degassing

        rinse = _extract_rinse(workup_text)
        if rinse:
            item["rinse"] = rinse

        wait_after_rinse = _extract_wait_after_rinse(workup_text)
        if wait_after_rinse:
            item["wait_after_rinse"] = wait_after_rinse
            item["wait_after_rinse_unit"] = "h"

        wash_solid = _extract_wash_solid(workup_text)
        if wash_solid:
            item["wash_solid"] = wash_solid

        if _extract_evaporate(workup_text):
            item["evaporate"] = True


def _reaction_text(description: str) -> str:
    lowered = description.lower()
    marker_positions = [
        lowered.find(marker)
        for marker in ("procedure", "reaction")
        if lowered.find(marker) >= 0
    ]
    if marker_positions:
        return description[min(marker_positions):].strip()

    text = description.split("Analysis", 1)[0]
    return text.split("PXRD", 1)[0].strip()


def _workup_text(observation: str) -> str:
    text = observation.split("Analysis", 1)[0]
    return text.split("PXRD", 1)[0].strip()


def _extract_vessel(text: str) -> str | None:
    lowered = text.lower()
    if "microwave vial" in lowered:
        return "microwave vial"
    if any(term in lowered for term in ["pressure tube", "j. young tube", "schlenk bomb"]):
        return "Schlenk bomb"
    return None


def _extract_degassing(text: str) -> str | None:
    lowered = text.lower()
    if "fpt" in lowered or "ar replace" in lowered:
        return "Ar"
    return None


def _extract_rinse(text: str) -> list[str]:
    lowered = text.lower()
    result: list[str] = []
    for search_term, solvent in SUPPORTED_RINSE_SOLVENTS.items():
        if search_term in lowered and solvent not in result:
            result.append(solvent)
    return result


def _extract_wait_after_rinse(text: str) -> int | None:
    lowered = text.lower()
    if "soxhlet" in lowered or "open to air" in lowered:
        return 24
    return None


def _extract_wash_solid(text: str) -> str | None:
    lowered = text.lower()
    if "samples under fillers" in lowered or "meoh filled up" in lowered:
        return "MeOH+scCO2"
    if any(term in lowered for term in ["supercritical co2", "scco<sub>2</sub>", "scco2", "scco₂", "scco₂"]):
        return "scCO2"
    return None


def _extract_evaporate(text: str) -> bool:
    lowered = text.lower()
    for marker in ["scco", "supercritical co2"]:
        parts = lowered.split(marker, 1)
        if len(parts) > 1 and "vacuum" in parts[1]:
            return True
    return False
