def calculate_precision(
    true_positives: int,
    false_positives: int,
) -> float:
    denominator = (
        true_positives
        + false_positives
    )

    if denominator == 0:
        return 0.0

    return (
        true_positives
        / denominator
    )


def calculate_recall(
    true_positives: int,
    false_negatives: int,
) -> float:
    denominator = (
        true_positives
        + false_negatives
    )

    if denominator == 0:
        return 0.0

    return (
        true_positives
        / denominator
    )


def calculate_f1(
    precision: float,
    recall: float,
) -> float:
    denominator = (
        precision + recall
    )

    if denominator == 0:
        return 0.0

    return (
        2
        * precision
        * recall
        / denominator
    )


def calculate_metrics(
    true_positives: int,
    false_positives: int,
    false_negatives: int,
):
    precision = calculate_precision(
        true_positives,
        false_positives,
    )

    recall = calculate_recall(
        true_positives,
        false_negatives,
    )

    f1 = calculate_f1(
        precision,
        recall,
    )

    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": round(
            precision,
            4,
        ),
        "recall": round(
            recall,
            4,
        ),
        "f1": round(
            f1,
            4,
        ),
    }