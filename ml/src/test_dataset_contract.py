from dataset_contract import TRAINABLE_SPECIES, classify_folder


def test_study_all_and_research_grade():
    assert classify_folder("Enhalus acoroides dataset (all)") == (
        "enhalus_acoroides",
        "study",
        "all",
    )
    assert classify_folder("Enhalus acoroides dataset (research-grade)") == (
        "enhalus_acoroides",
        "study",
        "research-grade",
    )


def test_rotundata_without_all_suffix():
    assert classify_folder("Cymodocea rotundata dataset") == (
        "cymodocea_rotundata",
        "study",
        "all",
    )


def test_copy_and_extra_taxon():
    assert classify_folder("Halophila ovalis dataset (research-grade) - Copy") == (
        "halophila_ovalis",
        "study",
        "copy",
    )
    assert classify_folder("Halophila spinulosa dataset (all)")[1] == "extra"


def test_v1_drops_thalassia():
    assert "thalassia_hemprichii" not in TRAINABLE_SPECIES
    assert len(TRAINABLE_SPECIES) == 8


if __name__ == "__main__":
    test_study_all_and_research_grade()
    test_rotundata_without_all_suffix()
    test_copy_and_extra_taxon()
    test_v1_drops_thalassia()
    print("ok")
