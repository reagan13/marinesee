"""Stratified 70 / 15 / 15 split."""

from __future__ import annotations

from sklearn.model_selection import train_test_split

from .dataset_contract import SPLIT_SEED


def split_labels(
    items: list,
    labels: list[str],
    seed: int = SPLIT_SEED,
) -> tuple[list, list, list, list[str], list[str], list[str]]:
    temp_items, test_items, temp_y, test_y = train_test_split(
        items,
        labels,
        test_size=0.15,
        stratify=labels,
        random_state=seed,
    )
    val_ratio = 0.15 / 0.85
    train_items, val_items, train_y, val_y = train_test_split(
        temp_items,
        temp_y,
        test_size=val_ratio,
        stratify=temp_y,
        random_state=seed,
    )
    return train_items, val_items, test_items, train_y, val_y, test_y
